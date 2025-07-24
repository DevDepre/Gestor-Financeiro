from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List

from backend.models import Financa, Category
from backend.database import criar_tabelas, SessionLocal
from backend.schemas import FinancaSchema, CategorySchema

app = FastAPI()
criar_tabelas()
print("Tabelas criadas com sucesso.")

app.mount("/frontend/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/frontend/script", StaticFiles(directory="frontend/script"), name="script")

templates = Jinja2Templates(directory="frontend/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/form", response_class=HTMLResponse)
async def mostrar_formulario(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(Category).all()
    return templates.TemplateResponse("form_finance.html", {
        "request": request,
        "categorias": categorias
    })

@app.get("/category", response_class=HTMLResponse)
async def mostrar_formulario_categoria(request: Request):
    return templates.TemplateResponse("new_category.html", {"request": request})

@app.post("/form", response_model=FinancaSchema)
async def enviar_formulario(
    name: str = Form(...),
    value: float = Form(...),
    type_input: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    db: Session = Depends(get_db),
):
    financa = Financa(
        name=name,
        value=value,
        type_input=type_input,
        description=description,
        category_id=category_id
    )
    db.add(financa)
    db.commit()
    db.refresh(financa)
    return RedirectResponse(url="/", status_code=303)
@app.post("/category", response_model=CategorySchema)
async def criar_categoria(
    name: str = Form(...),
    db: Session = Depends(get_db)
):

    category = Category (
        name=name
    )

    db.add(category)
    db.commit()
    db.refresh(category)
    return RedirectResponse(url="/form" , status_code=303)

@app.get("/financas/", response_model=List[FinancaSchema])
def listar_financas(db: Session = Depends(get_db)):
    return db.query(Financa).all()

@app.get("/categories/", response_model=List[CategorySchema])
def listar_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


