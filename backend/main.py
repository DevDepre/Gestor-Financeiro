from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from backend.models import tipoEnum, Financas, Category
from backend.database import criar_tabelas, SessionLocal

app = FastAPI()
criar_tabelas()
print("tabelas criadas com sucesso.")

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/script", StaticFiles(directory="frontend/script"), name="script")

templates = Jinja2Templates(directory="frontend")