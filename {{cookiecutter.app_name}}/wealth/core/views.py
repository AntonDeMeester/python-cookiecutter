from fastapi import APIRouter, Depends

from wealth.core.authentication import WealthJwt
from wealth.database.models import WealthItem

router = APIRouter()
