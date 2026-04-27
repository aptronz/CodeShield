import os

from flask import Flask, jsonify, render_template, request

from detector.ai_generator import generate_solution_from_ai, generate_solution_locally
from detector.engine import detect_plagiarism


app = Flask(__name__)


def _load_env_file():
    env_path = ".env"
    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip().lstrip("\ufeff")
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            # Always let .env be the source of truth for local runs.
            if key:
                os.environ[key] = value


_load_env_file()


def _is_truthy(value):
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/api/detect", methods=["POST"])
def api_detect():
    payload = request.get_json(silent=True) or {}
    code = payload.get("code", "")
    language = payload.get("language", "python")
    problem_statement = payload.get("problem_statement", "")
    strict_ai = _is_truthy(payload.get("strict_ai", False)) or _is_truthy(os.environ.get("GEMINI_STRICT", "0"))

    if not code.strip():
        return jsonify({"error": "Please provide code input."}), 400

    generated_solution = ""
    ai_provider = ""
    warning = ""
    if problem_statement.strip():
        try:
            generated_solution, ai_provider = generate_solution_from_ai(
                problem_statement=problem_statement, language=language
            )
        except RuntimeError as exc:
            if strict_ai:
                return jsonify({"error": f"Gemini strict mode enabled: {exc}"}), 502
            # Fallback mode keeps detector functional even without valid API key/quota.
            generated_solution = generate_solution_locally(problem_statement=problem_statement, language=language)
            ai_provider = "local-fallback"
            warning = f"AI API unavailable: {exc}. Used local fallback solution for comparison."
    else:
        # Keep API backward-compatible with older clients that only send code/language.
        generated_solution = generate_solution_locally(problem_statement=code, language=language)
        ai_provider = "local-fallback"
        warning = "No problem statement provided. Used local fallback solution for comparison."

    result = detect_plagiarism(code=code, language=language, ai_reference_code=generated_solution)
    result["generated_solution"] = generated_solution
    result["ai_provider"] = ai_provider
    if warning:
        result["warning"] = warning
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)
