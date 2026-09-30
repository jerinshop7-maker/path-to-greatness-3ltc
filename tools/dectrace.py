#!/usr/bin/env python3
"""Stage-by-stage AES-256 decrypt trace, matching decdrv.c output format.

usage: python3 tools/dectrace.py <key-hex-64> <ct-hex-32>
"""
import sys

key = bytes.fromhex(sys.argv[1])
ct = bytes.fromhex(sys.argv[2])

SBOX = bytes.fromhex(
    "637c777bf26b6fc53001672bfed7ab76ca82c97dfa5947f0add4a2af9ca472c0"
    "b7fd9326363ff7cc34a5e5f171d8311504c723c31896059a071280e2eb27b275"
    "09832c1a1b6e5aa0523bd6b329e32f8453d100ed20fcb15b6acbbe394a4c58cf"
    "d0efaafb434d338545f9027f503c9fa851a3408f929d38f5bcb6da2110fff3d2"
    "cd0c13ec5f974417c4a77e3d645d197360814fdc222a908846eeb814de5e0bdb"
    "e0323a0a4906245cc2d3ac629195e479e7c8376d8dd54ea96c56f4ea657aae08"
    "ba78252e1ca6b4c6e8dd741f4bbd8b8a703eb5664803f60e613557b986c11d9e"
    "e1f8981169d98e949b1e87e9ce5528df8ca1890dbfe6426841992d0fb054bb16")
ISBOX = bytearray(256)
for _x in range(256):
    ISBOX[SBOX[_x]] = _x
ISBOX = bytes(ISBOX)


def xt(x):
    return ((x << 1) ^ 0x1b) & 0xff if x & 0x80 else (x << 1)


M1 = [xt(x) for x in range(256)]
M2 = [M1[M1[x]] for x in range(256)]
M8 = [M1[M2[x]] for x in range(256)]
M9 = [M8[x] ^ x for x in range(256)]
M11 = [M8[x] ^ M1[x] ^ x for x in range(256)]
M13 = [M8[x] ^ M2[x] ^ x for x in range(256)]
M14 = [M8[x] ^ M2[x] ^ M1[x] for x in range(256)]

# key schedule (identical to sweep.c)
rk = list(key)
RCON = [0, 1, 2, 4, 8, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
i = 8
while i < 60:
    t = rk[4 * i - 4:4 * i]
    if i % 8 == 0:
        t = [SBOX[t[1]] ^ RCON[i // 8], SBOX[t[2]], SBOX[t[3]], SBOX[t[0]]]
    elif i % 8 == 4:
        t = [SBOX[b] for b in t]
    rk += [rk[4 * (i - 8)] ^ t[0], rk[4 * (i - 8) + 1] ^ t[1],
           rk[4 * (i - 8) + 2] ^ t[2], rk[4 * (i - 8) + 3] ^ t[3]]
    i += 1


def H(b):
    return "".join("%02x" % v for v in b)


s = list(ct)
for i in range(16):
    s[i] ^= rk[224 + i]
print("ARK14", H(s))
for r in range(13, 0, -1):
    u = [0] * 16
    u[0] = ISBOX[s[0]];  u[4] = ISBOX[s[4]];  u[8] = ISBOX[s[8]];   u[12] = ISBOX[s[12]]
    u[1] = ISBOX[s[13]]; u[5] = ISBOX[s[1]];  u[9] = ISBOX[s[5]];   u[13] = ISBOX[s[9]]
    u[2] = ISBOX[s[10]]; u[6] = ISBOX[s[14]]; u[10] = ISBOX[s[2]];  u[14] = ISBOX[s[6]]
    u[3] = ISBOX[s[7]];  u[7] = ISBOX[s[11]]; u[11] = ISBOX[s[15]]; u[15] = ISBOX[s[3]]
    print("ISB%02d" % r, H(u))
    u = [u[i] ^ rk[16 * r + i] for i in range(16)]
    print("ARK%02d" % r, H(u))
    t = [0] * 16
    for c in range(4):
        a = u[4 * c:4 * c + 4]
        t[4 * c + 0] = M14[a[0]] ^ M11[a[1]] ^ M13[a[2]] ^ M9[a[3]]
        t[4 * c + 1] = M9[a[0]] ^ M14[a[1]] ^ M11[a[2]] ^ M13[a[3]]
        t[4 * c + 2] = M13[a[0]] ^ M9[a[1]] ^ M14[a[2]] ^ M11[a[3]]
        t[4 * c + 3] = M11[a[0]] ^ M13[a[1]] ^ M9[a[2]] ^ M14[a[3]]
    s = t
    print("IMC%02d" % r, H(s))
u = [0] * 16
u[0] = ISBOX[s[0]];  u[4] = ISBOX[s[4]];  u[8] = ISBOX[s[8]];   u[12] = ISBOX[s[12]]
u[1] = ISBOX[s[13]]; u[5] = ISBOX[s[1]];  u[9] = ISBOX[s[5]];   u[13] = ISBOX[s[9]]
u[2] = ISBOX[s[10]]; u[6] = ISBOX[s[14]]; u[10] = ISBOX[s[2]];  u[14] = ISBOX[s[6]]
u[3] = ISBOX[s[7]];  u[7] = ISBOX[s[11]]; u[11] = ISBOX[s[15]]; u[15] = ISBOX[s[3]]
u = [u[i] ^ rk[i] for i in range(16)]
print("out  ", H(u))

# ground truth
from Cryptodome.Cipher import AES
print("truth", AES.new(key, AES.MODE_ECB).decrypt(ct).hex())
