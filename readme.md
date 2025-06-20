## A Django web application for managing and viewing vacation packages with user authentication, role-based permissions, and interactive features.

## Features
-------------------------------------------------------
- User authentication (Sign up / Log in / Log out)
- Not authenticated user only can see the vacation list
- Admin & regular user roles
- Create / Read / Update / Delete vacations (admin only)
- Like vacations (users only)
- RESTful API endpoints
- Crispy form styling (with `django-crispy-forms`)
- Unit & integration tests
-------------------------------------------------------
1)  **Create and activate a virtual environment (recommended)**
        for windows:
                 python -m venv venv
                 venv\Scripts\activate

        for mac:
                  python3 -m venv venv
                   source venv/bin/activate



2)  **Install dependencies:**

          pip install -r requirements.txt

2)  **Apply migrations:**

          python manage.py migrate

3)  **Load sample data (if you choose to work with my db):**

          python manage.py loaddata data.json

4)  **Run development server:**

          python manage.py runserver


5)   **Users Example**

| Role    | Email               | Password    |
| ------- | ------------------- | ----------- |
| Admin   | `admin@gmail.com`   | `admin`     |
| Regular | `igor406@gmail.com` | `test12345` |


6) **Useful Links**

        Home: http://localhost:8000/
        Admin Panel: http://localhost:8000/admin

     ## To log into the Admin Panel:

                                 Username=admin
                                 Password=admin

7)   **Testing**
       You can test individual apps:

                           
                    a)python manage.py test api.tess

                    b)python manage.py test user.tests
                    
                    c)python manage.py test vacation.tests
        
        Or run all tests at once:

                     python manage.py test


8)    **Notes**

            Not authenticated user only can see the vacation list

            Only admins can create, edit, or delete vacations.

            Only regular users can like vacations.

            Includes both frontend views and REST API support.









