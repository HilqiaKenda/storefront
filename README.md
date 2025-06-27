# 🛍️ StoreFront API — E-Commerce Backend (Dockerized)

StoreFront API is a **modular, scalable e-commerce backend** built with Django and Django REST Framework. It offers a clean, RESTful API to manage core e-commerce features like products, orders, carts, and customers. The project is containerized using Docker for consistency across environments, making it easy to set up, run, and deploy.

---

## 📦 Features

* ✅ Full-featured product and collection management
* ✅ Shopping cart and checkout workflow
* ✅ Customer and order management
* ✅ RESTful API with browsable interface via Django REST Framework
* ✅ MySQL database integration
* ✅ Redis for caching and background tasks (e.g., Celery)
* ✅ Containerized with Docker for reliable and reproducible deployment

---

## 🌐 API Endpoints

Base URL:

```
http://127.0.0.1:8000/store/
```

| Endpoint        | Description                                  |
| --------------- | -------------------------------------------- |
| `/products/`    | 🧾 List, create, update, and delete products |
| `/collections/` | 🗂️ Manage product collections               |
| `/carts/`       | 🛒 Handle shopping cart operations           |
| `/customers/`   | 👤 Manage customer profiles                  |
| `/orders/`      | 📦 Create and manage orders                  |

Each endpoint follows REST principles, supporting `GET`, `POST`, `PUT`, `PATCH`, and `DELETE` as appropriate.

---

## ⚙️ Tech Stack

* **Language:** Python 3.12
* **Framework:** Django 5.x + Django REST Framework
* **Database:** MySQL
* **Containerization:** Docker, Docker Compose
* **Caching / Tasks:** Redis (for caching and/or Celery workers)
* **Environment Management:** `.env`, Docker volumes, and secrets

---

## 🚀 Getting Started (Dockerized Setup)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/storefront.git
cd storefront
```

### 2️⃣ Build and start the containers

```bash
docker-compose up --build
```

This will:

* Build the Django application container
* Start MySQL and Redis containers
* Expose the Django app on `localhost:8000`

### 3️⃣ Apply migrations

```bash
docker-compose exec web python manage.py migrate
```

### 4️⃣ Create a superuser (optional but recommended)

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5️⃣ Access the API and Admin Panel

* API: [http://127.0.0.1:8000/store/](http://127.0.0.1:8000/store/)
* Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## ☁️ Production Deployment (Heroku)

You can deploy StoreFront to Heroku for production usage. Below are the recommended steps:

### 1️⃣ Prepare your project

* Add `gunicorn` to `requirements.txt`
* Add `Procfile`:

```
web: gunicorn store_front.wsgi --log-file -
```

* Make sure `ALLOWED_HOSTS` in `settings.py` includes your Heroku domain.

### 2️⃣ Initialize Heroku app

```bash
heroku create your-app-name
```

### 3️⃣ Add Heroku add-ons

```bash
heroku addons:create jawsdb:kitefly  # For MySQL
heroku addons:create heroku-redis:hobby-dev  # For Redis
```

> You may also use `Cache To Go`, `Stackhero`, or `Redis Cloud` as Redis add-ons.

### 4️⃣ Push code to Heroku

```bash
git push heroku main  # Or 'master' depending on your branch
```

### 5️⃣ Set environment variables

```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=mysql://...  # From JawsDB
heroku config:set REDIS_URL=redis://...     # From Redis add-on
```

### 6️⃣ Run migrations and create superuser

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## 🧪 Testing Locally

* Use `docker-compose exec web pytest` or `python manage.py test` inside the container
* Add test cases in `tests/` or `store/tests.py`

---

## 🛠️ Developer Notes

* All app services (Django, DB, Redis) run inside containers
* Django management commands are run via:

  ```bash
  docker-compose exec web python manage.py <command>
  ```
* You can also connect to the container shell using:

  ```bash
  docker-compose exec web bash
  ```

---

## 📁 Directory Structure

```
storefront/
├── store_front/          # Django project root
├── store/                # Main e-commerce app
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
└── .env                  # Environment variables
```

---

## 🧰 Useful Commands

* Build and run containers: `docker-compose up --build`
* Stop containers: `docker-compose down`
* View logs: `docker-compose logs -f web`
* Enter container shell: `docker-compose exec web bash`
* Run tests: `docker-compose exec web pytest`

---

## 🙌 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a pull request 🎉

---

## 📄 License

MIT License

---

## 💬 Contact

For feedback, reach out to [hilkiakenda@gmail.com](mailto:hilkiakenda@gmail.com) or open an issue on the GitHub repo.

---

Happy coding! 🚀
