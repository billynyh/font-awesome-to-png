# generating action bar icons following the design guideline
# http://developer.android.com/design/style/iconography.html
# http://developer.android.com/design/style/metrics-grids.html

from font_to_png import *
from color_util import color_hex_to_tuple

ICON_SIZE_DIP = 24
ICON_CANVAS_DIP = 32

DENSITY = [
  { "name":"mdpi", "ratio":1},
  { "name":"hdpi", "ratio":1.5},
  { "name":"xhdpi", "ratio":2},
]

LIST = [
  "play", "fire", "beaker", "bell"
]

MDPI = 1
HDPI = 1.5
XHDPI = 2

color1 = color_hex_to_tuple("#0951B5", (int)(256*0.8))
color2 = color_hex_to_tuple("#0951B5", (int)(256*0.3))

def main():
    config = assets[FONT_AWESOME]
    icons = load_icon_mapping(config)

    for d in DENSITY:
        name = d["name"]
        ratio = d["ratio"]

        print "Generating images for %s" % name

        text_size = (int)(ICON_SIZE_DIP * ratio)
        outter_size = (int)(ICON_CANVAS_DIP * ratio)

        OUTDIR = "gen-android/drawable-%s/" % name
        if not path.exists(OUTDIR):
            makedirs(OUTDIR)

        dummy_image = new_canvas_image(config, text_size)

        for s in LIST:
            fname = OUTDIR + "ic_%s_normal.png" % s 
            print "Exporting icon %s" % fname
            export_icon(config, icons[s], text_size, fname, color1, 
                image=dummy_image, outter_size=outter_size)

            fname = OUTDIR + "ic_%s_pressed.png" % s 
            print "Exporting icon %s" % fname
            export_icon(config, icons[s], text_size, fname, color2, 
                image=dummy_image, outter_size=outter_size)

if __name__ == "__main__":
    main()
