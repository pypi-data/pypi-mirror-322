from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from webcomponents.main.render import render

router_index = APIRouter()


@router_index.get("/wiki/{path:path}", response_class=HTMLResponse)
async def router_static_(request: Request, path: str):
    return render()
    # try:
    #     return render()
    # # except TemplateNotFound:
    # #     raise HTTPException(
    # #         status_code=404, detail=f"Doc not found: {path}"
    # #     ) from None
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=500, detail=f"An unexpected error occurred: {str(e)}"
    #     ) from None
