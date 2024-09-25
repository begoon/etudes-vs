from collections import Counter
from functools import reduce
from pathlib import Path
from itertools import batched
import random
from ra import RA

def LETTER_INDEX(c: str) -> int:
    return ALPHABET.index(c)

def encrypt(s :str, plain_alphabet: str, mixed_alphabet: str) -> str:
    r = ""
    for c in s:
        try:
            i = plain_alphabet.index(c)
        except ValueError:
            i = -1
        if i == -1 or i >= len(mixed_alphabet):
            r += "."
        else:
            r += mixed_alphabet[i]
    return r

def nicer(s: str) -> str:
    return "\n".join([" ".join(x) for x in batched(["".join(v) for v in batched(s, 5)], 24)])

def liner(v: list[str]) -> str:
    return "".join(v)

original = Path("text-ru-2.txt").read_text()

clean = liner(map(str.lower, filter(lambda x: x.isalpha(), original)))

print(clean, "\n")

ALPHABET = liner([x[0] for x in RA])
print(ALPHABET)

randomized_alphabet = [v for v in ALPHABET]
random.shuffle(randomized_alphabet)
randomized_alphabet = liner(randomized_alphabet)
print(randomized_alphabet, "\n")

encrypted = encrypt(clean, ALPHABET, randomized_alphabet)
print(nicer(encrypted), "\n")

decryted_check = encrypt(encrypted, randomized_alphabet, ALPHABET)
assert clean == decryted_check

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

diffs = sum([1 for i in range(len(clean)) if clean[i] != decryted[i]])
print(diffs, len(clean), diffs / len(clean) * 100, "\n")

print(nicer(decryted), "\n")

print(nicer(clean))
