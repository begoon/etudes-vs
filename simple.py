from collections import Counter
from functools import reduce
import locale
from pathlib import Path
from itertools import batched
import random
from ra import RA

TEXT ="text-ru-XXX.txt"

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8') 

RA_dict = dict(RA)
RA_ordered = sorted(RA, key=lambda v: v[0])

def substitution(s: str, from_alphabet: str, to_alphabet: str) -> str:
    r = ""
    for c in s:
        i = from_alphabet.find(c)
        assert i >= 0, f"{c=} not in {from_alphabet=}"
        assert i < len(to_alphabet), f"{c=} {i=}, {len(to_alphabet)=}"
        r += to_alphabet[i]
    return r

def table5(s: str) -> str:
    return "\n".join([" ".join(x) for x in batched(["".join(v) for v in batched(s, 5)], 24)])

def to_string(v: list[str]) -> str:
    return "".join(v)

def println(v: str | int | float, title: str = None, width: int = 0, nl: bool = False):
    title_ = f"{title}: " if title else ""
    if isinstance(v, (int, float)):
        print(f"{title_:>{width}} {v}")
    else:
        print(f"{title_:>{width}}({len(v)}) {v[:100]}")
    if nl:
        print()

def print5(s: str, title: str):
    print(f"{title}: {len(s)=}")
    s = s if len(s) < 1000 else s[:500] + "..."
    print(table5(s))
    print()


AZ = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
def COUNT(s: str) -> list[tuple[str, int, float]]:
    counters = Counter(s)
    counters_flat = counters.most_common(len(counters))
    counters_normalized = [(k, v, v / len(s)) for k, v in counters_flat]
    missing = set(AZ) - set([x[0] for x in counters_normalized])
    counters_normalized.extend([(k, 0, 0) for k in missing])
    assert len(counters_normalized) == len(AZ), f"{len(counters_normalized)=} != {len(AZ)=}"

    total_count = sum([x[1] for x in counters_normalized])
    total_sum = sum([x[2] for x in counters_normalized])

    chi = CHI_SQUARE(s)
    ci = COINCIDENCE(s)
    print(f'length={len(s)} chi={chi} ci={ci}')
    assert total_count == len(s), f"{total_count=} != {len(s)=}"
    assert total_sum == 1.0, f"{total_sum=} != 1.0"

    for batch in batched(counters_normalized, 4):
        print(" | ".join([f"{l} {c: 7} {f:0.6f}" for l, c, f in batch]))
    print()

    return counters_normalized

def CHI_SQUARE(s: str) -> float:
    counters = Counter(s)
    counters_flat = counters.most_common(len(counters))
    diffs = []
    for k, v in counters_flat:
        v_expected = len(s) * RA_dict[k]
        False and print(f"{k=} {v=} {v_expected=}")
        diffs.append((v - v_expected) ** 2 / v_expected)
    return sum(diffs)

def COINCIDENCE(s: str) -> float:
    counters = Counter(s)
    counters_flat = counters.most_common(len(counters))
    counters_normalized = [(k, v, v / len(s)) for k, v in counters_flat]
    return sum([v * (v - 1) for k, v, p in counters_normalized]) / (len(s) * (len(s) - 1))

def cmp(a: str, b: str) -> int:
    assert len(a) == len(b), f"{len(a)=} != {len(b)=}"
    for i, [x, y] in enumerate(zip(a, b)):
        assert x == y, f"{i}: {x} != {y}"
    return 0

# -------------------------------

ALPHABET = to_string([x[0] for x in RA])
println(ALPHABET, "ALPHABET", nl=True)

original = Path(TEXT).read_text()

plain = to_string(filter(lambda x: x in RA_dict, map(lambda x: x.lower(), original)))

print5(plain, "plain")

print("clean:")
plain_counts = COUNT(plain)

randomized_alphabet = [v for v in ALPHABET]
# random.shuffle(randomized_alphabet)
randomized_alphabet = to_string(randomized_alphabet)

println(ALPHABET, "plain alphabet", 22)
println(randomized_alphabet, "randomized alphabet", 22)
print()

encrypted = substitution(plain, ALPHABET, randomized_alphabet)
print5(encrypted, "encrypted")

println(COINCIDENCE(plain), "clean coincidence", 23)
println(COINCIDENCE(encrypted), "encrypted coincidence", 23)
print()

decryted_check = substitution(encrypted, randomized_alphabet, ALPHABET)
assert plain == decryted_check, cmp(plain, decryted_check)

encrypted_counters = COUNT(encrypted)

recovered_alphabet = to_string([l for l, c, f in encrypted_counters])

println(ALPHABET, "plain alphabet", 22)
println(randomized_alphabet, "randomized alphabet", 22)
println(recovered_alphabet, "recovered alphabet", 22)
mismatches = "".join(['^' if a != b else ' ' for a, b in zip(randomized_alphabet, recovered_alphabet)])
println(mismatches, "mismatches", 22)
print()

for i, [[ra_l, ra_f], [l, c, f]] in enumerate(zip(RA, encrypted_counters), 1):
    mismatch = "❌" if ra_l != l else "✅"
    print(f"{i:2}:", f"{ra_l} {ra_f:0.6f}", "~>", f"{l} {f:0.6f} ({c:5})", "-", f"±{abs(ra_f - f):0.6f}", mismatch)
print()


decryted = substitution(encrypted, recovered_alphabet, ALPHABET)

print("decrypted coincidence:", COINCIDENCE(decryted))


diff = sum([1 for i in range(len(plain)) if plain[i] != decryted[i]])
print(f"{diff=}", f"{len(plain)=}", f"{diff/len(plain)*100=}", "\n")

if len(plain) < 2000:
    print(table5(decryted), "\n")
    print(table5(plain))
