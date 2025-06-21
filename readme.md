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

3) **DB settings:**

       Ensure that PostgreSQL is installed and running.
       Create a PostgreSQL database named vacation_project_db, or update the settings below in vacation_project/settings.py:
             
              'NAME': 'vacation_project_db',          
              'USER': 'postgres',         
              'PASSWORD': 'your password',         
              'HOST': 'localhost',
              'PORT': '5432',


3)  **Apply migrations:**

          python manage.py migrate

4)  **Load sample data (if you choose to work with my db):**
        
          Ensure the data.json file is saved with UTF-8 encoding before loading:
          
                    python manage.py loaddata data.json

5)  **Run development server:**

          python manage.py runserver


6)   **Users Example**

| Role    | Email               | Password    |
| ------- | ------------------- | ----------- |
| Admin   | `admin@gmail.com`   | `admin`     |
| Regular | `igor406@gmail.com` | `test12345` |


7) **Useful Links**

        Home: http://localhost:8000/
        Admin Panel: http://localhost:8000/admin

     ## To log into the Admin Panel:

                                 Username=admin
                                 Password=admin

8)   **Testing**
       You can test individual apps:

                           
                    a)python manage.py test api.tests

                    b)python manage.py test user.tests
                    
                    c)python manage.py test vacation.tests
        
        Or run all tests at once:

                     python manage.py test


9)    **Notes**

            Not authenticated user only can see the vacation list

            Only admins can create, edit, or delete vacations.

            Only regular users can like vacations.

            Includes both frontend views and REST API support.









