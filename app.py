from flask import Flask, jsonify, render_template, request

from detector.engine import detect_plagiarism


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/api/detect", methods=["POST"])
def api_detect():
    payload = request.get_json(silent=True) or {}
    code = payload.get("code", "")
    language = payload.get("language", "python")

    if not code.strip():
        return jsonify({"error": "Please provide code input."}), 400

    result = detect_plagiarism(code=code, language=language)
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)
