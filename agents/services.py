from django.db import transaction
from django.utils import timezone

from .models import (
    AgentProperty,
    AgentPropertyFieldValue,
    AgentPropertyImage,
    AgentPropertySellingPoint,
    AgentPropertyLandmark,

    ExpiredAgentProperty,
    ExpiredAgentPropertyFieldValue,
    ExpiredAgentPropertyImage,
    ExpiredAgentPropertySellingPoint,
    ExpiredAgentPropertyLandmark,
)


@transaction.atomic
def restore_expired_properties_for_agent(
    agent,
    subscription
):
    """
    Restore ALL expired properties of an agent
    back into AgentProperty.

    IMPORTANT:
    ---------------------------------------------------------
    1. Only called for an ACTIVE subscription.
    2. Does NOT increase Subscription.used_listings.
    3. Does NOT consume a new property slot.
    4. Copies all property-related data.
    5. Keeps the original property UUID.
    6. Deletes the expired copy only after successful restore.
    """

    # =========================================================
    # VALIDATE AGENT
    # =========================================================

    if not agent:

        return {
            "success": False,
            "restored": 0,
            "message": "Agent is required."
        }

    # =========================================================
    # VALIDATE SUBSCRIPTION
    # =========================================================

    if not subscription:

        return {
            "success": False,
            "restored": 0,
            "message": "Subscription is required."
        }

    # =========================================================
    # MAKE SURE SUBSCRIPTION BELONGS TO THIS AGENT
    # =========================================================

    if subscription.agent_id != agent.id:

        return {
            "success": False,
            "restored": 0,
            "message": "Subscription does not belong to this agent."
        }

    # =========================================================
    # CHECK ACTIVE SUBSCRIPTION
    # =========================================================

    today = timezone.now().date()

    if not subscription.is_active:

        return {
            "success": False,
            "restored": 0,
            "message": "Subscription is not active."
        }

    if subscription.start_date > today:

        return {
            "success": False,
            "restored": 0,
            "message": "Subscription has not started yet."
        }

    if subscription.end_date < today:

        return {
            "success": False,
            "restored": 0,
            "message": "Subscription has expired."
        }

    # =========================================================
    # SAVE CURRENT AGENT PROPERTY COUNTER
    #
    # AgentProperty.save() currently increases:
    #
    # agent.properties_listed += 1
    #
    # when a property is created.
    #
    # Restored properties are NOT new listings.
    # So we preserve the original counter.
    # =========================================================

    original_properties_listed = (
        agent.properties_listed
    )

    # =========================================================
    # GET ALL EXPIRED PROPERTIES FOR THIS AGENT
    # =========================================================

    expired_properties = list(

        ExpiredAgentProperty.objects
        .filter(
            agent=agent
        )
        .select_related(
            "agent",
            "category",
            "subcategory",
            "purpose",
            "subscription",
        )
        .prefetch_related(
            "amenities",
            "field_values",
            "images",
            "selling_points",
            "landmarks",
        )
        .order_by("created_at")
    )

    # =========================================================
    # NOTHING TO RESTORE
    # =========================================================

    if not expired_properties:

        return {
            "success": True,
            "restored": 0,
            "message": "No expired properties found."
        }

    restored_count = 0

    skipped_count = 0

    # =========================================================
    # RESTORE EACH PROPERTY
    # =========================================================

    for expired_property in expired_properties:

        # =====================================================
        # ORIGINAL UUID
        #
        # Your move_to_expired() stores:
        #
        # ExpiredAgentProperty.id = AgentProperty.id
        #
        # So we can restore the same UUID.
        # =====================================================

        property_id = expired_property.id

        # =====================================================
        # CHECK IF ALREADY EXISTS IN ACTIVE TABLE
        # =====================================================

        active_property = (
            AgentProperty.objects
            .filter(
                pk=property_id
            )
            .first()
        )

        if active_property:

            # -------------------------------------------------
            # Property is already active.
            #
            # We don't create duplicate AgentProperty.
            # Remove stale expired copy.
            # -------------------------------------------------

            expired_property.delete()

            skipped_count += 1

            continue

        # =====================================================
        # CREATE ACTIVE PROPERTY
        # =====================================================

        active_property = AgentProperty.objects.create(

            # Preserve original UUID
            id=expired_property.id,

            agent=expired_property.agent,

            property_hash_id=(
                expired_property.property_hash_id
            ),

            category=expired_property.category,

            subcategory=expired_property.subcategory,

            purpose=expired_property.purpose,

            label=expired_property.label,

            land_area=expired_property.land_area,

            sq_ft=expired_property.sq_ft,

            description=expired_property.description,

            image=expired_property.image,

            screenshot=expired_property.screenshot,

            perprice=expired_property.perprice,

            price=expired_property.price,

            deposit=expired_property.deposit,

            whatsapp=expired_property.whatsapp,

            phone=expired_property.phone,

            location=expired_property.location,

            city=expired_property.city,

            pincode=expired_property.pincode,

            district=expired_property.district,

            land_mark=expired_property.land_mark,

            owner=expired_property.owner,

            taluk=expired_property.taluk,

            village=expired_property.village,

            state=expired_property.state,

            paid=expired_property.paid,

            is_featured=expired_property.is_featured,

            notes=expired_property.notes,

            # -------------------------------------------------
            # IMPORTANT
            #
            # Attach the NEW active subscription.
            # -------------------------------------------------

            subscription=subscription,

            # -------------------------------------------------
            # Keep duration at 0.
            #
            # Active subscription protects the property.
            # -------------------------------------------------

            duration_days=0,
        )

        # =====================================================
        # AMENITIES
        # =====================================================

        amenities = list(
            expired_property.amenities.all()
        )

        if amenities:

            active_property.amenities.set(
                amenities
            )

        # =====================================================
        # DYNAMIC FIELDS
        # =====================================================

        dynamic_field_objects = []

        for expired_field in (
            expired_property.field_values.all()
        ):

            dynamic_field_objects.append(

                AgentPropertyFieldValue(

                    property=active_property,

                    field=expired_field.field,

                    value=expired_field.value,
                )
            )

        if dynamic_field_objects:

            AgentPropertyFieldValue.objects.bulk_create(
                dynamic_field_objects
            )

        # =====================================================
        # IMAGES
        # =====================================================

        image_objects = []

        for expired_image in (
            expired_property.images.all()
        ):

            image_objects.append(

                AgentPropertyImage(

                    property=active_property,

                    image=expired_image.image,
                )
            )

        if image_objects:

            AgentPropertyImage.objects.bulk_create(
                image_objects
            )

        # =====================================================
        # SELLING POINTS
        # =====================================================

        selling_point_objects = []

        for expired_point in (
            expired_property.selling_points.all()
        ):

            selling_point_objects.append(

                AgentPropertySellingPoint(

                    property=active_property,

                    point=expired_point.point,
                )
            )

        if selling_point_objects:

            AgentPropertySellingPoint.objects.bulk_create(
                selling_point_objects
            )

        # =====================================================
        # LANDMARKS
        # =====================================================

        landmark_objects = []

        for expired_landmark in (
            expired_property.landmarks.all()
        ):

            landmark_objects.append(

                AgentPropertyLandmark(

                    property=active_property,

                    name=expired_landmark.name,

                    distance=expired_landmark.distance,
                )
            )

        if landmark_objects:

            AgentPropertyLandmark.objects.bulk_create(
                landmark_objects
            )

        # =====================================================
        # DELETE EXPIRED COPY
        #
        # Only reached after ALL data was copied successfully.
        # =====================================================

        expired_property.delete()

        restored_count += 1

    # =========================================================
    # RESTORED PROPERTIES ARE NOT NEW LISTINGS
    #
    # AgentProperty.save() increments properties_listed.
    #
    # Restore the old value.
    # =========================================================

    agent.properties_listed = (
        original_properties_listed
    )

    agent.save(
        update_fields=[
            "properties_listed"
        ]
    )

    # =========================================================
    # VERY IMPORTANT
    #
    # DO NOT CHANGE:
    #
    # subscription.used_listings
    #
    # These are restored properties.
    # They are NOT new subscription listings.
    # =========================================================

    return {
        "success": True,

        "restored": restored_count,

        "skipped": skipped_count,

        "message": (
            f"{restored_count} expired properties "
            f"restored successfully."
        )
    }