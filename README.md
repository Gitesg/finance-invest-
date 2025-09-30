
## ⚙️ Environment Variables

The API connects to the database using:

```
DATABASE_URL=postgresql://postgres:password@db:5432/fintech_db
```


---

## 📖 API Documentation

Once the server is running, access Swagger UI at:

👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📂 Project Structure

```
.
├── app/                
│   ├── models.py       
│   ├── schemas.py      
│   ├── database.py     
│   └── main.py         
├── Dockerfile          
├── docker-compose.yml  
└── README.md           
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






