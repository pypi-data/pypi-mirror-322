from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)
from fastapi_mail import MessageSchema, MessageType
from jwt.exceptions import PyJWTError

router_login = APIRouter()


# Step 1: Render login page to accept email
# @router_login.get('/', response_class=HTMLResponse)
# async def myroot(request: Request):
#     return RedirectResponse(url='/signup')


@router_login.get("/signup", response_class=HTMLResponse)
async def login_form(request: Request):
    deps = request.app.deps
    templates = deps.get_templates()

    return templates.TemplateResponse(
        "heroweb/signup.html", {"request": request}
    )


# Step 2: Handle form submission, generate token, send login email
@router_login.post("/loginsubmit")
async def send_login_email(request: Request, email: str = Form(...)):
    deps = request.app.deps
    if not email:
        # Redirect to signup page if email is not provided
        return RedirectResponse(url="/signup")
    jwt_handler = deps.get_jwt_handler()
    templates = deps.get_templates()
    # Generate the access token and email link
    access_token = jwt_handler.create_access_token({"sub": email})
    email_link = f"{deps.serverhost}/register?token={access_token}"

    # Render the email template with the email link
    template = templates.get_template("heroweb/email.html")
    rendered_template = template.render({"email_link": email_link})

    # Create the email message
    message = MessageSchema(
        subject="Login to your account",
        recipients=[email],  # List of recipient emails
        body=rendered_template,  # The rendered HTML content
        subtype=MessageType.html,  # Specify the subtype as HTML
    )

    # Send the email
    fm = deps.get_fastmail()
    await fm.send_message(message)

    return {"message": "Login link has been sent to your email."}


# Step 3: Handle email link redirection and set JWT in cookies
@router_login.get("/register")
async def register(request: Request, token: str):
    deps = request.app.deps
    jwt_handler = deps.get_jwt_handler()
    try:
        jwt_handler.verify_access_token(token)
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token") from None

    response = RedirectResponse(url="/info")
    response.set_cookie(key="access_token", value=token)
    return response


# Step 4: User info page, read JWT from cookies
@router_login.get("/info", response_class=HTMLResponse)
async def get_user_info(request: Request):
    deps = request.app.deps
    jwt_handler = deps.get_jwt_handler()
    templates = deps.get_templates()
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
        # return RedirectResponse(url='/signup')

    try:
        email = jwt_handler.verify_access_token(token)
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
        # return RedirectResponse(url='/signup')

    return templates.TemplateResponse(
        "heroweb/info.html", {"request": request, "email": email}
    )
