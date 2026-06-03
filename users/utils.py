# from playwright.sync_api import sync_playwright
# from cloudinary.uploader import upload
# import tempfile

# def capture_screenshot_and_upload(url: str):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)  # Launch browser in headless mode
#         page = browser.new_page()  # Create a new page

#         # Navigate to the URL and wait until the network is idle
#         page.goto(url, timeout=90000, wait_until="domcontentloaded")  

#         screenshot = page.screenshot()  # Take a screenshot of the page
#         browser.close()  # Close the browser

#     # Save the screenshot to a temporary file
#     with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
#         tmpfile.write(screenshot)  # Write the screenshot to the temporary file
#         tmpfile.close()

#         # Upload the screenshot to Cloudinary and return the URL
#         response = upload(tmpfile.name, folder="houses/screenshot")
#         return response['secure_url']


# utils.py
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.conf import settings
import cloudinary.uploader
import os
from agents.models import AgentProperty
import re

from django.utils import timezone

from developer.models import UserProfile,Property
from developer.models import *


def capture_property_screenshot(property_obj):
    """
    Uses Selenium to capture a screenshot of the property page
    and uploads it to Cloudinary. Returns Cloudinary URL.
    """
    # Configure headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1200,800")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Build absolute URL for the property detail page
        url = f"{settings.SITE_URL}/property_detail/{property_obj.id}/"
        driver.get(url)

        # Take screenshot into a temporary file
        tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        driver.save_screenshot(tmp_file.name)

        # Upload screenshot to Cloudinary
        upload_result = cloudinary.uploader.upload(
            tmp_file.name,
            folder="property_screenshots",
            use_filename=True,
            unique_filename=False
        )

        # Return Cloudinary URL
        return upload_result.get("secure_url")

    finally:
        driver.quit()




import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings


def send_otp_email(to_email, otp):

    # API Configuration
    configuration = sib_api_v3_sdk.Configuration()

    configuration.api_key['api-key'] = settings.BREVO_API_KEY

    api_client = sib_api_v3_sdk.ApiClient(configuration)

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

    subject = "Your Email Verification OTP"

    html_content = f"""
    <div style="font-family:Arial;padding:20px">

        <h2>Email Verification</h2>

        <p>Your OTP is:</p>

        <h1 style="color:#0ea5e9">{otp}</h1>

        <p>This OTP is valid for 5 minutes.</p>

        <hr>

        <small>If you didn't request this, ignore this email.</small>

    </div>
    """

    send_email = sib_api_v3_sdk.SendSmtpEmail(

        to=[{"email": to_email}],

        sender={
            "email": settings.DEFAULT_FROM_EMAIL,
            "name": "BuySel"
        },

        subject=subject,

        html_content=html_content,
    )

    try:

        response = api_instance.send_transac_email(send_email)

        print("Brevo Email Sent:", response)

        return True

    except ApiException as e:

        print("Brevo API Error :", e)

        return False

import jwt
from datetime import datetime, timedelta
from django.conf import settings


def generate_access_token(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def generate_refresh_token(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=7),  # 7 days
        "iat": datetime.utcnow(),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

from django.conf import settings
from hashids import Hashids

hashids = Hashids(
    salt=settings.SECRET_KEY,
    min_length=16
)


def encode_id(id):
    return hashids.encode(id)


def decode_id(hash_id):
    decoded = hashids.decode(hash_id)
    return decoded[0] if decoded else None

def check_agent_property_limit(agent, category_name=None):
    """
    Check if the agent can add a new property within their plan limits.
    Returns (True/False, message)
    """
    total_limit, residential_limit, commercial_limit = agent.get_plan_limits()

    total_used = AgentProperty.objects.filter(agent=agent).count()

    # TOTAL LIMIT CHECK (for Premium + Elite)
    if total_used >= total_limit:
        return False, f"You have reached your total listing limit ({total_limit})"

    # Only Premium agents check category limits
    if agent.plan and category_name:
        if category_name.lower() == "residential":
            residential_used = AgentProperty.objects.filter(
                agent=agent,
                category__name__iexact="Residential"
            ).count()

            if residential_used >= residential_limit:
                return False, f"You reached Residential limit ({residential_limit})"

        elif category_name.lower() == "commercial":
            commercial_used = AgentProperty.objects.filter(
                agent=agent,
                category__name__iexact="Commercial"
            ).count()

            if commercial_used >= commercial_limit:
                return False, f"You reached Commercial limit ({commercial_limit})"

    return True, "Allowed"



import razorpay

from django.conf import settings


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)



import re

from django.utils import timezone


FREE_PROPERTY_LIMIT = 2


def get_property_remaining_counts(user):

    profile = UserProfile.objects.filter(
        user=user
    ).first()

    user_properties = (
        Property.objects
        .filter(user=user)
        .order_by("created_at")
    )

    total_properties = user_properties.count()

    # =====================================================
    # DEFAULT VALUES
    # =====================================================

    total_property_limit = FREE_PROPERTY_LIMIT

    total_residential_limit = FREE_PROPERTY_LIMIT
    total_commercial_limit = FREE_PROPERTY_LIMIT

    residential_used = 0
    commercial_used = 0

    residential_remaining = 0
    commercial_remaining = 0

    # =====================================================
    # FIRST 2 PROPERTIES ARE FREE
    # =====================================================

    free_property_ids = list(
        user_properties.values_list(
            "id",
            flat=True
        )[:FREE_PROPERTY_LIMIT]
    )

    # =====================================================
    # ACTIVE SUBSCRIPTIONS
    # =====================================================

    subscriptions = (
        UserPlanSubscription.objects
        .filter(
            user=user,
            is_active=True,
            expiry_date__gt=timezone.now()
        )
        .select_related("plan")
    )

    has_active_plan = subscriptions.exists()

    # =====================================================
    # ADD ALL PLAN LIMITS
    # =====================================================

    if has_active_plan:

        for sub in subscriptions:

            plan = sub.plan

            # ==========================================
            # PROPERTY LIMIT
            # ==========================================

            try:

                property_limit = int(
                    "".join(
                        filter(
                            str.isdigit,
                            str(
                                plan.property_listing_limit
                            )
                        )
                    ) or 0
                )

            except Exception:

                property_limit = 0

            total_property_limit += property_limit

            # ==========================================
            # LISTING TYPE
            # Example:
            # "6 Residential / 6 Commercial"
            # ==========================================

            listing_type = str(
                getattr(
                    plan,
                    "listing_type",
                    ""
                )
            ).lower()

            residential_match = re.search(
                r"(\d+)\s*residential",
                listing_type
            )

            commercial_match = re.search(
                r"(\d+)\s*commercial",
                listing_type
            )

            if residential_match:

                total_residential_limit += int(
                    residential_match.group(1)
                )

            if commercial_match:

                total_commercial_limit += int(
                    commercial_match.group(1)
                )

    # =====================================================
    # USED COUNTS
    # FIRST 2 FREE PROPERTIES SHOULD NOT
    # CONSUME PLAN LIMITS
    # =====================================================

    paid_properties = user_properties.exclude(
        id__in=free_property_ids
    )

    residential_used = paid_properties.filter(
        category__name__icontains="residential"
    ).count()

    commercial_used = paid_properties.filter(
        category__name__icontains="commercial"
    ).count()

    # =====================================================
    # REMAINING COUNTS
    # =====================================================

    residential_remaining = max(
        total_residential_limit -
        residential_used,
        0
    )

    commercial_remaining = max(
        total_commercial_limit -
        commercial_used,
        0
    )

    remaining_property = max(
        total_property_limit -
        total_properties,
        0
    )

    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "remaining_property":
        remaining_property,

        "residential_remaining":
        residential_remaining,

        "commercial_remaining":
        commercial_remaining,

        "total_properties":
        total_properties,

        "free_property_ids":
        free_property_ids,

        "residential_used":
        residential_used,

        "commercial_used":
        commercial_used,

        "total_residential_limit":
        total_residential_limit,

        "total_commercial_limit":
        total_commercial_limit,

        "total_property_limit":
        total_property_limit,

        "has_active_plan":
        has_active_plan,

        "active_subscription_count":
        subscriptions.count()
    }

# FREE_PROPERTY_LIMIT = 2


# def get_property_remaining_counts(user):

#     profile = (
#         UserProfile.objects
#         .filter(user=user)
#         .select_related("user_plan")
#         .first()
#     )

#     user_properties = (
#         Property.objects
#         .filter(user=user)
#         .order_by("created_at")
#     )

#     total_properties = user_properties.count()

#     # =====================================================
#     # DEFAULT VALUES
#     # =====================================================

#     residential_limit = 0
#     commercial_limit = 0

#     total_residential_limit = 0
#     total_commercial_limit = 0

#     residential_used = 0
#     commercial_used = 0

#     residential_remaining = 0
#     commercial_remaining = 0

#     remaining_property = 0

#     has_active_plan = False
#     active_plan = None

#     # =====================================================
#     # ACTIVE PLAN CHECK
#     # =====================================================

#     if (
#         profile
#         and profile.user_plan
#         and profile.plan_expiry_date
#         and profile.plan_expiry_date >= timezone.now()
#     ):

#         has_active_plan = True
#         active_plan = profile.user_plan

#     # =====================================================
#     # FREE PROPERTY IDS
#     # FIRST 2 PROPERTIES ARE FREE
#     # =====================================================

#     free_property_ids = list(
#         user_properties.values_list(
#             "id",
#             flat=True
#         )[:FREE_PROPERTY_LIMIT]
#     )

#     # =====================================================
#     # PLAN LOGIC
#     # =====================================================

#     if has_active_plan and active_plan:

#         listing_type = (
#             str(active_plan.listing_type)
#             .lower()
#             .strip()
#         )

#         # =================================================
#         # "no" means 0
#         # =================================================

#         if listing_type == "no":

#             residential_remaining = 0
#             commercial_remaining = 0
#             remaining_property = 0

#         else:

#             # =============================================
#             # RESIDENTIAL LIMIT
#             # =============================================

#             residential_match = re.search(
#                 r"(\d+)\s*residential",
#                 listing_type
#             )

#             if residential_match:

#                 residential_limit = int(
#                     residential_match.group(1)
#                 )

#             # =============================================
#             # COMMERCIAL LIMIT
#             # =============================================

#             commercial_match = re.search(
#                 r"(\d+)\s*commercial",
#                 listing_type
#             )

#             if commercial_match:

#                 commercial_limit = int(
#                     commercial_match.group(1)
#                 )

#             # =============================================
#             # TOTAL LIMITS
#             # =============================================

#             total_residential_limit = residential_limit
#             total_commercial_limit = commercial_limit

#             # =============================================
#             # PLAN PROPERTIES ONLY
#             # EXCLUDE FIRST 2 FREE PROPERTIES
#             # =============================================

#             paid_properties = user_properties.exclude(
#                 id__in=free_property_ids
#             )

#             # =============================================
#             # USED COUNTS
#             # =============================================

#             residential_used = paid_properties.filter(
#                 category__name__icontains="residential"
#             ).count()

#             commercial_used = paid_properties.filter(
#                 category__name__icontains="commercial"
#             ).count()

#             # =============================================
#             # REMAINING
#             # =============================================

#             residential_remaining = (
#                 total_residential_limit
#                 - residential_used
#             )

#             commercial_remaining = (
#                 total_commercial_limit
#                 - commercial_used
#             )

#             if residential_remaining < 0:
#                 residential_remaining = 0

#             if commercial_remaining < 0:
#                 commercial_remaining = 0

#             remaining_property = (
#                 residential_remaining
#                 + commercial_remaining
#             )

#     else:

#         # =================================================
#         # FREE USER
#         # =================================================

#         remaining_property = (
#             FREE_PROPERTY_LIMIT
#             - total_properties
#         )

#         if remaining_property < 0:
#             remaining_property = 0

#         # =================================================
#         # FREE USER CAN ADD ANY TYPE
#         # =================================================

#         residential_remaining = remaining_property
#         commercial_remaining = remaining_property

#     # =====================================================
#     # RESPONSE
#     # =====================================================

#     return {

#         "remaining_property":
#         remaining_property,

#         "residential_remaining":
#         residential_remaining,

#         "commercial_remaining":
#         commercial_remaining,

#         "total_properties":
#         total_properties,

#         "free_property_ids":
#         free_property_ids,

#         "residential_used":
#         residential_used,

#         "commercial_used":
#         commercial_used,

#         "total_residential_limit":
#         total_residential_limit,

#         "total_commercial_limit":
#         total_commercial_limit,
#     }