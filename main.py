import numpy as np

#######
# All calculations come from:
# - https://www.color.org/sRGB.pdf doc
# - https://www.wikiwand.com/en/CIELAB_color_space page
###

def calculate_linear_value_ICCv2(normalized_level):

    if normalized_level <= 0.04045:
        linear_value = normalized_level / 12.92
    else:
        linear_value = ((normalized_level + 0.055) / 1.055) ** 2.4

    return linear_value


def calculate_linear_value_ICCv2_precise(normalized_level):

    if normalized_level <= 0.0392857:
        linear_value = normalized_level / 12.9232102
    else:
        linear_value = ((normalized_level + 0.055) / 1.055) ** 2.4

    return linear_value


def calculate_linear_value_ICCv4(normalized_level):

    if normalized_level <= 0.04045:
        linear_value = 0.0772059 * normalized_level + 0.0025
    else:
        linear_value = (0.946879 * normalized_level + 0.0520784) ** 2.4 + 0.0025

    return linear_value


# Convert linearRGB to XYZ
R709_TO_XYZ_D65 = [
    [0.4124564, 0.3575761, 0.1804375],
    [0.2126729, 0.7151522, 0.0721750],
    [0.0193339, 0.1191920, 0.9503041]
]

### ONLY for calculating monochrome!!!
def calculate_Lstar_value_for_monochrome(linear_value):

    # Define the matrix and vector
    matrix = np.array(R709_TO_XYZ_D65)
    vector = np.array(
        [
            linear_value, 
            linear_value, 
            linear_value
        ]
    )
    
    # Multiply R709_TO_XYZ_D65 matrix by vector with linear_value
    XYZ_D65 = np.dot(matrix, vector)    
    
    # Calculate L* value for D65
    Yn = 1  # Reference white point
    Y = XYZ_D65[1] #Y coordinate
    Y_div_Yn = Y / Yn

    if Y_div_Yn > 0.008856:
        L_star = 116 * Y_div_Yn ** (1/3) - 16
    else:
        L_star = 903.3 * Y_div_Yn

    return L_star



def stat(int_level__ICCv2, int_level__ICCv4, bit_depth):

    SUBSTR = "for input integer RGB level {:5d} /{:2d} "

    NORMALIZED_LEVEL__ICCv2 = int_level__ICCv2 / (pow(2, bit_depth) - 1)
    print((SUBSTR + "normalized level in range [0..1]: {:.5f} (ICC v2)").format(int_level__ICCv2, bit_depth, NORMALIZED_LEVEL__ICCv2))
    
    NORMALIZED_LEVEL__ICCv4 = int_level__ICCv4 / (pow(2, bit_depth) - 1)
    print((SUBSTR + "normalized level in range [0..1]: {:.5f} (ICC v4)").format(int_level__ICCv4, bit_depth, NORMALIZED_LEVEL__ICCv4))
    
    LINEAR_VALUE__ICCv2 = calculate_linear_value_ICCv2(NORMALIZED_LEVEL__ICCv2)
    print((SUBSTR + "linear value in range [0..1]: {:.5f} (ICC v2)").format(int_level__ICCv2, bit_depth, LINEAR_VALUE__ICCv2))

    LINEAR_VALUE__ICCv2_precise = calculate_linear_value_ICCv2_precise(NORMALIZED_LEVEL__ICCv2)
    print((SUBSTR + "linear value in range [0..1]: {:.5f} (ICC v2 precise)").format(int_level__ICCv2, bit_depth, LINEAR_VALUE__ICCv2_precise))
    
    LINEAR_VALUE__ICCv4 = calculate_linear_value_ICCv4(NORMALIZED_LEVEL__ICCv4)
    print((SUBSTR + "linear value in range [0..1]: {:.5f} (ICC v4)").format(int_level__ICCv4, bit_depth, LINEAR_VALUE__ICCv4))
    
    L_STAR_VALUE__ICCv2 = calculate_Lstar_value_for_monochrome(LINEAR_VALUE__ICCv2)
    print((SUBSTR + "L* value in range [0..100]: {:.2f} (ICC v2)").format(int_level__ICCv2, bit_depth, L_STAR_VALUE__ICCv2))
    
    L_STAR_VALUE__ICCv4 = calculate_Lstar_value_for_monochrome(LINEAR_VALUE__ICCv4)
    print((SUBSTR + "L* value in range [0..100]: {:.2f} (ICC v4)").format(int_level__ICCv4, bit_depth, L_STAR_VALUE__ICCv4))

    print()


stat(
    int_level__ICCv2 = 1, # very dark color (ICC v2)
    int_level__ICCv4 = 1, # very dark color (ICC v4)
    bit_depth = 8
)

stat(
    int_level__ICCv2 = 1, # very dark color (ICC v2)
    int_level__ICCv4 = 1, # very dark color (ICC v4)
    bit_depth = 16
)

stat(
    int_level__ICCv2 = 2 ** 8 - 2, # brightess color (ICC v2)
    int_level__ICCv4 = 2 ** 8 - 2, # brightess color (ICC v4)
    bit_depth = 8
)

stat(
    int_level__ICCv2 = 2 ** 16 - 2, # brightess color (ICC v2)
    int_level__ICCv4 = 2 ** 16 - 2, # brightess color (ICC v4)
    bit_depth = 16
)

stat(
    int_level__ICCv2 = 124, # 20% Image surround reflectance, because its linear value is 0.20156 (ICC v2)
    int_level__ICCv4 = 123, # 20% Image surround reflectance, because its linear value is 0.20007 (ICC v4)
    bit_depth = 8
)

stat(
    int_level__ICCv2 = 118, # 18% gray card, because its linear value is 0.18116 (ICC v2)
    int_level__ICCv4 = 117, # 18% gray card, because its linear value is 0.17994 (ICC v4)
    bit_depth = 8
)

stat(
    int_level__ICCv2 = 15117, # 18% gray card, because its linear value is 0.17999 (ICC v2)
    int_level__ICCv4 = 15037, # 18% gray card, because its linear value is 0.18001 (ICC v4)
    bit_depth = 15
)

stat(
    int_level__ICCv2 = 30235, # 18% gray card, because its linear value is 0.18000 (ICC v2)
    int_level__ICCv4 = 30074, # 18% gray card, because its linear value is 0.18001 (ICC v4)
    bit_depth = 16
)

###