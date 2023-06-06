def calculate_linear_value_ICCv2(normalized_level):

    if normalized_level <= 0.04045:
      linear_level = normalized_level / 12.92
    else:
      linear_level = pow(((normalized_level + 0.055) / 1.055), 2.4)

    return linear_level


def calculate_Lstar_gray(linear_level_gray):

    # Convert linearRGB to XYZ
    matrix = [[0.4124564, 0.3575761, 0.1804375],
              [0.2126729, 0.7151522, 0.0721750],
              [0.0193339, 0.1191920, 0.9503041]]
    xyz = [sum([matrix[i][j] * linear_level_gray for j in range(3)]) for i in range(3)]

    # Calculate L* value
    Yn = 1.0  # Reference white point
    f = lambda t: t ** (1/3) if t > 0.008856 else 903.3 * t
    L_star = 116 * f(xyz[1] / Yn) - 16

    return L_star


######## Input RGB level for ---> 8 <--- bit per channel
int_level_8bit = 118

####  for ---> 8 <--- bit per channel
normalized_level_8bit = int_level_8bit / (pow(2, 8) - 1)

print("for int_level {}/{} normalized level in range [0..1]: {:.5f}".format(int_level_8bit, 8, normalized_level_8bit))
###    

#### for ---> 8 <--- bit per channel (ICC v2)
linear_level_ICCv2_8bit = calculate_linear_value_ICCv2(normalized_level_8bit)

print("for int_level {}/{} linear value in range [0..1]: {:.5f} (ICC v2)".format(int_level_8bit, 8, linear_level_ICCv2_8bit))
###

#### for ---> 8 <--- bit per channel (ICC v2)
L_star_ICCv2_8bit = calculate_Lstar_gray(linear_level_ICCv2_8bit)

print("for int_level {}/{} L* value in range [0..100]: {:.2f} (ICC v2)".format(int_level_8bit, 8, L_star_ICCv2_8bit))
###

