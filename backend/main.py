"""
DD Workshop - Backend API
FastAPI con vulnerabilidades intencionales, APM ddtrace y endpoint de performance degradado.
"""
import sqlite3
import subprocess
import hashlib
import os
import time
import logging
import random
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

# ---------------------------------------------------------------
# VULN 1: Hardcoded credentials
# ---------------------------------------------------------------
DB_PASSWORD    = "admin123"
SECRET_API_KEY = "sk-prod-xK9mN2pL8qR4tY7wZ1aB3cD5eF6gH0iJ"
JWT_SECRET     = "mysupersecretkey"
ADMIN_PASSWORD = "admin123"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DD Workshop API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------
# DB setup (SQLite in-memory)
# ---------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, email TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER, category TEXT)""")
    conn.execute("INSERT INTO users VALUES (1,'admin','admin123','admin','admin@workshop.dev')")
    conn.execute("INSERT INTO users VALUES (2,'matias','password123','user','matias@workshop.dev')")
    conn.execute("INSERT INTO users VALUES (3,'demo','demo2024','user','demo@workshop.dev')")
    for i in range(1, 51):
        conn.execute(f"INSERT INTO products VALUES ({i},'Product {i}',{round(random.uniform(10,500),2)},{random.randint(0,100)},'Category {(i%5)+1}')")
    conn.commit()
    return conn

# Shared DB instance (para el demo — no thread-safe intencional)
_db = get_db()

def db():
    return _db

# ---------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int
    category: str

def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.replace("Bearer ", "")
    if token != JWT_SECRET:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

# ---------------------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------------------

@app.get("/api/health")
def health():
    # BUG: simula fallo crítico del servicio para demo de Continuous Testing
    raise HTTPException(status_code=500, detail="Service unavailable")

@app.get("/")
def root():
    return {"message": "DD Workshop API v2", "docs": "/docs"}

# VULN 2: Sensitive data in logs + hardcoded check
@app.post("/api/auth/login")
def login(req: LoginRequest, conn: sqlite3.Connection = Depends(db)):
    logger.info(f"Login attempt: user={req.username} password={req.password}")
    cursor = conn.cursor()
    # VULN 3: SQL Injection
    query = f"SELECT * FROM users WHERE username = '{req.username}' AND password = '{req.password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "token": JWT_SECRET,
        "user": {"id": user["id"], "username": user["username"], "role": user["role"], "email": user["email"]}
    }

@app.get("/api/auth/me")
def me(token: str = Depends(verify_token), conn: sqlite3.Connection = Depends(db)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, email FROM users WHERE id = 1")
    user = cursor.fetchone()
    return dict(user)

# Products CRUD
@app.get("/api/products")
def list_products(
    page: int = 1,
    limit: int = 10,
    category: Optional[str] = None,
    token: str = Depends(verify_token),
    conn: sqlite3.Connection = Depends(db)
):
    cursor = conn.cursor()
    offset = (page - 1) * limit
    if category:
        # FIX: Use parameterized query to prevent SQL injection
        cursor.execute("SELECT * FROM products WHERE category = ? LIMIT ? OFFSET ?", (category, limit, offset))
    else:
        cursor.execute("SELECT * FROM products LIMIT ? OFFSET ?", (limit, offset))
    products = [dict(r) for r in cursor.fetchall()]
    cursor.execute("SELECT COUNT(*) FROM products")
    total = cursor.fetchone()[0]
    return {"products": products, "total": total, "page": page, "limit": limit}

@app.get("/api/products/{product_id}")
def get_product(product_id: int, token: str = Depends(verify_token), conn: sqlite3.Connection = Depends(db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return dict(product)

@app.post("/api/products")
def create_product(product: ProductCreate, token: str = Depends(verify_token), conn: sqlite3.Connection = Depends(db)):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, stock, category) VALUES (?, ?, ?, ?)",
        (product.name, product.price, product.stock, product.category)
    )
    conn.commit()
    return {"id": cursor.lastrowid, **product.model_dump()}

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, token: str = Depends(verify_token), conn: sqlite3.Connection = Depends(db)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    return {"deleted": product_id}

# ---------------------------------------------------------------
# ENDPOINT DE PERFORMANCE DEGRADADO (intencional para demo)
# ---------------------------------------------------------------
@app.get("/api/products/report/slow")
def slow_report(token: str = Depends(verify_token), conn: sqlite3.Connection = Depends(db)):
    """
    Endpoint intencionalmente lento para demo de APM y Synthetics.
    Simula: N+1 queries + sleep artificial + hash innecesario.
    """
    logger.warning("slow_report called — this endpoint has known performance issues")
    results = []
    cursor = conn.cursor()

    # N+1 query problem intencional
    cursor.execute("SELECT id FROM products")
    ids = [r[0] for r in cursor.fetchall()]

    for pid in ids:
        # Query individual por cada producto (N+1)
        cursor.execute("SELECT * FROM products WHERE id = ?", (pid,))
        product = dict(cursor.fetchone())

        # Sleep artificial simulando llamada externa lenta
        time.sleep(0.05)

        # Hash innecesario en cada iteración
        product["hash"] = hashlib.md5(str(product).encode()).hexdigest()
        results.append(product)

    # Sleep adicional simulando procesamiento
    time.sleep(random.uniform(0.5, 2.0))

    return {
        "report": results,
        "total": len(results),
        "generated_at": time.time(),
        "warning": "This endpoint is slow by design for demo purposes"
    }

# ---------------------------------------------------------------
# VULN 5: Command Injection
# ---------------------------------------------------------------
@app.get("/api/utils/ping")
def ping(host: str, token: str = Depends(verify_token)):
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)
    return {"output": result.stdout, "returncode": result.returncode}

# ---------------------------------------------------------------
# VULN 6: Path Traversal
# ---------------------------------------------------------------
@app.get("/api/files/read")
def read_file(filename: str, token: str = Depends(verify_token)):
    file_path = os.path.join("/app/static", filename)
    try:
        with open(file_path, "r") as f:
            return {"content": f.read()}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

# ---------------------------------------------------------------
# VULN 7: Weak hash para passwords
# ---------------------------------------------------------------
@app.post("/api/utils/hash")
def hash_password(password: str):
    return {"hash": hashlib.md5(password.encode()).hexdigest(), "algorithm": "md5"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
