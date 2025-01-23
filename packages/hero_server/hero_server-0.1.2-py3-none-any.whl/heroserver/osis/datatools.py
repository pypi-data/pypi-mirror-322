import re

def normalize_email(email: str) -> str:
    # Normalize email by stripping spaces and converting to lower case
    #EmailStr.validate(email)  #TODO
    return email.strip().lower()

def normalize_phone(phone: str) -> str:
    # Normalize phone number by removing dots and spaces, and ensure it matches the pattern +<digits>
    phone = phone.replace(".", "").replace(" ", "")
    if not re.match(r"^\+\d+$", phone):
        raise ValueError(f"Invalid phone number: {phone}")
    return phone    
