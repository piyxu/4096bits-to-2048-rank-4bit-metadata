# -------------------------------------------------
# encode.py - 4096/2048k test
# MIT LICENSE
# MESUT ERTURHAN
https://github.com/piyxu/4096bits-to-2048-rank-4bit-metadata/
# -------------------------------------------------

from math import comb
import random

# -------------------------------------------------
#  Combination Rank / Unrank (fixed n, k)
# -------------------------------------------------

def unrank_nk(n: int, k: int, r: int):
    """
    Lexicographic combinational unrank.
    0 <= r < C(n,k)
    """
    bits = []
    rem = k
    for i in range(n):
        z = comb(n - i - 1, rem) if rem <= (n - i - 1) else 0
        if r < z:
            bits.append(0)
        else:
            bits.append(1)
            r -= z
            rem -= 1
    return bits

def rank_nk(bits, k_fixed: int):
    """
    Lexicographic combinational rank with fixed k.
    """
    n = len(bits)
    rem = k_fixed
    r = 0
    for i, b in enumerate(bits):
        if b == 1:
            z = comb(n - i - 1, rem)
            r += z
            rem -= 1
    return r

# -------------------------------------------------
#  4096 / 2048k helpers
# -------------------------------------------------


def unrank_4096_2048(r: int):
    return unrank_nk(4096, 2048, r)

def rank_4096_2048(bits):
    return rank_nk(bits, 2048)

C4096 = comb(4096, 2048)
MASK_4096 = (1 << 4096) - 1  # 4096-bit masking

def encode4096(R: int):
    """
    R in [0, 16 * C4096)
    Output:
        bits4096 : 4096-bit, contains 2048 ones
        m       : 0..15 (4-bit metadata)
    """

    if not (0 <= R < 16 * C4096):
        raise ValueError("R must be in [0, 16*C(4096,2048))")

    m   = R // C4096
    idx = R  % C4096
    bits4096 = unrank_4096_2048(idx)
    return bits4096, m

# -------------------------------------------------
#  MAIN PROGRAM
# -------------------------------------------------


def main():
    rng = random.Random()
    num_tests = 50  # increase/decrease if you like

    with open("originals.txt", "w") as f_ori, \
         open("encode.txt", "w") as f_enc:

        for _ in range(num_tests):
            # R in the range 0 .. 16*C4096
            R = rng.randrange(16 * C4096)

            # originals.txt: 4096-bit view of R (upper bits are discarded by masking)
            ori_bits = format(R & MASK_4096, "04096b")
            f_ori.write(ori_bits + "\n")

            # encode: R -> (balanced_4096, m)
            bits4096, m = encode4096(R)

            meta_bin = format(m, "04b")
            enc_bits = "".join(str(b) for b in bits4096)

            # encode.txt: 4 bit meta + 4096 bit balanced
            f_enc.write(meta_bin + enc_bits + "\n")

    print("Encode completed → originals.txt, encode.txt")

if __name__ == "__main__":
    main()


