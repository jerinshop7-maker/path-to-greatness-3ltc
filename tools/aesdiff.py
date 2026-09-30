#!/usr/bin/env python3
"""Round-by-round diff of the C engine's AES-256 against pycryptodomex.

Reimplements exactly the C logic in sweep.c (flat-index ShiftRows, per-column
MixColumns, key schedule, 13 body rounds + final round) and compares the state
after every round against the trusted implementation.
"""
from Cryptodome.Cipher import AES

SBOX = bytes.fromhex(
    "637c777bf26b6fc53001672bfed7ab76ca82c97dfa5947f0add4a2af9ca472c0"
    "b7fd9326363ff7cc34a5e5f171d8311504c723c31896059a071280e2eb27b275"
    "09832c1a1b6e5aa0523bd6b329e32f8453d100ed20fcb15b6acbbe394a4c58cf"
    "d0efaafb434d338545f9027f503c9fa851a3408f929d38f5bcb6da2110fff3d2"
    "cd0c13ec5f974417c4a77e3d645d197360814fdc222a908846eeb814de5e0bdb"
    "e0323a0a4906245cc2d3ac629195e479e7c8376d8dd54ea96c56f4ea657aae08"
    "ba78252e1ca6b4c6e8dd741f4bbd8b8a703eb5664803f60e613557b986c11d9e"
    "e1f8981169d98e949b1e87e9ce5528df8ca1890dbfe6426841992d0fb054bb16")
RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

MUL1 = [((x << 1) ^ 0x1b) & 0xff if x & 0x80 else (x << 1) for x in range(256)]
MUL2 = [MUL1[MUL1[x]] for x in range(256)]
MUL3 = [MUL1[x] ^ x for x in range(256)]  # 3x = 2x ^ x


def expand(key32):
    rk = list(key32)
    i = 8
    while i < 60:
        t = rk[4 * i - 4:4 * i]
        if i % 8 == 0:
            t = [SBOX[t[1]] ^ RCON[i // 8], SBOX[t[2]], SBOX[t[3]], SBOX[t[0]]]
        elif i % 8 == 4:
            t = [SBOX[b] for b in t]
        rk += [(rk[4 * (i - 8)] ^ t[0]), (rk[4 * (i - 8) + 1] ^ t[1]),
               (rk[4 * (i - 8) + 2] ^ t[2]), (rk[4 * (i - 8) + 3] ^ t[3])]
        i += 1
    return rk


def sub_shift_flat(s):
    """C engine's flat-index SubBytes+ShiftRows: u[4c+r] = SBOX[s[4*((c+r)%4)+r]]..."""
    u = [0] * 16
    u[0] = SBOX[s[0]];  u[4] = SBOX[s[4]];  u[8] = SBOX[s[8]];   u[12] = SBOX[s[12]]
    u[1] = SBOX[s[5]];  u[5] = SBOX[s[9]];  u[9] = SBOX[s[13]];  u[13] = SBOX[s[1]]
    u[2] = SBOX[s[10]]; u[6] = SBOX[s[14]]; u[10] = SBOX[s[2]];  u[14] = SBOX[s[6]]
    u[3] = SBOX[s[15]]; u[7] = SBOX[s[3]];  u[11] = SBOX[s[7]];  u[15] = SBOX[s[11]]
    return u


def mix_col(a):
    return [(MUL1[a[0]] ^ MUL3[a[1]] ^ a[2] ^ a[3]),
            (a[0] ^ MUL1[a[1]] ^ MUL3[a[2]] ^ a[3]),
            (a[0] ^ a[1] ^ MUL1[a[2]] ^ MUL3[a[3]]),
            (MUL3[a[0]] ^ a[1] ^ a[2] ^ MUL1[a[3]])]


def my_encrypt(key32, pt16, trace=None):
    rk = expand(key32)
    s = list(pt16)
    if trace is not None:
        trace.append(("input", bytes(s)))
    for r in range(13):
        for i in range(16):
            s[i] ^= rk[16 * r + i]
        if trace is not None:
            trace.append((f"after ARK{r}", bytes(s)))
        u = sub_shift_flat(s)
        t = [0] * 16
        for c in range(4):
            t[4 * c:4 * c + 4] = mix_col(u[4 * c:4 * c + 4])
        s = t
        if trace is not None:
            trace.append((f"after round{r}", bytes(s)))
    # final: ARK(13) then SubBytes+ShiftRows then ARK(14)
    for i in range(16):
        s[i] ^= rk[208 + i]
    u = sub_shift_flat(s)
    out = [u[i] ^ rk[224 + i] for i in range(16)]
    if trace is not None:
        trace.append(("out", bytes(out)))
    return bytes(out)


def main():
    key = bytes.fromhex("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4")
    pt = bytes.fromhex("6bc1bee22e409f96e93d7e117393172a")
    want = bytes.fromhex("f3eed1bdb5d2a03c064b5a7e3db181f8")
    got = my_encrypt(key, pt)
    print("mine    :", got.hex())
    print("expected:", want.hex())
    print("MATCH" if got == want else "MISMATCH")

    # also compare against pycryptodome ECB
    c = AES.new(key, AES.MODE_ECB)
    print("pycrypto:", c.encrypt(pt).hex())

    trace = []
    my_encrypt(key, pt, trace)
    for name, st in trace:
        print(f"  {name:12s} {st.hex()}")


if __name__ == "__main__":
    main()
