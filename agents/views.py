import json
from django.shortcuts import render, redirect, get_object_or_404, redirect
from . models import *
from developer .models import *

from . forms import *
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
# import requests
# from geopy.distance import geodesic
from users .views import*
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.http import require_POST
import tempfile
from selenium import webdriver
from users.utils import capture_property_screenshot


def agent_messages(request):
    # Check if agent is logged in
    premium_id = request.session.get("premium_user_id")
    if not premium_id:
        return redirect("agentslogin")

    try:
        agent = Premium.objects.get(id=premium_id)
    except Premium.DoesNotExist:
        messages.error(request, "Session expired. Please log in again.")
        return redirect("agentslogin")

    # Get messages matching the agent's pin code
    matching_messages = Inbox.objects.filter(pin_code=agent.pincode, is_removed=False)

    # Mark messages as read
    matching_messages.update(is_read=True)

    return render(request, "agent_messagebox.html", {
        "agent": agent,
        "messages": matching_messages
    })


def delete_inbox_message(request, message_id):
    # Ensure agent is logged in
    premium_id = request.session.get("premium_user_id")
    if not premium_id:
        return redirect("agentslogin")

    # Get agent and message
    agent = get_object_or_404(Premium, id=premium_id)
    message = get_object_or_404(Inbox, id=message_id)

    # Only allow deletion if the message matches agent's pin code
    if message.pin_code == agent.pincode:
        message.is_removed = True
        message.save()
        messages.success(request, "Message deleted successfully ✅")
    else:
        messages.error(request, "You cannot delete this message.")

    return redirect("agent_messages")



# def base1(request):
#     if "name" not in request.session:
#         return redirect('login')  # Redirect to login if session is not found
#
#     username = request.session["name"]
#     try:
#         agent = UserProfile.objects.get(login__username=username)
#     except UserProfile.DoesNotExist:
#         return redirect('login')  # Redirect if no agent profile exists
#
#     # Count unread messages (assuming 'is_read' is a boolean field in your Inbox model)
#     unread_messages_count = Inbox.objects.filter(is_read=False).count()  # Count unread messages
#
#     return render(
#         request,
#         'base1.html',
#         {'username': username, 'agent': agent, 'unread_messages_count': unread_messages_count}
#     )

# def remove_message(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         message_id = data.get('message_id')
#         print(message_id,'messageid')

#         try:
#             message = Inbox.objects.get(id=message_id)
#             message.is_removed = True
#             message.save()  # Save the removed status to the database
#             print(message,'messageeee')
#             return JsonResponse({'status': 'success'}, status=200)
#         except Inbox.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Message not found'}, status=404)

#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def delete_message(request, message_id):
    # Only allow deletion if the method is POST
    if request.method == 'POST':
        # Get the message to delete
        message = get_object_or_404(Inbox, id=message_id)
        
        # Delete the message from the database
        message.delete()
        
        # Redirect to the previous page or wherever you need
        return redirect('check_pin_code_messages')  # Replace 'message_list' with the appropriate view name

    # If not POST, redirect or return an error (you could use a 405 Method Not Allowed)
    return redirect('check_pin_code_messages')  # Ad



def premium_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        try:
            premium_user = Premium.objects.get(username__iexact=username)

            # ✅ check hashed password
            if not check_password(password, premium_user.password):
                messages.error(request, "Invalid username or password.")
                return redirect("agentslogin")

            # ✅ check expiry
            if premium_user.is_expired():
                messages.error(request, "Your Premium account has expired.")
                return redirect("agentslogin")

            # ✅ store session
            request.session["premium_user_id"] = premium_user.id
            messages.success(request, f"Welcome {premium_user.name}!")
            return redirect("agent_dashboard")

        except Premium.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect("agentslogin")

    return render(request, "agentslogin.html")


def change_password(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        old_password = request.POST.get("old_password", "").strip()
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        try:
            premium_user = Premium.objects.get(username__iexact=username)

            # ✅ Check old password
            if not check_password(old_password, premium_user.password):
                messages.error(request, "Old password is incorrect.")
                return redirect("change_password")

            # ✅ Check new vs confirm
            if new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
                return redirect("change_password")

            # ✅ Prevent reusing old password
            if check_password(new_password, premium_user.password):
                messages.error(request, "New password cannot be the same as the old password.")
                return redirect("change_password")

            # ✅ Save hashed new password
            premium_user.password = make_password(new_password)
            premium_user.save()

            messages.success(request, "Password updated successfully. Please log in again.")
            return redirect("agentslogin")

        except Premium.DoesNotExist:
            messages.error(request, "Username not found.")
            return redirect("change_password")

    return render(request, "agentslogin.html")




def submit(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        Request.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        return redirect("request")
    return render(request, "submitform.html")






def agents_dashboard(request):
    premium_id = request.session.get("premium_user_id")
    if not premium_id:
        return redirect("agentslogin")

    try:
        user = Premium.objects.get(id=premium_id)
    except Premium.DoesNotExist:
        messages.error(request, "Session expired. Please log in again.")
        return redirect("agentslogin")

    if request.method == "POST":
        # Collect updated data from form
        user.name = request.POST.get("name")
        user.speacialised = request.POST.get("speacialised")
        user.phone = request.POST.get("phone")
        user.whatsapp = request.POST.get("whatsapp")
        user.email = request.POST.get("email")
        user.location = request.POST.get("location")
        user.city = request.POST.get("city")

        if "image" in request.FILES:
            user.image = request.FILES["image"]

        user.save()
        messages.success(request, "Profile updated successfully ✅")
        return redirect("agent_dashboard")

    return render(request, "agent_dashboard.html", {"agent": user})

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Premium, AgentProperty, AgentPropertyImage, Category, Purpose

#
# def agents_add_property(request):
#     premium_id = request.session.get("premium_user_id")
#     if not premium_id:
#         return redirect("agentslogin")  # force login
#
#     agent = get_object_or_404(Premium, id=premium_id)
#     categories = Category.objects.all()
#     purposes = Purpose.objects.all()
#     properties = agent.properties.all()  # ✅ uses related_name
#
#     if request.method == "POST":
#         category_id = request.POST.get("category")
#         purpose_id = request.POST.get("purpose")
#
#         amenities = request.POST.getlist("amenities")
#         amenities_str = ", ".join([a.strip() for a in amenities if a.strip()])
#
#         uploaded_images = request.FILES.getlist("images")
#         main_image = uploaded_images[0] if uploaded_images else None
#
#         # ✅ Auto-assign to logged-in Premium agent
#         property_obj = AgentProperty.objects.create(
#             agent=agent,
#             category_id=category_id,
#             purpose_id=purpose_id,
#             label=request.POST.get("label"),
#             land_area=request.POST.get("land_area"),
#             sq_ft=request.POST.get("sq_ft"),
#             description=request.POST.get("description"),
#             amenities=amenities_str,
#             image=main_image,
#             perprice=request.POST.get("perprice"),
#             price=request.POST.get("price"),
#             whatsapp=request.POST.get("whatsapp"),
#             phone=request.POST.get("phone"),
#             location=request.POST.get("location"),
#             city=request.POST.get("city"),
#             pincode=request.POST.get("pincode"),
#             district=request.POST.get("district"),
#             land_mark=request.POST.get("land_mark"),
#         )
#
#         # ✅ Save extra images
#         for extra_img in uploaded_images[1:]:
#             AgentPropertyImage.objects.create(property=property_obj, image=extra_img)
#
#         messages.success(request, "Property added successfully ✅")
#         return redirect("agent_add_property")
#
#     return render(request, "agent_propertylistings.html", {
#         "categories": categories,
#         "purposes": purposes,
#         "properties": properties,
#     })
#
#
# @require_POST
# def agent_edit_property(request, property_id):
#     premium_id = request.session.get("premium_user_id")
#     if not premium_id:
#         return redirect("agentslogin")
#
#     agent = get_object_or_404(Premium, id=premium_id)
#     prop = get_object_or_404(AgentProperty, id=property_id, agent=agent)
#
#     category_id = request.POST.get("category")
#     purpose_id = request.POST.get("purpose")
#
#     # --- Update property fields ---
#     prop.label = request.POST.get('label')
#     prop.land_area = request.POST.get("land_area")
#     prop.sq_ft = request.POST.get("sq_ft")
#     prop.description = request.POST.get("description")
#
#     # ✅ Use the hidden field (already comma-joined in JS)
#     prop.amenities = request.POST.get("amenities", "")
#
#     prop.perprice = request.POST.get("perprice")
#     prop.price = request.POST.get("price")
#     prop.whatsapp = request.POST.get("whatsapp")
#     prop.phone = request.POST.get("phone")
#     prop.location = request.POST.get("location")
#     prop.city = request.POST.get("city")
#     prop.pincode = request.POST.get("pincode")
#     prop.district = request.POST.get("district")
#     prop.land_mark = request.POST.get("land_mark")
#
#     if category_id:
#         prop.category_id = category_id
#     if purpose_id:
#         prop.purpose_id = purpose_id
#
#     prop.save()
#
#     # ✅ Add new images
#     for img in request.FILES.getlist("images"):
#         AgentPropertyImage.objects.create(property=prop, image=img)
#
#     # ✅ Delete selected images
#     delete_images = request.POST.getlist("delete_images")
#     if delete_images:
#         AgentPropertyImage.objects.filter(id__in=delete_images, property=prop).delete()
#
#     messages.success(request, "Property updated successfully ✅")
#     return redirect('agent_add_property')
#
# @require_POST
# def agent_delete_property(request, pk):
#     premium_id = request.session.get("premium_user_id")
#     if not premium_id:
#         return redirect("agentslogin")
#
#     agent = get_object_or_404(Premium, id=premium_id)
#     prop = get_object_or_404(AgentProperty, pk=pk, agent=agent)
#     prop.delete()
#
#     messages.success(request, "Property deleted ✅")
#     return redirect('agent_add_property')


def agents_add_property(request):
    """Display property list and handle adding a new property for the logged-in agent."""
    premium_id = request.session.get("premium_user_id")
    if not premium_id:
        return redirect("agentslogin")

    agent = get_object_or_404(Premium, id=premium_id)
    categories = Category.objects.all()
    purposes = Purpose.objects.all()
    properties = agent.properties.all()

    if request.method == "POST":
        category_id = request.POST.get("category")
        purpose_id = request.POST.get("purpose")

        amenities = request.POST.getlist("amenities")
        amenities_str = ", ".join([a.strip() for a in amenities if a.strip()])

        uploaded_images = request.FILES.getlist("images")
        main_image = uploaded_images[0] if uploaded_images else None

        # Create property
        property_obj = AgentProperty.objects.create(
            agent=agent,
            category_id=category_id,
            purpose_id=purpose_id,
            label=request.POST.get("label"),
            land_area=request.POST.get("land_area"),
            sq_ft=request.POST.get("sq_ft"),
            description=request.POST.get("description"),
            amenities=amenities_str,
            image=main_image,
            perprice=request.POST.get("perprice"),
            price=request.POST.get("price"),
            whatsapp=request.POST.get("whatsapp"),
            phone=request.POST.get("phone"),
            location=request.POST.get("location"),
            city=request.POST.get("city"),
            pincode=request.POST.get("pincode"),
            district=request.POST.get("district"),
            land_mark=request.POST.get("land_mark"),
        )

        # Save extra images
        for extra_img in uploaded_images[1:]:
            AgentPropertyImage.objects.create(property=property_obj, image=extra_img)

        # Capture screenshot for sharing
        screenshot_url = capture_property_screenshot(property_obj)
        if screenshot_url:
            property_obj.screenshot = screenshot_url
            property_obj.save()

        messages.success(request, "Property added successfully ✅")
        return redirect("agent_add_property")

    return render(request, "agent_propertylistings.html", {
        "categories": categories,
        "purposes": purposes,
        "properties": properties,
    })


@require_POST
def agent_edit_property(request, property_id):
    """Edit an existing property for the logged-in agent."""
    premium_id = request.session.get("premium_user_id")
    if not premium_id:
        return redirect("agentslogin")

    agent = get_object_or_404(Premium, id=premium_id)
    prop = get_object_or_404(AgentProperty, id=property_id, agent=agent)

    category_id = request.POST.get("category")
    purpose_id = request.POST.get("purpose")

    prop.label = request.POST.get('label')
    prop.land_area = request.POST.get("land_area")
    prop.sq_ft = request.POST.get("sq_ft")
    prop.description = request.POST.get("description")
    prop.amenities = request.POST.get("amenities", "")
    prop.perprice = request.POST.get("perprice")
    prop.price = request.POST.get("price")
    prop.whatsapp = request.POST.get("whatsapp")
    prop.phone = request.POST.get("phone")
    prop.location = request.POST.get("location")
    prop.city = request.POST.get("city")
    prop.pincode = request.POST.get("pincode")
    prop.district = request.POST.get("district")
    prop.land_mark = request.POST.get("land_mark")

    if category_id:
        prop.category_id = category_id
    if purpose_id:
        prop.purpose_id = purpose_id

    prop.save()

    # Add new images
    for img in request.FILES.getlist("images"):
        AgentPropertyImage.objects.create(property=prop, image=img)

    # Delete selected images
    delete_images = request.POST.getlist("delete_images")
    if delete_images:
        AgentPropertyImage.objects.filter(id__in=delete_images, property=prop).delete()

    # Update screenshot
    screenshot_url = capture_property_screenshot(prop)
    if screenshot_url:
        prop.screenshot = screenshot_url
        prop.save()

    messages.success(request, "Property updated successfully ✅")
    return redirect('agent_add_property')


@require_POST
def agent_delete_property(request, pk):
    """Delete a property for the logged-in agent."""
    premium_id = request.session.get("premium_user_id")
    if not premium_id:
        return redirect("agentslogin")

    agent = get_object_or_404(Premium, id=premium_id)
    prop = get_object_or_404(AgentProperty, pk=pk, agent=agent)
    prop.delete()

    messages.success(request, "Property deleted ✅")
    return redirect('agent_add_property')



@require_POST
def agent_delete_property(request, pk):
    prop = get_object_or_404(AgentProperty, pk=pk)
    prop.delete()
    return redirect('agent_add_property')


# Show all contact requests
def contact_requests_list(request):
    contacts = ContactRequest.objects.all().order_by("-created_at")
    return render(request, "agent_enquiry.html", {"contacts": contacts})

# Delete a specific contact request
def delete_contact_request(request, pk):
    contact = get_object_or_404(ContactRequest, pk=pk)
    contact.delete()
    messages.success(request, "❌ Contact request deleted successfully.")
    return redirect("contact_requests_list")


