"""
DD Workshop - API de usuarios
Vulnerabilidades intencionales para demo de Datadog Code Analysis.
"""
import sqlite3
import subprocess
import hashlib
import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

# ---------------------------------------------------------------
# VULN 1: Hardcoded credentials (SAST: hardcoded-secret)
# ---------------------------------------------------------------
DB_PASSWORD    = "admin123"
SECRET_API_KEY = "sk-prod-xK9mN2pL8qR4tY7wZ1aB3cD5eF6gH0iJ"
JWT_SECRET     = "mysupersecretkey"

app = FastAPI(title="DD Workshop API", version="1.0.0")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("""CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)""")
    conn.execute("INSERT INTO users VALUES (1,'admin','admin123','admin')")
    conn.execute("INSERT INTO users VALUES (2,'alice','password','user')")
    conn.execute("INSERT INTO users VALUES (3,'bob','qwerty','user')")
    conn.commit()
    return conn


@app.get("/")
def root():
    return {"message": "DD Workshop API running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# ---------------------------------------------------------------
# VULN 2: SQL Injection (SAST: sql-injection)
# ---------------------------------------------------------------
@app.get("/users/search")
def search_user(username: str):
    conn = get_db()
    cursor = conn.cursor()
    # FIXED: using parameterized query to prevent SQL injection
    query = "SELECT id, username, role FROM users WHERE username = ?"
    logger.info(f"Executing: {query} with params: ({username},)")
    cursor.execute(query, (username,))
    rows = cursor.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="User not found")
    return {"users": [{"id": r[0], "username": r[1], "role": r[2]} for r in rows]}


# ---------------------------------------------------------------
# VULN 3: Command Injection (SAST: command-injection)
# ---------------------------------------------------------------
@app.get("/utils/ping")
def ping_host(host: str):
    # BAD: input del usuario directo al shell
    result = subprocess.run(
        f"ping -c 1 {host}",
        shell=True,
        capture_output=True,
        text=True
    )
    return {"output": result.stdout, "returncode": result.returncode}


# ---------------------------------------------------------------
# VULN 4: Weak hashing (SAST: weak-hash)
# ---------------------------------------------------------------
@app.post("/users/password-hash")
def hash_password(password: str):
    # BAD: MD5 es criptográficamente inseguro para contraseñas
    hashed = hashlib.md5(password.encode()).hexdigest()
    return {"hash": hashed, "algorithm": "md5"}


# ---------------------------------------------------------------
# VULN 5: Path Traversal (SAST: path-traversal)
# ---------------------------------------------------------------
@app.get("/files/read")
def read_file(filename: str):
    # BAD: sin sanitización del path
    base_dir = "/app/static"
    file_path = os.path.join(base_dir, filename)
    try:
        with open(file_path, "r") as f:
            return {"content": f.read()}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------
# VULN 6: Sensitive data in logs (SAST: sensitive-data-logging)
# ---------------------------------------------------------------
@app.post("/users/login")
def login(username: str, password: str):
    # BAD: contraseña en texto plano en los logs
    logger.info(f"Login attempt: user={username} password={password}")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, role FROM users WHERE username=? AND password=?",
                   (username, password))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"user_id": user[0], "role": user[1], "token": JWT_SECRET}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
