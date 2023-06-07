import numpy as np

class LinearValueCalculator:
    def calculate_linear_value(self, normalized_level):
        pass

    def get_short_name(self):
        return self.__class__.__name__        

class ICCv2(LinearValueCalculator):
    def calculate_linear_value(self, normalized_level):
        if normalized_level <= 0.04045:
            return normalized_level / 12.92
        else:
            return ((normalized_level + 0.055) / 1.055) ** 2.4

class ICCv2_precise(LinearValueCalculator):
    def calculate_linear_value(self, normalized_level):
        if normalized_level <= 0.0392857:
            return normalized_level / 12.9232102
        else:
            return ((normalized_level + 0.055) / 1.055) ** 2.4

class ICCv4(LinearValueCalculator):
    def calculate_linear_value(self, normalized_level):
        if normalized_level <= 0.04045:
            return 0.0772059 * normalized_level + 0.0025
        else:
            return (0.946879 * normalized_level + 0.0520784) ** 2.4 + 0.0025

def calculate_Lstar_value_for_monochrome(linear_value):
    R709_TO_XYZ_D65 = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]
    ])

    XYZ_D65 = np.dot(R709_TO_XYZ_D65, [linear_value] * 3)

    Yn = 1.0  # Reference white point
    Y = XYZ_D65[1]  # Y coordinate
    Y_div_Yn = Y / Yn

    if Y_div_Yn > 0.008856:
        L_star = 116 * Y_div_Yn ** (1/3) - 16
    else:
        L_star = 903.3 * Y_div_Yn

    return L_star

ICCv2_CALC = ICCv2()
ICCv2_precise_CALC = ICCv2_precise()
ICCv4_CALC = ICCv4()
ALL_CALCS = [ICCv2_CALC, ICCv2_precise_CALC, ICCv4_CALC]

def stat(int_level__ICCv2, int_level__ICCv4, bit_depth):
    int_levels = {
        ICCv2_CALC: int_level__ICCv2,
        ICCv2_precise_CALC: int_level__ICCv2,
        ICCv4_CALC: int_level__ICCv4
    }

    normalized_levels = {}
    linear_values = {}
    Lstar_values = {}

    for calc in ALL_CALCS:
        normalized_levels[calc] = int_levels[calc] / (2 ** bit_depth - 1)
        linear_values[calc] = calc.calculate_linear_value(normalized_levels[calc])
        Lstar_values[calc] = calculate_Lstar_value_for_monochrome(linear_values[calc])

    for calc in ALL_CALCS:
        print(f"level {int_levels[calc]:5d} /{bit_depth:2d} normalized level in range [0..1]: {normalized_levels[calc]:0.5f} ({calc.get_short_name()})")

    for calc in ALL_CALCS:
        print(f"level {int_levels[calc]:5d} /{bit_depth:2d} linear value in range [0..1]: {linear_values[calc]:0.5f} ({calc.get_short_name()})")

    for calc in ALL_CALCS:
        print(f"level {int_levels[calc]:5d} /{bit_depth:2d} L* value in range [0..100]: {Lstar_values[calc]:0.2f} ({calc.get_short_name()})")

    print()

stat(0, 0, 8)  # BLACK - 8-bit
stat(0, 0, 16)  # BLACK - 16-bit
stat(1, 1, 8)  # very dark color - 8-bit
stat(1, 1, 16)  # very dark color - 16-bit
stat(2**8 - 2, 2**8 - 2, 8)  # brightness color - 8-bit
stat(2**16 - 2, 2**16 - 2, 16)  # brightness color - 16-bit
stat(124, 123, 8)  # 20% Image surround reflectance - 8-bit
stat(118, 117, 8)  # 18% gray card - 8-bit
stat(15117, 15037, 15)  # 18% gray card - 15-bit
stat(30235, 30074, 16)  # 18% gray card - 16-bit