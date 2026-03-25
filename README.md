# CodeShield Website

CodeShield is a plagiarism detection website for code submissions.

## Features

- Accepts one code submission at a time.
- Supports `python`, `javascript`, `java`, and `cpp`.
- Uses a custom tokenizer and structure extractor (no built-in plagiarism library).
- Computes an AI similarity score and plagiarism verdict.
- Displays the architecture image in the web UI.

## Architecture Pipeline

User Code -> Tokenizer -> Structure Extractor -> Feature Sequence ->
Compare with AI Reference Solutions -> Similarity Engine ->
Report (AI Similarity Score)

## Run Locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start server:

   ```bash
   python app.py
   ```

3. Open:

   [http://127.0.0.1:5000](http://127.0.0.1:5000)
