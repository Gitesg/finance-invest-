

````markdown
# Finance Invest API

A modern fintech API for investment and finance management, built with **Python**, **FastAPI**, and **PostgreSQL**.  
Easily deployable with **Docker Compose** for seamless local development.

---

## ✨ Features

- RESTful API for managing **financial data and investments**
- Built with **FastAPI** (Uvicorn server)
- **PostgreSQL** database backend
- **Dockerized** for simple setup and environment isolation
- Hot-reloading for rapid development
- **Product & Inventory Management**
  - Create, Read, Update, Delete products
  - Increase / decrease stock with validations
  - Low-stock alerts with thresholds

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Clone the Repository

```bash
git clone https://github.com/Gitesg/finance-invest-.git
cd finance-invest-
````

### Start the Application

```bash
docker-compose up
```

This will start:

* The **API server** on [http://localhost:8000](http://localhost:8000)
* A **PostgreSQL database** on port `5432`

---

## ⚙️ Environment Variables

The API connects to the database using:

```
DATABASE_URL=postgresql://postgres:password@db:5432/fintech_db
```

You can customize this in the `docker-compose.yml`.

---

## 📖 API Documentation

Once the server is running, access Swagger UI at:

👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📂 Project Structure

```
.
├── app/                # Main API application
│   ├── models.py       # SQLAlchemy models
│   ├── schemas.py      # Pydantic schemas
│   ├── database.py     # DB session and engine
│   └── main.py         # FastAPI entrypoint
├── Dockerfile          # API container definition
├── docker-compose.yml  # Multi-container orchestration
└── README.md           # Project information
```

---

## 🔑 Endpoints

### 🟢 Product Management

| Method     | Endpoint         | Description            |
| ---------- | ---------------- | ---------------------- |
| **POST**   | `/products`      | Create a new product   |
| **GET**    | `/products`      | List all products      |
| **GET**    | `/products/{id}` | Retrieve product by ID |
| **PUT**    | `/products/{id}` | Update product details |
| **DELETE** | `/products/{id}` | Delete product         |

#### Example – Create Product

```bash
curl -X POST "http://127.0.0.1:8000/products" \
-H "Content-Type: application/json" \
-d '{
  "name": "Laptop",
  "description": "Gaming laptop with RTX 4070",
  "stock_quantity": 10,
  "low_stock_threshold": 5
}'
```

---

### 📦 Inventory Logic

| Method   | Endpoint                          | Description                         |
| -------- | --------------------------------- | ----------------------------------- |
| **POST** | `/products/increasing-stock/{id}` | Increase stock for a product        |
| **POST** | `/products/decreasing-stock/{id}` | Decrease stock (with validation)    |
| **GET**  | `/products/low-stock`             | List products below stock threshold |

#### Example – Increase Stock

```bash
curl -X POST "http://127.0.0.1:8000/products/increasing-stock/1" \
-H "Content-Type: application/json" \
-d '{"quantity": 20}'
```

#### Example – Decrease Stock

```bash
curl -X POST "http://127.0.0.1:8000/products/decreasing-stock/1" \
-H "Content-Type: application/json" \
-d '{"quantity": 5}'
```

#### Example – Low Stock Products

```bash
curl -X GET "http://127.0.0.1:8000/products/low-stock"
```

---

## 🧪 Testing

Unit tests (with `pytest`) validate stock operations:

```bash
pytest
```

Covers edge cases:

* Prevent removing more stock than available
* Reject negative stock additions
* Detect products below threshold

---


