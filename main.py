from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from db.core import get_db
from db.event import get_all_future_events, update_db_events, delete_db_events
from model.event_calendar import Month
from routers.event import route as event_route
from routers.event_calendar import route as calendar_route
from routers.limiter import limiter
from services.google_calendar import get_events as get_google_events, delete_events as delete_google_events

app = FastAPI()
app.include_router(router=event_route)
app.include_router(router=calendar_route)
app.state.limiter = limiter
templates = Jinja2Templates(directory="templates")
app.mount(
    "/templates",
    StaticFiles(directory=Path(__file__).parent.absolute() / "templates"),
    name="templates",
)


@app.get("/", response_class=HTMLResponse, tags=["get"])
@limiter.limit("1/second")
async def get_all_events(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    current_date = datetime.now()
    all_google_events = get_google_events(current_date)
    update_db_events(all_google_events, db)
    deleted_events = delete_db_events(all_google_events, db)
    delete_google_events(deleted_events)
    events = get_all_future_events(current_date, db)
    context = {
        'request': request,
        'month': Month.create(events, current_date.date()),
        'month_and_year_name': current_date.strftime("%B %Y").capitalize(),
        'date': current_date.strftime("%d.%m.%Y"),
    }
    return templates.TemplateResponse('calendar.html', context=context)
