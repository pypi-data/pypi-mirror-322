from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from jinja2 import TemplateNotFound

router_template = APIRouter()


# def get_app(app: FastAPI = Depends()):
#     return app


@router_template.get(
    "/example/{template_path:path}", response_class=HTMLResponse
)
async def read_template(request: Request, template_path: str):
    deps = request.app.deps
    try:
        if not template_path.endswith(".html"):
            template_path += ".html"
        templates = deps.get_templates()
        template = templates.get_template(template_path)
        return template.render(request=request)
    except TemplateNotFound:
        raise HTTPException(
            status_code=404, detail=f"Template not found: {template_path}"
        ) from None
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        ) from None
