import asyncio
import json
import os
import random
from datetime import datetime

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import TemplateNotFound

router_pdf = APIRouter()

connected_clients = set()


@router_pdf.get('/pdf/{path}', response_class=HTMLResponse)
async def read_pdf(request: Request, path: str):
    deps = request.app.deps
    if not path.endswith('.pdf'):
        path += '.pdf'
    pdf_url = f'/static/pdf/{path}'
    templates = deps.get_templates()
    # import pudb

    # pudb.set_trace()
    try:
        return templates.TemplateResponse(
            'heroweb/pdf_viewer.html', {'pdf_url': pdf_url, 'request': request}
        )
    except TemplateNotFound:
        raise HTTPException(
            status_code=404,
            detail='Template not found: heroweb/pdf_viewer.html',
        ) from None
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f'An unexpected error occurred: {str(e)}'
        ) from None


@router_pdf.get('/preso/{path}', response_class=HTMLResponse)
async def read_preso(request: Request, path: str):
    deps = request.app.deps
    if not path.endswith('.pdf'):
        path += '.pdf'
    pdf_url = f'/static/pdf/{path}'
    templates = deps.get_templates()
    # import pudb

    # pudb.set_trace()
    try:
        return templates.TemplateResponse(
            'heroweb/pdf_preso.html', {'pdf_url': pdf_url, 'request': request}
        )
    except TemplateNotFound:
        raise HTTPException(
            status_code=404,
            detail='Template not found: heroweb/pdf_preso.html',
        ) from None
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f'An unexpected error occurred: {str(e)}'
        ) from None


@router_pdf.post('/pdf-interaction')
async def pdf_interaction(request: Request):
    interaction = await request.json()

    # Add request.state.email in the interaction
    interaction['user_email'] = request.state.email
    print(interaction)

    # Add a server timestamp
    interaction['server_timestamp'] = datetime.utcnow().isoformat()

    # Log the interaction (you might want to save this to a database instead)
    # with open('pdf_interactions.log', 'a') as f:
    #     json.dump(interaction, f)
    #     f.write('\n')

    return JSONResponse({'status': 'success'}, status_code=200)


# New function to handle page redirection
@router_pdf.post('/redirectpage')
async def redirect_page(request: Request):
    data = await request.json()
    print(data)
    url = data.get('url')
    print(url)
    if url:
        message = json.dumps({'action': 'redirect', 'url': url})
        await broadcast(message, None)
        return {'status': 'success', 'message': f'Redirecting to {url}'}
    return {'status': 'error', 'message': 'No URL provided'}


@router_pdf.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await broadcast(data, websocket)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


async def broadcast(message: str, sender: WebSocket):
    for client in connected_clients:
        if client != sender:
            await client.send_text(message)


# Function to randomly change pages
async def random_page_change():
    while True:
        await asyncio.sleep(5)  # Wait for 5 seconds
        if connected_clients:
            random_page = random.randint(
                1, 10
            )  # Assume 10 pages, adjust as needed
            message = json.dumps({'action': 'changePage', 'page': random_page})
            # message2 = json.dumps(
            #     {'action': 'redirect', 'url': 'https://www.google.com'}
            # )
            await broadcast(message, None)
            # await broadcast(message2, None)


# @router_pdf.on_event('startup')
# async def startup_event():
#     asyncio.create_task(random_page_change())


@router_pdf.get('/slider/{path}', response_class=HTMLResponse)
async def read_slider(request: Request, path: str):
    mypath = os.path.abspath(
        os.path.expanduser('~/Downloads/THREEFOLD, v4, Intro')
    )
    prefix = '/static/slides/threefold_v4_intro/'
    files = [
        prefix + f
        for f in os.listdir(mypath)
        if os.path.isfile(os.path.join(mypath, f))
    ]
    files.sort()
    print(files)

    deps = request.app.deps
    templates = deps.get_templates()
    # import pudb

    # pudb.set_trace()
    try:
        return templates.TemplateResponse(
            'heroweb/swiper.html', {'files': files, 'request': request}
        )
    except TemplateNotFound:
        raise HTTPException(
            status_code=404,
            detail='Template not found: heroweb/swiper.html',
        ) from None
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f'An unexpected error occurred: {str(e)}'
        ) from None


@router_pdf.post('/report-viewed-file')
async def image_interaction(request: Request):
    interaction = await request.json()

    # Add request.state.email in the interaction
    interaction['user_email'] = request.state.email
    print(interaction)

    # Add a server timestamp
    interaction['server_timestamp'] = datetime.utcnow().isoformat()

    # Log the interaction (you might want to save this to a database instead)
    # with open('pdf_interactions.log', 'a') as f:
    #     json.dump(interaction, f)
    #     f.write('\n')

    return JSONResponse({'status': 'success'}, status_code=200)
