# Mola-Shop

This project is an online shopping website built using Django for the backend and HTML, CSS, and JavaScript for the frontend. The application provides a complete shopping experience with features like product listings, user authentication, shopping cart, and order management.

## Features

- User authentication (registration, login, logout)
- Product listings with search and filter capabilities
- Shopping cart management (add, remove, update quantities)
- Order management (place orders, view order history)
- Responsive design

## Technologies Used

- Django (Python)
- HTML
- CSS
- JavaScript

## Getting Started

### Prerequisites

- Python
- Django

### Installation


1. **Clone the repository**:
    ```bash
    git clone https://github.com/sanoy-si/Molla-Shop.git
    cd Molla-Shop
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install the required Python packages**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Apply the database migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser to access the admin panel**:
    ```bash
    python manage.py createsuperuser
    ```

7. **Collect static files**:
    ```bash
    python manage.py collectstatic

### Running the Development Server

Start the Django development server:

```bash
python manage.py runserver
```
### Visit http://127.0.0.1:8000/ in your web browser to see the application in action
![molla-shop2](https://github.com/user-attachments/assets/af27d8e6-d557-4eb4-b1d9-49a7565cf365)


