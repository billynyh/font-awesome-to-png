
HEX = "0123456789abcdef"

def hex2_to_int(str):
    return HEX.index(str[0]) * 16 + HEX.index(str[1])

def color_hex_to_tuple(str, alpha=255, rgb_only=False):
    if str[0] == "#":
        str = str[1:]
    if len(str) < 6:
        raise Exception("Color Hex too short")
    str = str.lower()

    r = hex2_to_int(str[0:2])
    g = hex2_to_int(str[2:4])
    b = hex2_to_int(str[4:6])

    if rgb_only:
        return (r, g, b)

    if len(str) >= 8:
        alpha = hex2_to_int(str[6:8])
    return (r, g, b, alpha)

if __name__ == "__main__":
    s = "#88aaf2"
    print color_hex_to_tuple(s)
    print color_hex_to_tuple(s, 60)
    print color_hex_to_tuple(s, rgb_only = True)
