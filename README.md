# Coderr Backend

This is the Backend for the Coderr-Project, a freelancer platform build with Django Rest Framework. Freelancers can create Offers as business-user which customer-users can order. Customer-users can write reviewes for the business-users. Both can edit their profiles and their offers, orders and reviews.

## Before you start

Python and pip is required to install this project.
For the Frontend I recommend the [Live-Server-Extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) for VS Code. Just right-click the index.html and click on 'open with live server'.

## Getting Started

1. Clone the Project
    - Frontend:
        ```bash
        git clone https://github.com/Simon-Kral/Coderr-Frontend
        ```
    - Backend:
        ```bash
        git clone https://github.com/Simon-Kral/Coderr-Backend
        ```

2. Python Virtual Environment
    - create a virtual environment:
        - open a terminal and navigate to the backend folder:
            ```bash
            cd Coderr-Backend
            python -m venv env
            ```
    - activate the virtual environment:
        - for Windows:
            ```bash
            env\Scripts\activate
            ```
        - for Linux/MacOS:
            ```bash
            source env/bin/activate
            ```

3. Requirements
    - Install the required packages:
        ```bash
        pip install -r requirements.txt
        ```

5. Setup Database
    - make and apply the Migrations
        ```bash
        python manage.py makemigrations
        python manage.py migrate
        ```

6. Run the Backend-Server
    ```bash
    python manage.py runserver
    ```

7. Optional
    - to enable the Guest-Users and add dummy data:
        ```bash
        python dummy_data.py
        ```
    - Guest-Users:
        - Customer:
            - Username: andrey
            - Password: asdasd
        - Business:
            - Username: kevin
            - Password: asdasd
    - to create an admin-user:
        ```bash
        python manage.py createsuperuser
        ```
Your Backend is now ready to be utilized by the Frontend.
A detailed backend documentation can be found in Coderr-Backend/docs/_build/html/index.html.
