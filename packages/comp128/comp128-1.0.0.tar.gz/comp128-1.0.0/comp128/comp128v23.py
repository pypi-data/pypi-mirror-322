"""
    Comp128v23 - A Python implementation of the COMP128v2 / v3 algorithm used in GSM SIM cards

    This code is a Python conversion of the C code found in libosmocore:
    https://gitea.osmocom.org/osmocom/libosmocore/src/branch/master/src/gsm/comp128v23.c

    Copyright (C) 2011 sysmocom s.f.m.c. GmbH

    Converted to Python by:
    Lennart Rosam <hello@takuto.de>

    Original Authors:
    (C) 2010 by Harald Welte <laforge@gnumonks.org>
    (C) 2013 by Kévin Redon <kevredon@mail.tsaitgaist.info

    SPDX-License-Identifier: GPL-2.0+

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

class Comp128v23:
    """
    A Python implementation of the COMP128v2 / v3 algorithm used in GSM SIM cards
    """

    def __init__(self):
        self.table0 = [197, 235, 60, 151, 98, 96, 3, 100, 248, 118, 42, 117, 172, 211, 181, 203, 61,
                       126, 156, 87, 149, 224, 55, 132, 186, 63, 238, 255, 85, 83, 152, 33, 160,
                       184, 210, 219, 159, 11, 180, 194, 130, 212, 147, 5, 215, 92, 27, 46, 113,
                       187, 52, 25, 185, 79, 221, 48, 70, 31, 101, 15, 195, 201, 50, 222, 137,
                       233, 229, 106, 122, 183, 178, 177, 144, 207, 234, 182, 37, 254, 227, 231, 54,
                       209, 133, 65, 202, 69, 237, 220, 189, 146, 120, 68, 21, 125, 38, 30, 2,
                       155, 53, 196, 174, 176, 51, 246, 167, 76, 110, 20, 82, 121, 103, 112, 56,
                       173, 49, 217, 252, 0, 114, 228, 123, 12, 93, 161, 253, 232, 240, 175, 67,
                       128, 22, 158, 89, 18, 77, 109, 190, 17, 62, 4, 153, 163, 59, 145, 138,
                       7, 74, 205, 10, 162, 80, 45, 104, 111, 150, 214, 154, 28, 191, 169, 213,
                       88, 193, 198, 200, 245, 39, 164, 124, 84, 78, 1, 188, 170, 23, 86, 226,
                       141, 32, 6, 131, 127, 199, 40, 135, 16, 57, 71, 91, 225, 168, 242, 206,
                       97, 166, 44, 14, 90, 236, 239, 230, 244, 223, 108, 102, 119, 148, 251, 29,
                       216, 8, 9, 249, 208, 24, 105, 94, 34, 64, 95, 115, 72, 134, 204, 43,
                       247, 243, 218, 47, 58, 73, 107, 241, 179, 116, 66, 36, 143, 81, 250, 139,
                       19, 13, 142, 140, 129, 192, 99, 171, 157, 136, 41, 75, 35, 165, 26]
        self.table1 = [170, 42, 95, 141, 109, 30, 71, 89, 26, 147, 231, 205, 239, 212, 124, 129, 216,
                       79, 15, 185, 153, 14, 251, 162, 0, 241, 172, 197, 43, 10, 194, 235, 6,
                       20, 72, 45, 143, 104, 161, 119, 41, 136, 38, 189, 135, 25, 93, 18, 224,
                       171, 252, 195, 63, 19, 58, 165, 23, 55, 133, 254, 214, 144, 220, 178, 156,
                       52, 110, 225, 97, 183, 140, 39, 53, 88, 219, 167, 16, 198, 62, 222, 76,
                       139, 175, 94, 51, 134, 115, 22, 67, 1, 249, 217, 3, 5, 232, 138, 31,
                       56, 116, 163, 70, 128, 234, 132, 229, 184, 244, 13, 34, 73, 233, 154, 179,
                       131, 215, 236, 142, 223, 27, 57, 246, 108, 211, 8, 253, 85, 66, 245, 193,
                       78, 190, 4, 17, 7, 150, 127, 152, 213, 37, 186, 2, 243, 46, 169, 68,
                       101, 60, 174, 208, 158, 176, 69, 238, 191, 90, 83, 166, 125, 77, 59, 21,
                       92, 49, 151, 168, 99, 9, 50, 146, 113, 117, 228, 65, 230, 40, 82, 54,
                       237, 227, 102, 28, 36, 107, 24, 44, 126, 206, 201, 61, 114, 164, 207, 181,
                       29, 91, 64, 221, 255, 48, 155, 192, 111, 180, 210, 182, 247, 203, 148, 209,
                       98, 173, 11, 75, 123, 250, 118, 32, 47, 240, 202, 74, 177, 100, 80, 196,
                       33, 248, 86, 157, 137, 120, 130, 84, 204, 122, 81, 242, 188, 200, 149, 226,
                       218, 160, 187, 106, 35, 87, 105, 96, 145, 199, 159, 12, 121, 103, 112]

    def _comp128_v23_internal(self, output: bytearray, kxor: bytearray, rand: bytearray):
        temp = bytearray(16)
        km_rm = bytearray(32)

        for i in range(0, 16):
            km_rm[i] = rand[i]
            km_rm[i + 16] = kxor[i]

        for i in range(0, 5):
            for z in range(0, 16):
                temp[z] = self.table0[self.table1[km_rm[16 + z]] ^ km_rm[z]]

            j = 0
            while (1 << i) > j:
                k = 0
                while (1 << (4 - i)) > k:
                    km_rm[((2 * k + 1) << i) + j] = self.table0[
                        self.table1[temp[(k << i) + j]] ^ (km_rm[(k << i) + 16 + j])]
                    km_rm[(k << (i + 1)) + j] = temp[(k << i) + j]
                    k += 1
                j += 1

        for i in range(0, 16):
            output[i] = 0
            for j in range(0, 8):
                output[i] ^= (((km_rm[int((19 * (j + 8 * i) + 19) % 256 / 8)] >> (3 * j + 3) % 8) & 1) << j)

    def comp128v3(self, ki: bytearray, rand: bytearray):
        """
        Calculates SRES and KC using Comp128 V3
        :param ki: The SIM key (16 bytes)
        :param rand: 16 random bytes
        :return: A tuple of SRES and KC
        """
        k_mix = bytearray(16)
        rand_mix = bytearray(16)
        katyvasz = bytearray(16)
        output = bytearray(16)

        for i in range(0, 8):
            k_mix[i] = ki[15 - i]
            k_mix[15 - i] = ki[i]

        for i in range(0, 8):
            rand_mix[i] = rand[15 - i]
            rand_mix[15 - i] = rand[i]

        for i in range(0, 16):
            katyvasz[i] = k_mix[i] ^ rand_mix[i]

        for i in range(0, 8):
            self._comp128_v23_internal(rand_mix, katyvasz, rand_mix)

        for i in range(0, 16):
            output[i] = rand_mix[15 - i]

        output[4:12] = output[8:16]


        sres = bytearray(4)
        kc = bytearray(8)

        sres[:] = output[0:4]
        kc[:] = output[4:12]

        return sres, kc

    def comp128v2(self, ki: bytearray, rand: bytearray):
        """
        Calculates SRES and KC using Comp128 V2
        :param ki: The SIM key (16 bytes)
        :param rand: 16 random bytes
        :return: A tuple of SRES and KC
        """
        sres, kc = self.comp128v3(ki, rand)
        kc[7] = 0
        kc[6] &= 0xfc

        return sres, kc