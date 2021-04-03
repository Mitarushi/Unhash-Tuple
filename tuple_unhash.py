import random
import typing
import argparse


# https://tjkendev.github.io/procon-library/python/math/modular-multiplicative-inverse.html
def extgcd(a, b):
    if b:
        d, y, x = extgcd(b, a % b)
        y -= (a // b)*x
        return d, x, y
    return a, 1, 0


def inverse(a, m):
    d, x, _ = extgcd(a, m)
    if d != 1:
        # no inverse exists
        return -1
    return x % m


# https://github.com/python/cpython/blob/80017752ba938852d53f9d83a404b4ecd9ff2baa/Objects/tupleobject.c#L392
MOD = 1 << 64
INT_HASH_MOD = (1 << 61) + 1
PYHASH_XXPRIME_1 = 11400714785074694791
PYHASH_XXPRIME_2 = 14029467366897019727
PYHASH_XXPRIME_5 = 2870177450012600261
PYHASH_XXPRIME_1_INV = inverse(PYHASH_XXPRIME_1, MOD)
PYHASH_XXPRIME_2_INV = inverse(PYHASH_XXPRIME_2, MOD)

# https://github.com/python/cpython/blob/caba55b3b735405b280273f7d99866a046c18281/Objects/tupleobject.c#L348
PYHASH_PARAM_OLD_1 = 0x345678
PYHASH_PARAM_OLD_2 = 1000003
PYHASH_PARAM_OLD_3 = 82520
PYHASH_PARAM_OLD_4 = 97531
PYHASH_PARAM_OLD_2_INV = inverse(PYHASH_PARAM_OLD_2, MOD)


def PYHASH_XXROTATE(x: int) -> int:
    return ((x << 31) | (x >> 33)) % MOD


def PYHASH_XXROTATE_REV(x: int) -> int:
    return ((x << 33) | (x >> 31)) % MOD


# https://github.com/python/cpython/blob/80017752ba938852d53f9d83a404b4ecd9ff2baa/Objects/tupleobject.c#L405
def tuple_hash(v: typing.Tuple[int]) -> int:
    length = len(v)

    acc = PYHASH_XXPRIME_5
    for i in v:
        lane = hash(i)
        acc = (acc + lane * PYHASH_XXPRIME_2) % MOD
        acc = PYHASH_XXROTATE(acc)
        acc = (acc * PYHASH_XXPRIME_1) % MOD

    acc = (acc + (length ^ PYHASH_XXPRIME_5 ^ 3527539)) % MOD

    return acc


def _tuple_unhash(length: int,
                  acc: int,
                  rand_min: int = 0,
                  rand_max: int = INT_HASH_MOD-1) -> typing.Tuple[int]:
    acc = (acc - (length ^ PYHASH_XXPRIME_5 ^ 3527539)) % MOD
    v = []

    for i in range(length - 1):
        x = random.randint(rand_min, rand_max)
        lane = hash(x)
        v.append(x)

        acc = acc * PYHASH_XXPRIME_1_INV % MOD
        acc = PYHASH_XXROTATE_REV(acc)
        acc = (acc - lane * PYHASH_XXPRIME_2) % MOD

    acc = acc * PYHASH_XXPRIME_1_INV % MOD
    acc = PYHASH_XXROTATE_REV(acc)
    lane = (acc - PYHASH_XXPRIME_5) * PYHASH_XXPRIME_2_INV % MOD
    v.append(lane)

    return tuple(v[::-1])


def tuple_unhash(length: int,
                 h: int = -1,
                 rand_min: int = 0,
                 rand_max: int = INT_HASH_MOD-1) -> typing.Tuple[int]:
    if h == -1:
        h = random.randint(0, MOD-1)
    assert 0 <= h < MOD
    assert rand_max < INT_HASH_MOD

    while True:
        v = _tuple_unhash(length, h, rand_min, rand_max)

        if rand_min <= v[0] <= rand_max:
            return v


def tuple_hash_old(v: typing.Tuple[int]) -> int:
    length = len(v)
    acc = PYHASH_PARAM_OLD_1
    mult = PYHASH_PARAM_OLD_2

    for i in v:
        length -= 1
        x = hash(i)
        acc = (acc ^ x) * mult % MOD
        mult = (mult + PYHASH_PARAM_OLD_3 + length * 2)

    acc = (acc + PYHASH_PARAM_OLD_4) % MOD
    return acc


def _tuple_unhash_old(length: int,
                      acc: int,
                      rand_min: int = 0,
                      rand_max: int = INT_HASH_MOD-1) -> typing.Tuple[int]:
    acc = (acc - PYHASH_PARAM_OLD_4) % MOD
    mult = (PYHASH_PARAM_OLD_2 + PYHASH_PARAM_OLD_3 * length) % MOD
    mult = (mult + (length - 1) * length) % MOD

    v = []

    for i in range(length - 1):
        x = random.randint(rand_min, rand_max)
        lane = hash(x)
        v.append(x)

        mult = (mult - PYHASH_PARAM_OLD_3 - i * 2) % MOD
        acc = acc * inverse(mult, MOD) % MOD ^ x

    lane = acc * inverse(PYHASH_PARAM_OLD_2, MOD) % MOD ^ PYHASH_PARAM_OLD_1
    v.append(lane)

    return tuple(v[::-1])


def tuple_unhash_old(length: int,
                     h: int = -1,
                     rand_min: int = 0,
                     rand_max: int = INT_HASH_MOD-1) -> typing.Tuple[int]:
    if h == -1:
        h = random.randint(0, MOD-1)
    assert 0 <= h < MOD
    assert rand_max < INT_HASH_MOD

    while True:
        v = _tuple_unhash_old(length, h, rand_min, rand_max)

        if rand_min <= v[0] <= rand_max:
            return v


parser = argparse.ArgumentParser()
parser.add_argument("N", type=int,
                    help="number of tuples")
parser.add_argument("length", type=int,
                    help="tuple length")
parser.add_argument("-hash", type=int, default=-1,
                    help="hash of tuples ( hash=-1 : hash is set to a random number )")
parser.add_argument("-rand_min", type=int, default=1,
                    help="minimum of tuple item (default : 1 )")
parser.add_argument("-rand_max", type=int, default=10**18,
                    help="maximum of tuple item (default : 10^18 )")
parser.add_argument("-o", "--old", action="store_true",
                    help="old version hash algorithm")
parser.add_argument("-f", "--format", action="store_true",
                    help="output formatted tuple")


if __name__ == "__main__":
    args = parser.parse_args()

    N = args.N
    length = args.length
    h = args.hash
    rand_min = args.rand_min
    rand_max = args.rand_max

    if h == -1:
        h = random.randint(0, MOD-1)

    for _ in range(N):
        if args.old:
            v = tuple_unhash_old(length, h, rand_min, rand_max)
        else:
            v = tuple_unhash(length, h, rand_min, rand_max)

        if args.format:
            if args.old:
                hashed = tuple_hash_old(v)
            else:
                hashed = tuple_hash(v)

            print("tuple: %s\thash: %s" % (v, hashed))
        else:
            print(*v)
