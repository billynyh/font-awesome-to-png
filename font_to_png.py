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

DEBUG = True
#DEBUG = False

#iconset = "font-awesome"
#iconset = "elusive"

FONT_AWESOME = "font-awesome"
ELUSIVE = "elusive"

assets = {
    FONT_AWESOME : {
        "mapping" : "assets/font-awesome/font-awesome.css",
        "ttf" : "assets/font-awesome/fontawesome-webfont.ttf",
        "canvas_ratio" : (1,1),
        "pattern" : "\.icon-(.*):before(.*)(f...)\""
    },
    ELUSIVE : {
        "mapping" : "assets/elusive-iconfont/elusive-webfont.css",
        "ttf" : "assets/elusive-iconfont/Elusive-Icons.ttf",
        "canvas_ratio" : (20, 20),
        "pattern" : "\.icon-(.*):before(.*)(e...)\""
    } 
}

def load_icon_mapping(config):
    fname = config["mapping"]
    f = open(fname, "r")
    p = re.compile(config["pattern"], re.MULTILINE)
    icons = {}
    ss = f.read()

    ss = ss.replace("{\n", "{")
    l = ss.splitlines()
    for s in l:
        m = p.match(s)
        if m:
            key = m.group(1)
            value = m.group(3)
            value = unichr(int(value, 16))
            icons[key] = value

    return icons

def load_icon_mapping_bak(config):
    fname = config["mapping"]
    f = open(fname, "r")
    p = re.compile(config["pattern"])
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
        for iconset in [FONT_AWESOME, ELUSIVE]:
            print iconset
            icons = load_icon_mapping(assets[iconset])
            for icon in sorted(icons.keys()):
                print "  " + icon
        exit(0)

def new_canvas_image(config, size):
    canvas_ratio = config["canvas_ratio"]
    canvas_size = (size * canvas_ratio[0], size * canvas_ratio[1])
    image = Image.new("RGBA", canvas_size, color=(0,0,0,0))
    return image

def export_icon(config, char, size, filename, color, image=None, outter_size=None):
    font = config["ttf"]

    if image is None:
        image = new_canvas_image(config, size)
    if outter_size is None:
        outter_size = size

    draw = ImageDraw.Draw(image)

    # Initialize font
    font = ImageFont.truetype(font, size, encoding="unic")

    # Determine the dimensions of the icon
    width,height = draw.textsize(char, font=font)

    if DEBUG:
        print "%d %d" % (width, height)

    canvas_ratio = config["canvas_ratio"]
    canvas_size = (size * canvas_ratio[0], size * canvas_ratio[1])
    x,y  = ( (canvas_size[0]-width)/2, (canvas_size[1]-height)/2 )
    draw.text((x, y), char, font=font, fill=color)

    # Get bounding box
    bbox = image.getbbox()
    if DEBUG:
        print bbox

    if bbox:
        image = image.crop(bbox)

        borderw = (outter_size - (bbox[2] - bbox[0])) / 2
        borderh = (outter_size - (bbox[3] - bbox[1])) / 2

        borderw = max(0, borderw)
        borderh = max(0, borderh)

        if DEBUG:
            print (borderw, borderh)

        # Create background image
        bg = Image.new("RGBA", (outter_size, outter_size), (0,0,0,0))

        bg.paste(image, (borderw,borderh))

        # Save file
        bg.save(filename)
    else:
        print "Error - bbox is None"
    # clear image
    draw.rectangle(bbox, fill=(0,0,0,0))


def main(iconset = "font-awesome"):
    parser = argparse.ArgumentParser(
            description="Exports Font Awesome icons as PNG images.")

    parser.add_argument("icon", type=str, nargs="+",
            help="The name(s) of the icon(s) to export (or \"ALL\" for all icons)")
    parser.add_argument("--color", type=str, default="black",
            help="Color (HTML color code or name, default: black)")
    parser.add_argument("--filename", type=str,
            help="The name of the output file. If all files are exported, it is " +
            "used as a prefix.")
    parser.add_argument("--list", nargs=0, action=ListAction,
            help="List available icon names and exit")
    parser.add_argument("--size", type=int, default=16,
            help="Icon size in pixels (default: 16)")
    parser.add_argument("--outter", type=int, default=16,
            help="Outter size in pixels (default: 16)")
    parser.add_argument("--outdir", type=str, default=None,
            help="outdir")

    args = parser.parse_args()
    icon = args.icon
    size = args.size
    outter_size = args.outter
    color = args.color
    OUTDIR = args.outdir

    config = assets[iconset]
    icons = load_icon_mapping(config)

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
    if OUTDIR is None:
        OUTDIR = "gen-%s/" % iconset
    if not OUTDIR.endswith("/"):
        OUTDIR = OUTDIR + "/"
    if not path.exists(OUTDIR):
        makedirs(OUTDIR)

    dummy_image = new_canvas_image(config, size)

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
        
        export_icon(config, icons[icon], size, filename, color, image=dummy_image, outter_size=outter_size)

if __name__=="__main__":
    main()

