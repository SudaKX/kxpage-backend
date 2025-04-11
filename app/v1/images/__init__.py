
import os
import aiofiles
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from app.config import IMAGE_STORE


image_router = APIRouter(
    prefix="/api/images", tags=["images"]
)

@image_router.get("/")
async def image_get(h: str):
    try:
        async with aiofiles.open(os.path.join(IMAGE_STORE, h), "rb") as rd:
            img = await rd.read()
    except Exception as e:
        return JSONResponse(
            content={
                "message": "Image not found."
            },
            status_code=404,
            headers={
                'X-Requested-With': 'XMLHttpRequest'
            },
            media_type="application/json"
        )
    _, ext = h.split('.')
    return Response(
        content=img,
        status_code=200,
        headers={
            'X-Requested-With': 'XMLHttpRequest'
        },
        media_type=f"image/{ext}"
    )