"""
    Comp128 v1 test cases
    Copyright (C) 2025  Lennart Rosam <hello@takuto.de>

    SPDX-License-Identifier: GPL-2.0-or-later

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see
    <https://www.gnu.org/licenses/>.
"""

from unittest import TestCase
from parameterized import parameterized
from comp128.comp128v1 import Comp128v1

class Comp128TestV1(TestCase):

 @parameterized.expand(
  [
   ["112233445566778899AABBCCDDEEFF00", "2233445566778899AABBCCDDEEFF0011", "3C0DCFBD", "F84A72DC312F6000"],
   ["AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB", "2EB9F582", "59A9CF45911C3400"],
  ]
 )

 def test_comp128v1(self, ki: str, rand: str, expected_sres: str, expected_kc: str):
     # GIVEN
     ki = bytearray.fromhex(ki)
     rand = bytearray.fromhex(rand)

     expected_sres = bytearray.fromhex(expected_sres)
     expected_kc = bytearray.fromhex(expected_kc)

     # WHEN
     under_test = Comp128v1()
     sres, kc = under_test.comp128v1(ki, rand)

     # THEN
     self.assertEqual(expected_sres, sres)
     self.assertEqual(expected_kc, kc)