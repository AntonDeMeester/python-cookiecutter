from fastapi.routing import APIRouter

from .core import authentication
from .core import views as core_views

router = APIRouter()

router.include_router(authentication.router, prefix="/auth", tags=["auth"])
router.include_router(core_views.router, tags=["core"])
