import numpy as np

class ClinearCalculator:
    
    def calc_Clinear(self, CsRGB):
        pass

    def get_name(self):
        return self.__class__.__name__        


class ICCv2(ClinearCalculator):

    def calc_Clinear(self, CsRGB):
    
        if CsRGB <= 0.04045:
            return CsRGB / 12.92
        else:
            return ((CsRGB + 0.055) / 1.055) ** 2.4


class ICCv2_precise(ClinearCalculator):

    def calc_Clinear(self, CsRGB):
        
        if CsRGB <= 0.0392857:
            return CsRGB / 12.9232102
        else:
            return ((CsRGB + 0.055) / 1.055) ** 2.4


class ICCv4(ClinearCalculator):
    def calc_Clinear(self, CsRGB):
        if CsRGB <= 0.04045:
            return 0.0772059 * CsRGB + 0.0025
        else:
            return (0.946879 * CsRGB + 0.0520784) ** 2.4 + 0.0025


def calc_Lstar_for_monochrome(Clinear):

    R709_TO_XYZ_D65 = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]
    ])

    XYZ_D65 = np.dot(R709_TO_XYZ_D65, [Clinear] * 3)

    Yn = 1.0  # Reference white point
    Y = XYZ_D65[1]  # Y coordinate
    Y_div_Yn = Y / Yn

    if Y_div_Yn > 0.008856:
        return 116 * Y_div_Yn ** (1/3) - 16
    else:
        return 903.3 * Y_div_Yn


ICCv2_CALC = ICCv2()
ICCv2_precise_CALC = ICCv2_precise()
ICCv4_CALC = ICCv4()
ALL_CALCS = [ICCv2_CALC, ICCv2_precise_CALC, ICCv4_CALC]


def stat(CsRGB_number__ICCv2, CsRGB_number__ICCv4, bit_depth):

    CsRGB_numbers = {
        ICCv2_CALC: CsRGB_number__ICCv2,
        ICCv2_precise_CALC: CsRGB_number__ICCv2,
        ICCv4_CALC: CsRGB_number__ICCv4
    }

    CsRGBs = {}
    Clinears = {}
    Lstars = {}

    for calc in ALL_CALCS:
        CsRGBs[calc] = CsRGB_numbers[calc] / (2 ** bit_depth - 1)
        Clinears[calc] = calc.calc_Clinear(CsRGBs[calc])
        Lstars[calc] = calc_Lstar_for_monochrome(Clinears[calc])

    for calc in ALL_CALCS:
        print(f"CsRGB number {CsRGB_numbers[calc]:5d} /{bit_depth:2d} CsRGB in range [0..1]: {CsRGBs[calc]:0.5f} ({calc.get_name()})")

    for calc in ALL_CALCS:
        print(f"CsRGB number {CsRGB_numbers[calc]:5d} /{bit_depth:2d} Clinear in range [0..1]: {Clinears[calc]:0.5f} ({calc.get_name()})")

    for calc in ALL_CALCS:
        print(f"CsRGB number {CsRGB_numbers[calc]:5d} /{bit_depth:2d} L* in range [0..100]: {Lstars[calc]:0.2f} ({calc.get_name()})")

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