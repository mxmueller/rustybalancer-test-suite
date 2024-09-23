from aiohttp import web
import aiohttp_jinja2
import jinja2
import qrcode
from io import BytesIO

routes = web.RouteTableDef()

@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def home(request):
    return {}

@routes.get('/generate')
async def generate_qr_get(request):
    data = request.query.get('data')
    return await generate_qr_response(data)

@routes.post('/generate')
async def generate_qr_post(request):
    data = await request.post()
    return await generate_qr_response(data.get('data'))

async def generate_qr_response(data):
    if not data:
        return web.Response(text="No data provided", status=400)

    img = qrcode.make(data)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return web.Response(body=img_io.getvalue(), content_type='image/png')

async def init_app():
    app = web.Application()
    app.add_routes(routes)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    return app

if __name__ == '__main__':
    app = init_app()
    web.run_app(app, port=8080)