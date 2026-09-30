#!/usr/bin/env python3
"""Plant a witness for sweep.c: choose a 32-char key template with a few free
positions, encrypt a known 8-byte payload under segment N's IV, and print the
base64 ciphertext plus the sweep invocation."""
import base64
import sys
sys.path.insert(0, "tools")
from Cryptodome.Cipher import AES

IVS = {1: b"few_n_far_btween", 2: b"nocturnal_sugars",
       3: b"colors_on_leaves", 4: b"seconds_of_dream"}

seg = int(sys.argv[1]) if len(sys.argv) > 1 else 1
key = (sys.argv[2] if len(sys.argv) > 2 else "HELLOWORLD_this_is_a_witness_key_")
key = key[:32].ljust(32)
payload = (sys.argv[3] if len(sys.argv) > 3 else "WITNESS8").encode()[:8]
assert len(payload) == 8
pt = payload + b"\x08" * 8
ct = AES.new(key.encode(), AES.MODE_CBC, IVS[seg]).encrypt(pt)
print("key     :", key)
print("payload :", payload.decode())
print("ct b64  :", base64.b64encode(ct).decode())
