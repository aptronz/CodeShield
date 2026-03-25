def extract_structure(tokens):
    sequence = []
    idx = 0
    n = len(tokens)

    while idx < n:
        token = tokens[idx]
        nxt = tokens[idx + 1] if idx + 1 < n else ""

        if token in ("def", "function"):
            sequence.append("FUNC_DEF")
        elif token == "class":
            sequence.append("CLASS_DEF")
        elif token == "for":
            sequence.append("LOOP_FOR")
        elif token == "while":
            sequence.append("LOOP_WHILE")
        elif token in ("if", "elif", "else"):
            sequence.append("BRANCH")
        elif token in ("try", "except", "catch"):
            sequence.append("EXCEPTION")
        elif token == "return":
            sequence.append("RETURN")
        elif token == "import":
            sequence.append("IMPORT")
        elif token == "include":
            sequence.append("INCLUDE")
        elif token == "public":
            sequence.append("ACCESS")
        elif token == "private":
            sequence.append("ACCESS")
        elif token == "protected":
            sequence.append("ACCESS")
        elif token == "static":
            sequence.append("STATIC")
        elif token == "new":
            sequence.append("ALLOC")
        elif token == "void":
            sequence.append("VOID")
        elif token == "ID" and nxt == "(":
            sequence.append("CALL")
        elif token == "=":
            sequence.append("ASSIGN")
        elif token in ("+", "-", "*", "/", "%"):
            sequence.append("ARITH")
        elif token in ("<", ">", "<=", ">=", "==", "!="):
            sequence.append("COMPARE")

        idx += 1

    return sequence
