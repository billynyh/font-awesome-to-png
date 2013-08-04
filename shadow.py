from font_to_png import *

config = assets[FONT_AWESOME]
icons = load_icon_mapping(config)
size = 32
outter_size = 40
color = "#ffffff"
dummy_image = new_canvas_image(config, size)

OUTDIR = "gen-menu-shadow/"
if not path.exists(OUTDIR):
    makedirs(OUTDIR)

name_map = {
    "fire" : "hot",
    "leaf" : "fresh", 
    "beaker" : "trending",
    "off" : "logout",
    "envelope" : "feedback",
    "user" : "profile"
}

for icon in ["fire", "leaf", "beaker", "off", "user", "envelope"]:
    filename = OUTDIR + "navdrawer_" + name_map[icon] + ".png"
    print("Exporting icon \"%s\" as %s (%ix%i pixels)" %
            (icon, filename, size, size))
    img = get_icon_image(config, icons[icon], size, color, image=dummy_image, 
        outter_size=outter_size, shadow=True)
    bg = Image.new("RGBA", (outter_size + 14, outter_size + 8), (0,0,0,0))
    bg.paste(img, (0, 8))
    bg.save(filename)
