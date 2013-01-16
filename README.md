Font Awesome to PNG
===================

This program allows you to extract the awesome
[Font Awesome] (http://fortawesome.github.com/Font-Awesome/) icons as PNG images
of specified size.

### Usage

    font-to-png.py [-h] [--color COLOR] [--filename FILENAME]
                           [--list] [--size SIZE]
                           icon [icon ...]

    positional arguments:
      icon                 The name(s) of the icon(s) to export (or "ALL" for
                           all icons)

    optional arguments:
      --color COLOR        Color (HTML color code or name, default: black)
      --filename FILENAME  The name of the output file. If all files are
                           exported, it is used as a prefix.
      --list               List available icon names and exit
      --size SIZE          Icon size in pixels (default: 16)


You can also use elusive.py for [Elusive Icons] (http://aristath.github.com/elusive-iconfont/)

To use the program, you need the Font Awesome TTF file, which is available in
[Font Awesome Github repository] (https://github.com/FortAwesome/Font-Awesome).

### Examples

Export the "play" and "stop" icons as 24x24 pixels images:

    font-awesome-to-png.py --size 24 play stop

Export the asterisk icon as 32x32 pixels image, in blue:

    font-awesome-to-png.py --size 32 --color blue asterisk

Export all icons as 16x16 pixels images:

    font-awesome-to-png.py ALL
