# Library Management System API

This project is a **Library Management System API** built using Django and Django REST Framework. It allows users to perform various library-related operations, including managing books, users, and borrowing records. The API is designed for both library staff and users, offering features such as book management, user authentication, and tracking borrowed books.

---

## Features

### 1. **User Authentication**
- User registration
- Login and logout
- Role-based access control (e.g., admin, staff, and regular users)

### 2. **Book Management**
- Add, update, and delete books (admin/staff only)
- Search for books by title, author, or genre
- List all available books

### 3. **Borrowing System**
- Borrow and return books
- View borrowing history for users
- Track overdue books

### 4. **Advanced Features**
- Pagination and filtering for API responses
- Secure authentication using JWT

---

## API Endpoints

### Authentication
| Method | Endpoint          | Description              |
|--------|-------------------|--------------------------|
| POST   | `/api/register/`  | Register a new user      |
| POST   | `/api/login/`     | Login and get JWT token  |
| POST   | `/api/logout/`    | Logout a user            |

### Books
| Method | Endpoint               | Description                  |
|--------|------------------------|------------------------------|
| GET    | `/api/books/`          | List all books               |
| POST   | `/api/books/`          | Add a new book (admin only)  |
| GET    | `/api/books/<id>/`     | Retrieve details of a book   |
| PUT    | `/api/books/<id>/`     | Update a book (admin only)   |
| DELETE | `/api/books/<id>/`     | Delete a book (admin only)   |

### Borrowing
| Method | Endpoint                        | Description                        |
|--------|---------------------------------|------------------------------------|
| POST   | `/api/borrow/`                  | Borrow a book                      |
| POST   | `/api/return/`                  | Return a book                      |
| GET    | `/api/borrowed-books/`          | List all borrowed books (user)     |
| GET    | `/api/overdue-books/`           | List all overdue books (admin)     |

---

## Installation and Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment tools (e.g., `venv` or `virtualenv`)

### Steps to Run the Project

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Tamagne/Library_Management_System_API.git
   cd Library_Management_System_API
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python3 -m venv env
   source env/bin/activate for mac
   env/Scripts/activate for window
 
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   cd library_api
   python manage.py migrate
   ```

5. **Create a Superuser** (optional for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the API**
   Open your browser and go to:
   - `http://127.0.0.1:8000/admin/` for the admin panel
   - `http://127.0.0.1:8000/api/` for API endpoints

---


---

## Future Enhancements
- Add user profile management.
- Implement notifications for overdue books.
- Add support for multiple libraries.



## Author
**Tamagne Gedefaye**
- GitHub: [Tamagne](https://github.com/Tamagne)
- Email: tamagne13@gmail.com
