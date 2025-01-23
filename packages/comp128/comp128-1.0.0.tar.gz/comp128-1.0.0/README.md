# COMP128 algorithms for Python

This is a Python implementation of the COMP128 algorithms used in the GSM A3/A8 authentication process.

## Usage example

```python
from comp128.comp128v23 import Comp128v23
from comp128.comp128v1 import Comp128v1

ki = bytearray(bytes.fromhex("00112233445566778899AABBCCDDEEFF"))
rand = bytearray(bytes.fromhex("00112233445566778899AABBCCDDEEFF"))

v1_sres, v1_kc = Comp128v1().comp128v1(ki, rand)
v2_sres, v2_kc = Comp128v23().comp128v2(ki, rand)
v3_sres, v3_kc = Comp128v23().comp128v3(ki, rand)

print(f"v1 SRES: {v1_sres.hex()}, KC: {v1_kc.hex()}")
print(f"v2 SRES: {v2_sres.hex()}, KC: {v2_kc.hex()}")
print(f"v3 SRES: {v3_sres.hex()}, KC: {v3_kc.hex()}")

```

This should output:

```
v1 SRES: 04a66ba8, KC: f87eb8222cea3400
v2 SRES: 6fb9eb06, KC: 605d954ffdefe800
v3 SRES: 6fb9eb06, KC: 605d954ffdefea7f
```

## Acknowledgements

This code is a Python conversion of the C source code of [libosmocore][1]. Full credit goes to the original authors:
- Harald Welte
- Kévin Redon
- Sylvain Munaut

and also to Alexander Couzens for invaluable help and feedback during this conversion.

## State of this project

This code is ready for use and has been tested to calculate correct authentication vectors both in unit-tests
and in a real-world scenario when calculating 2G authentication vectors on the 38C3 GSM network.

As such, this project is considered "done" and will not receive any further updates unless a bug is found,
or a future Python version breaks the code.

[1]: https://gitea.osmocom.org/osmocom/libosmocore