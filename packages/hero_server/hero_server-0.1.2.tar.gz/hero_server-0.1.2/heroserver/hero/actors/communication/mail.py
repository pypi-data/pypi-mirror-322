from pydantic import BaseModel, Field
from openrpc import RPCRouter
from typing import List,Optional
import redis

# Setup Redis connection
redis_conn = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

# Initialize RPC Router for method handling
router = RPCRouter()

# Redis Hash Key for Email Configurations
config_key = "hero:mail"

class EmailConfig(BaseModel):
    name: str = Field(..., description="Name of the mail profile", example="referral")
    brevo_api_key: str = Field(..., description="The API key as used in Brevo", example="xkeysib-example-api-key")
    from_email: str = Field(..., description="The email address we are sending from", example="info@example.com")
    from_name: str = Field(..., description="The name used to send from", example="Referral System")

@router.method()
def set(email_config: EmailConfig) -> EmailConfig:
    """
    Sets or updates the email configuration based on its name.
    """
    config_json = email_config.model_dump_json()
    redis_conn.hset(config_key, email_config.name, config_json)
    return email_config

@router.method()
def get(name: str) -> Optional[EmailConfig]:
    """
    Retrieves an email configuration by its name.
    """
    config_json = redis_conn.hget(config_key, name)
    if config_json:
        return EmailConfig.model_validate_json(config_json)
    return None

@router.method()
def delete(name: str) -> bool:
    """
    Deletes an email configuration by its name.
    """
    return redis_conn.hdel(config_key, name) > 0



class EmailDest(BaseModel):
    name: str = Field(..., description="Name of the person we want to send email to", example="aname")
    email: str = Field(..., description="Email address", example="mail@mail.com")

class EmailSendRequest(BaseModel):
    mailprofile: str = Field(..., description="Name of the mail profile", example="referral")
    to: List[EmailDest] = Field(..., description="List of destinations", example=[{"name": "something", "email": "info@kkk.com"}, {"name": "name", "email": "mail@mail.com"}])
    subject: str = Field(..., description="Subject for your email", example="This is my subject from my email.")
    content: str = Field(..., description="Content of the email", example="{title}\nPlease come and visit our place in Arusha.")

@router.method()
def send(request: EmailSendRequest) -> str:
    """
    Simulates sending an email by logging or queuing the request for further processing.
    """
    # Extract and prepare email destinations
    to = [{"email": dest.email, "name": dest.name} for dest in request.to]

    #now we need to send the email

    print(f"Sending email from profile '{request.mailprofile}' to {to}, subject: '{request.subject}'")

    return "OK"

#
