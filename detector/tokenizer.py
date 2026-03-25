KEYWORDS = {
    "python": {
        "def",
        "class",
        "for",
        "while",
        "if",
        "elif",
        "else",
        "return",
        "import",
        "from",
        "try",
        "except",
        "with",
        "lambda",
    },
    "javascript": {
        "function",
        "class",
        "for",
        "while",
        "if",
        "else",
        "return",
        "import",
        "from",
        "try",
        "catch",
        "const",
        "let",
        "var",
    },
    "java": {
        "class",
        "public",
        "private",
        "protected",
        "static",
        "void",
        "for",
        "while",
        "if",
        "else",
        "return",
        "try",
        "catch",
        "new",
    },
    "cpp": {
        "class",
        "public",
        "private",
        "protected",
        "static",
        "void",
        "for",
        "while",
        "if",
        "else",
        "return",
        "try",
        "catch",
        "new",
        "include",
    },
}


def _is_word_char(ch):
    return ch.isalnum() or ch == "_"


def _normalize_token(token, language):
    kw = KEYWORDS.get(language, KEYWORDS["python"])
    if token in kw:
        return token
    if token.isdigit():
        return "NUM"
    return "ID"


def tokenize(code, language):
    tokens = []
    idx = 0
    n = len(code)

    while idx < n:
        ch = code[idx]

        if ch.isspace():
            idx += 1
            continue

        if _is_word_char(ch):
            start = idx
            while idx < n and _is_word_char(code[idx]):
                idx += 1
            word = code[start:idx]
            tokens.append(_normalize_token(word, language))
            continue

        if ch in ("'", '"'):
            quote = ch
            idx += 1
            while idx < n and code[idx] != quote:
                if code[idx] == "\\" and idx + 1 < n:
                    idx += 2
                else:
                    idx += 1
            idx += 1
            tokens.append("STR")
            continue

        if ch in "{}()[],:;.+-*/%<>=!&|^~":
            tokens.append(ch)
            idx += 1
            continue

        tokens.append("SYM")
        idx += 1

    return tokens
