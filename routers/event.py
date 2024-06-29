from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db.core import get_db
from db.event import create_db_event, __check_if_daily_events_are_full
from services.google_calendar import get_g_calendar
from .limiter import limiter
from fastapi import APIRouter, Request

from models.api_event import EventCreate

route = APIRouter(prefix="/event")
templates = Jinja2Templates(directory="templates")


@route.post("/", response_class=HTMLResponse, tags=["create"], description="Generates a html calendar with ")
@limiter.limit("10/second")
async def create_event(
        request: Request,
        event: EventCreate = Depends(EventCreate.as_form),
        db: Session = Depends(get_db),
        g_calendar: get_g_calendar = Depends(get_g_calendar)
) -> HTMLResponse:

    if __check_if_daily_events_are_full(event.start, event.event_type, db):
        return templates.TemplateResponse('error_page.html', context={'request': request}, status_code=409)
    google_event = g_calendar.add_new_event(event)
    db_event = create_db_event(event, google_event.event_id, db)
    if db_event:
        return templates.TemplateResponse('success_page.html', context={'request': request})
