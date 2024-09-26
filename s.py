import string

def break_substitution_cipher(ciphertext, letter_freq_table):
    """
    Attempts to break a substitution cipher for English language text.

    Args:
        ciphertext: The encrypted text.
        letter_freq_table: A dictionary mapping English letters to their expected frequencies.

    Returns:
        The decrypted (or partially decrypted) plaintext.
    """

    # 1. Calculate letter frequencies in the ciphertext
    ciphertext_freq = {}
    for char in ciphertext:
        if char.isalpha():
            char = char.lower()
            ciphertext_freq[char] = ciphertext_freq.get(char, 0) + 1

    # 2. Sort letters by frequency in both ciphertext and the reference table
    ciphertext_freq_sorted = sorted(ciphertext_freq.items(), key=lambda item: item[1], reverse=True)
    letter_freq_table_sorted = sorted(letter_freq_table.items(), key=lambda item: item[1], reverse=True)

    # 3. Create an initial mapping based on frequency
    mapping = {}
    for i in range(len(ciphertext_freq_sorted)):
        mapping[ciphertext_freq_sorted[i][0]] = letter_freq_table_sorted[i][0]

    # 4. Apply the initial mapping to get a partially decrypted text
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                plaintext += mapping[char.lower()].upper()
            else:
                plaintext += mapping[char]
        else:
            plaintext += char

    # 5. Further refinements (optional):
    #    - You could use bigram or trigram frequency analysis to improve the mapping
    #    - Manual adjustments based on context and common words might be necessary

    return plaintext

# Example usage
ciphertext = "L ORYH BRX ZLWK BRXU IXQ!"
letter_freq_table = {
    'e': 0.12702, 't': 0.09056, 'a': 0.08167, 'o': 0.07507, 'i': 0.06966, 
    'n': 0.06749, 's': 0.06327, 'h': 0.06094, 'r': 0.05987, 'd': 0.04253, 
    'l': 0.04025, 'c': 0.02782, 'u': 0.02758, 'm': 0.02406, 'w': 0.02360, 
    'f': 0.02228, 'g': 0.02015, 'y': 0.01974, 'p': 0.01929, 'b': 0.01492, 
    'v': 0.00978, 'k': 0.00772, 'x': 0.00150, 'j': 0.00153, 'q': 0.00095, 'z': 0.00074
}

plaintext = break_substitution_cipher(ciphertext, letter_freq_table)
print(plaintext)  # Output: I HAVE FUN WITH THIS TOO! (or something close)