#######
# All calculations are from https://www.color.org/sRGB.pdf doc
###

def calculate_linear_value_ICCv2(normalized_level):

    if normalized_level <= 0.04045:
        linear_value = normalized_level / 12.92
    else:
        linear_value = pow(((normalized_level + 0.055) / 1.055), 2.4)

    return linear_value


def calculate_linear_value_ICCv4(normalized_level):

    if normalized_level <= 0.04045:
        linear_value = 0.0772059 * normalized_level + 0.0025
    else:
        linear_value = pow((0.946879 * normalized_level + 0.0520784), 2.4) + 0.0025

    return linear_value


def calculate_Lstar_value_gray(linear_level_gray):

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



def stat(int_level__ICCv2, int_level__ICCv4, bit_depth):

    SUBSTR = "for input integer RGB level {:5d} /{:2d} "

    NORMALIZED_LEVEL__ICCv2 = int_level__ICCv2 / (pow(2, bit_depth) - 1)
    print((SUBSTR + "normalized level in range [0..1]: {:.5f} (ICC v2)").format(int_level__ICCv2, bit_depth, NORMALIZED_LEVEL__ICCv2))
    
    NORMALIZED_LEVEL__ICCv4 = int_level__ICCv4 / (pow(2, bit_depth) - 1)
    print((SUBSTR + "normalized level in range [0..1]: {:.5f} (ICC v4)").format(int_level__ICCv4, bit_depth, NORMALIZED_LEVEL__ICCv4))
    
    LINEAR_VALUE__ICCv2 = calculate_linear_value_ICCv2(NORMALIZED_LEVEL__ICCv2)
    print((SUBSTR + "linear value in range [0..1]: {:.5f} (ICC v2)").format(int_level__ICCv2, bit_depth, LINEAR_VALUE__ICCv2))
    
    LINEAR_VALUE__ICCv4 = calculate_linear_value_ICCv4(NORMALIZED_LEVEL__ICCv4)
    print((SUBSTR + "linear value in range [0..1]: {:.5f} (ICC v4)").format(int_level__ICCv4, bit_depth, LINEAR_VALUE__ICCv4))
    
    L_STAR_VALUE__ICCv2 = calculate_Lstar_value_gray(LINEAR_VALUE__ICCv2)
    print((SUBSTR + "L* value in range [0..100]: {:.2f} (ICC v2)").format(int_level__ICCv2, bit_depth, L_STAR_VALUE__ICCv2))
    
    L_STAR_VALUE__ICCv4 = calculate_Lstar_value_gray(LINEAR_VALUE__ICCv4)
    print((SUBSTR + "L* value in range [0..100]: {:.2f} (ICC v4)").format(int_level__ICCv4, bit_depth, L_STAR_VALUE__ICCv4))
    

######## Input RGB level for ---> 8 <--- bit per channel

stat(
    int_level__ICCv2 = 118, # 18% gray card, because its linear value is 0.18116 (ICC v2)
    int_level__ICCv4 = 117, # 18% gray card, because its linear value is 0.17994 (ICC v4)
    bit_depth = 8
)

###


######## Input RGB level for ---> 16 <--- bit per channel

stat(
    int_level__ICCv2 = 30235, # 18% gray card, because its linear value is 0.18000 (ICC v2)
    int_level__ICCv4 = 30074, # 18% gray card, because its linear value is 0.18001 (ICC v4)
    bit_depth = 16
)

###