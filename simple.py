from collections import Counter
from functools import reduce
import locale
from pathlib import Path
from itertools import batched
import random
from ra import RA

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8') 

RA_dict = dict(RA)
print(RA_dict)

RA_ordered = sorted(RA, key=lambda v: v[0])

def encrypt(s :str, plain_alphabet: str, mixed_alphabet: str) -> str:
    r = ""
    for c in s:
        try:
            i = plain_alphabet.index(c)
        except ValueError:
            print(c)
            raise
        if i == -1 or i >= len(mixed_alphabet):
            r += "."
        else:
            r += mixed_alphabet[i]
    return r

def nicer(s: str) -> str:
    return "\n".join([" ".join(x) for x in batched(["".join(v) for v in batched(s, 5)], 24)])

def liner(v: list[str]) -> str:
    return "".join(v)

original = Path("text-ru.txt").read_text()

clean = liner(filter(lambda x: x in RA_dict, map(lambda x: x.lower(), original)))

print("clean:")
print(clean, "\n")

ALPHABET = liner([x[0] for x in RA])
print(ALPHABET)

randomized_alphabet = [v for v in ALPHABET]
random.shuffle(randomized_alphabet)
randomized_alphabet = liner(randomized_alphabet)
print(randomized_alphabet, "\n")

encrypted = encrypt(clean, ALPHABET, randomized_alphabet)
print(nicer(encrypted), "\n")

def cmp(a: str, b: str) -> int:
    assert len(a) == len(b), f"{len(a)=} != {len(b)=}"
    for i, [x, y] in enumerate(zip(a, b)):
        assert x == y, f"{i}: {x} != {y}"
    return 0

decryted_check = encrypt(encrypted, randomized_alphabet, ALPHABET)
assert clean == decryted_check, cmp(clean, decryted_check)


encrypted_counters = Counter(encrypted)
print("encrypted_counters:")
print(encrypted_counters, len(encrypted_counters), "\n")

encrypted_counters_flat = encrypted_counters.most_common(len(encrypted_counters))
print("encrypted_counters_flat:")
print(encrypted_counters_flat, "\n")

encrypted_counters_normalized = [(k, v / len(encrypted)) for k, v in encrypted_counters_flat]
print("encrypted_counters_normalized:")
print(encrypted_counters_normalized, "\n")

missing_letters = set(ALPHABET) - set([x[0] for x in encrypted_counters_normalized])
print(missing_letters, "\n")

for v in missing_letters:
    encrypted_counters_normalized.append((v, 0))
assert len(encrypted_counters_normalized) == len(ALPHABET)

print(encrypted_counters_normalized, "\n")
print(RA, "\n")

recovered_alphabet = liner([x[0] for x in encrypted_counters_normalized])
print(ALPHABET)
print(randomized_alphabet)
print(recovered_alphabet, "\n")

for z in zip(RA, encrypted_counters_normalized):
    print(z, abs(z[0][1] - z[1][1]))


decryted = encrypt(encrypted, recovered_alphabet, ALPHABET)

diff = sum([1 for i in range(len(clean)) if clean[i] != decryted[i]])
print(f"{diff=}", f"{len(clean)=}", f"{diff/len(clean)*100=}", "\n")

print(nicer(decryted), "\n")
print(nicer(clean))
