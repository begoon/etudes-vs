RA0: list[tuple[str, float]] = [
    ("О", 0.11180),
    ("Е", 0.0875),
    ("А", 0.0764),
    ("И", 0.0709),
    ("Н", 0.0678),
    ("Т", 0.0609),
    ("С", 0.0497),
    ("Л", 0.0496),
    ("В", 0.0438),
    ("Р", 0.0423),
    ("К", 0.0330),
    ("М", 0.0317),
    ("Д", 0.0309),
    ("П", 0.0247),
    ("Ы", 0.0236),
    ("У", 0.0222),
    ("Б", 0.0201),
    ("Я", 0.0196),
    ("Ь", 0.0184),
    ("Г", 0.0172),
    ("З", 0.0148),
    ("Ч", 0.0140),
    ("Й", 0.0121),
    ("Ж", 0.0101),
    ("Х", 0.0095),
    ("Ш", 0.0072),
    ("Ю", 0.0047),
    ("Ц", 0.0039),
    ("Э", 0.0036),
    ("Щ", 0.0030),
    ("Ф", 0.0021),
    ("Ё", 0.0020),
    ("Ъ", 0.0002),
]

RA = [(l.lower(), f) for l, f in RA0]
