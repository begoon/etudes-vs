import locale
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

from ra import RA

TEXT ="text-ru.txt"

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8') 

RA_dict = dict(RA)

# Example usage
ciphertext = """
кмырс ейией диоте зьмро риовт нднте слобс дачаи пюиор смуйт ашагу кеста ырьйо книнч адинр тожво мнряв оедие рсрыч нссел ежтьл нозси оыием псира
лннлт ейоие моспн сяомп чораи пюиур очлох тосип гиозь сдача ипков обаыо мыиьс лобма чаюин яомио вабок астум ырьси вонип иадуц рахту цгаси пявое
диака ипежх нчтпк ьйатн евнил нвоси ташая авите всдаы явобв аллая окиро нлчаз оимнр ьлнио гтьлр чбмык олвок нмасп васэр емано звема сезын иеяев
пяеве караы еерта кехть евудн иьяев екаеш пухет елмак етгнд аадве ядоси оыщеб отато байла мьшал темнг тонык улацд олатк аяокк евхни летыр юиолз
ьморк ойтор мыцще нтаке хтова зоиаи псиоз ожиро есоге иатне кемнд аитос инсив аиебн гесдо борчб мыкан явофе сснот амнчл аскем амние зыиад нлрах
тьлнг метол долат кьгио иезыз укеиу хасто тейра иаипт оюиос рнкеи емпси рорьс огажш ебояв офесс нотам нчлас улеип теиом пдорь сивон иптон тажин
сезея веелт нданя евека ипкем аиадг иольл ьтеяо гурси рорам ндоге дтаюи ожсле тьтоя огурс ируел тейра идуие зымнг тоняо иолуы такец спгио сиозо
жтагт еивас иннва сшнвы ипсыс ореис ореит ндорб вуяяа иейдо лутер севар тоташ езуку щеенд иояок кевхн итасс ореио лнвед олетк аэнеж рзуку щелте
явоща елсын такец спозт ыипмн гторя овиуб амнну двант еяваб енмнб кеиое ще 
"""
letter_freq_table = RA_dict

plaintext = break_substitution_cipher(ciphertext, letter_freq_table)
print(plaintext)  # Output: I HAVE FUN WITH THIS TOO! (or something close)