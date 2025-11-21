# 🧠 Code-to-Flow — Automated Code-to-Flowchart Generator

A full-stack web application that takes **Python source code** as input and automatically generates an **interactive flowchart** representing the program’s control flow.

This tool helps learners, educators, and developers quickly **visualize Python code logic** using an easy-to-use web interface and modern visualization libraries.

---

## 🚀 Features

✅ Accepts Python code as input  
✅ Parses the code into an **Abstract Syntax Tree (AST)**  
✅ Identifies key code structures — **loops, conditionals, functions, assignments**  
✅ Generates interactive **flowcharts using Mermaid.js**  
✅ Allows **exporting flowcharts as PNG images**  
✅ Clean, responsive frontend with modular backend structure  
✅ Easily extendable to other languages (C, Java, etc.)

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Python, Flask, Flask-CORS |
| **Frontend** | HTML, CSS, JavaScript |
| **Visualization** | Mermaid.js, html2canvas.js |
| **Parsing** | Python `ast` module |
| **Version Control** | Git & GitHub |

---

## 📁 Project Structure

Code-to-Flow/
│
├── backend/
│ ├── app.py # Flask backend (API server)
│ ├── parser/
│ │ ├── python_parser.py # AST logic (if used separately)
│
├── frontend/
│ ├── index.html # UI layout
│ ├── style.css # Styling
│ ├── script.js # Frontend logic & API calls
│
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── venv/ # Virtual environment (optional)


---

## ⚙️ Installation & Setup Guide

### 🧩 Prerequisites
Make sure you have:
- Python 3.8 or higher installed
- Node.js (optional, only if expanding later)
- Git (to clone repository)

---

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/Code-to-Flow.git
cd Code-to-Flow


---

## ⚙️ Installation & Setup Guide

### 🧩 Prerequisites
Make sure you have:
- Python 3.8 or higher installed
- Node.js (optional, only if expanding later)
- Git (to clone repository)

---

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/Code-to-Flow.git
cd Code-to-Flow

### 2️⃣ Run the Backend
cd BackEnd
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
python app.py

### 3️⃣ Run the FrontEnd
cd FrontEnd
python -m http.server <4 digit number>
http://localhost:<those 4 digit number>

👨‍💻 Author
Swayamrajsinh Jethwa
mailto:jethwaswayamraj@gmail.com
https://www.linkedin.com/in/swayamrajsinh-jethwa-154a2a292
https://github.com/Swayamraj7