import json
from pathlib import Path

from fastapi import Body, FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from localization import Localization
from logic import PlayerState

player_state = PlayerState(player_id=1, current_location_id="loc1", health = 3, health_max = 5)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="pages")
BASE_DIR = Path(__file__).resolve().parent
LOCATIONS = {
    "loc1": "loc1.html",
    "loc2": "loc2.html",
}
DEFAULT_LOCATION = "loc1"


class LocationSaveRequest(BaseModel):
    main_location: str
    extra_location: str | None = None


def create_localization(lang: str) -> Localization:
    loc = Localization()
    if lang != loc.current_lang:
        loc.set_language(lang)
    return loc


def valid_location(name: str) -> bool:
    return name in LOCATIONS


@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    lang = request.cookies.get("lang", "ru")
    if lang not in ("ru", "en"):
        lang = "ru"

    active_location = request.cookies.get("main_loc", DEFAULT_LOCATION)
    if not valid_location(active_location):
        active_location = DEFAULT_LOCATION

    extra_location = request.cookies.get("extra_loc", "")
    if not valid_location(extra_location):
        extra_location = ""

    loc = create_localization(lang)

    return templates.TemplateResponse(
        request,
        "main.html",
        {
            "request": request,
            "lang": lang,
            "loc": loc,
            "player_state": player_state,
            "active_location": active_location,
            "extra_location": extra_location,
            "locations": list(LOCATIONS.keys()),
        },
    )


@app.get("/toggle-language")
async def toggle_language(request: Request):
    current_lang = request.cookies.get("lang", "ru")
    next_lang = "en" if current_lang == "ru" else "ru"

    response = RedirectResponse(url="/")
    response.set_cookie(key="lang", value=next_lang, max_age=31536000, path="/")
    return response


@app.get("/location/{name}")
async def get_location(request: Request, name: str):
    if not valid_location(name):
        return HTMLResponse("<p>Location not found</p>", status_code=404)

    template_name = LOCATIONS[name]
    fragment_path = BASE_DIR / "pages" / template_name
    if not fragment_path.exists():
        return HTMLResponse("<p>Location fragment missing</p>", status_code=404)

    lang = request.cookies.get("lang", "ru")
    if lang not in ("ru", "en"):
        lang = "ru"

    loc = create_localization(lang)
    return templates.TemplateResponse(
        template_name,
        {"request": request, "lang": lang, "loc": loc},
    )


@app.post("/location/save")
async def save_location(request: LocationSaveRequest):
    main_location = request.main_location if valid_location(request.main_location) else DEFAULT_LOCATION
    extra_location = request.extra_location or ""
    if extra_location and not valid_location(extra_location):
        extra_location = ""

    response = JSONResponse({"status": "ok", "main_location": main_location, "extra_location": extra_location})
    response.set_cookie(key="main_loc", value=main_location, max_age=31536000, path="/")
    response.set_cookie(key="extra_loc", value=extra_location, max_age=31536000, path="/")
    return response

