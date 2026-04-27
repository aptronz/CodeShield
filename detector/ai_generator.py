import json
import os
import time
from urllib import error, request


GEMINI_API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GEMINI_MODELS_URL = "https://generativelanguage.googleapis.com/v1beta/models"


def _build_prompt(problem_statement, language):
    return (
        "You are an expert competitive programmer. "
        "Generate only one clean and correct solution for the given problem. "
        "Return only source code with no markdown fences and no explanation.\n\n"
        f"Target language: {language}\n"
        f"Problem statement:\n{problem_statement}\n"
    )


def _normalize_secret(raw_value):
    value = (raw_value or "").strip()
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1].strip()
    return value


def _extract_error_message(body):
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        return ""
    err = parsed.get("error", {})
    message = err.get("message", "")
    if isinstance(message, str):
        return message
    return ""


def _is_authorization_issue(message):
    msg = (message or "").lower()
    return (
        "api key not valid" in msg
        or "permission denied" in msg
        or "not authorized" in msg
        or "method doesn't allow unregistered callers" in msg
    )


def _is_model_not_found_issue(message):
    msg = (message or "").lower()
    return (
        "is not found for api version" in msg
        or "not supported for generatecontent" in msg
        or "model not found" in msg
    )


def _candidate_models():
    configured = os.environ.get("GEMINI_MODEL", "").strip()
    defaults = [
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
    ]
    out = []
    if configured:
        out.append(configured)
    for model in defaults:
        if model not in out:
            out.append(model)
    return out


def _extract_model_id(name):
    if not isinstance(name, str):
        return ""
    if name.startswith("models/"):
        return name.split("/", 1)[1]
    return name


def _discover_generate_content_models(api_key):
    req = request.Request(
        GEMINI_MODELS_URL,
        headers={"x-goog-api-key": api_key},
        method="GET",
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
    except Exception:
        return []

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return []

    models = parsed.get("models", [])
    discovered = []
    for entry in models:
        methods = entry.get("supportedGenerationMethods", [])
        if "generateContent" not in methods:
            continue
        model_id = _extract_model_id(entry.get("name", ""))
        if model_id and model_id not in discovered:
            discovered.append(model_id)
    return discovered


def _call_gemini_once(url, api_key, data):
    req = request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        method="POST",
    )
    with request.urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8")


def _generate_with_gemini(problem_statement, language):
    api_key = _normalize_secret(os.environ.get("GEMINI_API_KEY", ""))
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY environment variable.")

    payload = {
        "contents": [{"parts": [{"text": _build_prompt(problem_statement, language)}]}],
        "generationConfig": {"temperature": 0.2},
    }
    data = json.dumps(payload).encode("utf-8")

    discovered_models = _discover_generate_content_models(api_key)
    model_errors = []
    raw = ""
    used_model = ""
    all_candidates = []
    for model_name in _candidate_models():
        if model_name not in all_candidates:
            all_candidates.append(model_name)
    for model_name in discovered_models:
        if model_name not in all_candidates:
            all_candidates.append(model_name)

    for model_name in all_candidates:
        url = GEMINI_API_URL_TEMPLATE.format(model=model_name)
        max_attempts = 3
        attempt = 0
        try_next_model = False
        while attempt < max_attempts:
            attempt += 1
            try:
                raw = _call_gemini_once(url, api_key, data)
                used_model = model_name
                break
            except error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="ignore")
                message = _extract_error_message(body)
                if _is_model_not_found_issue(message):
                    model_errors.append(f"{model_name}: not available")
                    try_next_model = True
                    break
                if exc.code in (400, 401, 403):
                    if _is_authorization_issue(message):
                        raise RuntimeError(
                            "Gemini key unauthorized. Use a Google AI Studio key and enable Generative Language API for your project."
                        ) from exc
                    raise RuntimeError(
                        "Gemini API key is invalid or unauthorized. Set a valid GEMINI_API_KEY."
                    ) from exc
                if exc.code == 429:
                    if attempt < max_attempts:
                        time.sleep(1.5 * attempt)
                        continue
                    raise RuntimeError("Gemini API is rate-limited. Please retry shortly.") from exc
                if message:
                    raise RuntimeError(f"Gemini API error: {message}") from exc
                raise RuntimeError(f"Gemini API request failed with status {exc.code}.") from exc
            except error.URLError as exc:
                if attempt < max_attempts:
                    time.sleep(1.0 * attempt)
                    continue
                raise RuntimeError(f"Gemini API request failed: {exc.reason}") from exc
        if used_model:
            break
        if not try_next_model:
            break

    if not used_model:
        if model_errors:
            raise RuntimeError(
                "No compatible Gemini model found. Tried: " + ", ".join(model_errors)
            )
        raise RuntimeError("Gemini API did not return a valid response.")

    parsed = json.loads(raw)
    candidates = parsed.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini API returned no candidates.")
    content = candidates[0].get("content", {})
    parts = content.get("parts", [])
    if not parts:
        raise RuntimeError("Gemini API returned empty content.")
    text = parts[0].get("text", "")
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError("Gemini API returned empty text output.")
    return text.strip()


def generate_solution_from_ai(problem_statement, language):
    return _generate_with_gemini(problem_statement, language), "gemini"


def generate_solution_locally(problem_statement, language):
    low = problem_statement.lower()
    lang = (language or "").lower()

    if "factorial" in low:
        if lang == "python":
            return "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)"
        if lang == "java":
            return (
                "class Main {\n"
                "    static int factorial(int n) {\n"
                "        if (n <= 1) return 1;\n"
                "        return n * factorial(n - 1);\n"
                "    }\n"
                "}"
            )
        if lang == "cpp":
            return (
                "int factorial(int n) {\n"
                "    if (n <= 1) return 1;\n"
                "    return n * factorial(n - 1);\n"
                "}"
            )
        return "function factorial(n) {\n  if (n <= 1) return 1;\n  return n * factorial(n - 1);\n}"

    if "fibonacci" in low:
        if lang == "python":
            return "def fibonacci(n):\n    a, b = 0, 1\n    out = []\n    for _ in range(n):\n        out.append(a)\n        a, b = b, a + b\n    return out"
        if lang == "java":
            return (
                "class Main {\n"
                "    static int fib(int n) {\n"
                "        if (n <= 1) return n;\n"
                "        return fib(n - 1) + fib(n - 2);\n"
                "    }\n"
                "}"
            )
        if lang == "cpp":
            return "int fib(int n) {\n    if (n <= 1) return n;\n    return fib(n - 1) + fib(n - 2);\n}"
        return "function fib(n) { if (n <= 1) return n; return fib(n - 1) + fib(n - 2); }"

    if lang == "python":
        return "def solve(data):\n    return data"
    if lang == "java":
        return "class Main {\n    static int solve(int x) {\n        return x;\n    }\n}"
    if lang == "cpp":
        return "int solve(int x) {\n    return x;\n}"
    return "function solve(x) { return x; }"
