import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.conf import settings
import cloudinary.uploader
import os
from agents.models import AgentProperty
import re
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.utils import timezone
from hashids import Hashids
import razorpay
import jwt
from datetime import datetime, timedelta
import logging
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










logger = logging.getLogger(__name__)


def send_otp_email(to_email, otp):

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.BREVO_API_KEY

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

        <small>If you didn't request this, please ignore this email.</small>
    </div>
    """

    send_email = sib_api_v3_sdk.SendSmtpEmail(
        sender={
            "email": settings.DEFAULT_FROM_EMAIL,
            "name": "BuySel",
        },
        to=[
            {
                "email": to_email,
            }
        ],
        subject=subject,
        html_content=html_content,
    )

    try:
        response = api_instance.send_transac_email(send_email)
        logger.info("Brevo Email Sent: %s", response)
        return True

    except ApiException as e:
        logger.error("Brevo API Error: %s", e)
        return False

    except Exception as e:
        logger.exception("Unexpected Email Error: %s", e)
        return False










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









client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)








FREE_PROPERTY_LIMIT = 2

def get_available_subscription(user, category_name):

    subscriptions = (
        UserPlanSubscription.objects
        .filter(
            user=user,
            is_active=True,
            expiry_date__gt=timezone.now()
        )
        .select_related("plan")
        .order_by("purchased_at")
    )

    category_name = category_name.lower().strip()

    for subscription in subscriptions:

        listing_type = subscription.plan.listing_type.lower()

        residential_match = re.search(
            r"(\d+)\s*residential",
            listing_type
        )

        commercial_match = re.search(
            r"(\d+)\s*commercial",
            listing_type
        )

        residential_limit = (
            int(residential_match.group(1))
            if residential_match else 0
        )

        commercial_limit = (
            int(commercial_match.group(1))
            if commercial_match else 0
        )

        if category_name in ["residential", "plot/land"]:

            if (
                subscription.residential_property_used
                < residential_limit
            ):
                return subscription

        elif category_name in ["commercial", "industrial"]:

            if (
                subscription.commercial_property_used
                < commercial_limit
            ):
                return subscription

    return None

def get_available_edit_subscription(user):

    subscriptions = (
        UserPlanSubscription.objects
        .filter(
            user=user,
            is_active=True,
            expiry_date__gt=timezone.now()
        )
        .order_by("purchased_at")
    )

    for subscription in subscriptions:

        if subscription.has_no_edit:
            continue

        if subscription.is_unlimited_edit:
            return subscription

        if subscription.remaining_edit > 0:
            return subscription

    return None


def get_property_remaining_counts(user):

    # ==========================================================
    # USER PROPERTIES
    # ==========================================================

    user_properties = (
        Property.objects
        .filter(user=user)
        .order_by("created_at")
    )

    # IMPORTANT:
    # Do NOT use user_properties.count() for property usage.
    #
    # Property count represents currently existing properties.
    # If a property is deleted, this count decreases.
    #
    # UserProfile.total_property_used is the historical usage
    # counter and should NOT decrease when a property is deleted.

    profile = user.profile

    # ==========================================================
    # HISTORICAL PROPERTY USAGE
    # ==========================================================

    free_total_used = profile.total_property_used or 0
    free_residential_used = profile.residential_property_used or 0
    free_commercial_used = profile.commercial_property_used or 0

    # Property IDs are only for display/reference.
    free_property_ids = list(
        user_properties.values_list(
            "id",
            flat=True
        )[:FREE_PROPERTY_LIMIT]
    )

    # ==========================================================
    # ACTIVE SUBSCRIPTIONS
    # ==========================================================

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

    # ==========================================================
    # NO ACTIVE PLAN
    # ==========================================================

    if not subscriptions.exists():

        # Remaining free properties must be calculated from
        # UserProfile.total_property_used, NOT Property.objects.count().

        remaining = max(
            FREE_PROPERTY_LIMIT - free_total_used,
            0
        )

        # IMPORTANT:
        # property_listed/total_properties is historical usage.
        # It must NOT decrease when a Property is deleted.

        return {
            "remaining_property": remaining,

            "residential_remaining": max(
                FREE_PROPERTY_LIMIT - free_residential_used,
                0
            ),

            "commercial_remaining": max(
                FREE_PROPERTY_LIMIT - free_commercial_used,
                0
            ),

            "total_properties": free_total_used,

            # If your API uses property_listed,
            # this value should be mapped to total_properties.
            "property_listed": free_total_used,

            "free_property_ids": free_property_ids,

            "residential_used": free_residential_used,
            "commercial_used": free_commercial_used,

            "total_residential_limit": FREE_PROPERTY_LIMIT,
            "total_commercial_limit": FREE_PROPERTY_LIMIT,
            "total_property_limit": FREE_PROPERTY_LIMIT,

            "has_active_plan": False,
            "active_subscription_count": 0,
        }

    # ==========================================================
    # ACTIVE PLAN EXISTS
    # ==========================================================

    residential_used = free_residential_used
    commercial_used = free_commercial_used

    residential_remaining = 0
    commercial_remaining = 0

    residential_limit = 0
    commercial_limit = 0

    # ==========================================================
    # SUBSCRIPTION USAGE
    # ==========================================================

    for subscription in subscriptions:

        listing_type = str(
            subscription.plan.listing_type or ""
        ).lower()

        sub_residential_used = (
            subscription.residential_property_used or 0
        )

        sub_commercial_used = (
            subscription.commercial_property_used or 0
        )

        # ------------------------------------------------------
        # GET PLAN LIMIT
        # ------------------------------------------------------

        sub_residential_limit = 0
        sub_commercial_limit = 0

        residential_match = re.search(
            r"(\d+)\s*residential",
            listing_type
        )

        commercial_match = re.search(
            r"(\d+)\s*commercial",
            listing_type
        )

        if residential_match:
            sub_residential_limit = int(
                residential_match.group(1)
            )

        if commercial_match:
            sub_commercial_limit = int(
                commercial_match.group(1)
            )

        residential_limit += sub_residential_limit
        commercial_limit += sub_commercial_limit

        # ------------------------------------------------------
        # USED COUNTS
        # ------------------------------------------------------

        residential_used += sub_residential_used
        commercial_used += sub_commercial_used

        # ------------------------------------------------------
        # REMAINING COUNTS
        # ------------------------------------------------------

        sub_residential_remaining = max(
            sub_residential_limit -
            sub_residential_used,
            0
        )

        sub_commercial_remaining = max(
            sub_commercial_limit -
            sub_commercial_used,
            0
        )

        residential_remaining += (
            sub_residential_remaining
        )

        commercial_remaining += (
            sub_commercial_remaining
        )

    # ==========================================================
    # FREE REMAINING
    # ==========================================================

    # IMPORTANT:
    # This uses UserProfile.total_property_used.
    #
    # If a property is deleted:
    #
    # Property.objects.count()  -> decreases
    #
    # profile.total_property_used -> stays the same
    #
    # Therefore remaining_property will NOT increase.

    free_remaining = max(
        FREE_PROPERTY_LIMIT - free_total_used,
        0
    )

    # ==========================================================
    # TOTAL REMAINING
    # ==========================================================

    remaining_property = (
        free_remaining
        + residential_remaining
        + commercial_remaining
    )

    # ==========================================================
    # HISTORICAL PROPERTY LISTED
    # ==========================================================

    # DO NOT use:
    #
    # total_properties = user_properties.count()
    #
    # because deletion will decrease it.
    #
    # Use the historical UserProfile counter instead.

    property_listed = free_total_used

    # ==========================================================
    # DEBUG
    # ==========================================================

    print("\n================ COUNT DEBUG ================")

    print(
        "Profile Total Property Used :",
        free_total_used
    )

    print(
        "Profile Residential Used :",
        free_residential_used
    )

    print(
        "Profile Commercial Used :",
        free_commercial_used
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
        "Free Remaining :",
        free_remaining
    )

    print(
        "Total Remaining :",
        remaining_property
    )

    print(
        "Property Listed :",
        property_listed
    )

    print(
        "Active Subscriptions :",
        subscriptions.count()
    )

    print("============================================")

    # ==========================================================
    # RESPONSE
    # ==========================================================

    return {
        "remaining_property": remaining_property,

        "residential_remaining": residential_remaining,

        "commercial_remaining": commercial_remaining,

        # Historical count.
        # This will NOT decrease when Property is deleted.
        "total_properties": property_listed,

        "property_listed": property_listed,

        "free_property_ids": free_property_ids,

        "residential_used": residential_used,

        "commercial_used": commercial_used,

        "total_residential_limit": residential_limit,

        "total_commercial_limit": commercial_limit,

        "total_property_limit": (
            residential_limit +
            commercial_limit
        ),

        "has_active_plan": True,

        "active_subscription_count": subscriptions.count(),
    }


def get_edit_remaining_count(user):

    profile = user.profile

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
        "remaining_edit": max(total_limit - total_used, 0),
        "has_unlimited_edit": False
    }
