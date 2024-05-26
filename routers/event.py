from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db.core import get_db
from db.event import create_db_event
from services.google_calendar import add_event
from .limiter import limiter
from fastapi import APIRouter, Request

from model.api_event import Event, EventCreate

route = APIRouter(prefix="/event")
templates = Jinja2Templates(directory="templates")


@route.post("/", response_class=HTMLResponse, tags=["create"])
@limiter.limit("1/second")
async def create_event(request: Request, event: EventCreate = Depends(EventCreate.as_form), db: Session = Depends(get_db)) -> HTMLResponse:
    google_event = add_event(event)
    db_event = create_db_event(event, google_event.event_id, db)
    if db_event:
        return templates.TemplateResponse('success_page.html', context={'request': request})


@route.get("/{event_id}", tags=["get"])
@limiter.limit("1/second")
async def get_event(request, event_id: str) -> Event:
    ...


@route.put("/{event_id}", tags=["update"])
@limiter.limit("1/second")
async def update_event(request, event_id: str) -> Event:
    ...


@route.delete("/{event_id}", tags=["delete"])
@limiter.limit("1/second")
async def delete_event(request, event_id: str) -> Event:
    ...
