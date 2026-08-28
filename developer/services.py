from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from developer.models import (
    Property,
    PropertyFeature,
    PropertyImage,
    ExpiredProperty,
)


def get_restore_duration_days(subscription):
    """
    Calculate the duration for a restored property.

    Priority:
        1. Remaining subscription duration
        2. Plan validity
        3. 30 days fallback
    """

    import re

    now = timezone.now()

    # ----------------------------------------------------------
    # Existing subscription expiry
    # ----------------------------------------------------------

    if subscription.expiry_date:

        remaining_seconds = (
            subscription.expiry_date - now
        ).total_seconds()

        if remaining_seconds > 0:

            remaining_days = int(
                remaining_seconds / 86400
            )

            return max(
                remaining_days,
                1
            )

    # ----------------------------------------------------------
    # Plan validity fallback
    # ----------------------------------------------------------

    plan = subscription.plan

    validity = getattr(
        plan,
        "validity",
        None
    )

    if validity:

        numbers = re.findall(
            r"\d+",
            str(validity)
        )

        if numbers:

            return max(
                int(numbers[0]),
                1
            )

    # ----------------------------------------------------------
    # Final fallback
    # ----------------------------------------------------------

    return 30


@transaction.atomic
def restore_one_expired_property(
    expired_property,
    subscription
):
    """
    Convert one ExpiredProperty back into Property.
    """

    # ----------------------------------------------------------
    # Lock the expired property
    # ----------------------------------------------------------

    expired_property = (
        ExpiredProperty.objects
        .select_for_update()
        .select_related(
            "category",
            "subcategory",
            "purpose",
            "user",
            "package",
            "subscription",
            "single_property_package",
        )
        .prefetch_related(
            "amenities",
            "property_features__field",
            "images",
        )
        .get(
            pk=expired_property.pk
        )
    )

    # ----------------------------------------------------------
    # Safety check
    # ----------------------------------------------------------

    if (
        expired_property.user_id
        !=
        subscription.user_id
    ):

        raise ValueError(
            "Expired property does not belong "
            "to the subscription user."
        )

    # ----------------------------------------------------------
    # Prevent duplicate active property
    # ----------------------------------------------------------

    existing_property = (
        Property.objects
        .filter(
            property_code=
                expired_property.property_code
        )
        .first()
    )

    if existing_property:

        # It is already active.

        expired_property.delete()

        return existing_property

    # ----------------------------------------------------------
    # Calculate new property duration
    # ----------------------------------------------------------

    duration_days = (
        get_restore_duration_days(
            subscription
        )
    )

    now = timezone.now()

    expiry_date = (
        now +
        timedelta(
            days=duration_days
        )
    )

    # ----------------------------------------------------------
    # Create active property
    # ----------------------------------------------------------

    active_property = Property.objects.create(

        category=expired_property.category,

        subcategory=expired_property.subcategory,

        purpose=expired_property.purpose,

        property_code=expired_property.property_code,

        label=expired_property.label,

        land_area=expired_property.land_area,

        sq_ft=expired_property.sq_ft,

        description=expired_property.description,

        image=expired_property.image,

        screenshot=expired_property.screenshot,

        perprice=expired_property.perprice,

        price=expired_property.price,

        deposit=expired_property.deposit,

        user=expired_property.user,

        owner=expired_property.owner,

        package=expired_property.package,

        # ----------------------------------------------
        # IMPORTANT
        # ----------------------------------------------

        subscription=subscription,

        single_property_package=(
            expired_property.single_property_package
        ),

        single_property_edit_limit=(
            expired_property.single_property_edit_limit
        ),

        single_property_edit_used=(
            expired_property.single_property_edit_used
        ),

        whatsapp=expired_property.whatsapp,

        phone=expired_property.phone,

        location=expired_property.location,

        city=expired_property.city,

        district=expired_property.district,

        taluk=expired_property.taluk,

        village=expired_property.village,

        state=expired_property.state,

        pincode=expired_property.pincode,

        land_mark=expired_property.land_mark,

        selling_points=expired_property.selling_points,

        paid=expired_property.paid,

        added_by=expired_property.added_by,

        market_staff=expired_property.market_staff,

        message=expired_property.message,

        note=expired_property.note,

        is_featured=expired_property.is_featured,

        created_at=expired_property.created_at,

        duration_days=duration_days,

        expiry_date=expiry_date,
    )

    # ----------------------------------------------------------
    # Property.save() already contains existing project logic.
    #
    # Explicitly enforce the restored subscription values after
    # creation so they cannot be overwritten by existing logic.
    # ----------------------------------------------------------

    Property.objects.filter(
        pk=active_property.pk
    ).update(
        subscription=subscription,
        duration_days=duration_days,
        expiry_date=expiry_date,
    )

    # ----------------------------------------------------------
    # Amenities
    # ----------------------------------------------------------

    active_property.amenities.set(
        expired_property.amenities.all()
    )

    # ----------------------------------------------------------
    # Dynamic features
    # ----------------------------------------------------------

    for feature in (
        expired_property.property_features.all()
    ):

        PropertyFeature.objects.create(

            property=active_property,

            field=feature.field,

            value=feature.value,

            icon=feature.icon,
        )

    # ----------------------------------------------------------
    # Images
    # ----------------------------------------------------------

    for image in expired_property.images.all():

        PropertyImage.objects.create(

            property=active_property,

            image=image.image,
        )

    # ----------------------------------------------------------
    # Delete expired copy
    # ----------------------------------------------------------

    expired_property.delete()

    return active_property


@transaction.atomic
def restore_user_expired_properties(
    subscription
):
    """
    Restore every expired property belonging to the user
    of this UserPlanSubscription.
    """

    # ----------------------------------------------------------
    # Subscription must be active
    # ----------------------------------------------------------

    if not subscription.is_active:

        return {
            "restored": 0,
            "skipped": 0,
        }

    # ----------------------------------------------------------
    # Check subscription expiry
    # ----------------------------------------------------------

    if (
        subscription.expiry_date
        and
        subscription.expiry_date <= timezone.now()
    ):

        return {
            "restored": 0,
            "skipped": 0,
        }

    # ----------------------------------------------------------
    # Find user's expired properties
    # ----------------------------------------------------------

    expired_properties = (
        ExpiredProperty.objects
        .filter(
            user_id=subscription.user_id
        )
        .prefetch_related(
            "amenities",
            "property_features__field",
            "images",
        )
        .order_by(
            "created_at"
        )
    )

    restored_count = 0
    skipped_count = 0

    # ----------------------------------------------------------
    # Restore each property
    # ----------------------------------------------------------

    for expired_property in expired_properties:

        try:

            restore_one_expired_property(
                expired_property=
                    expired_property,
                subscription=
                    subscription,
            )

            restored_count += 1

        except ExpiredProperty.DoesNotExist:

            skipped_count += 1

    return {
        "restored": restored_count,
        "skipped": skipped_count,
    }