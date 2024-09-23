from fastapi import FastAPI, Query, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.responses import Response
import qrcode
from io import BytesIO
from functools import lru_cache
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@lru_cache(maxsize=1000)
def generate_qr_cached(data: str) -> bytes:
    img = qrcode.make(data)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    return img_io.getvalue()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_qr(data: str = Form(...)):
    if not data:
        return Response(content="No data provided", status_code=400)
    img_bytes = generate_qr_cached(data)
    return Response(content=img_bytes, media_type="image/png")

@app.get("/generate")
async def generate_qr_get(data: str = Query(...)):
    if not data:
        return Response(content="No data provided", status_code=400)
    img_bytes = generate_qr_cached(data)
    return Response(content=img_bytes, media_type="image/png")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)