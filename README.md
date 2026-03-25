\# 🛡️ CodeShield — Plagiarism Detection using AST Analysis



CodeShield is a smart plagiarism detection system that analyzes the \*\*structural similarity of source code\*\* using Abstract Syntax Trees (AST), rather than relying only on plain text comparison. This makes it effective against code modifications like variable renaming, formatting changes, and minor logic restructuring.



\---



\## 🚀 Features



\* 🔍 \*\*AST-Based Code Analysis\*\*

&#x20; Detects deep structural similarities in code.



\* 🧠 \*\*Smart Similarity Engine\*\*

&#x20; Compares logic instead of just text.



\* 📊 \*\*Similarity Scoring\*\*

&#x20; Provides a clear percentage of similarity between files.



\* 🌐 \*\*Web Interface\*\*

&#x20; Simple and user-friendly UI for uploading and analyzing code.



\* ⚡ \*\*Fast Processing\*\*

&#x20; Efficient comparison even for multiple files.



\---



\## 🏗️ Project Structure



```

CodeShield/

│── app.py                  # Main Flask application

│── detector/               # Core detection logic

│   ├── engine.py

│   ├── tokenizer.py

│   ├── structure.py

│   ├── similarity.py

│   └── reference\_db.py

│── templates/              # HTML files

│── static/                 # CSS, JS, Images

│── requirements.txt        # Dependencies

│── README.md

```



\---



\## ⚙️ Installation \& Setup



\### 1️⃣ Clone the repository



```bash

git clone https://github.com/aptronz/CodeShield.git

cd CodeShield

```



\### 2️⃣ Create virtual environment (recommended)



```bash

python -m venv venv

venv\\Scripts\\activate   # Windows

```



\### 3️⃣ Install dependencies



```bash

pip install -r requirements.txt

```



\### 4️⃣ Run the application



```bash

python app.py

```



\---



\## 🌐 Usage



1\. Open your browser

2\. Go to: `http://127.0.0.1:5000/`

3\. Upload code files

4\. View similarity results instantly



\---



\## 🧠 How It Works



1\. \*\*Code Parsing\*\* → Converts source code into AST

2\. \*\*Tokenization\*\* → Breaks code into meaningful components

3\. \*\*Structure Analysis\*\* → Extracts logical structure

4\. \*\*Similarity Calculation\*\* → Compares AST patterns

5\. \*\*Result Output\*\* → Displays similarity score



\---



\## 📌 Use Cases



\* Academic plagiarism detection

\* Code similarity checking in interviews

\* Assignment verification for colleges

\* Code review assistance



\---



\## 🛠️ Tech Stack



\* \*\*Backend:\*\* Python, Flask

\* \*\*Frontend:\*\* HTML, CSS, JavaScript

\* \*\*Core Logic:\*\* AST parsing, custom similarity algorithms



\---



\## 📈 Future Improvements



\* Support for multiple programming languages

\* Advanced visualization of similarities

\* Integration with GitHub repositories

\* Machine learning-based detection



\---



\## 🤝 Contributing



Contributions are welcome!

Feel free to fork the repo and submit a pull request.



\---



\## 📄 License



This project is open-source and available under the MIT License.



\---



\## 👨‍💻 Author



\*\*Your Name\*\*

GitHub: https://github.com/aptronz



\---



\## ⭐ If you like this project



Give it a star ⭐ on GitHub — it helps a lot!



