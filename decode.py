# -------------------------------------------------
# encode.py - 4096/2048k test
# MIT LICENSE
# MESUT ERTURHAN
# https://github.com/piyxu/4096bits-to-2048k-rank-4bit-metadata/
# -------------------------------------------------

from math import comb

# -------------------------------------------------
#  Combination Rank / Unrank
# -------------------------------------------------


def unrank_nk(n: int, k: int, r: int):
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
    n = len(bits)
    rem = k_fixed
    r = 0
    for i, b in enumerate(bits):
        if b == 1:
            z = comb(n - i - 1, rem)
            r += z
            rem -= 1
    return r

def unrank_4096_2048(r: int):
    return unrank_nk(4096, 2048, r)

def rank_4096_2048(bits):
    return rank_nk(bits, 2048)

C4096 = comb(4096, 2048)
MASK_4096 = (1 << 4096) - 1

def decode4096(bits4096, m: int):
    """
    encode4096'in tersi:
        bits4096 (2048 tane 1) + m → R
    """
    idx = rank_4096_2048(bits4096)
    R = m * C4096 + idx
    return R

# -------------------------------------------------
#  MAIN PROGRAM
# -------------------------------------------------

def main():
    with open("originals.txt") as f_ori, \
         open("encode.txt") as f_enc, \
         open("decode.txt", "w") as f_dec, \
         open("reports.txt", "w") as f_rep:

        ori_lines = [line.strip() for line in f_ori]
        enc_lines = [line.strip() for line in f_enc]

        for idx, (ori, enc) in enumerate(zip(ori_lines, enc_lines)):

            # encode.txt: 4 bit meta + 4096 bit balanced
            meta_bin = enc[:4]
            bits_str = enc[4:]

            m = int(meta_bin, 2)
            bits4096 = [int(b) for b in bits_str]

            # ---- decode: only from encode.txt ----
            R2 = decode4096(bits4096, m)

            # rebuild 4096-bit form (same rule as MASK_4096)
            dec_bits = format(R2 & MASK_4096, "04096b")
            f_dec.write(dec_bits + "\n")

            # ---- K values ----
            k_ori = ori.count("1")
            k_enc = bits_str.count("1")       # expected to be 2048
            k_dec = dec_bits.count("1")

            same = "TRUE" if ori == dec_bits else "FALSE"

            f_rep.write(
                f"{idx:03d}: "
                f"K_ori={k_ori:3d}  "
                f"K_enc={k_enc:3d}  "
                f"K_dec={k_dec:3d}  "
                f"SAME={same}\n"
            )

    print("Decode completed → decode.txt, reports.txt")

if __name__ == "__main__":
    main()
