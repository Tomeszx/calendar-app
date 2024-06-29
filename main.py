import pathlib
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from db.core import get_db
from db.event import get_all_future_events, update_db_events, delete_db_events
from models.event_calendar import Month
from routers.event import route as event_route
from routers.calendar import route as calendar_route
from routers.limiter import limiter
from services.google_calendar import get_g_calendar
from utilites.config_parser import get_config_data

app = FastAPI()
app.include_router(router=event_route)
app.include_router(router=calendar_route)
app.state.limiter = limiter
templates_path = pathlib.Path(__file__).parent.absolute().joinpath("templates")
templates = Jinja2Templates(directory=str(templates_path))
app.mount("/templates", StaticFiles(directory=templates_path), name="templates")


@app.get("/", response_class=HTMLResponse, tags=["get"])
@limiter.limit("1/second")
async def read_root(
        request: Request, db: Session = Depends(get_db), g_calendar: get_g_calendar = Depends(get_g_calendar)
) -> HTMLResponse:

    current_date = datetime.now()
    all_google_events = g_calendar.get_google_events(current_date)
    update_db_events(all_google_events, db)
    deleted_events = delete_db_events(all_google_events, db)
    g_calendar.delete_events(deleted_events)
    events = get_all_future_events(current_date, db)
    events_names = dict(get_config_data('events_max_per_day'))

    context = {
        'request': request,
        'month': Month.create(events, current_date.date(), list(events_names.values())[0]),
        'month_and_year_name': current_date.strftime("%B %Y").capitalize(),
        'date': current_date.strftime("%d.%m.%Y"),
        'events': enumerate(events_names.keys())
    }
    return templates.TemplateResponse(name='calendar.html', context=context)
