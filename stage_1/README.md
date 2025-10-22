# 🔤 String Analysis API

A Django REST API that analyzes, stores, and filters strings based on various computed properties such as length, word count, palindrome detection, unique character count, and SHA256 hash generation.  
This project was built as part of **HNG Stage 1 Backend Task**.

---

## 🚀 Features

- **Analyze Strings:** Automatically computes:
  - String length  
  - Word count  
  - Unique characters  
  - Palindrome status  
  - SHA256 hash  
  - Character frequency map  
- **Retrieve Strings:** Fetch all analyzed strings or a single string by its hash.
- **Delete Strings:** Remove strings from the database.
- **Natural Language Filtering:** Query strings using simple natural language (e.g.  
  > “all single word palindromic strings”  
  > “strings with 3 unique characters”  
  > “strings longer than 10 characters”)
- **Persistent Storage:** Uses Django ORM for data persistence.

---

## 🧰 Tech Stack

- **Language:** Python 3.10+
- **Framework:** Django + Django REST Framework
- **Database:** SQLite (default)
- **Hashing:** hashlib (SHA256)
- **Runtime:** WSGI

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Hawanah-01/stage_1.git
cd stage_1
2. Create and Activate Virtual Environment
bash
Copy code
python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On macOS/Linux
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Apply Migrations
bash
Copy code
python manage.py makemigrations
python manage.py migrate
5. Run the Server
bash
Copy code
python manage.py runserver
Server runs by default on http://127.0.0.1:8000/

🧩 API Endpoints
1. Analyze String
POST /strings/

Request Body:

json
Copy code
{
  "text": "madam"
}
Response:

json
Copy code
{
  "length": 5,
  "is_palindrome": true,
  "unique_characters": 3,
  "word_count": 1,
  "sha256_hash": "765cc52b3dbc1bb8ec279ef9c8ec3d0f251c0c92a6ecdc1870be8f7dc7538b21",
  "character_frequency_map": {"m": 2, "a": 2, "d": 1}
}
2. Get All Strings
GET /strings/all/

Returns all previously analyzed strings.

3. Get Single String
GET /strings/get/?hash=<sha256_hash>

Fetch a single string by its SHA256 hash.

4. Delete String
DELETE /strings/<string_value>/

Deletes a string from the database.
Response: 204 No Content

5. Natural Language Filtering
GET /strings/filter-by-natural-language/?query=<your_query>

Examples:

/strings/filter-by-natural-language/?query=all%20single%20word%20palindromic%20strings

/strings/filter-by-natural-language/?query=strings%20with%203%20unique%20characters

/strings/filter-by-natural-language/?query=strings%20longer%20than%2010%20characters

🧮 Example Response
json
Copy code
{
  "data": [
    {
      "id": "765cc52b3dbc1bb8ec279ef9c8ec3d0f251c0c92a6ecdc1870be8f7dc7538b21",
      "value": "madam",
      "properties": {
        "length": 5,
        "is_palindrome": true,
        "unique_characters": 3,
        "word_count": 1,
        "sha256_hash": "765cc52b3dbc1bb8ec279ef9c8ec3d0f251c0c92a6ecdc1870be8f7dc7538b21",
        "character_frequency_map": {"m": 2, "a": 2, "d": 1}
      },
      "created_at": "2025-10-22T19:16:37.055715+00:00Z"
    }
  ],
  "count": 1,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "is_palindrome": true,
      "word_count": 1
    }
  }
}
🌐 Deployment
You can deploy this API easily on:

Render

Railway

Vercel (via WSGI adapter)

PythonAnywhere

Deployment Steps (Render Example)
Push your code to GitHub.

Create a new Web Service on Render.

Choose your repo → set environment to Python 3.

Add a requirements.txt and set:

Start Command: gunicorn stage_1.wsgi

Deploy!