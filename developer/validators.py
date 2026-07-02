from django.core.exceptions import ValidationError
import re


def validate_rate_limit(value):
    if value < 0:
        raise ValidationError(
            "Rate limit cannot be negative."
        )

    if value > 1000:
        raise ValidationError(
            "Rate limit too large."
        )
    
def validate_phone_number(value):
    if not value.isdigit():
        raise ValidationError("Phone number must contain only digits.")

    if len(value) != 10:
        raise ValidationError("Phone number must be exactly 10 digits.")


def validate_agent_name(value):
    if len(value.strip()) < 3:
        raise ValidationError("Name must be at least 3 characters long.")


def validate_email(value):
    if value:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, value):
            raise ValidationError("Enter a valid email address.")


def validate_category(value):
    if len(value.strip()) < 2:
        raise ValidationError("Category must not be empty.")
    

def validate_pincode(value):
    if not value.isdigit():
        raise ValidationError("Pincode must contain only numbers.")

    if len(value) != 6:
        raise ValidationError("Pincode must be exactly 6 digits.")


def validate_text_min_3(value):
    if len(value.strip()) < 3:
        raise ValidationError("This field must be at least 3 characters long.")
    
    
def validate_blog_title(value):
    if len(value.strip()) < 5:
        raise ValidationError("Blog title must be at least 5 characters long.")


def validate_blog_content(value):
    if len(value.strip()) < 20:
        raise ValidationError("Blog content must be at least 20 characters long.")
    

def validate_username(value):
    if len(value.strip()) < 4:
        raise ValidationError("Username must be at least 4 characters long.")


def validate_password(value):
    if len(value) < 6:
        raise ValidationError("Password must be at least 6 characters long.")

    # optional: prevent only whitespace passwords
    if value.strip() != value:
        raise ValidationError("Password cannot start or end with spaces.")

    # optional strength check (recommended)
    if not re.search(r"[A-Za-z]", value):
        raise ValidationError("Password must contain at least one letter.")

    if not re.search(r"\d", value):
        raise ValidationError("Password must contain at least one number.")
    
def validate_safe_message(value):
    if not value:
        return
    value = str(value).strip()
    
    if value == "":
        return

    blocked_patterns = [
        r"<script.*?>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe.*?>",
        r"<.*?script.*?>",
    ]

    for pattern in blocked_patterns:
        if re.search(pattern, value, re.IGNORECASE | re.DOTALL):
            raise ValidationError("Invalid content detected in message.")

    # if len(value.strip()) < 10:
        # raise ValidationError("Message must be at least 10 characters long.")

def validate_budget(value):
    if not value:
        raise ValidationError("Budget cannot be empty.")

    value = value.strip()

    pattern = r"^[0-9]+(\.[0-9]+)?(\s?[-to]+\s?[0-9]+(\.[0-9]+)?)?\s*(k|K|l|L|cr|CR|Cr|crore|Crore)?$"

    if not re.match(pattern, value):
        raise ValidationError(
            "Enter a valid budget (e.g., 10000, 10k, 1L, 1.5L, 1Cr, 1.15Cr, 1-5L, 1-2Cr)."
        )

def validate_safe_text(value):
    if value is None:
        return

    value = str(value).strip()

    if value == "":
        return

    blocked_patterns = [
        r"<script.*?>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe.*?>",
        r"<.*?script.*?>",
        r"data:text/html"
    ]

    for pattern in blocked_patterns:
        if re.search(pattern, value, re.IGNORECASE | re.DOTALL):
            raise ValidationError("Invalid content detected.")

    # if len(value) < 1:
    #     raise ValidationError("This field cannot be empty.")


def validate_name(value):
    # Allow empty or null
    if value is None or value == "":
        return value  

    value = value.strip()

    if len(value) < 1:
        raise ValidationError("Last name must be at least 3 characters long.")

    return value

