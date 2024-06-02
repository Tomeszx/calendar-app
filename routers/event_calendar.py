from datetime import datetime

from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from db.core import get_db
from db.event import get_all_future_events
from model.event_calendar import Month
from utilites.config_parser import get_config_data
from .limiter import limiter
from fastapi import APIRouter, Request

route = APIRouter(prefix="/calendar", tags=["calendar"])
templates = Jinja2Templates(directory="templates")


@route.get("/{year}/{month}", response_model=Month)
@limiter.limit("3/second")
async def get_all_events(request: Request, year: int, month: int, event: str, db: Session = Depends(get_db)) -> Month:
    date = datetime(year=year, month=month, day=1)
    events = get_all_future_events(date.date(), db)
    max_events_num = get_config_data('events_max_per_day', event)
    return Month.create(events, date.date(), max_events_num)
