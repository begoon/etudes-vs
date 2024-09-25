from collections import Counter
from pathlib import Path
from itertools import batched
import random
from ra import RA

def encrypt(s :str, alphabet: str) -> str:
    assert len(ALPHABET_LETTERS) == 33
    if len(alphabet) < len(ALPHABET_LETTERS):
        print(f"warning: {len(alphabet)=} is too short")
    r = ""
    for c in s:
        i = ALPHABET_LETTERS.index(c)
        if i >= len(alphabet):
            r += "."
        else:
            r += alphabet[i]
    return r

original = Path("text-ru.txt").read_text()
clean = "".join(map(str.lower, filter(lambda x: x.isalpha(), original)))

def nicer(s: str) -> str:
    return "\n".join([" ".join(x) for x in batched(["".join(v) for v in batched(s, 5)], 16)])

def liner(v: list[str]) -> str:
    return "".join(v)

print(nicer(clean))

ALPHABET_LETTERS = [x[0] for x in RA]
print(liner(ALPHABET_LETTERS), "\n")

randomized_letters = ALPHABET_LETTERS.copy()
random.shuffle(randomized_letters)
print(liner(randomized_letters), "\n")

encrypted = encrypt(clean, liner(randomized_letters))
print(nicer(encrypted), end="\n\n")

letters_counts = Counter(ALPHABET_LETTERS)
print(letters_counts, "\n")
letters_counts_tuples = letters_counts.most_common(len(letters_counts))
print(letters_counts_tuples, "\n")


encrypted_counters = Counter(encrypted)
print(encrypted_counters, len(encrypted_counters), "\n")
encrypted_counters_flat = encrypted_counters.most_common(len(encrypted_counters))
print(encrypted_counters_flat, "\n")
encrypted_counters_normalized = [(k, v / len(encrypted)) for k, v in encrypted_counters.items()]
print(encrypted_counters_normalized, "\n")
encrypted_counters_normalized_sorted = sorted(encrypted_counters_normalized, key=lambda x: x[1], reverse=True)
print(encrypted_counters_normalized_sorted, "\n")

print(RA, "\n")

recovered_letters = [x[0] for x in encrypted_counters_normalized_sorted]
recovered_alphabet = liner(recovered_letters)
print(recovered_alphabet, "\n")

# print("".join(randomized_letters), "\n")

decryted = encrypt(encrypted, recovered_alphabet)
print(nicer(decryted))
