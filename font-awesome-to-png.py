#!/usr/bin/env python

#
# font-awesome-to-png.py
#
# Exports Font Awesome icons as PNG images.
#
# Copyright (c) 2012 Michal Wojciechowski (http://odyniec.net/)
#
# Font Awesome - http://fortawesome.github.com/Font-Awesome
#

import sys, argparse
from os import path, access, R_OK, makedirs
import Image, ImageFont, ImageDraw
import re

icons = {}

def load_icon_mapping(fname = "font-awesome.css"):
    f = open(fname, "r")
    p = re.compile("\.icon-(.*):before(.*)(f...)\"")
    icons = {}

    while True:
        s = f.readline()
        if not s:
            break 
        m = p.match(s)
        if m:
            key = m.group(1)
            value = m.group(3)
            value = unichr(int(value, 16))
            icons[key] = value
    return icons

class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for icon in sorted(icons.keys()):
            print icon
        exit(0)

def export_icon(icon, size, filename, font, color):
    image = Image.new("RGBA", (size, size), color=(0,0,0,0))

    draw = ImageDraw.Draw(image)

    # Initialize font
    font = ImageFont.truetype(font, size)

    # Determine the dimensions of the icon
    width,height = draw.textsize(icons[icon], font=font)

    draw.text(((size - width) / 2, (size - height) / 2), icons[icon],
            font=font, fill=color)

    # Get bounding box
    bbox = image.getbbox()

    if bbox:
        image = image.crop(bbox)

    borderw = (size - (bbox[2] - bbox[0])) / 2
    borderh = (size - (bbox[3] - bbox[1])) / 2

    # Create background image
    bg = Image.new("RGBA", (size, size), (0,0,0,0))

    bg.paste(image, (borderw,borderh))

    # Save file
    bg.save(filename)

def main():
    parser = argparse.ArgumentParser(
            description="Exports Font Awesome icons as PNG images.")

    parser.add_argument("icon", type=str, nargs="+",
            help="The name(s) of the icon(s) to export (or \"ALL\" for all icons)")
    parser.add_argument("--color", type=str, default="black",
            help="Color (HTML color code or name, default: black)")
    parser.add_argument("--filename", type=str,
            help="The name of the output file. If all files are exported, it is " +
            "used as a prefix.")
    parser.add_argument("--font", type=str, default="fontawesome-webfont.ttf",
            help="Font file to use (default: fontawesome-webfont.ttf)")
    parser.add_argument("--list", nargs=0, action=ListAction,
            help="List available icon names and exit")
    parser.add_argument("--size", type=int, default=16,
            help="Icon size in pixels (default: 16)")

    args = parser.parse_args()
    icon = args.icon
    size = args.size
    font = args.font
    color = args.color

    global icons
    icons = load_icon_mapping()
    print icons
    if args.font:
        if not path.isfile(args.font) or not access(args.font, R_OK):
            print >> sys.stderr, ("Error: Font file (%s) can't be opened"
                    % (args.font))
            exit(1)

    if args.icon == [ "ALL" ]:
        # Export all icons
        selected_icons = sorted(icons.keys())
    else:
        selected_icons = []
        
        # Icon name was given
        for icon in args.icon:
            # Strip the "icon-" prefix, if present 
            if icon.startswith("icon-"):
                icon = icon[5:]

            if icon in icons:
                selected_icons.append(icon)
            else:
                print >> sys.stderr, "Error: Unknown icon name (%s)" % (icon)
                sys.exit(1)

    OUTDIR = "gen/"
    if not path.exists(OUTDIR):
        makedirs(OUTDIR)


    for icon in selected_icons:
        if len(selected_icons) > 1:
            # Exporting multiple icons -- treat the filename option as name prefix
            filename = (args.filename or "") + icon + ".png"
        else:
            # Exporting one icon
            if args.filename:
                filename = args.filename
            else:
                filename = icon + ".png"

        filename = OUTDIR + filename
        print("Exporting icon \"%s\" as %s (%ix%i pixels)" %
                (icon, filename, size, size))

        export_icon(icon, size, filename, font, color)

main()

