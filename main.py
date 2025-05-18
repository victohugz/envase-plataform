from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from datetime import datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cidade TEXT NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS envase (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            data TEXT,
            total INTEGER,
            recusados INTEGER,
            quebrados INTEGER,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );
    """)
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM clientes")
    clientes = cur.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "clientes": clientes})

@app.post("/registrar")
def registrar(
    request: Request,
    cliente_id: int = Form(...),
    total: int = Form(...),
    recusados: int = Form(...),
    quebrados: int = Form(...)
):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO envase (cliente_id, data, total, recusados, quebrados)
        VALUES (?, ?, ?, ?, ?)
    """, (cliente_id, datetime.now().strftime('%Y-%m-%d'), total, recusados, quebrados))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)