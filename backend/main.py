from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from typing import List
from datetime import datetime

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
async def home(request: Request, db: Session = Depends(get_db)):
    ganhos = db.query(Financa).filter(Financa.type_input == "Ganho").all()
    gastos = db.query(Financa).filter(Financa.type_input == "Gasto").all()

    total_ganhos = sum(g.value for g in ganhos)
    total_gastos = sum(g.value for g in gastos)
    saldo_atual = total_ganhos - total_gastos

    return templates.TemplateResponse("home.html", {"request": request, "total_ganhos":total_ganhos, "total_gastos": total_gastos, "saldo_atual": saldo_atual})

@app.get("/form", response_class=HTMLResponse)
async def mostrar_formulario(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(Category).all()
    return templates.TemplateResponse("form_finance.html", {
        "request": request,
        "categorias": categorias
    })

@app.get("/dashboard_income", response_class=HTMLResponse)
async def mostrar_dashboard_income(request: Request, mes: int = None, db: Session = Depends(get_db)):

    if mes is None:
        mes = datetime.now().month

    receitas = db.query(Financa).filter(Financa.type_input == "Ganho").filter(extract("month", Financa.created_at) == mes).all()
    total_receitas = sum([g.value for g in receitas])

    nomes_meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    return templates.TemplateResponse("dashboard_income.html", {"request": request, "receitas": receitas,
    "total_receitas": total_receitas, "nomes_mes":nomes_meses[mes - 1], "mes_atual": mes})

@app.get("/dashboard_expenses", response_class=HTMLResponse)
async def mostrar_dashboard_expenses(request: Request, mes: int = None, db: Session = Depends(get_db)):

    if mes is None:
        mes = datetime.now().month

    despesas = db.query(Financa).filter(Financa.type_input == "Gasto").filter(extract("month", Financa.created_at) == mes).all()
    total_despesas = sum([g.value for g in despesas])

    nomes_meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    return templates.TemplateResponse("dashboard_expenses.html", {"request": request, "despesas": despesas,
    "total_despesas":total_despesas, "nomes_mes":nomes_meses[mes - 1], "mes_atual": mes})

@app.get("/dashboard_geral", response_class=HTMLResponse)
async def mostrar_dashboard_geral(request: Request, mes: int = None, db: Session = Depends(get_db)):

    if mes is None:
        mes = datetime.now().month

    gerais = db.query(Financa).filter(extract("month", Financa.created_at) == mes).all()
    receitas = db.query(Financa).filter(Financa.type_input == "Ganho").all()
    despesas = db.query(Financa).filter(Financa.type_input == "Gasto").all()

    total_receitas = sum([g.value for g in receitas])
    total_despesas = sum([g.value for g in despesas])
    media = (total_receitas + total_despesas) / 2

    nomes_meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    return templates.TemplateResponse("dashboard_geral.html", {"request": request, "gerais": gerais, "total_receitas":total_receitas, 
    "total_despesas":total_despesas, "media": media, "nomes_mes":nomes_meses[mes - 1], "mes_atual": mes})

@app.get("/api/graficos_income/mensal")
async def dados_grafico_income_mensal(db: Session = Depends(get_db)):
    ganhos = (
        db.query(
            extract("month", Financa.created_at).label("mes"),
            func.sum(Financa.value).label("total")
        )
        .filter(Financa.type_input == "Ganho")
        .group_by("mes")
        .order_by("mes")
        .all()
    )

    return JSONResponse({"ganhos": [{"mes": int(g.mes), "total": float(g.total)} for g in ganhos]})

@app.get("/api/graficos_expenses/mensal")
async def dados_grafico_expenses_mensal(db:Session = Depends(get_db)):
    gastos = (
        db.query(
            extract("month", Financa.created_at).label("mes"),
            func.sum(Financa.value).label("total")
        )
        .filter(Financa.type_input == "Gasto")
        .group_by("mes")
        .order_by("mes")
        .all()
    )

    return JSONResponse({"gastos": [{"mes": int(g.mes), "total": float(g.total)} for g in gastos]})

@app.get("/api/graficos_geral/mensal")
async def dados_grafico_geral_mensal(db: Session = Depends(get_db)):
    ganhos = (
        db.query(
            extract("month", Financa.created_at).label("mes"),
            func.sum(Financa.value).label("total")
        )
        .filter(Financa.type_input == "Ganho")
        .group_by("mes")
        .order_by("mes")
        .all()
    )

    gastos = (
        db.query(
            extract("month", Financa.created_at).label("mes"),
            func.sum(Financa.value).label("total")
        )
        .filter(Financa.type_input == "Gasto")
        .group_by("mes")
        .order_by("mes")
        .all()
    )

    return JSONResponse({
        "ganhos": [{"mes": int(g.mes), "total": float(g.total)} for g in ganhos],
        "gastos": [{"mes": int(g.mes), "total": float(g.total)} for g in gastos]
    })

@app.get("/category", response_class=HTMLResponse)
async def mostrar_formulario_categoria(request: Request):
    return templates.TemplateResponse("new_category.html", {"request": request})

@app.get("/editar_receita/{id}", response_class=HTMLResponse)
async def editar_receita(request: Request, id: int, db: Session = Depends(get_db)):
    receita = db.query(Financa).filter(Financa.id == id, Financa.type_input == "Ganho").first()

    if not receita:
        return templates.TemplateResponse("erro_404.html", {"request": request}, status_code= 404)

    categorias = db.query(Category).all()
    return templates.TemplateResponse("edit_form_finance_income.html", {"request": request, "receita": receita, "categorias":categorias}) 

@app.get("/editar_dispesa/{id}", response_class=HTMLResponse)
async def editar_dispesa(request: Request, id: int, db: Session = Depends(get_db)):
    dispesa = db.query(Financa).filter(Financa.id == id, Financa.type_input == "Gasto").first()

    if not dispesa:
        return templates.TemplateResponse("erro_404.html", {"request": request}, status_code= 404)

    categorias = db.query(Category).all()
    return templates.TemplateResponse("edit_form_finance_expenses.html", {"request": request, "dispesa": dispesa, "categorias":categorias}) 

@app.get("/editar_geral/{id}", response_class=HTMLResponse)
async def editar_geral(request: Request, id: int, db: Session = Depends(get_db)):
    geral = db.query(Financa).filter(Financa.id == id).first()

    if not geral:
        return templates.TemplateResponse("erro_404.html", {"request": request}, status_code=404)

    categorias = db.query(Category).all()
    return templates.TemplateResponse("/edit_form_finance_geral.html", {"request": request, "geral": geral, "categorias": categorias})

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

@app.post("/acao_receita")
async def tratar_acao_receita(
    id: int = Form(...),
    action: str = Form(...),
    db: Session = Depends(get_db)
):
    if action == "excluir":
        receita = db.query(Financa).filter(Financa.id == id, Financa.type_input == "Ganho").first()
        if receita:
            db.delete(receita)
            db.commit()
        return RedirectResponse(url="/dashboard_income", status_code= 303)

    elif action == "editar":
        return RedirectResponse(url=f"/editar_receita/{id}", status_code= 303)

@app.post("/acao_dispesa")
async def tratar_acao_dispensa(
    id: int = Form(...),
    action: str = Form(...),
    db: Session = Depends(get_db)
):
    if action == "excluir":
        dispensa = db.query(Financa).filter(Financa.id == id, Financa.type_input == "Gasto").first()

        if dispensa:
            db.delete(dispensa)
            db.commit()
        return RedirectResponse(url="/dashboard_expenses", status_code= 303)

    elif action == "editar":
        return RedirectResponse(url=f"/editar_dispesa/{id}", status_code= 303)

@app.post("/acao_geral")
async def tratar_acao_geral(id: int = Form(...), action: str = Form(...), db: Session = Depends(get_db)):

    if action == "excluir":
        gerais = db.query(Financa).filter(Financa.id == id).first()

        if gerais:
            db.delete(gerais)
            db.commit()
        return RedirectResponse(url="/dashboard_geral", status_code= 303)

    elif action == "editar":
        return RedirectResponse(url=f"/editar_geral/{id}", status_code= 303)

@app.post("/editar_receita/{id}")
async def salvar_edicao_receita(
    request: Request,
    id: int,
    name: str = Form(...),
    value: float = Form(...),
    type_input: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    db: Session = Depends(get_db),
):

    receita = db.query(Financa).filter(Financa.id == id, Financa.type_input == "Ganho").first()

    if not receita:
        return templates.TemplateResponse("erro_404.html", {"request": request}, status_code=404)

    receita.name = name
    receita.value = value
    receita.description = description
    receita.type_input = type_input
    receita.category_id = category_id

    db.commit()

    return RedirectResponse(url="/dashboard_income", status_code=303)

@app.post("/editar_dispesa/{id}")
async def salvar_edicao_dispesa(
    request: Request,
    id: int,
    name: str = Form(...),
    value: float = Form(...),
    type_input: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    db: Session = Depends(get_db),
):

    dispesa = db.query(Financa).filter(Financa.id == id, Financa.type_input == "Gasto").first()

    if not dispesa:
        return templates.TemplateResponse("erro_404.html", {"request": request}, status_code=404)

    dispesa.name = name
    dispesa.value = value
    dispesa.description = description
    dispesa.type_input = type_input
    dispesa.category_id = category_id

    db.commit()

    return RedirectResponse(url="/dashboard_expenses", status_code=303)

@app.post("/editar_geral/{id}")
async def salvar_edicao_geral(
    request: Request,
    id: int,
    name: str = Form(...),
    value: str = Form(...),
    type_input: str = Form(...),
    description: str = Form(...),
    category_id: str = Form(...),
    db: Session = Depends(get_db)
):

    geral = db.query(Financa).filter(Financa.id == id).first()

    if not geral:
        return templates.TemplateResponse("erro_404.html", {"request": request}, status_code=404)


    geral.name = name
    geral.value = value
    geral.description = description
    geral.type_input = type_input
    geral.category_id = category_id
    
    db.commit()

    return RedirectResponse("/dashboard_geral", status_code= 303)
    
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