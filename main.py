from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Usuario y contraseña fija (esto luego se puede mejorar con DB)
USER = "yeis"
PASSWORD = "230624Mili"

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == USER and password == PASSWORD:
        return templates.TemplateResponse("maik.html", {"request": request, "user": username})
    return RedirectResponse("/", status_code=302)
