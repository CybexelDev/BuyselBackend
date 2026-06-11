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
from django.db.models import Q

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

from django.db.models import Q
from django.utils import timezone


FREE_PROPERTY_LIMIT = 2


def get_property_remaining_counts(user):

    user_properties = (
        Property.objects
        .filter(user=user)
        .order_by("created_at")
    )

    total_properties = user_properties.count()

    free_property_ids = list(
        user_properties.values_list(
            "id",
            flat=True
        )[:FREE_PROPERTY_LIMIT]
    )

    subscriptions = (
        UserPlanSubscription.objects
        .filter(
            user=user,
            is_active=True,
            expiry_date__gt=timezone.now()
        )
        .select_related("plan")
        .order_by("-purchased_at")
    )

    if not subscriptions.exists():

        remaining = max(
            FREE_PROPERTY_LIMIT - total_properties,
            0
        )

        return {

            "remaining_property": remaining,

            "residential_remaining": remaining,

            "commercial_remaining": remaining,

            "total_properties": total_properties,

            "residential_used": total_properties,

            "commercial_used": total_properties,

            "has_active_plan": False,

            "active_subscription_count": 0,
        }

    # ===========================================
    # CURRENT ACTIVE SUBSCRIPTION
    # ===========================================

    current_subscription = subscriptions.first()

    # ===========================================
    # ONLY CURRENT SUBSCRIPTION PROPERTIES
    # ===========================================

    current_properties = Property.objects.filter(

        user=user,

        subscription=current_subscription

    )

    residential_used = current_properties.filter(

        Q(category__name__iexact="Residential") |
        Q(category__name__iexact="Plot/Land")

    ).count()

    commercial_used = current_properties.filter(

        Q(category__name__iexact="Commercial") |
        Q(category__name__iexact="Industrial")

    ).count()

    # ===========================================
    # CURRENT PLAN LIMIT ONLY
    # ===========================================

    listing_type = str(
        current_subscription.plan.listing_type
    ).lower()

    residential_limit = 0
    commercial_limit = 0

    residential_match = re.search(

        r"(\d+)\s*residential",

        listing_type

    )

    commercial_match = re.search(

        r"(\d+)\s*commercial",

        listing_type

    )

    if residential_match:

        residential_limit = int(

            residential_match.group(1)

        )

    if commercial_match:

        commercial_limit = int(

            commercial_match.group(1)

        )

    residential_remaining = max(

        residential_limit -

        residential_used,

        0

    )

    commercial_remaining = max(

        commercial_limit -

        commercial_used,

        0

    )

    remaining_property = (

        residential_remaining +

        commercial_remaining

    )

    # ===========================================
    # DEBUG
    # ===========================================

    print("\n================ COUNT DEBUG ================")

    print(

        "Current Subscription :",

        current_subscription.id

    )

    print(

        "Plan :",

        current_subscription.plan.name

    )

    print(

        "Residential Used :",

        residential_used

    )

    print(

        "Commercial Used :",

        commercial_used

    )

    print(

        "Residential Limit :",

        residential_limit

    )

    print(

        "Commercial Limit :",

        commercial_limit

    )

    print(

        "Residential Remaining :",

        residential_remaining

    )

    print(

        "Commercial Remaining :",

        commercial_remaining

    )

    print(

        "Total Remaining :",

        remaining_property

    )

    print("============================================")

    return {

        "remaining_property": remaining_property,

        "residential_remaining": residential_remaining,

        "commercial_remaining": commercial_remaining,

        "total_properties": total_properties,

        "free_property_ids": free_property_ids,

        "residential_used": residential_used,

        "commercial_used": commercial_used,

        "total_residential_limit": residential_limit,

        "total_commercial_limit": commercial_limit,

        "total_property_limit": residential_limit + commercial_limit,

        "has_active_plan": True,

        "active_subscription_count": subscriptions.count(),
    }

# import re

# from django.utils import timezone


# FREE_PROPERTY_LIMIT = 2


# def get_property_remaining_counts(user):

#     user_properties = (
#         Property.objects
#         .filter(user=user)
#         .order_by("created_at")
#     )

#     total_properties = user_properties.count()

#     # =====================================================
#     # FIRST 2 PROPERTIES ARE FREE
#     # =====================================================

#     free_property_ids = list(
#         user_properties.values_list(
#             "id",
#             flat=True
#         )[:FREE_PROPERTY_LIMIT]
#     )

#     # =====================================================
#     # ACTIVE SUBSCRIPTIONS
#     # =====================================================

#     subscriptions = (
#         UserPlanSubscription.objects
#         .filter(
#             user=user,
#             is_active=True,
#             expiry_date__gt=timezone.now()
#         )
#         .select_related("plan")
#     )

#     has_active_plan = subscriptions.exists()

#     # =====================================================
#     # FREE USER
#     # =====================================================

#     if not has_active_plan:

#         remaining_property = max(
#             FREE_PROPERTY_LIMIT -
#             total_properties,
#             0
#         )

#         return {

#             "remaining_property":
#             remaining_property,

#             "residential_remaining":
#             remaining_property,

#             "commercial_remaining":
#             remaining_property,

#             "total_properties":
#             total_properties,

#             "free_property_ids":
#             free_property_ids,

#             "residential_used":
#             total_properties,

#             "commercial_used":
#             total_properties,

#             "total_residential_limit":
#             FREE_PROPERTY_LIMIT,

#             "total_commercial_limit":
#             FREE_PROPERTY_LIMIT,

#             "total_property_limit":
#             FREE_PROPERTY_LIMIT,

#             "has_active_plan":
#             False,

#             "active_subscription_count":
#             0
#         }

#     # =====================================================
#     # PAID USER
#     # FIRST 2 FREE PROPERTIES DO NOT
#     # CONSUME PLAN LIMITS
#     # =====================================================

#     # paid_properties = user_properties.exclude(
#     #     id__in=free_property_ids
#     # )
#     active_subscription = (
#         UserPlanSubscription.objects
#         .filter(
#             user=user,
#             is_active=True,
#             expiry_date__gt=timezone.now()
#         )
#         .order_by("-purchased_at")
#         .first()
#     )

#     if active_subscription:

#         paid_properties = Property.objects.filter(
#             user=user,
#             subscription=active_subscription
#         )

#     else:

#         paid_properties = Property.objects.none()
#         print("\n========== COUNT DEBUG ==========")

#         print(
#             "Active Subscription :",
#             active_subscription.id if active_subscription else None
#         )

#         print(
#             "Paid Property Count :",
#             paid_properties.count()
#         )

#         for p in paid_properties:

#             print(
#                 p.id,
#                 p.category.name,
#                 p.subscription_id
#             )

#         print("=================================\n")

#     # residential_used = paid_properties.filter(
#     #     category__name__icontains="residential"
#     # ).count()

#     # commercial_used = paid_properties.filter(
#     #     category__name__icontains="commercial"
#     # ).count()
#     residential_used = paid_properties.filter(
#         Q(category__name__iexact="Residential") |
#         Q(category__name__iexact="Plot/Land")
#     ).count()

#     commercial_used = paid_properties.filter(
#         Q(category__name__iexact="Commercial") |
#         Q(category__name__iexact="Industrial")
#     ).count()

#     total_residential_limit = 0
#     total_commercial_limit = 0

#     # =====================================================
#     # ADD ALL ACTIVE PLAN LIMITS
#     # =====================================================

#     for sub in subscriptions:

#         listing_type = str(
#             getattr(
#                 sub.plan,
#                 "listing_type",
#                 ""
#             )
#         ).lower()

#         residential_match = re.search(
#             r"(\d+)\s*residential",
#             listing_type
#         )

#         commercial_match = re.search(
#             r"(\d+)\s*commercial",
#             listing_type
#         )

#         if residential_match:

#             total_residential_limit += int(
#                 residential_match.group(1)
#             )

#         if commercial_match:

#             total_commercial_limit += int(
#                 commercial_match.group(1)
#             )

#     # =====================================================
#     # REMAINING COUNTS
#     # =====================================================

#     residential_remaining = max(
#         total_residential_limit -
#         residential_used,
#         0
#     )

#     commercial_remaining = max(
#         total_commercial_limit -
#         commercial_used,
#         0
#     )

#     remaining_property = (
#         residential_remaining +
#         commercial_remaining
#     )

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

#         "total_property_limit":
#         (
#             total_residential_limit +
#             total_commercial_limit
#         ),

#         "has_active_plan":
#         True,

#         "active_subscription_count":
#         subscriptions.count()
#     }

# import re

# from django.utils import timezone


# FREE_PROPERTY_LIMIT = 2


# def get_property_remaining_counts(user):

#     profile = UserProfile.objects.filter(
#         user=user
#     ).first()

#     user_properties = (
#         Property.objects
#         .filter(user=user)
#         .order_by("created_at")
#     )

#     total_properties = user_properties.count()

#     # =====================================================
#     # DEFAULT VALUES
#     # =====================================================
#     residential_used = 0
#     commercial_used = 0

#     residential_remaining = 0
#     commercial_remaining = 0

#     # =====================================================
#     # FIRST 2 PROPERTIES ARE FREE
#     # =====================================================

#     free_property_ids = list(
#         user_properties.values_list(
#             "id",
#             flat=True
#         )[:FREE_PROPERTY_LIMIT]
#     )

#     # =====================================================
#     # ACTIVE SUBSCRIPTIONS
#     # =====================================================

#     subscriptions = (
#         UserPlanSubscription.objects
#         .filter(
#             user=user,
#             is_active=True,
#             expiry_date__gt=timezone.now()
#         )
#         .select_related("plan")
#     )

#     has_active_plan = subscriptions.exists()

#     if has_active_plan:

#         total_property_limit = 0

#         total_residential_limit = 0

#         total_commercial_limit = 0

#     else:

#         total_property_limit = FREE_PROPERTY_LIMIT

#         total_residential_limit = FREE_PROPERTY_LIMIT

#         total_commercial_limit = FREE_PROPERTY_LIMIT

#     # =====================================================
#     # ADD ALL PLAN LIMITS
#     # =====================================================

#     if has_active_plan:

#         for sub in subscriptions:

#             plan = sub.plan

#             # ==========================================
#             # PROPERTY LIMIT
#             # ==========================================

#             try:

#                 property_limit = int(
#                     "".join(
#                         filter(
#                             str.isdigit,
#                             str(
#                                 plan.property_listing_limit
#                             )
#                         )
#                     ) or 0
#                 )

#             except Exception:

#                 property_limit = 0

#             total_property_limit += property_limit

#             # ==========================================
#             # LISTING TYPE
#             # Example:
#             # "6 Residential / 6 Commercial"
#             # ==========================================

#             listing_type = str(
#                 getattr(
#                     plan,
#                     "listing_type",
#                     ""
#                 )
#             ).lower()

#             residential_match = re.search(
#                 r"(\d+)\s*residential",
#                 listing_type
#             )

#             commercial_match = re.search(
#                 r"(\d+)\s*commercial",
#                 listing_type
#             )

#             if residential_match:

#                 total_residential_limit += int(
#                     residential_match.group(1)
#                 )

#             if commercial_match:

#                 total_commercial_limit += int(
#                     commercial_match.group(1)
#                 )

#     # =====================================================
#     # USED COUNTS
#     # FIRST 2 FREE PROPERTIES SHOULD NOT
#     # CONSUME PLAN LIMITS
#     # =====================================================

#     # =====================================================
#     # USED COUNTS
#     # =====================================================

#     if has_active_plan:

#         # Only paid properties consume plan limits
#         used_properties = user_properties.exclude(
#             id__in=free_property_ids
#         )

#     else:

#         # Free properties consume free limits
#         used_properties = user_properties

#     residential_used = used_properties.filter(
#         category__name__icontains="residential"
#     ).count()

#     commercial_used = used_properties.filter(
#         category__name__icontains="commercial"
#     ).count()

#     #Remaining count
#     remaining_property = max(
#         total_property_limit -
#         total_properties,
#         0
#     )

#     # =====================================================
#     # FREE USER
#     # =====================================================

#     if not has_active_plan:

#         residential_remaining = remaining_property

#         commercial_remaining = remaining_property

#     # =====================================================
#     # PAID USER
#     # =====================================================

#     else:

#         residential_remaining = max(
#             total_residential_limit -
#             residential_used,
#             0
#         )

#         commercial_remaining = max(
#             total_commercial_limit -
#             commercial_used,
#             0
#         )

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

#         "total_property_limit":
#         total_property_limit,

#         "has_active_plan":
#         has_active_plan,

#         "active_subscription_count":
#         subscriptions.count()
#     }

def get_edit_remaining_count(user):

    subscriptions = (
        UserPlanSubscription.objects
        .filter(
            user=user,
            is_active=True,
            expiry_date__gt=timezone.now()
        )
        .select_related("plan")
    )

    if not subscriptions.exists():

        return {
            "remaining_edit": 0,
            "has_unlimited_edit": False
        }

    total_limit = 0
    total_used = 0

    for sub in subscriptions:

        if sub.is_unlimited_edit:

            return {
                "remaining_edit": "Unlimited",
                "has_unlimited_edit": True
            }

        total_limit += sub.edit_limit_count or 0

        total_used += sub.edit_used

    return {

        "remaining_edit": max(
            total_limit - total_used,
            0
        ),

        "has_unlimited_edit": False
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