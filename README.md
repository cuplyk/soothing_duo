# 🛠️ Tecno Pronto (soothing_duo)

**Tecno Pronto** is a premium, after-hours IT support platform designed for busy professionals and families. It offers high-quality technical assistance outside of regular business hours, ensuring that your technology works when you need it most.

Built with a sleek, modern, dark-themed aesthetic inspired by [ready.so](https://ready.so), this project leverages the latest web technologies to provide a fast, responsive, and delightful user experience.

---

## 🚀 Features

- **Dynamic Hero Section:** A visually stunning entrance with glassmorphic elements and smooth transitions.
- **Service Availability:** Real-time availability tracking (`Mon-Fri 18:00-24:00 & Weekends`) with dynamic UI indicators.
- **Three-Step Process:** A clear, intuitive guide for users to get support.
- **Services Grid:** Organized display of IT solutions offered.
- **Account Management:** Secure user registration and authentication via `django-allauth`.
- **Blog & Tutorials:** A knowledge base for technical tips and guides.
- **Responsive Design:** Fully optimized for mobile, tablet, and desktop views.
- **High-End Aesthetics:** Custom dark mode with accent colors, modern typography (Outfit/Inter), and micro-animations.

---

## 🛠️ Technical Stack

- **Backend:** [Django 5.1](https://www.djangoproject.com/) & [Python 3.13](https://www.python.org/)
- **Frontend Logic:** [HTMX](https://htmx.org/) (for SPA-like feel without full page reloads)
- **Styling:** [Tailwind CSS](https://tailwindcss.com/) via `django-tailwind`
- **Database:** PostgreSQL (Neon DB recommended)
- **Authentication:** `django-allauth`
- **Static Assets:** [WhiteNoise](https://whitenoise.readthedocs.io/)
- **Environment Management:** [uv](https://github.com/astral-sh/uv)
- **Containerization:** Docker & Docker Compose

---

## 🏁 Getting Started

### Prerequisites

- [Python 3.13+](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv) (Fast Python package manager)
- [Node.js & npm](https://nodejs.org/) (For Tailwind CSS compilation)
- Docker (Optional, for containerized execution)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/soothing_duo.git
   cd soothing_duo
   ```

2. **Set up the virtual environment and install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY='your-secret-key'
   DEBUG=True
   DATABASE_URL='your-postgresql-url'
   ```

4. **Initialize Tailwind:**
   ```bash
   uv run .\manage.py tailwind install
   ```

5. **Apply Database Migrations:**
   ```bash
   uv run .\manage.py migrate
   ```

6. **Create a Superuser:**
   ```bash
   uv run .\manage.py createsuperuser
   ```

---

## 💻 Development

To start the development environment, you will need two terminal windows running:

### 1. Start Tailwind CSS Watcher
```bash
uv run .\manage.py tailwind start
```

### 2. Start Django Server
```bash
uv run .\manage.py runserver
```

The application will be available at `http://localhost:8000`.

---

## 🐳 Docker Deployment

For production or containerized testing:

1. **Build and Run:**
   ```bash
   docker-compose up --build
   ```

2. **Access the Container:**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

## 🚂 Deployment to Railway

This project is optimized for deployment on [Railway](https://railway.app/).

### Steps to Deploy:
1. **Connect your GitHub repository** to a new Railway project.
2. **Environment Variables:** Set the following variables in the Railway "Variables" tab:
   - `DEBUG`: `False`
   - `SECRET_KEY`: (A long random string)
   - `ALLOWED_HOSTS`: `.railway.app`
   - `CSRF_TRUSTED_ORIGINS`: `https://*.railway.app`
   - `DATABASE_URL`: (Automatically provided if you add a PostgreSQL plugin)
3. **Database:** Add a PostgreSQL service to your Railway project.
4. **Build:** Railway will automatically detect the `Dockerfile` and build the image.

---

## 🎨 Design Philosophy

Tecno Pronto follows a **Dark First** design language:
- **Primary Background:** `#080c0e` (Deep Obsidian)
- **Accent Color:** High-contrast oranges and custom gradients.
- **Typography:** Using modern, clean sans-serif fonts for readability.
- **Components:** Glassmorphic sidebars, floating background animations, and interactive hover states.

---

## 🧪 Testing

Run the test suite to ensure stability:
```bash
uv run .\manage.py test
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
