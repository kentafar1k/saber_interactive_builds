from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.models.schemas import BuildRequest, ErrorResponse
from app.core.config import build_service

router = APIRouter()

@router.post("/get_tasks", response_model=list[str], responses={
    404: {"model": ErrorResponse},
    400: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
})
async def get_tasks(request: BuildRequest):
    try:
        tasks = build_service.get_sorted_tasks(request.build)
        return tasks
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(e)})
    except RuntimeError as e:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": str(e)})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": f"Unexpected error: {e}"}) 