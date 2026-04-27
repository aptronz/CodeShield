from detector.reference_db import REFERENCE_SOLUTIONS
from detector.similarity import combined_similarity
from detector.structure import extract_structure
from detector.tokenizer import tokenize


def _clamp(value, min_value, max_value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


def _language_or_default(language):
    if language in REFERENCE_SOLUTIONS:
        return language
    if language == "auto":
        return "auto"
    return "python"


def _auto_detect_language(code):
    low = code.lower()
    if "<!doctype html" in low or ("<html" in low and "<script" in low):
        return "javascript"
    if "function " in low or "const " in low or "let " in low or "=>" in low:
        return "javascript"
    if "public class " in low or "system.out.println" in low:
        return "java"
    if "#include" in low or "std::" in low:
        return "cpp"
    return "python"


def _template_boost(code):
    low = code.lower()
    patterns = [
        "<!doctype html",
        "<html",
        "<script",
        "onclick=",
        "alert(",
        "function ",
        "click me",
    ]
    hits = 0
    for item in patterns:
        if item in low:
            hits += 1
    if hits >= 5:
        return 0.18
    if hits >= 3:
        return 0.10
    return 0.0


def _threshold_for_size(token_count):
    if token_count < 60:
        return 52
    if token_count < 120:
        return 60
    return 68


def _threshold_for_language(language, token_count):
    base = _threshold_for_size(token_count)
    if language == "python":
        return base - 2
    if language == "java":
        return base - 1
    if language == "cpp":
        return base + 11
    if language == "javascript":
        return base - 2
    return base


def _language_pattern_boost(code, language):
    low = code.lower()
    pattern_map = {
        "python": [
            "def ",
            "if __name__ == \"__main__\":",
            "for ",
            "while ",
            "return ",
            "range(",
            "print(",
        ],
        "java": [
            "public class ",
            "public static void main",
            "system.out.println",
            "for (int ",
            "return ",
            "class ",
        ],
        "cpp": [
            "#include",
            "using namespace std",
            "int main(",
            "cout <<",
            "for (int ",
            "return 0;",
        ],
        "javascript": [
            "function ",
            "const ",
            "let ",
            "return ",
            "alert(",
        ],
    }
    patterns = pattern_map.get(language, [])
    hits = 0
    for item in patterns:
        if item in low:
            hits += 1
    if hits >= 5:
        return 0.12
    if hits >= 3:
        return 0.07
    if hits >= 2:
        return 0.04
    return 0.0


def detect_plagiarism(code, language="python", ai_reference_code=None):
    language = _language_or_default(language)
    if language == "auto":
        language = _auto_detect_language(code)
    references = REFERENCE_SOLUTIONS.get(language, [])

    user_tokens = tokenize(code, language)
    user_structure = extract_structure(user_tokens)

    best_score = 0.0
    compared = 0

    for reference in references:
        ref_tokens = tokenize(reference, language)
        ref_structure = extract_structure(ref_tokens)
        score = combined_similarity(user_tokens, ref_tokens, user_structure, ref_structure)
        if score > best_score:
            best_score = score
        compared += 1

    ai_score = None
    if ai_reference_code and ai_reference_code.strip():
        ai_tokens = tokenize(ai_reference_code, language)
        ai_structure = extract_structure(ai_tokens)
        ai_score = combined_similarity(user_tokens, ai_tokens, user_structure, ai_structure)
        if ai_score > best_score:
            best_score = ai_score
        compared += 1

    tuned_score = _clamp(best_score + _template_boost(code) + _language_pattern_boost(code, language), 0.0, 1.0)
    percentage = int(_clamp(tuned_score * 100.0, 0.0, 100.0))
    threshold = _threshold_for_language(language, len(user_tokens))
    is_plagiarized = percentage >= threshold
    verdict = "Potential plagiarism detected." if is_plagiarized else "Likely original code."

    return {
        "language": language,
        "verdict": verdict,
        "is_plagiarized": is_plagiarized,
        "ai_similarity_score": percentage,
        "ai_reference_similarity_score": int(_clamp((ai_score or 0.0) * 100.0, 0.0, 100.0)),
        "used_generated_solution": bool(ai_reference_code and ai_reference_code.strip()),
        "references_compared": compared,
    }
