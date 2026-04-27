# CodeShield Website

CodeShield is a plagiarism detection website for code submissions.

## Features

- Takes a problem statement and asks Gemini API to generate a reference solution.
- Accepts one code submission at a time.
- Supports `python`, `javascript`, `java`, and `cpp`.
- Uses a custom tokenizer and structure extractor (no built-in plagiarism library).
- Compares user code with both built-in references and AI-generated solution.
- Computes an AI similarity score and plagiarism verdict.

## Architecture Pipeline

Problem Statement -> Gemini API -> AI Reference Solution
User Code -> Tokenizer -> Structure Extractor -> Feature Sequence ->
Compare with AI Reference Solution + Internal References -> Similarity Engine ->
Report (AI Similarity Score)

## Run Locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Add Gemini API settings (recommended: `.env`):

   - Create a `.env` file in project root (you can copy from `.env.example`)
   - Add:

   ```bash
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=gemini-1.5-flash
   ```

   Notes:
   - CodeShield uses Gemini for AI solution generation.

   CodeShield auto-loads this file on startup.

   Or set values directly in PowerShell:

   ```bash
   $env:GEMINI_API_KEY="your_gemini_api_key"
   ```

3. Start server:

   ```bash
   python app.py
   ```

4. Open:

   [http://127.0.0.1:5000](http://127.0.0.1:5000)
