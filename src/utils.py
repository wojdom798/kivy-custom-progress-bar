def rgba_to_color(rgba_tuple):
    if not isinstance(rgba_tuple, tuple) or len(rgba_tuple) < 4:
        raise ValueError("\"rgba_tuple\" must be a tuple of length 4")
    
    red = 1
    green = 1
    blue = 1
    alpha = 1

    if rgba_tuple[0] >= 0 and rgba_tuple[0] <= 255:
        red = rgba_tuple[0] / 255
    if rgba_tuple[1] >= 0 and rgba_tuple[1] <= 255:
        green = rgba_tuple[1] / 255
    if rgba_tuple[2] >= 0 and rgba_tuple[2] <= 255:
        blue = rgba_tuple[2] / 255
    if rgba_tuple[3] >= 0 and rgba_tuple[3] <= 255:
        alpha = rgba_tuple[3] / 255
        
    return (red, green, blue, alpha)