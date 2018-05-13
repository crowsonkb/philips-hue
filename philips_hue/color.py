import colour


def rgb_to_xybri(rgb):
    # TODO: make this use something other than D65
    x, y, Y = colour.XYZ_to_xyY(colour.sRGB_to_XYZ(rgb))
    bri = int(Y**(1/2.2) * 254)
    return {'xy': [x, y], 'bri': bri}
