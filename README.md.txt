# AI Resume Builder (Django)

A clean and easy-to-use **AI Resume Builder** built with **Django**.  
Users can generate professional resumes using **Modern, Simple, and ATS-friendly templates**, preview them in the browser, and download a clean PDF.

This project is ideal for developers, freelancers, and startups who want a ready-made resume builder to customize or deploy.

---

## ✨ Features

- User authentication (Login / Register)
- Email verification support
- Resume dashboard
- Multiple resume templates:
  - Modern (stylish preview)
  - Simple (clean & recruiter-friendly)
  - ATS (machine-readable & plain)
- Resume preview in browser
- PDF download (ATS-safe)
- Clean UI & responsive layout
- Django-based backend

---

## 🛠 Tech Stack

- Python 3.10+
- Django
- HTML / CSS
- ReportLab (PDF generation)
- SQLite (default)

---

## 📁 Project Structure

ai-resume-builder/
├── manage.py
├── README.md
├── LICENSE.txt
├── requirements.txt
├── users/
│ ├── views.py
│ ├── models.py
│ ├── urls.py
│ └── utils.py
├── templates/
│ ├── modern.html
│ ├── simple.html
│ └── ats.html
├── static/
└── media/



---

## 🚀 Setup Instructions

### 1️: Clone the project
```bash
git clone 
cd ai-resume-builder

2:Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

3️: Install dependencies
pip install -r requirements.txt

4️:Apply migrations
python manage.py migrate

5️: Run the server
python manage.py runserver


Visit: http://127.0.0.1:8000