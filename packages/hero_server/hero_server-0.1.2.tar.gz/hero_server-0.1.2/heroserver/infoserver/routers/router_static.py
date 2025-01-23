from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

router_static = APIRouter()


@router_static.get("/static/{path:path}", response_class=FileResponse)
async def router_index_(request: Request, path: str):
    # import pudb

    # pudb.set_trace()
    deps = request.app.deps
    static_dir = deps.static_dir
    static_dir2 = deps.static_dir2

    name = Path(path).name

    if path.endswith(".js"):
        file_path = Path(static_dir2) / "js" / name
        # print(f"Checking file path for JS: {file_path}")
    elif path.endswith(".css"):
        file_path = Path(static_dir2) / "css" / name
        # print(f"Checking file path for CSS: {file_path}")
    else:
        file_path = Path(static_dir2) / path
        # print(f"Checking file path: {file_path}")

    if not file_path.exists() or not file_path.is_file():
        if path.endswith(".js"):
            file_path = Path(static_dir) / "js" / name
            # print(f"Checking fallback file path for JS: {file_path}")
        elif path.endswith(".css"):
            file_path = Path(static_dir) / "css" / name
            # print(f"Checking fallback file path for CSS: {file_path}")
        else:
            file_path = Path(static_dir) / path
            # print(f"Checking fallback file path: {file_path}")

        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(
                status_code=404, detail=f"File not found.\n{file_path}"
            )

    return FileResponse(file_path)
