# HNG Backend – Stage 0: Dynamic Profile Endpoint

## 🚀 Overview
This project implements a simple **RESTful API** endpoint (`/me`) using **Python / Django**.  
The endpoint returns the developer’s profile information along with a **dynamic cat fact** fetched in real time from the [Cat Facts API](https://catfact.ninja/fact).

This task validates the ability to:
- Consume a third-party API.
- Format and return JSON responses.
- Handle dynamic data and timestamps.

---

## 🧠 Features
- Dynamic cat fact fetched from an external API.
- Real-time UTC timestamp in ISO 8601 format.
- Clean JSON response structure.
- Graceful error handling for API or network issues.

---

## 📁 Project Structure
stage_0/
├── manage.py
├── requirements.txt
├── venv/
└── profile_project/
├── init.py
├── asgi.py
├── settings.py
├── urls.py
├── wsgi.py
└── profile_app/
├── init.py
├── admin.py
├── apps.py
├── migrations/
├── models.py
├── tests.py
├── urls.py
└── views.py


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd stage_0

2️⃣ Create and Activate a Virtual Environment

Windows (Git Bash / PowerShell)

python -m venv venv
source venv/Scripts/activate

3️⃣ Install Dependencies
pip install django requests

4️⃣ Run the Development Server
python manage.py runserver

5️⃣ Access the Endpoint

Open your browser or API client and visit:
👉 http://127.0.0.1:8000/me/

🧾 Example Response
{
  "status": "success",
  "user": {
    "email": "olawaleawanat@gmail.com",
    "name": "Awanat Olawale",
    "stack": "Python/Django"
  },
  "timestamp": "2025-10-18T21:51:08.323664+00:00",
  "fact": "The largest breed of cat is the Ragdoll with males weighing in at 15 to 20 lbs..."
}

🧰 Tech Stack

Language: Python 3

Framework: Django 5

External API: Cat Facts API

🛡️ Error Handling

If the Cat Facts API is unreachable, the endpoint returns:

{
  "fact": "Could not fetch cat fact at the moment"
}

🧑🏽‍💻 Author

Awanat Olawale
Email: olawaleawanat@gmail.com

Stack: Python / Django