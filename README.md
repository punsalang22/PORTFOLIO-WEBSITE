PORTFOLIO WEBSITE (DJANGO)
=====================================

Requirements:
-------------
1. Python 3.x installed
2. Django installed

Project Setup:
--------------

Step 1: Open Terminal or PowerShell

Step 2: Navigate to the project folder

Example:

cd portfolio_django

Step 3: Create a virtual environment (if not yet created)

python -m venv venv

Step 4: Activate the virtual environment

PowerShell:

.\venv\Scripts\Activate

Command Prompt:

venv\Scripts\activate

Step 5: Install Django

pip install django

Step 6: Apply database migrations

python manage.py makemigrations
python manage.py migrate

Step 7: Run the development server

python manage.py runserver

Step 8: Open the website in a browser

Personal Information Page:
http://127.0.0.1:8000/personal/

Projects Page:
http://127.0.0.1:8000/projects/

Admin Page:
http://127.0.0.1:8000/admin/

GitHub Branch:
--------------
Project was developed in the "quiz2" branch and can be merged into the main branch through a Pull Request.

Features:
---------
1. Personal Information Page
   - First Name
   - Middle Name
   - Last Name
   - Summary
   - Contact Number
   - Email
   - Address

2. Project List Page
   - Displays available projects

3. Project Detail Page
   - Displays details of a selected project

4. Django Admin Integration
   - PersonalInformation model
   - Project model

Troubleshooting:
----------------

Error: "No module named django"

Solution:
1. Activate the virtual environment
2. Run:

pip install django

Error: Page not found (404)

Solution:
Use the correct URLs:

http://127.0.0.1:8000/personal/
http://127.0.0.1:8000/projects/


- Karl Punsalang
