import math

# import matplotlib.pyplot as pl
# import numpy as np


class Color:
    __rgb: (float, float, float)
    __hsl: (float, float, float)

    def __init__(self, r: float, g: float, b: float):
        for num in r, g, b:
            if not (0 <= num <= 255):
                raise ValueError(f"rgb value [{num}] invalid")

        self.__rgb = (r / 255, g / 255, b / 255)
        self.__hsl = self.__to_hsl()

    @classmethod
    def from_rgb_tuple(cls, rgb: (float, float, float)):
        return cls(rgb[0], rgb[1], rgb[2])

    @classmethod
    def from_hsl(cls, h: float, s: float, l: float):
        if not 0 <= h < 360:
            h = h % 360

        if not 0 <= s <= 1:
            raise ValueError(f"Saturation value[{s}] error")

        if not 0 <= l <= 1:
            raise ValueError(f"Lightness value[{l}] error")

        r = cls.__hsl_function(h, s, l, 0) * 255
        g = cls.__hsl_function(h, s, l, 8) * 255
        b = cls.__hsl_function(h, s, l, 4) * 255
        return cls(r, g, b)

    @classmethod
    def from_hsl_tuple(cls, hsl: (float, float, float)):
        return cls.from_hsl(hsl[0], hsl[1], hsl[2])

    @staticmethod
    def __hsl_function(h: float, s: float, l: float, n: int):
        a = s * min(l, 1 - l)
        k = (n + (h / 30)) % 12
        return l - a * max(min(k - 3, 9 - k, 1), -1)

    def get_rgb(self) -> (float, float, float):
        return self.__rgb

    def get_rgb_int(self) -> (int, int, int):
        return int(self.__rgb[0] * 255), int(self.__rgb[1] * 255), int(self.__rgb[2] * 255)

    def get_hsl(self) -> (float, float, float):
        return self.__hsl

    def to_code(self) -> str:
        return f"#{hex(int(self.__rgb[0] * 255))[-2:].replace('x', '0')}" \
            f"{hex(int(self.__rgb[1] * 255))[-2:].replace('x', '0')}" \
            f"{hex(int(self.__rgb[2] * 255))[-2:].replace('x', '0')}"

    def __str__(self):
        hsl_var = (math.degrees(self.__hsl[0]), self.__hsl[1], self.__hsl[2])
        return f"Color[rgb: {self.__rgb}, hsl: {hsl_var}, code: {self.to_code()}]"

    def __to_hsl(self) -> (float, float, float):
        """
        hsl indicates hue, saturation and lightness
        :return: hsl tri-tuple
        """
        max_c = max(self.__rgb)
        min_c = min(self.__rgb)

        h: float = 0
        s: float = 0
        l: float = 0.5 * (max_c + min_c)

        d = max_c - min_c

        # while max == min, rgb are equal to each other, that is, the sum vector is 0
        if d == 0:
            h = 0
        elif max_c == self.__rgb[0]:
            h = 60 * ((self.__rgb[1] - self.__rgb[2]) / d)
        elif max_c == self.__rgb[1]:
            h = 60 * (2 + ((self.__rgb[2] - self.__rgb[0]) / d))
        elif max_c == self.__rgb[2]:
            h = 60 * (4 + ((self.__rgb[0] - self.__rgb[1]) / d))
        h = math.radians(h)

        if not d == 0:
            s = ((max_c - l) / (min(l, 1 - l)))

        return h, s, l


white = Color(255, 255, 255)
black = Color(0, 0, 0)


class Divider:
    light_white = 0.8
    light_black = 0.2

    __divide_count: int

    __zero: int

    def __init__(self, divide_vector: int = 3, zero=0):
        self.__divide_count = divide_vector * 6
        self.__zero = zero

    def apply(self, target: Color) -> int:
        angle: float = 360.0 / self.__divide_count
        hsl = target.get_hsl()

        # if lightness > 0.8 -> white
        # else if lightness < 0.2 -> black
        if hsl[2] > Divider.light_white:
            return self.__divide_count + 1
        elif hsl[2] < Divider.light_black:
            return self.__divide_count
        return (int(((math.degrees(hsl[0]) - self.__zero + angle / 2) % 360) // angle)) % self.__divide_count

    def count(self):
        return self.__divide_count + 2

    def get_white_index(self):
        return self.__divide_count + 1

    def get_black_index(self):
        return self.__divide_count

    def get_color_by_index(self, index: int) -> Color:
        if index == self.get_white_index():
            return white
        elif index == self.get_black_index():
            return black
        else:
            angle: float = 360.0 / self.__divide_count
            return Color.from_hsl(self.__zero + angle * index, 1, 0.5)

    # def display(self, target: Color):
    #     """
    #     this is for visually testing, don't use it in data process
    #     """
    #     g = pl.subplot(111, polar=True)
    #     g.set_rmax(1)
    #     g.plot(0, 1)
    #     g.set_theta_zero_location('N')
    #     pl.thetagrids(range(360 // self.__divide_count // 2, 360, 360 // self.__divide_count))
    #
    #     r = np.arange(0, target.get_hsl()[1], 0.01)
    #     r.fill(1)
    #     g.plot(target.get_hsl()[0] * r,
    #            np.arange(0, target.get_hsl()[1], 0.01),
    #            color=target.to_code())
    #
    #     pl.show()
