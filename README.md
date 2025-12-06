# My Personal Blog

A simple Django-powered blog to share thoughts, tutorials, and projects.

## 🚀 Features

- Technical Stack
- Django 5.1 + Python 3.13
- PostgreSQL (Neon DB)
- HTMX for dynamic interactions
- WhiteNoise for static files
- Docker-ready deployment
- Custom 404, 500, and 403 error pages

- **Post Management:** Create, edit, and delete blog posts through the Django admin interface.
- **Categories and Tags:** Organize posts with categories and tags for easy navigation.
- **Dynamic Interactions:** HTMX is used for seamless, real-time interactions like post liking and comment submission without full page reloads.
- **Guest and Authenticated Likes:** Both registered users and guests can like posts.
- **Infinite Scroll:** Smoothly browse through a continuous list of posts.
- **Dockerized Environment:** Comes with `Dockerfile` and `docker-compose.yml` for easy setup and deployment.
- **Custom Error Pages:** User-friendly custom templates for 403, 404, and 500 errors.

## 🛠 Technical Stack

- **Backend:** Django 5.1, Python 3.13
- **Database:** PostgreSQL (Neon DB)
- **Frontend:** HTMX, Tailwind CSS
- **Static Files:** WhiteNoise
- **Deployment:** Docker

## 🏁 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

- Python 3.13+
- Docker and Docker Compose (recommended)
- Git

### Installation with Docker (Recommended)

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/my-personal-blog.git
    cd my-personal-blog
    ```

2.  **Create an environment file:**
    Create a `.env` file in the project root and add the following, replacing the placeholder values:

    ```
    SECRET_KEY='your-secret-key'
    DEBUG=True
    DATABASE_URL='your-postgresql-database-url'
    ```

3.  **Build and run the containers:**

    ```bash
    docker-compose up --build
    ```

4.  **Apply database migrations:**
    In a separate terminal, run:

    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Create a superuser:**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

The application will be available at `http://localhost:8000`.

### Manual Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/my-personal-blog.git
    cd my-personal-blog
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Create an environment file:**
    Follow step 2 from the Docker installation.

4.  **Apply database migrations and create a superuser:**

    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The application will be available at `http://localhost:8000`.

## usage Usage

- **Admin Interface:** Access the admin panel at `/admin` to manage posts, categories, and users.
- **Creating Posts:** Use the admin panel to create new blog posts with a rich text editor.
- **Commenting and Liking:** Engage with posts by leaving comments and liking them.

## 🧪 Running Tests

To run the test suite, use the following command:

```bash
python manage.py test
```
