# Least common multiple of all possible character widths. A line wrap must occur when the combined widths of all of the
# characters on a line reach this value.
LINE_WIDTH = 1801800

# Attempting to display more lines in a single text box will cause additional lines to bleed past the bottom of the box.
LINES_PER_BOX = 4

# Attempting to display more characters in a single text box will cause buffer overflows. First, visual artifacts will
# appear in lower areas of the text box. Eventually, the text box will become uncloseable.
MAX_CHARACTERS_PER_BOX = 200

LINE_BREAK = '&'
BOX_BREAK = '^'


def lineWrap(text):
    boxes = text.split(BOX_BREAK)
    boxesWithWrappedLines = []

    for box in boxes:
        forcedLines = box.split(LINE_BREAK)
        lines = [line.strip() for forcedLine in forcedLines for line in _wrapLines(forcedLine)]
        wrapped = LINE_BREAK.join(lines)

        if len(lines) > LINES_PER_BOX:
            print('Wrapped text exceeds maximum lines per text box. Original text:\n' + box)

        # Subtracting line count so that line breaks aren't counted as characters
        if len(wrapped) - (len(lines) - 1) > MAX_CHARACTERS_PER_BOX:
            print('Text length exceeds maximum characters per text box. Original text:\n' + box)

        boxesWithWrappedLines.append(wrapped)

    return BOX_BREAK.join(boxesWithWrappedLines)


def _wrapLines(text):
    lines = []
    currentLine = []
    currentWidth = 0

    for word in text.split(' '):
        currentLinePlusWord = currentLine.copy()
        currentLinePlusWord.append(word)
        currentLinePlusWordWidth = _calculateWidth(currentLinePlusWord)

        if (currentLinePlusWordWidth <= LINE_WIDTH):
            currentLine = currentLinePlusWord
            currentWidth = currentLinePlusWordWidth
        else:
            lines.append(' '.join(currentLine))
            currentLine = [word]
            currentWidth = _calculateWidth(currentLine)

    lines.append(' '.join(currentLine))

    return lines


def _calculateWidth(words):
    wordsWidth = sum([_getCharacterWidth(character) for word in words for character in word])
    spacesWidth = _getCharacterWidth(' ') * (len(words) - 1)

    return wordsWidth + spacesWidth


def _getCharacterWidth(character):
    try:
        return characterTable[character]
    except KeyError:
        # Control character for color settings; does not affect the width
        if character == '#':
            return 0
        # Control character for displaying the player's name; assume greater than average width
        elif character == '@':
            return characterTable['M'] * 8
        # A sane default with the most common character width
        else :
            return characterTable[' ']


# Tediously measured by filling a full line of a gossip stone's text box with one character until it is reasonably full
# (with a right margin) and counting how many characters fit. OoT does not appear to use any kerning, but, if it does,
# it will only make the characters more space-efficient, so this is an underestimate of the number of letters per line,
# at worst. This ensures that we will never bleed text out of the text box while line wrapping.
# Larger numbers in the denominator mean more of that character fits on a line; conversely, larger values in this table
# mean the character is wider and can't fit as many on one line.
characterTable = {
    'a':  51480, # LINE_WIDTH /  35
    'b':  51480, # LINE_WIDTH /  35
    'c':  51480, # LINE_WIDTH /  35
    'd':  51480, # LINE_WIDTH /  35
    'e':  51480, # LINE_WIDTH /  35
    'f':  34650, # LINE_WIDTH /  52
    'g':  51480, # LINE_WIDTH /  35
    'h':  51480, # LINE_WIDTH /  35
    'i':  25740, # LINE_WIDTH /  70
    'j':  34650, # LINE_WIDTH /  52
    'k':  51480, # LINE_WIDTH /  35
    'l':  25740, # LINE_WIDTH /  70
    'm':  81900, # LINE_WIDTH /  22
    'n':  51480, # LINE_WIDTH /  35
    'o':  51480, # LINE_WIDTH /  35
    'p':  51480, # LINE_WIDTH /  35
    'q':  51480, # LINE_WIDTH /  35
    'r':  42900, # LINE_WIDTH /  42
    's':  51480, # LINE_WIDTH /  35
    't':  42900, # LINE_WIDTH /  42
    'u':  51480, # LINE_WIDTH /  35
    'v':  51480, # LINE_WIDTH /  35
    'w':  81900, # LINE_WIDTH /  22
    'x':  51480, # LINE_WIDTH /  35
    'y':  51480, # LINE_WIDTH /  35
    'z':  51480, # LINE_WIDTH /  35
    'A':  81900, # LINE_WIDTH /  22
    'B':  51480, # LINE_WIDTH /  35
    'C':  72072, # LINE_WIDTH /  25
    'D':  72072, # LINE_WIDTH /  25
    'E':  51480, # LINE_WIDTH /  35
    'F':  51480, # LINE_WIDTH /  35
    'G':  81900, # LINE_WIDTH /  22
    'H':  60060, # LINE_WIDTH /  30
    'I':  25740, # LINE_WIDTH /  70
    'J':  51480, # LINE_WIDTH /  35
    'K':  60060, # LINE_WIDTH /  30
    'L':  51480, # LINE_WIDTH /  35
    'M':  81900, # LINE_WIDTH /  22
    'N':  72072, # LINE_WIDTH /  25
    'O':  81900, # LINE_WIDTH /  22
    'P':  51480, # LINE_WIDTH /  35
    'Q':  81900, # LINE_WIDTH /  22
    'R':  60060, # LINE_WIDTH /  30
    'S':  60060, # LINE_WIDTH /  30
    'T':  51480, # LINE_WIDTH /  35
    'U':  60060, # LINE_WIDTH /  30
    'V':  72072, # LINE_WIDTH /  25
    'W': 100100, # LINE_WIDTH /  18
    'X':  72072, # LINE_WIDTH /  25
    'Y':  60060, # LINE_WIDTH /  30
    'Z':  60060, # LINE_WIDTH /  30
    ' ':  51480, # LINE_WIDTH /  35
    '1':  25740, # LINE_WIDTH /  70
    '2':  51480, # LINE_WIDTH /  35
    '3':  51480, # LINE_WIDTH /  35
    '4':  60060, # LINE_WIDTH /  30
    '5':  51480, # LINE_WIDTH /  35
    '6':  51480, # LINE_WIDTH /  35
    '7':  51480, # LINE_WIDTH /  35
    '8':  51480, # LINE_WIDTH /  35
    '9':  51480, # LINE_WIDTH /  35
    '0':  60060, # LINE_WIDTH /  30
    '!':  51480, # LINE_WIDTH /  35
    '?':  72072, # LINE_WIDTH /  25
    '\'': 17325, # LINE_WIDTH / 104
    '"':  34650, # LINE_WIDTH /  52
    '.':  25740, # LINE_WIDTH /  70
    ',':  25740, # LINE_WIDTH /  70
    '/':  51480, # LINE_WIDTH /  35
    '-':  34650, # LINE_WIDTH /  52
    '_':  51480, # LINE_WIDTH /  35
    '(':  42900, # LINE_WIDTH /  42
    ')':  42900, # LINE_WIDTH /  42
    '$':  51480  # LINE_WIDTH /  35
}
