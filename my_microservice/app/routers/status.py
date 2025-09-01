from http import HTTPStatus

from fastapi import APIRouter

from my_microservice.app.database.engine import check_availability
from my_microservice.app.models.AppStatus import AppStatus


router = APIRouter()


@router.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(database=check_availability())
