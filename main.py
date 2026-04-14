from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from localization import Localization

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")


def create_localization(lang: str) -> Localization:
    loc = Localization()
    if lang != loc.current_lang:
        loc.set_language(lang)
    return loc


@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    lang = request.cookies.get("lang", "ru")
    if lang not in ("ru", "en"):
        lang = "ru"

    loc = create_localization(lang)

    return templates.TemplateResponse(
        request,
        "main.html",
        {"request": request, "lang": lang, "loc": loc},
    )


@app.get("/toggle-language")
async def toggle_language(request: Request):
    current_lang = request.cookies.get("lang", "ru")
    next_lang = "en" if current_lang == "ru" else "ru"

    loc = create_localization(next_lang)
    response = templates.TemplateResponse(
        request,
        "main.html",
        {"request": request, "lang": next_lang, "loc": loc},
    )
    response.set_cookie(key="lang", value=next_lang, max_age=31536000, path="/")
    return response
