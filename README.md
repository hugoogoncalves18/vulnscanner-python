# Vulnerability Scanner - Python + Flask

This is a simple vulnerability scanner using **Nmap** with a web interface built with **Flask** and **Bootstrap**.

## Features
- User registration and login (SQLite)
- Port scanning using Nmap
- PDF report generation
- Web interface with Bootstrap

## Requirements
- Python 3.10+
- Flask
- Flask-SQLAlchemy
- pdfkit
- nmap
- wkhtmltopdf (installed on Windows)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/hugoogoncalves18/vulnscanner-python.git
cd vulnscanner-python-main
## Create s virtusl environment
python -m venv venv
venv\Scripts\activate
## Install dependencies
pip install -r requirements.txt
## Initialize the database
from app import db, app
with app.app_context():
    db.create_all()
```
## Running the App
python app.py

## Notes
Make sure wkhtmltopdf is installed and the path is correctly set in app.py.
This project is intended for educational purposes only. Use responsibly and legally.

