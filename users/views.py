from django.shortcuts import render,redirect
from developer.models import *
from agents.models import *
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import Http404
# import requests 
# from geopy.distance import geodesic
from . models import*
from agents.views import *
from math import radians, cos, sin, sqrt, atan2
# Create your views here.
from django.db.models import Min, Max
import uuid
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Sum
from django.db.models import Prefetch
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from cloudinary.uploader import upload
from django.utils import timezone
from django.http import FileResponse
import os
from django.conf import settings
import re
from developer.models import Premium
from django.core.validators import validate_email
from django.db.models import F
import tempfile
from selenium import webdriver
from urllib.parse import quote
from django.http import JsonResponse
from django.db.models import Q
from .utils import send_otp_email
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import NotAuthenticated
from .authentication import UserJWTAuthentication
from rest_framework import generics
from agents.utils import check_plan_notifications
from agents.utils import create_notification
from .utils import *
import json
import uuid
import base64
from django.core.cache import cache
from rest_framework.response import Response
import base64
import tempfile
import os
import cloudinary.uploader



def base(request):
    return render(request, 'base.html')


def base(request):
    return render(request, 'more.html')

def about(request):
    return render(request, 'about.html')




def more(request):
    return render(request,'more.html')



# def blog(request):
#     blogs = Blog.objects.all()
    
   
#     paginator = Paginator(blogs, 10) 
#     page_number = request.GET.get('page') 
#     page_obj = paginator.get_page(page_number)  

#     return render(request, 'blog.html', {'page_obj': page_obj})

def blog(request):
    blogs = Blog.objects.all().order_by('-date')  # show latest first

    paginator = Paginator(blogs, 9)  # ✅ show 9 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog.html', {'page_obj': page_obj})

# def detail_view(request, id):
#     context = {}

#     try:
#         house = House.objects.get(id=id)
#         context = {
#             'house': house, 
#             'is_house': True,
            
#         }
#     except House.DoesNotExist:
#         try:
#             land = Land.objects.get(id=id)
#             context = {
#                 'land': land,
#                 'is_land': True,
               
#             }
#         except Land.DoesNotExist:
#             try:
#                 commercial = Commercial.objects.get(id=id)
#                 context = {
#                     'commercial': commercial,
#                     'is_commercial': True,
                    
#                 }
#             except Commercial.DoesNotExist:
#                 context = {'error': 'Property not found.'}

#     return render(request, 'detail.html', context)




def validate_uuid(object_id):
    """
    Helper function to validate if the given object_id is a valid UUID.
    """
    try:
        return uuid.UUID(object_id)
    except ValueError:
        return None









def faq(request):
    return render(request,'faq.html')

def sitemap_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'users/templates/sitemap.xml')
    return FileResponse(open(file_path, 'rb'), content_type='application/xml')












# def agents_detail(request, model_name, object_id):
#     # Define the model classes for agent listings
#     model_classes = {
#         'agenthouse': AgentHouse,
#         'agentland': AgentLand,
#         'agentcommercial': AgentCommercial,
#         'agentoffplan': AgentOffPlan,
#     }

#     # Get the model class dynamically
#     model_class = model_classes.get(model_name.lower())

#     if not model_class:
#         raise Http404("Invalid model name")

#     # Fetch the object
#     obj = get_object_or_404(model_class, id=object_id)

#     # Fetch related images
#     images = obj.images.all() if hasattr(obj, 'images') else []

#     # Debugging: Print images in the console
#     print(f"Images for {model_name} (ID: {object_id}):")
#     for img in images:
#         print(f" - Image URL: {img.image.url}")  # Check if the images exist

#     return render(request, 'agent_detail.html', {'object': obj, 'images': images})





# def agent_form(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         address = request.POST['address']
#         phone_number = request.POST['phone_number']
#         dealings = request.POST['Dealings']
#         image = request.FILES['image']

#         # Create and save the new agent instance
#         agent = AgentForm(
#             name=name,
#             email=email,
#             address=address,
#             phone_number=phone_number,
#             Dealings=dealings,
#             image=image
#         )
        
#         try:
#             agent.save()
#             messages.success(request, "Agent created successfully!")
#             return redirect('index')  # Redirect to agent list page
#         except ValidationError as e:
#             messages.error(request, f"Error: {e}")
#             return render(request, 'agent_form.html')
    
#     return render(request, 'agent_form.html')
from .forms import AgentRegister
def agent_form(request):
    if request.method == 'POST':
        form = AgentRegister(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Agent registered successfully!'})
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})

    return render(request, 'agent_form.html')

# def property_form(request):
#     if request.method == 'POST':
#         # Get form data from the request
#         property_name = request.POST.get('property_name')
#         locations = request.POST.get('locations')
#         price = request.POST.get('price')
#         about_the_property = request.POST.get('about_the_property')
#         image = request.FILES.get('image')  # Get the uploaded image

#         if not property_name or not locations or not price or not about_the_property or not image:
#             messages.error(request, "All fields are required!")
#             return redirect('property_form')  # Redirect back to the form if data is missing

#         # Create a new Propertylist object and save it
#         property = Propertylist(
#             property_name=property_name,
#             locations=locations,
#             price=price,
#             about_the_property=about_the_property,
#             image=image
#         )
#         property.save()
        
#         messages.success(request, "Property has been created successfully.")
#         return redirect('index')  # Redirect to the property list view

#     return render(request, 'property_form.html')

from .forms import PropertyForm

def property_form(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return render(request, 'property_form.html')




from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from geopy.distance import geodesic
from django.shortcuts import render, redirect
from django.http import JsonResponse
from math import radians, sin, cos, sqrt, atan2
import re



# def index(request):
#     purposes = Purpose.objects.all()
#     properties = Property.objects.all()
#
#     if request.method == 'POST':
#         # ------------------- Inbox form -------------------
#         if "messages_text" in request.POST:
#             Inbox.objects.create(
#                 name=request.POST.get("name"),
#                 pin_code=request.POST.get("pin_code"),
#                 contact=request.POST.get("contact"),
#                 messages_text=request.POST.get("messages_text")
#             )
#             return redirect("index")
#
#         # ------------------- Agent form -------------------
#         elif "Dealings" in request.POST and "image" in request.FILES:
#             AgentForm.objects.create(
#                 name=request.POST.get("name"),
#                 email=request.POST.get("email"),
#                 address=request.POST.get("address"),
#                 phone_number=request.POST.get("phone_number"),
#                 Dealings=request.POST.get("Dealings"),
#                 image=request.FILES.get("image")
#             )
#             return redirect("index")
#
#         # ------------------- Property form -------------------
#         elif "about_the_property" in request.POST and "image" in request.FILES:
#             Propertylist.objects.create(
#                 categories=request.POST.get("categories"),
#                 purposes_id=request.POST.get("purposes"),
#                 label=request.POST.get("label"),
#                 land_area=request.POST.get("land_area"),
#                 sq_ft=request.POST.get("sq_ft"),
#                 about_the_property=request.POST.get("about_the_property"),
#                 amenities=request.POST.get("amenities"),
#                 image=request.FILES.get("image"),
#                 price=request.POST.get("price"),
#                 owner=request.POST.get("owner"),
#                 phone=request.POST.get("phone"),
#                 locations=request.POST.get("locations"),
#                 pin_code=request.POST.get("pin_code"),
#                 land_mark=request.POST.get("land_mark"),
#                 total_price=request.POST.get("total_price"),
#                 duration=request.POST.get("duration"),
#                 whatsapp=request.POST.get("whatsapp"),
#                 city=request.POST.get("city"),
#                 District=request.POST.get("District"),
#             )
#             return redirect("index")
#
#     return render(request, 'index.html', {
#         "purposes": purposes,
#         "properties": properties,
#     })
#
from urllib.parse import quote

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from urllib.parse import quote
import re

from .models import  *
from developer.models import  *

from urllib.parse import quote
import re
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

def index(request):
    purposes = Purpose.objects.all()
    categories = Category.objects.all()
    premium = Premium.objects.all()
    districts = Property.objects.values_list("district", flat=True).distinct()
    cities = Property.objects.values_list("city", flat=True).distinct()

    District = taluk = village = state = ""

    # Base queryset
    properties = Property.objects.all().order_by('-created_at')[:20]

    # ------------------- SEARCH -------------------
    query = request.GET.get("q", "").strip()
    if query:
        properties = Property.objects.filter(
            Q(label__icontains=query) |
            Q(description__icontains=query) |
            Q(city__icontains=query) |
            Q(district__icontains=query) |
            Q(category__name__icontains=query) |
            Q(purpose__name__icontains=query) |
            Q(state__icontains=query) |
            Q(city__icontains=query) |
            Q(price__icontains=query) |
            Q(location__icontains=query)
        ).order_by('-created_at')

    # ------------------- POST REQUESTS -------------------
    if request.method == 'POST':
        # --- Inbox form ---
        if "messages_text" in request.POST:
            name = request.POST.get("name", "").strip()
            pin_code = request.POST.get("pin_code", "").strip()
            contact = request.POST.get("contact", "").strip()
            messages_text = request.POST.get("messages_text", "").strip()

            link_pattern = re.compile(r"(https?:\/\/|www\.)", re.IGNORECASE)
            if (link_pattern.search(name) or link_pattern.search(contact) or
                link_pattern.search(pin_code) or link_pattern.search(messages_text)):
                return JsonResponse({"success": False, "error": "Links are not allowed."}, status=400)

            Inbox.objects.create(
                name=name,
                pin_code=pin_code,
                contact=contact,
                messages_text=messages_text
            )
            return redirect("index")

        # --- Dealings form ---
        elif "Dealings" in request.POST and "image" in request.FILES:
            name = request.POST.get("name", "").strip()
            email = request.POST.get("email", "").strip()
            address = request.POST.get("address", "").strip()
            phone_number = request.POST.get("phone_number", "").strip()
            Dealings = request.POST.get("Dealings", "").strip()

            url_pattern = re.compile(r"(https?:\/\/|www\.|\b\S+\.(com|net|org|in|info|io|gov|co)\b)", re.IGNORECASE)
            for field_value, field_name in [(name, "Name"), (address, "Address"), (phone_number, "Phone")]:
                if url_pattern.search(field_value):
                    return render(request, 'index.html', {
                        "agent_error": f"Links are not allowed in {field_name}.",
                        "show_agent_modal": True,
                        "purposes": purposes,
                        "properties": properties,
                        "categories": categories,
                        "premium": premium,
                        "districts": districts,
                        "cities": cities,
                    })

            AgentForm.objects.create(
                name=name,
                email=email,
                address=address,
                phone_number=phone_number,
                Dealings=Dealings,
                image=request.FILES.get("image")
            )
            return redirect("index")

        # --- Property form ---
        elif "about_the_property" in request.POST and "image" in request.FILES:
            category_name = request.POST.get("categories", "").strip()
            purpose_name = request.POST.get("purposes", "").strip()
            label = request.POST.get("label", "").strip()
            land_area = request.POST.get("land_area", "").strip()
            sq_ft = request.POST.get("sq_ft", "").strip()
            description = request.POST.get("about_the_property", "").strip()
            amenities = request.POST.get("amenities", "").strip()
            owner = request.POST.get("owner", "").strip()
            phone = request.POST.get("phone", "").strip()
            whatsapp = request.POST.get("whatsapp", "").strip()
            location = request.POST.get("locations", "").strip()
            city = request.POST.get("city", "").strip()
            District = request.POST.get("District", "").strip()
            taluk = request.POST.get("taluk", "").strip()
            village = request.POST.get("village", "").strip()
            state = request.POST.get("state", "").strip()
            pin_code = request.POST.get("pin_code", "").strip()
            land_mark = request.POST.get("land_mark", "").strip()
            duration = request.POST.get("duration", "").strip()
            price = request.POST.get("price", "").strip()
            total_price = request.POST.get("total_price", "").strip()

            # 🚫 Link validation
            url_pattern = re.compile(r"(https?:\/\/|www\.|\b\S+\.(com|net|org|in|info|io|gov|co)\b)", re.IGNORECASE)
            for field_value, field_name in [
                (label, "Label"), (description, "Description"), (amenities, "Amenities"),
                (owner, "Owner"), (phone, "Phone"), (whatsapp, "WhatsApp"), (land_mark, "Landmark")
            ]:
                if url_pattern.search(field_value):
                    return render(request, "index.html", {
                        "property_error": f"Links are not allowed in {field_name}.",
                        "show_property_modal": True,
                        "purposes": purposes,
                        "properties": properties,
                        "categories": categories,
                        "premium": premium,
                        "District": District,
                        "taluk": taluk,
                        "village": village,
                        "state": state,
                        "cities": cities,
                    })

            Propertylist.objects.create(
                categories=category_name,
                purposes=purpose_name,
                label=label,
                land_area=land_area,
                description=description,
                sq_ft=sq_ft,
                amenities=amenities,
                owner=owner,
                locations=location,
                price=price,
                about_the_property=description,
                pin_code=pin_code,
                land_mark=land_mark,
                phone=phone,
                image=request.FILES.get("image"),
                total_price=total_price,
                duration=duration,
                whatsapp=whatsapp,
                city=city,
                District=District,
                taluk=taluk,
                village=village,
                state=state,
            )
            messages.success(request, "Property added successfully!")
            return redirect("index")

    # ------------------- GET REQUEST -------------------
    return render(request, 'index.html', {
        "purposes": purposes,
        "properties": properties,
        "categories": categories,
        "premium": premium,
        "District": District,
        "taluk": taluk,
        "village": village,
        "state": state,
        "districts": districts,
        "cities": cities,
        "search_query": query,  # Pass current search term to template
    })




def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points."""
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def nearest_property(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET method required"}, status=405)

    # Get user coordinates
    try:
        user_lat = float(request.GET.get("lat"))
        user_lng = float(request.GET.get("lng"))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid coordinates"}, status=400)

    properties = Property.objects.all()
    if not properties.exists():
        return JsonResponse({"error": "No properties found"}, status=404)

    results = []

    for prop in properties:
        lat = lng = None

        if prop.location:
            # Google Maps embed link: !2dLONG!3dLAT
            match = re.search(r"!2d([0-9.\-]+)!3d([0-9.\-]+)", prop.location)
            if match:
                lng = float(match.group(1))
                lat = float(match.group(2))

            # Google Maps share link: @LAT,LNG
            match2 = re.search(r"@([0-9.\-]+),([0-9.\-]+)", prop.location)
            if match2:
                lat = float(match2.group(1))
                lng = float(match2.group(2))

        if lat is not None and lng is not None:
            dist = haversine(user_lat, user_lng, lat, lng)

            # Get all images from RelatedManager safely
            images = (
                [request.build_absolute_uri(img.image.url) for img in prop.images.all()]
                if hasattr(prop, "images") and prop.images.exists()
                else [request.build_absolute_uri("/static/images/demo.png")]
            )

            results.append({
                "id": prop.id,
                "label": getattr(prop, "label", ""),
                "land_area": getattr(prop, "land_area", ""),
                "price": str(getattr(prop, "price", "")),
                "perprice": str(getattr(prop, "perprice", "")) if getattr(prop, "perprice", None) else "",
                "description": getattr(prop, "description", "") or "",
                "sq_ft": getattr(prop, "sq_ft", "") or "",
                "latitude": lat,
                "longitude": lng,
                "distance": round(dist, 2),
                "purpose_name": getattr(getattr(prop, "purpose", None), "name", "For Sale"),
                "images": images,
                "location": getattr(prop, "location", "") or "",
                "phone": getattr(prop, "phone", "") or "",
                "city": getattr(prop, "city", "") or "",
                "district": getattr(prop, "district", "") or "",
            })

    # Sort by nearest distance
    results.sort(key=lambda x: x["distance"])

    if not results:
        return JsonResponse({"error": "No nearby properties with valid coordinates"}, status=404)

    return JsonResponse(results, safe=False)



def properties(request):
    properties_list = Property.objects.all().order_by('-created_at')

    # 🔹 If nearby mode → DO NOT PAGINATE
    if request.GET.get("nearby") == "1":
        properties = properties_list  # full list
    else:
        paginator = Paginator(properties_list, 28)  # normal pagination
        page_number = request.GET.get('page')
        properties = paginator.get_page(page_number)

    purposes = Purpose.objects.all()
    categories = Category.objects.all()
    districts = Property.objects.values_list("district", flat=True).distinct()
    cities = Property.objects.values_list("city", flat=True).distinct()

    # Base queryset
    properties = Property.objects.all().order_by('-created_at')[:20]

    # ------------------- SEARCH -------------------
    query = request.GET.get("q", "").strip()
    if query:
        properties = Property.objects.filter(
            Q(label__icontains=query) |
            Q(description__icontains=query) |
            Q(city__icontains=query) |
            Q(district__icontains=query) |
            Q(category__name__icontains=query) |
            Q(purpose__name__icontains=query) |
            Q(state__icontains=query) |
            Q(city__icontains=query) |
            Q(price__icontains=query) |
            Q(location__icontains=query)
        ).order_by('-created_at')

    return render(request, 'properties.html', {
        "properties": properties,
        "districts": districts,
        "cities": cities,
        "purposes": purposes,
        "categories": categories,
        "search_query": query,
    })

def filter_properties(request):
    qs = Property.objects.all()

    purpose = request.GET.get("purpose")
    category = request.GET.get("category")
    district = request.GET.get("district")
    city = request.GET.get("city")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if purpose:
        qs = qs.filter(purpose_id=purpose)
    if category:
        qs = qs.filter(category_id=category)
    if district:
        qs = qs.filter(district__iexact=district)
    if city:
        qs = qs.filter(city__iexact=city)

    if min_price:
        try:
            qs = qs.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            qs = qs.filter(price__lte=float(max_price))
        except ValueError:
            pass

    data = [{
        "id": p.id,
        "label": p.label,
        "price": str(p.price),
        "perprice": str(p.perprice) if p.perprice else None,
        "sq_ft": p.sq_ft,
        "description": p.description,
        "purpose_name": p.purpose.name,
        "category_name": p.category.name,
        "district": p.district,
        "city": p.city,
        "location": p.location,
        "images": [img.image.url for img in p.images.all()],
    } for p in qs]

    return JsonResponse(data, safe=False)


def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    extra_images = property_obj.images.all()
    amenities = property_obj.amenities.split(",") if property_obj.amenities else []

    related_properties = Property.objects.filter(
        category=property_obj.category,
        purpose=property_obj.purpose,
        location__iexact=property_obj.location
    ).exclude(id=property_obj.id)

    if related_properties.count() < 6:
        related_properties = Property.objects.filter(
            category=property_obj.category,
            purpose=property_obj.purpose
        ).exclude(id=property_obj.id)

    related_properties = related_properties.order_by('?')[:6]

    return render(request, "detail_properties.html", {
        'property': property_obj,
        'extra_images': extra_images,
        'amenities': amenities,
        'related_properties': related_properties,
    })

from django.utils.safestring import mark_safe


@property
def map_embed(self):
    if not self.location:
        return ""

    # Check if the URL is already an embed link
    if "/embed?" in self.location:
        return mark_safe(
            f'<iframe src="{self.location}" class="w-full h-full rounded-md" style="border:0;" allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>')

    # Otherwise, treat it as a plain address and generate embed URL using API
    from urllib.parse import quote
    address = quote(self.location)
    api_key = "YOUR_GOOGLE_API_KEY"  # replace with your key
    embed_url = f"https://www.google.com/maps/embed/v1/place?key={api_key}&q={address}"
    return mark_safe(
        f'<iframe src="{embed_url}" class="w-full h-full rounded-md" style="border:0;" allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>')

def privacy(request):
    return render(request, 'privacy.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        # Block URLs/domains but allow emails
        url_pattern = re.compile(
            r'(https?://\S+|www\.\S+|(?<!@)\b[A-Za-z0-9-]+\.(com|net|org|in|info|io|gov|co)\b)',
            re.IGNORECASE
        )

        for field in [name, email, phone, message]:
            if url_pattern.search(field):
                messages.error(request, "Links are not allowed in any field.")
                return redirect("contact")

        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        messages.success(request, "Your message has been submitted successfully!")
        return redirect("contact")

    return render(request, "contact.html")



def agents(request):
    premium = Premium.objects.all()
    agents = Agents.objects.all()

    user_city = request.GET.get("city", None)

    nearest_premium = Premium.objects.none()
    nearest_agents = Agents.objects.none()
    fallback_city_premium = None
    fallback_city_agents = None

    if user_city:
        # Primary filter
        nearest_premium = Premium.objects.filter(city__iexact=user_city)
        nearest_agents = Agents.objects.filter(agentscity__iexact=user_city)

        # Fallback for Premium
        if not nearest_premium.exists():
            fallback_city_premium = (
                Premium.objects.values_list("city", flat=True)
                .distinct()
                .first()
            )
            if fallback_city_premium:
                nearest_premium = Premium.objects.filter(city__iexact=fallback_city_premium)

        # Fallback for Agents
        if not nearest_agents.exists():
            fallback_city_agents = (
                Agents.objects.values_list("agentscity", flat=True)
                .distinct()
                .first()
            )
            if fallback_city_agents:
                nearest_agents = Agents.objects.filter(agentscity__iexact=fallback_city_agents)

    # Handle AgentForm submission
    if request.method == "POST" and "specialised" in request.POST and "photo" in request.FILES:
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        address = request.POST.get("address", "").strip()
        phone_number = request.POST.get("phone", "").strip()
        Dealings = request.POST.get("specialised", "").strip()
        image = request.FILES.get("photo")

        # Block links and special characters in name, address, phone
        url_pattern = re.compile(r"(https?:\/\/|www\.|\b\S+\.(com|net|org|in|info|io|gov|co)\b)", re.IGNORECASE)
        special_char_pattern = re.compile(r"[<>\/\[\]{}~`+\-*]")

        error_message = None
        for value, field_name in [(name, "Name"), (address, "Address"), (phone_number, "Phone")]:
            if url_pattern.search(value):
                error_message = f"❌ Links are not allowed in {field_name}."
                break
            if special_char_pattern.search(value):
                error_message = f"❌ Special characters < > / [ ] {{ }} ~ ` + - * are not allowed in {field_name}."
                break

        if error_message:
            return render(request, "agents.html", {
                "premium": premium,
                "agents": agents,
                "nearest_premium": nearest_premium,
                "nearest_agents": nearest_agents,
                "user_city": user_city,
                "fallback_city_premium": fallback_city_premium,
                "fallback_city_agents": fallback_city_agents,
                "agent_error": error_message,  # pass error to template
                "show_agent_modal": True,      # keep modal open
            })

        # Save the agent form
        AgentForm.objects.create(
            name=name,
            email=email,
            address=address,
            phone_number=phone_number,
            Dealings=Dealings,
            image=image
        )
        return redirect("agents")  # redirect after successful save

    return render(
        request,
        "agents.html",
        {
            "premium": premium,
            "agents": agents,
            "nearest_premium": nearest_premium,
            "nearest_agents": nearest_agents,
            "user_city": user_city,
            "fallback_city_premium": fallback_city_premium,
            "fallback_city_agents": fallback_city_agents,
        },
    )


def agent_detail(request, pk):
    agent = get_object_or_404(Premium, pk=pk)
    properties = agent.properties.all()  # fetch properties linked to this agent

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        contact_method = request.POST.get("contact_method")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        # Save contact request
        ContactRequest.objects.create(
            first_name=first_name,
            last_name=last_name,
            contact_method=contact_method,
            email=email,
            phone=phone,
            message=message,
        )

        # If AJAX request, return JSON for modal
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})

        # Normal POST fallback
        messages.success(request, "✅ Your message has been sent to this agent!")
        return redirect("agent_detail", pk=pk)

    return render(request, "agent_detail.html", {
        "premium": agent,
        "properties": properties
    })





def agent_property_detail(request, pk):
    property_obj = get_object_or_404(AgentProperty, pk=pk)
    extra_images = property_obj.images.all()  # related_name from AgentPropertyImage
    amenities = property_obj.amenities.split(",") if property_obj.amenities else []

    # Fetch related properties (same category, purpose, and location)
    related_properties = AgentProperty.objects.filter(
        category=property_obj.category,
        purpose=property_obj.purpose,
        location__iexact=property_obj.location
    ).exclude(id=property_obj.id)[:6]  # Exclude current property, limit 6

    return render(request, "agent_detail_properties.html", {
        'property': property_obj,       # ✅ fixed naming
        'extra_images': extra_images,   # ✅ pass extra images
        'amenities': amenities,
        'related_properties': related_properties,
    })

def gallery(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)  # Use the correct model
    extra_images = PropertyImage.objects.filter(property=property_obj)

    return render(request, "gallery.html", {
        'property': property_obj,
        'extra_images': extra_images
    })


def property_gallery(request, pk):
    property_obj = get_object_or_404(AgentProperty, pk=pk)  # or your actual model name
    extra_images = AgentPropertyImage.objects.filter(property=property_obj)

    return render(request, "propertygallery.html", {
        'property': property_obj,
        'extra_images': extra_images
    })


@csrf_exempt
def upload_property_screenshot(request):
    if request.method == "POST":
        property_id = request.POST.get("property_id")
        screenshot_file = request.FILES.get("screenshot")

        if not property_id:
            return JsonResponse({"status": "error", "message": "Missing property ID"}, status=400)

        if not screenshot_file:
            return JsonResponse({"status": "error", "message": "No screenshot received"}, status=400)

        try:
            prop = Property.objects.get(id=property_id)
            prop.screenshot = screenshot_file
            prop.save()
            return JsonResponse({
                "status": "success",
                "screenshot_url": prop.screenshot.url
            })
        except Property.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Property not found"}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


@csrf_exempt
def upload_agents_screenshot(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    property_id = request.POST.get("property_id")
    screenshot = request.FILES.get("screenshot")

    if not property_id or not screenshot:
        return JsonResponse({"error": "Missing data"}, status=400)

    try:
        prop = AgentProperty.objects.get(id=property_id)
        prop.screenshot.save(f"property_{prop.id}.png", screenshot)
        prop.save()

        return JsonResponse({"success": True})

    except AgentProperty.DoesNotExist:
        return JsonResponse({"error": "Property not found"}, status=404)














from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.contrib.auth.hashers import check_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import re
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import get_user_model
import requests

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework.permissions import IsAuthenticated
from .utils import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from cloudinary.utils import cloudinary_url
import uuid
import secrets
from urllib.parse import urlencode
from rest_framework import generics


class PropertyViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = PropertySerializer

    queryset = Property.objects.prefetch_related(
        "images",
        "category",
        "purpose"
    ).order_by("-id")

    # -------------------------
    # Convert Budget String
    # -------------------------

    def convert_budget_to_number(self, text):

        text = text.lower()

        number = re.findall(r"\d+", text)

        if not number:
            return None

        value = int(number[0])

        # Crore support
        if "crore" in text:
            value = value * 10000000

        # Lakh support
        elif "lakh" in text:
            value = value * 100000

        return value


    # -------------------------
    # Extract Price Number
    # -------------------------

    def extract_price(self, price):

        if not price:
            return None

        price = price.lower()

        number = re.findall(r"\d+", price)

        if not number:
            return None

        value = int(number[0])

        if "crore" in price:
            value = value * 10000000

        elif "lakh" in price:
            value = value * 100000

        return value


    # -------------------------
    # FILTER SYSTEM
    # -------------------------

    def get_queryset(self):

        queryset = super().get_queryset()

        category = self.request.query_params.get("category")
        purpose = self.request.query_params.get("purpose")
        city = self.request.query_params.get("city")
        budget = self.request.query_params.get("budget")

        # CATEGORY NAME
        if category:
            queryset = queryset.filter(
                category__name__iexact=category
            )

        # PURPOSE NAME
        if purpose:
            queryset = queryset.filter(
                purpose__name__iexact=purpose
            )

        # CITY
        if city:
            queryset = queryset.filter(
                city__iexact=city
            )

        # -------------------------
        # BUDGET FILTER
        # -------------------------

        if budget:

            budget_value = self.convert_budget_to_number(
                budget
            )

            if budget_value:

                filtered_ids = []

                for property in queryset:

                    price_value = self.extract_price(
                        property.price
                    )

                    if not price_value:
                        continue

                    # BELOW
                    if "below" in budget.lower():

                        if price_value <= budget_value:
                            filtered_ids.append(property.id)

                    # ABOVE
                    elif "above" in budget.lower():

                        if price_value >= budget_value:
                            filtered_ids.append(property.id)

                    # DEFAULT
                    else:

                        if price_value <= budget_value:
                            filtered_ids.append(property.id)

                queryset = queryset.filter(
                    id__in=filtered_ids
                )

        return queryset


from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

# class PremiumLoginAPIView(APIView):

#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):

#         username = request.data.get("username")
#         password = request.data.get("password")

#         if not username or not password:
#             return Response(
#                 {"error": "Username and Password required"},
#                 status=400
#             )

#         try:
#             premium = Premium.objects.get(username=username)

#         except Premium.DoesNotExist:
#             return Response({"error": "Invalid Username"}, status=400)

#         if not check_password(password, premium.password):
#             return Response({"error": "Invalid Password"}, status=400)

#         refresh = RefreshToken()
#         refresh["premium_id"] = premium.id
#         refresh["username"] = premium.username

#         response = Response({

#             "message": "Login Success",
#             "access": str(refresh.access_token),

#             "premium": {
#                 "id": premium.id,
#                 "name": premium.name,
#                 "city": premium.city,
#                 "image": premium.image.url if premium.image else None
#             }

#         })

#         # Store refresh token in cookie
#         response.set_cookie(
#             key="refresh_token",
#             value=str(refresh),
#             httponly=True,
#             secure=False,
#             samesite="Lax",
#             max_age=7 * 24 * 60 * 60
#         )

#         return response


class RequestCreateAPIView(APIView):

    authentication_classes = []   # public form
    permission_classes = []

    def post(self, request):

        serializer = RequestSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({

                "message":"Request Submitted Successfully",
                "data":serializer.data

            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# class BudgetListAPIView(APIView):

#     def get(self, request):

#         budget = Budget.objects.all().order_by("id")

#         serializer = BudgetSerializer(
#             budget,
#             many=True
#         )

#         return Response({
#             "budget": serializer.data
#         })

class BudgetListAPIView(APIView):

    def get(self, request):

        try:
            budget = Budget.objects.all().order_by("created_at")

            serializer = BudgetSerializer(budget, many=True)

            return Response({
                "status": True,
                "budget": serializer.data
            }, status=200)

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=500)
        

class CategoryListView(APIView):
    def get(self, request):
        category = Category.objects.all().order_by("id")

        serializers = CategorySerializer(
            category,
            many=True
        )
        return Response({
            "category": serializers.data
        })

class PremiumPasswordChangeAPIView(APIView):

    def post(self, request):

        serializer = PremiumPasswordChangeSerializer(
            data=request.data
        )

        if serializer.is_valid():

            premium = serializer.validated_data["premium"]
            new_password = serializer.validated_data["new_password"]

            premium.password = new_password
            premium.save()

            return Response(
                {
                    "message": "Password Changed Successfully"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# class FeaturedPropertyViewSet(viewsets.ReadOnlyModelViewSet):

#     serializer_class = PropertyCardSerializer

#     def get_queryset(self):
#         return Property.objects.filter(
#             is_featured=True
#         ).prefetch_related(
#             "images",
#             "category",
#             "purpose"
#         ).order_by("-id")

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         request = self.request

#         wishlist_ids = set()
#         auth_header = request.headers.get("Authorization")

#         if auth_header:
#             try:
#                 token = auth_header.split(" ")[1]

#                 decoded = jwt.decode(
#                     token,
#                     settings.SECRET_KEY,
#                     algorithms=["HS256"]
#                 )

#                 user_id = int(decoded.get("user_id"))

#                 # ✅ IMPORTANT FIX: GET USER OBJECT FIRST
#                 user = UserCreate.objects.get(id=user_id)

#                 wishlist_ids = set(
#                     Wishlist.objects.filter(user=user)
#                     .values_list("property_id", flat=True)
#                 )

#             except jwt.ExpiredSignatureError:
#                 pass
#             except jwt.InvalidTokenError:
#                 pass
#             except UserCreate.DoesNotExist:
#                 pass
#             except Exception:
#                 pass

#         context["wishlist_ids"] = wishlist_ids
#         return context

import uuid
import jwt
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

# class FeaturedPropertyViewSet(viewsets.ModelViewSet):
#     serializer_class = PropertyCardSerializer
#     permission_classes = [AllowAny]
#     authentication_classes = []  
#     http_method_names = ["get"]

#     lookup_field = "uuid"              
#     lookup_url_kwarg = "uuid"          

#     def get_queryset(self):
#         return Property.objects.filter(
#             is_featured=True
#         ).prefetch_related(
#             "images",
#             "category",
#             "purpose"
#         )

#     def get_user(self):
#         auth_header = self.request.headers.get("Authorization")

#         if not auth_header:
#             return None

#         try:
#             token = auth_header.split(" ")[1]

#             decoded = jwt.decode(
#                 token,
#                 settings.SECRET_KEY,
#                 algorithms=["HS256"]
#             )

#             user_id = decoded.get("user_id")

#             if not user_id:
#                 return None

#             user_id = uuid.UUID(user_id)

#             return UserCreate.objects.filter(id=user_id).first()

#         except Exception as e:
#             print("Auth Error:", str(e))
#             return None

#     def get_serializer_context(self):
#         context = super().get_serializer_context()

#         user = self.get_user()
#         wishlist_ids = set()

#         if user:
#             wishlist_ids = set(
#                 Wishlist.objects.filter(user_id=user.id)
#                 .values_list("property_uuid", flat=True)
#             )

#         context["wishlist_ids"] = wishlist_ids
#         return context


import uuid
import jwt
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Property, Wishlist, UserCreate
from .serializers import PropertyCardSerializer


class FeaturedPropertyViewSet(viewsets.ModelViewSet):

    serializer_class = PropertyCardSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    http_method_names = ["get"]

    # ===============================
    # QUERYSET
    # ===============================
    def get_queryset(self):
        return Property.objects.filter(
            is_featured=True
        ).prefetch_related(
            "images",
            "category",
            "purpose"
        )

    # ===============================
    # USER
    # ===============================
    def get_user(self):
        auth_header = self.request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]

            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            user_id = decoded.get("user_id")

            if not user_id:
                return None

            # 🔥 SAFE UUID HANDLING
            try:
                user_id = uuid.UUID(str(user_id))
            except:
                return None

            return UserCreate.objects.filter(id=user_id).first()

        except Exception as e:
            print("Auth Error:", str(e))
            return None

    # ===============================
    # CONTEXT (WISHLIST FIX)
    # ===============================
    def get_serializer_context(self):
        context = super().get_serializer_context()

        user = self.get_user()
        wishlist_ids = set()

        if user:
            wishlist_ids = Wishlist.objects.filter(user=user).values_list(
                "property_uuid", flat=True
            )

            # 🔥 IMPORTANT: convert UUID → string
            wishlist_ids = {str(i) for i in wishlist_ids}

        context["wishlist_ids"] = wishlist_ids
        return context

class AgentFormView(APIView):

    # ✅ POST
    def post(self, request):

        serializer = AgentFormSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Request Submitted Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


    # ✅ GET ALL
    def get(self, request):

        agents = AgentForm.objects.all().order_by("-created_at")

        serializer = AgentFormSerializer(
            agents,
            many=True
        )

        return Response(
            {
                "message": "Agent List",
                "data": serializer.data
            }
        )

class RegisterAPI(APIView):

    def post(self, request):

        email = request.data.get("email")

        existing_user = UserCreate.objects.filter(email=email).first()

        if existing_user:

            # If already verified
            if existing_user.is_verified:
                return Response(
                    {"error": "Email already registered"},
                    status=400
                )

            # Block frequent OTP requests (30 seconds)
            if existing_user.otp_created_at and timezone.now() < existing_user.otp_created_at + timedelta(seconds=30):
                return Response(
                    {"error": "Please wait before requesting OTP again"},
                    status=429
                )

            # If OTP expired (2 minutes) delete user
            if existing_user.otp_created_at and timezone.now() > existing_user.otp_created_at + timedelta(minutes=2):
                existing_user.delete()

            else:
                return Response(
                    {"error": "OTP already sent. Please verify within 2 minutes."},
                    status=400
                )

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save()

            send_otp_email(user.email, otp)

            return Response(
                {
                    "message": "OTP sent to email",
                    "email" : email,

                 },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=400)



class VerifyOTPAPI(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data["email"]
            entered_otp = serializer.validated_data["otp"]

            try:
                user = UserCreate.objects.get(email=email)

                if not user.otp or not user.otp_created_at:
                    return Response({"error": "OTP not generated"}, status=400)

                # OTP expiry (2 minutes)
                if timezone.now() > user.otp_created_at + timedelta(minutes=2):
                    user.delete()
                    return Response(
                        {"error": "OTP expired. Please register again."},
                        status=400
                    )

                # Invalid OTP
                if user.otp != entered_otp:
                    return Response({"error": "Invalid OTP"}, status=400)

                # Successful verification
                user.is_verified = True
                user.otp = None
                user.otp_created_at = None
                user.save()

                refresh = RefreshToken.for_user(user)

                # ✅ Ensure profile exists
                profile, created = UserProfile.objects.get_or_create(user=user)

                # ✅ Get image safely
                # if profile.image:
                #     if hasattr(profile.image, "url"):
                #         image_url = profile.image.url
                #     else:
                #         image_url, _ = cloudinary_url(profile.image)
                # else:
                #     image_url, _ = cloudinary_url("Vector_te4oj7")

                image_url = profile.profile_image_url

                response = Response({
                    "message": "Email verified successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": uuid.uuid4().hex[:10],
                        "name": user.name,
                        "email": user.email,
                        "mobile": user.mobile,
                        "image": image_url
                    }
                })


                return response

            except UserCreate.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

        return Response(serializer.errors, status=400)


class ResendOTPAPI(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        email = request.data.get("email")

        try:
            user = UserCreate.objects.get(email=email)

            if user.is_verified:
                return Response(
                    {"error": "User already verified"},
                    status=400
                )

            if not user.otp_created_at:
                return Response(
                    {"error": "OTP not generated yet"},
                    status=400
                )

            # Prevent frequent resend (30 seconds)
            if timezone.now() < user.otp_created_at + timedelta(seconds=30):
                return Response(
                    {"error": "Please wait before requesting OTP again"},
                    status=429
                )

            # Generate new OTP
            otp = str(random.randint(100000, 999999))

            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save()

            send_otp_email(user.email, otp)

            return Response(
                {"message": "OTP resent successfully"},
                status=200
            )

        except UserCreate.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=404
            )

class ForgotPasswordAPI(APIView):

    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=400
            )

        email = serializer.validated_data["email"]

        try:

            user = UserCreate.objects.get(email=email)

            otp = user.generate_otp()

            user.otp = otp

            user.otp_created_at = timezone.now()

            user.save(
                update_fields=[
                    "otp",
                    "otp_created_at"
                ]
            )

            email_sent = send_otp_email(email, otp)

            if not email_sent:

                return Response(
                    {"error": "Failed to send OTP"},
                    status=500
                )

            return Response(
                {"message": "OTP sent successfully"},
                status=200
            )

        except UserCreate.DoesNotExist:

            return Response(
                {"error": "User not found"},
                status=404
            )

class VerifyForgotOTPAPI(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = VerifyForgotOTPSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(serializer.errors, status=400)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:

            user = UserCreate.objects.get(email=email)

            if not user.otp or not user.otp_created_at:

                return Response(
                    {"error": "OTP not generated"},
                    status=400
                )

            if timezone.now() > user.otp_created_at + timedelta(minutes=5):

                return Response(
                    {"error": "OTP expired"},
                    status=400
                )

            if str(user.otp) != str(otp):

                return Response(
                    {"error": "Invalid OTP"},
                    status=400
                )

            # ✅ clear otp
            user.otp = None
            user.otp_created_at = None
            user.save(update_fields=["otp","otp_created_at"])

            # ✅ create reset token
            reset = PasswordResetToken.objects.create(
                user=user
            )

            return Response(
                {
                    "message":"OTP verified",


                    "reset_token": str(reset.token)
                },
                status=200
            )

        except UserCreate.DoesNotExist:

            return Response(
                {"error":"User not found"},
                status=404
            )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
import random

class ForgotPasswordResendOTPAPI(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        email = request.data.get("email", "").strip().lower()

        if not email:
            return Response(
                {"error": "Email is required"},
                status=400
            )

        try:
            user = UserCreate.objects.get(email=email)

            # ✅ ONLY VERIFIED USERS CAN RESET PASSWORD
            if not user.is_verified:
                return Response(
                    {"error": "User is not verified"},
                    status=400
                )

            # ✅ Prevent spam (30 sec cooldown)
            if user.otp_created_at and timezone.now() < user.otp_created_at + timedelta(seconds=30):
                return Response(
                    {"error": "Please wait before requesting OTP again"},
                    status=429
                )

            # ✅ Generate OTP
            otp = str(random.randint(100000, 999999))

            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save(update_fields=["otp", "otp_created_at"])

            # ✅ Send mail
            send_otp_email(user.email, otp)

            return Response(
                {
                    "status": True,
                    "message": "OTP sent for password reset"
                },
                status=200
            )

        except UserCreate.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=404
            )

# import jwt
# from django.conf import settings
# from django.contrib.auth.hashers import make_password
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# class ChangePasswordAPI(APIView):

#     authentication_classes = []   # you are handling manually
#     permission_classes = [AllowAny]

#     def post(self, request):

#         serializer = ChangePasswordSerializer(data=request.data)

#         if not serializer.is_valid():
#             return Response(serializer.errors, status=400)

#         # ✅ Get Authorization Header
#         auth_header = request.headers.get("Authorization")

#         if not auth_header:
#             return Response(
#                 {"error": "Access token missing"},
#                 status=401
#             )

#         # ✅ Extract Bearer token
#         try:
#             token = auth_header.split(" ")[1]
#         except IndexError:
#             return Response(
#                 {"error": "Invalid Authorization header"},
#                 status=401
#             )

#         try:
#             # ✅ Decode JWT
#             decoded = jwt.decode(
#                 token,
#                 settings.SECRET_KEY,
#                 algorithms=["HS256"]
#             )

#             user_id = decoded.get("user_id")

#             if not user_id:
#                 return Response(
#                     {"error": "Invalid token payload"},
#                     status=401
#                 )

#             # ✅ Get user
#             user = UserCreate.objects.get(id=user_id)

#             # ✅ Change password
#             new_password = serializer.validated_data["new_password"]

#             user.password = make_password(new_password)
#             user.save(update_fields=["password"])

#             return Response(
#                 {"message": "Password changed successfully"},
#                 status=200
#             )

#         # ✅ Token expired
#         except ExpiredSignatureError:
#             return Response(
#                 {"error": "Token expired"},
#                 status=401
#             )

#         # ✅ Invalid token
#         except InvalidTokenError:
#             return Response(
#                 {"error": "Invalid token"},
#                 status=401
#             )

#         # ✅ User not found
#         except UserCreate.DoesNotExist:
#             return Response(
#                 {"error": "User not found"},
#                 status=404
#             )

#         except Exception as e:
#             return Response(
#                 {"error": str(e)},
#                 status=500
#             )
        


# class ChangePasswordAPI(APIView):

#     authentication_classes = []
#     permission_classes = [AllowAny]

#     def post(self, request):

#         serializer = ChangePasswordSerializer(data=request.data)

#         if not serializer.is_valid():

#             return Response(serializer.errors, status=400)

#         # ✅ Get Authorization Header
#         auth_header = request.headers.get("Authorization")

#         if not auth_header:

#             return Response(
#                 {"error": "Reset token missing"},
#                 status=400
#             )

#         # ✅ Remove Bearer
#         try:

#             reset_token = auth_header.split(" ")[1]

#         except IndexError:

#             return Response(
#                 {"error": "Invalid Authorization header"},
#                 status=400
#             )

#         try:

#             reset = PasswordResetToken.objects.get(
#                 token=reset_token
#             )

#             # expiry check
#             if reset.expires_at < timezone.now():

#                 return Response(
#                     {"error": "Reset token expired"},
#                     status=400
#                 )

#             user = reset.user

#             new_password = serializer.validated_data[
#                 "new_password"
#             ]

#             user.password = make_password(
#                 new_password
#             )

#             user.save(update_fields=["password"])

#             # delete token after use
#             reset.delete()

#             return Response(
#                 {"message": "Password changed successfully"},
#                 status=200
#             )

#         except PasswordResetToken.DoesNotExist:

#             return Response(
#                 {"error": "Invalid reset token"},
#                 status=400
#             )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class UserChangePasswordAPI(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        # -------------------------
        # STEP 1: GET NEW PASSWORD DIRECTLY
        # -------------------------
        new_password = request.data.get("new_password")

        if not new_password:
            return Response(
                {"error": "new_password is required"},
                status=400
            )

        # -------------------------
        # STEP 2: GET RESET TOKEN
        # -------------------------
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return Response(
                {"error": "Reset token missing"},
                status=400
            )

        try:
            reset_token = auth_header.split(" ")[1]
        except IndexError:
            return Response(
                {"error": "Invalid Authorization header"},
                status=400
            )

        # -------------------------
        # STEP 3: FIND TOKEN
        # -------------------------
        try:
            reset = PasswordResetToken.objects.get(token=reset_token)
        except PasswordResetToken.DoesNotExist:
            return Response(
                {"error": "Invalid reset token"},
                status=400
            )

        # -------------------------
        # STEP 4: CHECK EXPIRY
        # -------------------------
        if reset.expires_at < timezone.now():
            return Response(
                {"error": "Reset token expired"},
                status=400
            )

        # -------------------------
        # STEP 5: UPDATE PASSWORD
        # -------------------------
        user = reset.user
        user.password = make_password(new_password)
        user.save(update_fields=["password"])

        # -------------------------
        # STEP 6: DELETE TOKEN
        # -------------------------
        reset.delete()

        return Response(
            {"message": "Password changed successfully"},
            status=200
        )

# class UserLoginAPI(APIView):

#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):

#         serializer = UserLoginSerializer(data=request.data)

#         if not serializer.is_valid():
#             return Response(serializer.errors, status=400)

#         email = serializer.validated_data["email"]
#         password = serializer.validated_data["password"]

#         try:
#             user = UserCreate.objects.get(email=email)

#             if not user.is_verified:
#                 return Response({"error": "Email not verified"}, status=400)

#             if not check_password(password, user.password):
#                 return Response({"error": "Invalid credentials"}, status=400)

#             refresh = RefreshToken.for_user(user)

#             profile, created = UserProfile.objects.get_or_create(user=user)

#             # if profile.image:
#             #     profile_image = profile.image.url
#             # else:
#             #     profile_image, _ = cloudinary_url("Vector_te4oj7")
#             profile_image = profile.profile_image_url

#             return Response({
#                 "message": "Login successful",
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#                 "user": {
#                     "id": user.id,   # ✅ FIXED
#                     "email": user.email,
#                     "name": user.name,
#                     "image": profile_image
#                 }
#             })

#         except UserCreate.DoesNotExist:
#             return Response({"error": "Invalid credentials"}, status=400)

class UserLoginAPI(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = UserLoginSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=400
            )

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:

            user = UserCreate.objects.get(
                email=email
            )

            # =====================================
            # EMAIL VERIFIED CHECK
            # =====================================
            if not user.is_verified:

                return Response(
                    {
                        "error": "Email not verified"
                    },
                    status=400
                )

            # =====================================
            # PASSWORD CHECK
            # =====================================
            if not check_password(
                password,
                user.password
            ):

                return Response(
                    {
                        "error": "Invalid credentials"
                    },
                    status=400
                )

            is_plan = UserPlanSubscription.objects.filter(
                user=user,
                expiry_date__gte=timezone.now(),
                is_active=True
            ).exists()

            # =====================================
            # JWT TOKEN
            # =====================================
            refresh = RefreshToken.for_user(user)

            refresh["user_id"] = str(user.id)

            # =====================================
            # PROFILE
            # =====================================
            profile, created = UserProfile.objects.get_or_create(
                user=user
            )

            profile_image = profile.profile_image_url

            # =====================================
            # PROPERTY COUNTS
            # =====================================
            property_counts = get_property_remaining_counts(
                user
            )

            # =====================================
            # RESPONSE
            # =====================================
            return Response({

                "message": "Login successful",

                "access": str(
                    refresh.access_token
                ),

                "refresh": str(
                    refresh
                ),

                "login_as": "user",
                "is_plan": is_plan,

                "user": {

                    "id": str(user.id),
                    "email": user.email,
                    "name": user.name,
                    "image": profile_image,

                    "total_properties": (
                        property_counts.get(
                            "total_properties",
                            0
                        )
                    ),
                    "remaining_property": property_counts.get(
                        "remaining_property",
                        0
                    ),
                }

            }, status=200)

        except UserCreate.DoesNotExist:

            return Response(
                {
                    "error": "Invalid credentials"
                },
                status=400
            )

        except Exception as e:

            print("LOGIN ERROR:", e)

            return Response(
                {
                    "error": str(e)
                },
                status=500
            )

# class UserLoginAPI(APIView):

#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):

#         serializer = UserLoginSerializer(
#             data=request.data
#         )

#         if not serializer.is_valid():
#             return Response(
#                 serializer.errors,
#                 status=400
#             )

#         email = serializer.validated_data["email"]
#         password = serializer.validated_data["password"]

#         try:
#             user = UserCreate.objects.get(
#                 email=email
#             )

#             if not user.is_verified:
#                 return Response(
#                     {"error": "Email not verified"},
#                     status=400
#                 )

#             if not check_password(
#                 password,
#                 user.password
#             ):
#                 return Response(
#                     {"error": "Invalid credentials"},
#                     status=400
#                 )


#             # ------------------------
#             # UUID SAFE JWT
#             # ------------------------
#             refresh = RefreshToken.for_user(user)

#             # important after UUID migration
#             refresh["user_id"] = str(user.id)


#             profile, created = UserProfile.objects.get_or_create(
#                 user=user
#             )

#             profile_image = profile.profile_image_url


#             return Response({
#                 "message": "Login successful",

#                 "access": str(
#                     refresh.access_token
#                 ),

#                 "refresh": str(
#                     refresh
#                 ),
#                 "login_as": "user",

#                 # "type": user.role,

#                 "user": {
#                     "id": str(user.id),
#                     "email": user.email,
#                     "name": user.name,
#                     "image": profile_image
#                 }
#             })


#         except UserCreate.DoesNotExist:
#             return Response(
#                 {
#                     "error": "Invalid credentials"
#                 },
#                 status=400
#             )



class FacebookLoginAPI(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        access_token = request.data.get("access_token")

        if not access_token:
            return Response({"error": "Access token required"}, status=400)

        # ✅ Verify token & get user data from Facebook
        url = f"https://graph.facebook.com/me?fields=id,name,email,picture&access_token={access_token}"

        response = requests.get(url)
        data = response.json()

        if "error" in data:
            return Response({"error": "Invalid Facebook token"}, status=400)

        email = data.get("email")
        name = data.get("name")

        if not email:
            return Response({"error": "Email not provided by Facebook"}, status=400)

        # ✅ Check if user exists
        user = UserCreate.objects.filter(email=email).first()

        if not user:
            # ✅ Create new user
            user = UserCreate.objects.create(
                name=name,
                email=email,
                password="",  # No password for social login
                is_verified=True
            )

        # ✅ Ensure profile exists
        profile, created = UserProfile.objects.get_or_create(user=user)

        # ✅ Set auth provider
        profile.auth_provider = "facebook"
        profile.save()

        # ✅ Generate JWT
        refresh = RefreshToken.for_user(user)

        # ✅ Profile image from FB
        # image_url = None
        # if data.get("picture"):
        #     image_url = data["picture"]["data"]["url"]

        image_url = profile.profile_image_url

        return Response({
            "message": "Facebook login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "image": image_url
            }
        }, status=200)

User = get_user_model()


# import requests

# from django.contrib.auth import get_user_model

# from rest_framework.views import APIView
# from rest_framework.response import Response

# from rest_framework_simplejwt.tokens import RefreshToken

# User = get_user_model()


# class FacebookLoginAPI(APIView):

#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):

#         access_token = request.data.get("access_token")

#         if not access_token:

#             return Response({
#                 "status": False,
#                 "message": "Access token required"
#             }, status=400)

#         # =====================================================
#         # FACEBOOK GRAPH API
#         # =====================================================

#         url = (
#             "https://graph.facebook.com/me"
#             "?fields=id,name,email,picture.type(large)"
#             f"&access_token={access_token}"
#         )

#         response = requests.get(url)

#         data = response.json()

#         # =====================================================
#         # DEBUG
#         # =====================================================

#         print("FACEBOOK RESPONSE =>", data)

#         # =====================================================
#         # INVALID TOKEN
#         # =====================================================

#         if "error" in data:

#             return Response({
#                 "status": False,
#                 "message": "Invalid Facebook token",
#                 "facebook_error": data
#             }, status=400)

#         # =====================================================
#         # GET USER DATA
#         # =====================================================

#         email = data.get("email")
#         name = data.get("name")

#         # =====================================================
#         # EMAIL NOT FOUND
#         # =====================================================

#         if not email:

#             return Response({
#                 "status": False,
#                 "message": (
#                     "Facebook did not return email. "
#                     "Please login again and allow email permission."
#                 ),
#                 "facebook_response": data
#             }, status=400)

#         # =====================================================
#         # CHECK USER
#         # =====================================================

#         user = User.objects.filter(
#             email=email
#         ).first()

#         # =====================================================
#         # CREATE USER
#         # =====================================================

#         if not user:

#             user = User.objects.create(
#                 name=name,
#                 email=email,
#                 password="",
#                 is_verified=True
#             )

#         # =====================================================
#         # PROFILE
#         # =====================================================

#         profile, created = UserProfile.objects.get_or_create(
#             user=user
#         )

#         profile.auth_provider = "facebook"

#         # =====================================================
#         # FACEBOOK PROFILE IMAGE
#         # =====================================================

#         image_url = None

#         if data.get("picture"):

#             image_url = (
#                 data["picture"]
#                 .get("data", {})
#                 .get("url")
#             )

#             if image_url:
#                 profile.profile_image_url = image_url

#         profile.save()

#         # =====================================================
#         # JWT TOKENS
#         # =====================================================

#         refresh = RefreshToken.for_user(user)

#         # =====================================================
#         # RESPONSE
#         # =====================================================

#         return Response({
#             "status": True,
#             "message": "Facebook login successful",

#             "access": str(refresh.access_token),
#             "refresh": str(refresh),

#             "user": {
#                 "id": user.id,
#                 "name": user.name,
#                 "email": user.email,
#                 "image": image_url
#             }
#         }, status=200)


import requests
from django.core.files.base import ContentFile

def handle_google_user(email, name, picture):
    user, _ = UserCreate.objects.get_or_create(
        email=email,
        defaults={
            "name": name,
            "is_verified": True
        }
    )

    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={"auth_provider": "google"}
    )

    #  Ensure provider
    if profile.auth_provider != "google":
        profile.auth_provider = "google"

    #  Set full name
    if not profile.full_name:
        profile.full_name = name

    #  Save Google image (only first time)
    if picture and not profile.image:
        try:
            img_res = requests.get(picture, timeout=10)
            if img_res.status_code == 200:
                profile.image.save(
                    f"{email.split('@')[0]}.jpg",
                    ContentFile(img_res.content),
                    save=False
                )
        except Exception:
            pass

    profile.save()
    return user, profile

# class GoogleLoginView(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):
#         try:
#             access_token = request.data.get("access_token")
#             if not access_token:
#                 return Response({"error": "Access token required"}, status=400)

#             # 🔹 GET USER INFO FROM GOOGLE
#             google_res = requests.get(
#                 "https://www.googleapis.com/oauth2/v1/userinfo",
#                 params={"access_token": access_token},
#                 timeout=10
#             )

#             if google_res.status_code != 200:
#                 return Response({
#                     "error": "Invalid Google token",
#                     "details": google_res.text
#                 }, status=400)

#             user_info = google_res.json()
#             email = user_info.get("email")
#             name = user_info.get("name", "")
#             picture = user_info.get("picture", "")

#             if not email:
#                 return Response({"error": "Email not found"}, status=400)

#             # 🔹 CREATE OR GET USER
#             user, profile = handle_google_user(email, name, picture)

#             # 🔹 GENERATE JWT
#             refresh = RefreshToken.for_user(user)

#             # 🔹 SAFE IMAGE HANDLING
#             # image_url = getattr(profile.image, 'url', None)
#             # uploaded image or initials avatar
#             image_url = profile.profile_image_url

#             # 🔹 RESPONSE (NO COOKIES)
#             return Response({
#                 "message": "Login successful",
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#                 "user": {
#                     "id": user.id,
#                     "email": user.email,
#                     "name": user.name,
#                     "auth_provider": profile.auth_provider,
#                     "image": image_url,
#                     "is_profile_complete": profile.is_profile_complete
#                 },
#                 "login_as": "user"
#             }, status=200)

#         except requests.exceptions.Timeout:
#             return Response({"error": "Google timeout"}, status=504)

#         except Exception as e:
#             print("GoogleLoginView ERROR:", str(e))
#             return Response({
#                 "error": "Something went wrong",
#                 "details": str(e)
#             }, status=500)

class GoogleLoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        try:

            access_token = request.data.get(
                "access_token"
            )

            if not access_token:

                return Response({
                    "error": "Access token required"
                }, status=400)

            # =====================================
            # GOOGLE USER INFO
            # =====================================
            google_res = requests.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                params={
                    "access_token": access_token
                },
                timeout=10
            )

            if google_res.status_code != 200:

                return Response({
                    "error": "Invalid Google token",
                    "details": google_res.text
                }, status=400)

            user_info = google_res.json()
            
            email = user_info.get("email")
            name = user_info.get("name", "")
            picture = user_info.get("picture", "")

            if not email:

                return Response({
                    "error": "Email not found"
                }, status=400)

            # =====================================
            # CREATE / GET USER
            # =====================================
            user, profile = handle_google_user(
                email,
                name,
                picture
            )
            is_plan = UserPlanSubscription.objects.filter(
                user=user,
                expiry_date__gte=timezone.now(),
                is_active=True
            ).exists()


            # =====================================
            # JWT TOKEN
            # =====================================
            refresh = RefreshToken.for_user(user)

            refresh["user_id"] = str(user.id)

            # =====================================
            # PROFILE IMAGE
            # =====================================
            image_url = profile.profile_image_url

            # =====================================
            # PROPERTY COUNTS
            # =====================================
            property_counts = get_property_remaining_counts(
                user
            )

            # =====================================
            # RESPONSE
            # =====================================
            return Response({

                "message": "Login successful",

                "access": str(
                    refresh.access_token
                ),

                "refresh": str(
                    refresh
                ),

                "login_as": "user",
                "is_plan": is_plan,

                "user": {

                    "id": str(user.id),

                    "email": user.email,

                    "name": user.name,

                    "auth_provider": profile.auth_provider,

                    "image": image_url,

                    "is_profile_complete": (
                        profile.is_profile_complete
                    ),

                    # # =================================
                    # # PROPERTY COUNTS
                    # # =================================

                    # "remaining_property": (
                    #     property_counts.get(
                    #         "remaining_property",
                    #         0
                    #     )
                    # ),

                    # "residential_remaining": (
                    #     property_counts.get(
                    #         "residential_remaining",
                    #         0
                    #     )
                    # ),

                    # "commercial_remaining": (
                    #     property_counts.get(
                    #         "commercial_remaining",
                    #         0
                    #     )
                    # ),

                    # "residential_used": (
                    #     property_counts.get(
                    #         "residential_used",
                    #         0
                    #     )
                    # ),

                    # "commercial_used": (
                    #     property_counts.get(
                    #         "commercial_used",
                    #         0
                    #     )
                    # ),

                    "total_properties": (
                        property_counts.get(
                            "total_properties",
                            0
                        )
                    ),
                    "remaining_property": property_counts.get(
                        "remaining_property",
                        0
                    ),

                    # "total_residential_limit": (
                    #     property_counts.get(
                    #         "total_residential_limit",
                    #         0
                    #     )
                    # ),

                    # "total_commercial_limit": (
                    #     property_counts.get(
                    #         "total_commercial_limit",
                    #         0
                    #     )
                    # )
                }

            }, status=200)

        except requests.exceptions.Timeout:

            return Response({
                "error": "Google timeout"
            }, status=504)

        except Exception as e:

            print(
                "GoogleLoginView ERROR:",
                str(e)
            )

            return Response({
                "error": "Something went wrong",
                "details": str(e)
            }, status=500)


#  COMMON FUNCTION (UNCHANGED)
# def handle_google_user(email, name):
#     user, _ = UserCreate.objects.get_or_create(
#         email=email,
#         defaults={"name": name, "is_verified": True}
#     )
#
#     profile, _ = UserProfile.objects.get_or_create(
#         user=user,
#         defaults={"auth_provider": "google"}
#     )
#
#     if profile.auth_provider != "google":
#         profile.auth_provider = "google"
#         profile.save()
#
#     return user, profile
#
#
#
# #  REDIRECT LOGIN
# class GoogleLoginRedirectView(APIView):
#
#     authentication_classes = []
#     permission_classes = []
#
#     def get(self, request):
#
#         redirect_uri = request.build_absolute_uri("/api/auth/google/callback/")
#
#         state = secrets.token_urlsafe(16)
#
#         # ✅ Store in session safely
#         request.session["google_oauth_state"] = state
#         request.session.modified = True
#
#         params = {
#             "client_id": settings.GOOGLE_CLIENT_ID,
#             "response_type": "code",
#             "scope": "openid email profile",
#             "redirect_uri": redirect_uri,
#             "prompt": "select_account",
#             "state": state
#         }
#
#         google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
#
#         return redirect(google_auth_url)
#
#
# # ✅ CALLBACK (FIXED)
# FRONTEND_URL = "http://localhost:5173" # change in production
#
# class GoogleCallbackView(APIView):
#
#     authentication_classes = []
#     permission_classes = []
#
#     def get(self, request):
#
#         try:
#             code = request.GET.get("code")
#             state = request.GET.get("state")
#
#             saved_state = request.session.get("google_oauth_state")
#
#             if not state or state != saved_state:
#                 return redirect(f"{FRONTEND_URL}/login?error=state_error")
#
#             if not code:
#                 return redirect(f"{FRONTEND_URL}/login?error=no_code")
#
#             redirect_uri = request.build_absolute_uri("/api/auth/google/callback/")
#
#             # ✅ EXCHANGE CODE FOR TOKEN
#             token_response = requests.post(
#                 "https://oauth2.googleapis.com/token",
#                 data={
#                     "code": code,
#                     "client_id": settings.GOOGLE_CLIENT_ID,
#                     "client_secret": settings.GOOGLE_CLIENT_SECRET,
#                     "redirect_uri": redirect_uri,
#                     "grant_type": "authorization_code",
#                 },
#                 timeout=10
#             )
#
#             if token_response.status_code != 200:
#                 return redirect(f"{FRONTEND_URL}/login?error=token_failed")
#
#             token_json = token_response.json()
#
#             id_token_value = token_json.get("id_token")
#             if not id_token_value:
#                 return redirect(f"{FRONTEND_URL}/login?error=no_id_token")
#
#             # ✅ VERIFY TOKEN
#             idinfo = id_token.verify_oauth2_token(
#                 id_token_value,
#                 google_requests.Request(),
#                 settings.GOOGLE_CLIENT_ID
#             )
#
#             email = idinfo.get("email")
#             name = idinfo.get("name", "")
#
#             user, profile = handle_google_user(email, name)
#
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#
#             # ✅ SEND DATA TO FRONTEND VIA URL
#             query_params = urlencode({
#                 "access": access_token,
#                 "username": profile.username or "",
#                 "email": user.email
#             })
#
#             response = redirect(f"{FRONTEND_URL}/google-success?{query_params}")
#
#             # ✅ STORE REFRESH TOKEN IN COOKIE
#             response.set_cookie(
#                 key="refresh_token",
#                 value=str(refresh),
#                 httponly=True,
#                 secure=not settings.DEBUG,  # ✅ works locally + prod
#                 samesite="Lax" if settings.DEBUG else "None",
#                 max_age=7 * 24 * 60 * 60,
#                 path="/"
#             )
#
#             request.session.pop("google_oauth_state", None)
#
#             return response
#
#         except requests.exceptions.Timeout:
#             return redirect(f"{FRONTEND_URL}/login?error=timeout")
#
#         except Exception as e:
#             return redirect(f"{FRONTEND_URL}/login?error=server_error")




class FacebookLoginRedirectView(APIView):

    def get(self, request):
        redirect_uri = "http://127.0.0.1:8000/auth/facebook/callback/"

        facebook_auth_url = (
            "https://www.facebook.com/v19.0/dialog/oauth?"
            f"client_id={settings.FACEBOOK_APP_ID}"
            f"&redirect_uri={settings.FACEBOOK_REDIRECT_URI}"
            "&scope=email"
        )

        return redirect(facebook_auth_url)


import jwt
import uuid

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import UserCreate, UserProfile
from .serializers import UserProfileSerializer


class UserProfileView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]


    # ---------------------------------
    # GET USER FROM JWT TOKEN
    # ---------------------------------
    def get_user_from_token(self, request):

        auth_header = request.headers.get(
            "Authorization"
        )

        if not auth_header:
            return (
                None,
                Response(
                    {
                        "error":"Authorization header missing"
                    },
                    status=401
                )
            )


        try:
            token = auth_header.split(" ")[1]

            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )


            user_id = decoded.get(
                "user_id"
            )


            # UUID support
            user_uuid = uuid.UUID(
                str(user_id)
            )


            user = UserCreate.objects.get(
                id=user_uuid
            )


            return user,None


        except jwt.ExpiredSignatureError:
            return (
                None,
                Response(
                    {
                        "error":"Token expired"
                    },
                    status=401
                )
            )


        except jwt.InvalidTokenError:
            return (
                None,
                Response(
                    {
                        "error":"Invalid token"
                    },
                    status=401
                )
            )


        except UserCreate.DoesNotExist:
            return (
                None,
                Response(
                    {
                        "detail":"User not found",
                        "code":"user_not_found"
                    },
                    status=404
                )
            )


        except ValueError:
            return (
                None,
                Response(
                    {
                        "error":"Invalid UUID token"
                    },
                    status=400
                )
            )


        except Exception as e:
            print(e)

            return (
                None,
                Response(
                    {
                        "error":"Something went wrong"
                    },
                    status=400
                )
            )


    # ---------------------------------
    # GET PROFILE
    # ---------------------------------
    def get(self,request):

        user,error = self.get_user_from_token(
            request
        )

        if error:
            return error


        profile,_ = UserProfile.objects.get_or_create(
            user=user
        )


        serializer = UserProfileSerializer(
            profile,
            context={
                "request":request
            }
        )


        return Response(
            serializer.data
        )


    # ---------------------------------
    # UPDATE PROFILE
    # ---------------------------------
    def put(self,request):

        user,error = self.get_user_from_token(
            request
        )

        if error:
            return error


        profile,_ = UserProfile.objects.get_or_create(
            user=user
        )


        serializer = UserProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={"request": request}
        )


        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )


        return Response(
            serializer.errors,
            status=400
        )



import uuid
import jwt
import cloudinary.uploader

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import UserCreate, UserProfile


class UserProfileImageUpdateView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]


    # ----------------------------
    # GET USER FROM TOKEN
    # ----------------------------
    def get_user_from_token(
        self,
        request
    ):

        auth_header = request.headers.get(
            "Authorization"
        )

        if not auth_header:
            return (
                None,
                Response(
                    {
                        "error":"Authorization header missing"
                    },
                    status=401
                )
            )


        try:
            token = auth_header.split(
                " "
            )[1]


            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )


            # UUID FIX
            user_uuid = uuid.UUID(
                str(
                    decoded.get(
                        "user_id"
                    )
                )
            )


            user = UserCreate.objects.get(
                id=user_uuid
            )


            return user,None


        except jwt.ExpiredSignatureError:
            return (
                None,
                Response(
                    {
                        "error":"Token expired"
                    },
                    status=401
                )
            )


        except jwt.InvalidTokenError:
            return (
                None,
                Response(
                    {
                        "error":"Invalid token"
                    },
                    status=401
                )
            )


        except UserCreate.DoesNotExist:
            return (
                None,
                Response(
                    {
                        "error":"User not found"
                    },
                    status=404
                )
            )


        except ValueError:
            return (
                None,
                Response(
                    {
                        "error":"Invalid UUID token"
                    },
                    status=401
                )
            )


        except Exception as e:
            print(e)

            return (
                None,
                Response(
                    {
                        "error":"Invalid or expired token"
                    },
                    status=401
                )
            )


    # ----------------------------
    # UPDATE PROFILE IMAGE
    # ----------------------------
    def put(
        self,
        request
    ):

        user,error = self.get_user_from_token(
            request
        )

        if error:
            return error


        if "image" not in request.FILES:
            return Response(
                {
                    "error":"Image file is required"
                },
                status=400
            )


        profile,_ = UserProfile.objects.get_or_create(
            user=user
        )


        # delete old cloudinary image
        try:
            if (
                profile.image and
                profile.image.public_id
            ):
                cloudinary.uploader.destroy(
                    profile.image.public_id
                )
        except:
            pass


        # save new image
        profile.image = request.FILES[
            "image"
        ]

        profile.save()


        return Response(
            {
                "message":"Profile image updated successfully",
                "image_url":profile.image.url
            }
        )


# class RefreshTokenView(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):
#         refresh_token = request.data.get("refresh")

#         if not refresh_token:
#             return Response({"error": "Refresh token missing"}, status=401)

#         try:
#             #  Decode refresh token manually
#             decoded = jwt.decode(
#                 refresh_token,
#                 settings.SECRET_KEY,
#                 algorithms=["HS256"]
#             )

#             user_id = decoded.get("user_id")

#             #  Fetch user from YOUR model
#             user = UserCreate.objects.get(id=user_id)

#             #  Create new access token manually
#             access_payload = {
#                 "user_id": user.id,
#                 "exp": datetime.utcnow() + timedelta(minutes=2),
#                 "iat": datetime.utcnow(),
#             }

#             new_access_token = jwt.encode(
#                 access_payload,
#                 settings.SECRET_KEY,
#                 algorithm="HS256"
#             )

#             return Response({
#                 "access": new_access_token,
#                 "refresh": refresh_token  # reuse same refresh
#             })

#         except UserCreate.DoesNotExist:
#             return Response({"error": "User not found"}, status=401)

#         except jwt.ExpiredSignatureError:
#             return Response({"error": "Refresh token expired"}, status=401)

#         except jwt.InvalidTokenError:
#             return Response({"error": "Invalid token"}, status=401)




# class RefreshTokenView(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):
#         refresh_token = request.data.get("refresh") or request.COOKIES.get("refresh_token")

#         if not refresh_token:
#             return Response(
#                 {"error": "Refresh token missing"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             # ✅ Use SimpleJWT (same as agent)
#             refresh = RefreshToken(refresh_token)

#             new_access_token = str(refresh.access_token)
#             new_refresh_token = str(refresh)

#             return Response({
#                 "access": new_access_token,
#                 "refresh": new_refresh_token
#             })

#         except TokenError:
#             return Response(
#                 {"error": "Invalid or expired refresh token"},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        refresh_token = (
            request.data.get("refresh")
            or request.COOKIES.get("refresh_token")
        )

        if not refresh_token:
            return Response(
                {"error": "Refresh token missing"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)


            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=200)

        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token"},
                status=401
            )



class AmenitiesListCreateView(APIView):

    def get(self, request):
        amenities = Amenities.objects.all().order_by("-id")
        serializer = AmenitiesSerializer(amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitiesSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserChangePasswordView(APIView):

    authentication_classes = []  # bypass default auth
    permission_classes = []

    def post(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return Response({"message": "Authorization token missing"}, status=401)

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
        except Exception:
            return Response({"message": "Invalid token"}, status=401)

        # 🔎 Find user
        user_create = UserCreate.objects.filter(id=user_id).first()

        if not user_create:
            return Response({"message": "User not found"}, status=404)

        profile = UserProfile.objects.filter(user=user_create).first()

        if not profile:
            return Response({"message": "Profile not found"}, status=404)

        # ❌ BLOCK GOOGLE / FACEBOOK
        if profile.auth_provider in ["google", "facebook"]:
            return Response(
                {
                    "message": f"Password change not allowed for {profile.auth_provider} login users"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not check_password(old_password, user_create.password):
            return Response(
                {"message": "Old password incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_password:
            return Response(
                {"message": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_create.password = make_password(new_password)
        user_create.save()

        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK
        )

class LogoutAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        response = Response({"message": "Logged out"})
        response.delete_cookie("refresh_token")

        return response


from agents.authentication import AgentJWTAuthentication
class InboxCreateAPIView(APIView):

    authentication_classes = []   # public message form
    permission_classes = []

    def post(self, request):

        serializer = InboxSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Message Submitted Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class InboxListAPIView(APIView):

    authentication_classes = [AgentJWTAuthentication]  # ✅ FIX
    permission_classes = [IsAuthenticated]

    def get(self, request):
        agent = request.user

        inbox_messages = Inbox.objects.filter(
            pin_code=str(agent.pin_code),
            is_removed=False
        ).order_by("-created_at")

        serializer = InboxSerializer(inbox_messages, many=True)

        return Response({
            "message": "Inbox messages fetched successfully",
            "data": serializer.data
        })


class InboxDeleteAPIView(APIView):
    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        agent = request.user

        try:
            message = Inbox.objects.get(
                id=id,
                pin_code=str(agent.pin_code),
                is_removed=False
            )
        except Inbox.DoesNotExist:
            return Response({
                "status": False,
                "message": "Message not found"
            }, status=404)

        # Soft delete
        message.is_removed = True
        message.save()

        return Response({
            "status": True,
            "message": "Message deleted successfully"
        })


class AgentRegisterAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = AgentRegisterSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            agent = serializer.save()

            profile_image = (
                agent.profile_image.url
                if agent.profile_image
                else agent.avatar_url
            )

#             # Build response
#             return Response({
#                 "status": True,
#                 "message": "Agent Registered Successfully",
#                 "agent_details": {
#                     "agent_code": getattr(agent, "agent_code", None),
#                     "username": agent.username,
#                     "email": agent.email,
#                     "phone_number": agent.phone_number,
#                     "agent_type": agent.agent_type,
#                     "plan": plan_name,
#                     "profile_image": profile_image
#                 }
#             }, status=status.HTTP_201_CREATED)

#         # If serializer not valid
#         return Response({
#             "status": False,
#             "errors": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)



class AgentLoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = AgentLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)

            # Add role into token
            refresh['agent_type'] = user.agent_type
            refresh['agent_code'] = user.agent_code
            refresh['username'] = user.username

            profile_image = user.profile_image.url if user.profile_image else user.avatar_url

            agent_details = {
                "agent_id": user.agent_code,
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number,
                "agent_type": user.agent_type,
                "city": user.city or "",
                "profile_image": profile_image
            }

            response = Response({
                "message": "Agent login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),   # ← ADD THIS
                "agent_details": agent_details,
                "login_as": "agent",
                # "type": user.agent_type,
            })

            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite="Lax"
            )
            return response

        return Response(serializer.errors, status=400)

class AgentForgotPasswordAPI(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=400)

        try:
            agent = AgentUserProfile.objects.get(email=email)

            # ❗ Only verified agents (optional)
            if not agent.is_active:
                return Response({"error": "Agent is inactive"}, status=400)

            # ⛔ Rate limit (30 sec)
            if agent.reset_otp_created_at and \
               timezone.now() < agent.reset_otp_created_at + timedelta(seconds=30):
                return Response(
                    {"error": "Please wait before requesting OTP again"},
                    status=429
                )

            # ✅ Generate OTP
            otp = str(random.randint(100000, 999999))

            agent.reset_otp = otp
            agent.reset_otp_created_at = timezone.now()
            agent.save(update_fields=["reset_otp", "reset_otp_created_at"])

            # ✅ SEND EMAIL HERE
            send_otp_email(agent.email, otp)

            return Response({"message": "OTP sent to email"}, status=200)

        except AgentUserProfile.DoesNotExist:
            return Response({"error": "Agent not found"}, status=404)

class AgentResendForgotOTP(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "Email is required"},
                status=400
            )

        try:
            agent = AgentUserProfile.objects.get(email=email)

            # ❗ IMPORTANT: This is FORGOT PASSWORD → allow verified users
            if not agent.is_active:
                return Response(
                    {"error": "Agent account is inactive"},
                    status=400
                )

            # ❌ If OTP never generated
            if not agent.reset_otp_created_at:
                return Response(
                    {"error": "OTP not generated yet. Please request forgot password first."},
                    status=400
                )

            # ⛔ RATE LIMIT (30 sec)
            if timezone.now() < agent.reset_otp_created_at + timedelta(seconds=30):
                return Response(
                    {"error": "Please wait before requesting OTP again"},
                    status=429
                )

            # ✅ GENERATE NEW OTP
            otp = str(random.randint(100000, 999999))

            agent.reset_otp = otp
            agent.reset_otp_created_at = timezone.now()
            agent.save(update_fields=["reset_otp", "reset_otp_created_at"])

            # ✅ SEND EMAIL
            send_otp_email(agent.email, otp)

            return Response(
                {"message": "OTP resent successfully"},
                status=200
            )

        except AgentUserProfile.DoesNotExist:
            return Response(
                {"error": "Agent not found"},
                status=404
            )


class AgentVerifyForgotOTP(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"error": "Email and OTP required"}, status=400)

        try:
            agent = AgentUserProfile.objects.get(email=email)

            # ❌ OTP mismatch
            if agent.reset_otp != otp:
                return Response({"error": "Invalid OTP"}, status=400)

            # ⏰ Expiry (5 min)
            if agent.reset_otp_created_at < timezone.now() - timedelta(minutes=5):
                return Response({"error": "OTP expired"}, status=400)

            # ✅ Generate reset token
            token = uuid.uuid4()
            agent.reset_token = token

            # clear OTP
            agent.reset_otp = None
            agent.reset_otp_created_at = None

            agent.save(update_fields=["reset_token", "reset_otp", "reset_otp_created_at"])

            return Response({
                "message": "OTP verified",
                "reset_token": str(token)
            })

        except AgentUserProfile.DoesNotExist:
            return Response({"error": "Agent not found"}, status=404)

class AgentChangePasswordAPI(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        # ✅ Get token
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return Response({"error": "Reset token missing"}, status=400)

        try:
            token = auth_header.split(" ")[1]
        except:
            return Response({"error": "Invalid token format"}, status=400)

        new_password = request.data.get("new_password")

        if not new_password:
            return Response(
                {"error": "new_password is required"},
                status=400
            )

        try:
            validate_password(new_password)  
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        try:
            agent = AgentUserProfile.objects.get(reset_token=token)

            agent.set_password(new_password)
            agent.reset_token = None
            agent.save(update_fields=["password", "reset_token"])

            return Response(
                {"message": "Password changed successfully"},
                status=200
            )

        except AgentUserProfile.DoesNotExist:
            return Response(
                {"error": "Invalid or expired token"},
                status=400
            )


class AgentPendingRegisterAPIView(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("AUTH HEADER:", request.headers.get("Authorization"))
        print("USER:", request.user)
        print("IS AUTHENTICATED:", request.user.is_authenticated)
        
        data = request.data
        email = str(data.get("email", "")).strip().lower()
        password = str(data.get("password", "")).strip()
        agent_type = str(data.get("agent_type", "")).strip().lower()
        plan_id = data.get("plan_id")
        full_name = str(data.get("full_name", "")).strip()
        phone_number = str(data.get("phone_number", "")).strip()
        city = str(data.get("city", "")).strip()
        pin_code = str(data.get("pin_code", "")).strip()
        address = str(data.get("address", "")).strip()
        years_of_experience = data.get("years_of_experience")
        total_deals_served = data.get("total_deals_served", 0)

        if not re.fullmatch(r"\d{10}", phone_number):
            return Response(
                {
                    "status": False,
                    "message": "Mobile number must contain exactly 10 digits."
                },
                status=400
            )

        if not re.fullmatch(r"\d{6}", pin_code):
            return Response(
                {
                    "status": False,
                    "message": "Pincode must contain exactly 6 digits."
                },
                status=400
            )

        try:
            years_of_experience = (
                int(years_of_experience)
                if years_of_experience not in [None, ""]
                else None
            )

            deals_closed = (
                int(total_deals_served)
                if total_deals_served not in [None, ""]
                else 0
            )

        except ValueError:

            return Response({
                "status": False,
                "message": "years_of_experience and total_deals_served must be valid numbers."
            }, status=400)

        if not all([
            email,
            password,
            agent_type,
            full_name,
            phone_number,
            city,
            pin_code,
            address,
            years_of_experience,
            total_deals_served
        ]):
            return Response({
                "status": False,
                "message": "All fields are required."
            }, status=400)


        try:
            validate_email(email)

        except ValidationError:

            return Response({
                "status": False,
                "message": "Invalid email format."
            }, status=400)


        if PendingAgentRegistration.objects.filter(
            email=email,
            status='pending'
        ).exists():

            return Response({
                "status": False,
                "message": "You have already submitted a request."
            }, status=400)

        if AgentUserProfile.objects.filter(
            email=email
        ).exists():

            return Response({
                "status": False,
                "message": "Account already exists. Please login."
            }, status=400)

        valid_agent_types = [
            "basic",
            "premium",
            "elite"
        ]

        if agent_type not in valid_agent_types:

            return Response({
                "status": False,
                "message": "Invalid agent type."
            }, status=400)

        # =====================================================
        # PLAN HANDLING
        # =====================================================

        premium_plan = None
        elite_plan = None

        # ================= ELITE =================

        if agent_type == "elite":

            if not plan_id:

                return Response({
                    "status": False,
                    "message": "Elite plan required"
                }, status=400)

            elite_plan = ElitePlan.objects.filter(
                id=plan_id
            ).first()

            if not elite_plan:

                return Response({
                    "status": False,
                    "message": "Invalid elite plan"
                }, status=400)

        # ================= PREMIUM =================

        elif agent_type == "premium":

            if not plan_id:

                return Response({
                    "status": False,
                    "message": "Premium plan required"
                }, status=400)

            premium_plan = PremiumPlan.objects.filter(
                id=plan_id
            ).first()

            if not premium_plan:

                return Response({
                    "status": False,
                    "message": "Invalid premium plan"
                }, status=400)

        # ================= BASIC =================
        # NO PLAN REQUIRED

        # =====================================================
        # CREATE PENDING REGISTRATION
        # =====================================================
        print("agent_type =", request.POST.get("agent_type"))
        print("plan_id =", request.POST.get("plan_id"))
        print("plan_name =", request.POST.get("plan_name"))

        PendingAgentRegistration.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=password,
            city=city,
            pin_code=pin_code,
            address=address,
            agent_type=agent_type,
            premium_plan=premium_plan,
            elite_plan=elite_plan,
            years_of_experience=years_of_experience,
            deals_closed=deals_closed,
            submitted_by=request.user if request.user.is_authenticated else None,
            status="pending"
        )

        return Response({
            "status": True,
            "message": "Registration submitted. Waiting for admin approval."
        }, status=201)

class AgentTokenRefreshAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # Get refresh token from body or cookie
        refresh_token = request.data.get("refresh") or request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create RefreshToken instance
            refresh = RefreshToken(refresh_token)

            # New access token
            new_access_token = str(refresh.access_token)

            # Optional: rotate refresh token for security
            new_refresh_token = str(refresh)  # refresh token can remain the same or rotate

            response = Response({
                "access": new_access_token,
                "refresh": new_refresh_token
            })

            # Optional: update the cookie if using cookie-based refresh token
            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                httponly=True,
                secure=False,
                samesite="Lax"
            )

            return response

        except TokenError:
            return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)



class PremiumFeatureAPIView(APIView):
    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.agent_type not in ["premium", "elite"]:
            return Response({
                "error": "Only Premium and Elite agents allowed"
            }, status=403)

        return Response({
            "message": "Welcome Premium/Elite Agent"
        })
class EliteFeatureAPIView(APIView):
    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.agent_type != "elite":
            return Response({
                "error": "Only Elite agents allowed"
            }, status=403)

        return Response({
            "message": "Welcome Elite Agent"
        })


from rest_framework_simplejwt.tokens import AccessToken

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SubmitAgentReviewAPIView(APIView):

    permission_classes = []
    authentication_classes = []

    def get_user_from_token(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None, Response(
                {"error": "Authorization header missing"},
                status=401
            )

        try:

            token = auth_header.split(" ")[1]

            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            user_id = decoded.get("user_id")

            if not user_id:
                return None, Response(
                    {"error": "Invalid token payload"},
                    status=401
                )

            user = UserCreate.objects.filter(
                id=user_id
            ).first()

            if not user:
                return None, Response(
                    {"error": "User not found"},
                    status=404
                )

            return user, None

        except jwt.ExpiredSignatureError:
            return None, Response(
                {"error": "Token expired"},
                status=401
            )

        except jwt.InvalidTokenError:
            return None, Response(
                {"error": "Invalid token"},
                status=401
            )

        except Exception as e:
            return None, Response(
                {"error": str(e)},
                status=400
            )

    def post(self, request, agent_id):

        user, error = self.get_user_from_token(request)

        if error:
            return error

        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "full_name": user.name or "",
                "mobile": user.mobile or "",
                "auth_provider": "mobile",
            }
        )

        updated = False

        # full name sync
        if user.name and profile.full_name != user.name:
            profile.full_name = user.name
            updated = True

        if user.mobile and profile.mobile != user.mobile:
            profile.mobile = user.mobile
            updated = True

        if hasattr(profile, "image"):

            try:

                if profile.image:
                    pass

            except Exception:
                pass

        if updated:
            profile.save()

        try:

            try:

                agent = AgentUserProfile.objects.get(
                    id=uuid.UUID(agent_id)
                )

            except ValueError:

                agent = AgentUserProfile.objects.get(
                    agent_code=agent_id
                )

        except AgentUserProfile.DoesNotExist:

            return Response(
                {"error": "Agent not found"},
                status=404
            )

        if AgentReview.objects.filter(
            agent=agent,
            user=user
        ).exists():

            return Response(
                {
                    "message":
                    "You already reviewed this agent"
                },
                status=400
            )
        
        serializer = AgentReviewSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                agent=agent,
                user=user
            )

            return Response({
                "status": True,
                "message": "Review submitted successfully"
            }, status=201)

        return Response(
            serializer.errors,
            status=400
        )

from developer.models import UserCreate, UserProfile
import jwt
from django.conf import settings

class ToggleReviewLikeAPIView(APIView):
    permission_classes = []            # 🔥 disable DRF auth
    authentication_classes = []        # 🔥 avoid mismatch

    def get_user_from_token(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None, Response({"error": "Authorization header missing"}, status=401)

        try:
            token = auth_header.split(" ")[1]

            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            user_id = decoded.get("user_id")

            if not user_id:
                return None, Response({"error": "Invalid token payload"}, status=401)

            user = UserCreate.objects.filter(id=user_id).first()

            if not user:
                return None, Response({"error": "User not found"}, status=404)

            return user, None

        except jwt.ExpiredSignatureError:
            return None, Response({"error": "Token expired"}, status=401)

        except jwt.InvalidTokenError:
            return None, Response({"error": "Invalid token"}, status=401)

        except Exception as e:
            return None, Response({"error": str(e)}, status=400)

    def post(self, request, review_id):

        # ✅ STEP 1: Get logged-in user
        user, error = self.get_user_from_token(request)
        if error:
            return error

        # ✅ STEP 2: Get Review (UUID supported)
        try:
            review = AgentReview.objects.get(id=review_id)
        except AgentReview.DoesNotExist:
            return Response({"error": "Review not found"}, status=404)

        # ✅ STEP 3: Ensure profile exists (optional but safe)
        UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "full_name": user.name or "",
                "auth_provider": "mobile"
            }
        )

        # ✅ STEP 4: Toggle Like
        if review.likes.filter(id=user.id).exists():
            review.likes.remove(user)
            liked = False
        else:
            review.likes.add(user)
            liked = True

        return Response({
            "liked": liked,
            "total_likes": review.likes.count()
        })

class AgentListFrontendAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        agent_type = request.GET.get("type")  # all / Agent / PremiumAgent / EliteAgent

        agents = AgentUserProfile.objects.filter(is_active=True)

        # Mapping frontend → DB values
        type_mapping = {
            "Agent": "basic",
            "PremiumAgent": "premium",
            "EliteAgent": "elite"
        }

        if agent_type and agent_type != "all":
            mapped_type = type_mapping.get(agent_type)

            if mapped_type:
                agents = agents.filter(agent_type=mapped_type)
            else:
                return Response(
                    {"error": "Invalid agent type"},
                    status=400
                )

        serializer = AgentListFrontendSerializer(agents, many=True)
        return Response(serializer.data)

class AgentReviewListAPIView(APIView):

    authentication_classes = [UserJWTAuthentication]  # ✅ ADD THIS
    permission_classes = [AllowAny]  # keep public access

    def get(self, request, agent_id):

        try:
            try:
                agent = AgentUserProfile.objects.get(id=uuid.UUID(agent_id))
            except ValueError:
                agent = AgentUserProfile.objects.get(agent_code=agent_id)

        except AgentUserProfile.DoesNotExist:
            return Response({"error": "Agent not found"}, status=404)

        reviews = AgentReview.objects.filter(agent=agent).order_by("-created_at")

        serializer = AgentReviewSerializer(
            reviews,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)
    
class AgentListAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []   # ⭐ IMPORTANT FIX

    def get(self, request):
        agents = AgentUserProfile.objects.all()
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data)

class AgentProfileAPIView(APIView):
    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    # 🔹 Get Profile
    def get(self, request):
        serializer = AgentProfileSerializer(request.user)
        return Response({
            "status": True,
            "data": serializer.data
        })

    # 🔹 Update Profile
    def patch(self, request):
        serializer = AgentProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Profile Updated Successfully",
                "data": serializer.data
            })
        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=400)

    # 🔹 PUT same as PATCH
    def put(self, request):
        return self.patch(request)

class PublicAgentProfileAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, agent_code):
        try:
            agent = AgentUserProfile.objects.get(agent_code=agent_code)

            serializer = AgentProfileSerializer(agent, context={'request': request})

            return Response({
                "status": True,
                "data": serializer.data
            })

        except AgentUserProfile.DoesNotExist:
            return Response({
                "status": False,
                "message": "Agent not found"
            }, status=404)




from rest_framework.exceptions import AuthenticationFailed


class AgentJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")   # ✅ CHANGE HERE

        if not user_id:
            raise AuthenticationFailed("Invalid token")

        try:
            user_uuid = uuid.UUID(user_id)
            return AgentUserProfile.objects.get(id=user_uuid)
        except Exception:
            raise AuthenticationFailed("Agent not found")
        

from collections import defaultdict

from collections import defaultdict

class PlanListAPIView(APIView):

    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    # ================= HELPERS =================

    def get_premium_key(self, validity):
        return {
            90: "starter",
            180: "growth",
            365: "pro"
        }.get(validity)

    def get_elite_key(self, days):
        return {
            90: "silver",
            180: "gold",
            365: "platinum"
        }.get(days)

    def format_duration(self, days):
        return {
            90: "3 Months",
            180: "6 Months",
            365: "12 Months"
        }.get(days, f"{days} Days")

    # ================= FEATURE BUILDERS =================

    def build_premium_features(self, plan):
        return [
            f"{plan.total_listing} Property Listings",
            f"{plan.residential_limit} Residential Listings",
            f"{plan.commercial_limit} Commercial Listings",
            f"Edit: {plan.edit}",
            f"Enquiries: {plan.enquiries.strip()}",
            f"{plan.priority_search}",
            f"{plan.meta_ads.strip()}",
            f"{plan.bulk_whatsapp}",
            f"{plan.poster} Posters",
            f"{plan.social_media.strip()}",
            f"Lead Follow: {plan.lead_follow}",
            f"{plan.lead_management.strip()}",
            f"{plan.validity} Days Validity"
        ]

    def build_elite_features(self, plan):
        return [
            f"{plan.total_property_listings} Property Listings",
            f"{plan.featured_listings_limit} featured Listings",
            f"{plan.priority_search.strip()}",
            f"{plan.meta_ads_promotion.strip()}",
            f"{plan.bulk_whatsapp_messages}",
            f"{plan.poster_creation}",
            f"{plan.social_media_marketing.strip()}",
            f"{plan.lead_followup_support}",
            f"{plan.lead_management.strip()}",
            f"{plan.plan_validity_days} Days Validity"
        ]

    def build_ad_features(self, ad):
        return [
            f"{ad.ads_per_day} Ad(s) per day",
            f"Display Duration: {ad.display_seconds} seconds",
            f"Format: {ad.ad_format.capitalize()}",
            f"Package Type: {ad.package_type.capitalize()}",
            f"Price per day: ₹{ad.price_per_day}"
        ]

    def build_reel_features(self, reel):
        return [
            f"Format: {reel.reel_format}",
            f"Duration: {reel.duration}",
            f"{reel.description}",
            f"Price per day: ₹{reel.price_per_day}"
        ]

    # ================= GET =================

    def get(self, request):

        agent = request.user

        premium_plans_qs = PremiumPlan.objects.all()
        elite_plans_qs = ElitePlan.objects.all()

        ad_packages = AdvertisementPackage.objects.all()
        reel_packages = ReelPackage.objects.all()

        # ================= CURRENT PLAN =================

        # current_plan = None

        # if getattr(agent, "plan", None):

        #     plan = agent.plan

        #     current_plan = {
        #         "plan_id": str(plan.id),
        #         "plan_type": "premium",
        #         "plan_key": self.get_premium_key(plan.validity),
        #         "name": plan.name,
        #         "start_date": getattr(agent, "plan_start_date", None),
        #         "expiry_date": getattr(agent, "plan_expiry_date", None),
        #         "is_active": agent.is_plan_active()
        #     }

        # elif getattr(agent, "elite_plan", None):

        #     elite = agent.elite_plan

        #     current_plan = {
        #         "plan_id": str(elite.id),
        #         "plan_type": "elite",
        #         "plan_key": self.get_elite_key(elite.plan_validity_days),
        #         "name": elite.name,
        #         "start_date": getattr(agent, "plan_start_date", None),
        #         "expiry_date": getattr(agent, "plan_expiry_date", None),
        #         "is_active": agent.is_plan_active()
        #     }
        active_subscriptions = list(

            Subscription.objects.filter(
                agent=agent,
                is_active=True
            )

        )

        # =================================================
        # SORT BY PLAN PRICE (HIGHER PRICE = HIGHER PRIORITY)
        # =================================================

        def get_subscription_price(subscription):

            if subscription.plan_type == "premium":

                plan = PremiumPlan.objects.filter(
                    name=subscription.plan_name
                ).first()

                if plan:
                    return plan.price

            elif subscription.plan_type == "elite":

                plan = ElitePlan.objects.filter(
                    name=subscription.plan_name
                ).first()

                if plan:
                    return plan.price

            return 0
        active_subscriptions.sort(
            key=get_subscription_price,
            reverse=True
        )
        
        current_plan = None

        if active_subscriptions:

            highest_subscription = active_subscriptions[0]

            if highest_subscription.plan_type == "premium":

                plan = PremiumPlan.objects.filter(
                    name=highest_subscription.plan_name
                ).first()

                if plan:

                    current_plan = {
                        "plan_id": str(plan.id),
                        "plan_type": "premium",
                        "plan_key": self.get_premium_key(plan.validity),
                        "name": plan.name,
                        "start_date": highest_subscription.start_date,
                        "expiry_date": highest_subscription.end_date,
                        "is_active": highest_subscription.is_active
                    }

            elif highest_subscription.plan_type == "elite":

                plan = ElitePlan.objects.filter(
                    name=highest_subscription.plan_name
                ).first()

                if plan:

                    current_plan = {
                        "plan_id": str(plan.id),
                        "plan_type": "elite",
                        "plan_key": self.get_elite_key(
                            plan.plan_validity_days
                        ),
                        "name": plan.name,
                        "start_date": highest_subscription.start_date,
                        "expiry_date": highest_subscription.end_date,
                        "is_active": highest_subscription.is_active
                    }

        # ================= PREMIUM =================

        premium_plans = []

        for plan in premium_plans_qs:

            premium_plans.append({

                # ✅ CHANGED id -> plan_id
                "plan_id": str(plan.id),

                # ✅ ADDED PLAN TYPE
                "plan_type": "premium",

                "plan_key": self.get_premium_key(
                    plan.validity
                ),

                "label": plan.name,

                "duration": self.format_duration(
                    plan.validity
                ),

                "price": plan.price,

                "savings": self.format_duration(
                    plan.validity
                ),

                "features": self.build_premium_features(
                    plan
                )
            })

        # ================= ELITE =================

        elite_plans = []

        for plan in elite_plans_qs:

            elite_plans.append({

                # ✅ CHANGED id -> plan_id
                "plan_id": str(plan.id),

                # ✅ ADDED PLAN TYPE
                "plan_type": "elite",

                "plan_key": self.get_elite_key(
                    plan.plan_validity_days
                ),

                "label": plan.name,

                "duration": self.format_duration(
                    plan.plan_validity_days
                ),

                "price": plan.price,

                "savings": self.format_duration(
                    plan.plan_validity_days
                ),

                "features": self.build_elite_features(
                    plan
                )
            })

        # ================= GROUPED ADS =================

        ads_grouped = defaultdict(lambda: {
            "id": None,
            "name": "",
            "plans": []
        })

        for ad in ad_packages:

            group = ads_grouped[ad.name]

            group["id"] = group["id"] or str(ad.id)
            group["name"] = ad.name

            group["plans"].append({

                "plan_id": str(ad.id),

                "type": ad.package_type.lower(),

                "plan_type": ad.ad_format,

                "price_per_day": ad.price_per_day,

                "features": self.build_ad_features(ad)
            })

        formatted_ads = list(
            ads_grouped.values()
        )

        # ================= GROUPED REELS =================

        reels_grouped = defaultdict(lambda: {
            "id": None,
            "name": "",
            "plans": []
        })

        for reel in reel_packages:

            group = reels_grouped[reel.name]

            group["id"] = group["id"] or str(reel.id)
            group["name"] = reel.name

            group["plans"].append({

                "plan_id": str(reel.id),

                "type": reel.reel_type.lower(),

                "plan_type": reel.reel_type,

                "price_per_day": reel.price_per_day,

                "features": self.build_reel_features(
                    reel
                )
            })

        formatted_reels = list(
            reels_grouped.values()
        )
        
        # ================= ACTIVE SUBSCRIPTIONS =================

        # active_subscriptions = Subscription.objects.filter(
        #     agent=agent,
        #     is_active=True
        # ).order_by("start_date")

        upgrade_subscription = None

        # subscriptions_data = []

        # for subscription in active_subscriptions:

        #     data = {
        #         "subscription_id": str(subscription.id),
        #         "plan_name": subscription.plan_name,
        #         "property_limit": subscription.property_limit,
        #         "used_listings": subscription.used_listings,
        #         "remaining_listings": (
        #             subscription.property_limit -
        #             subscription.used_listings
        #         ),
        #         "start_date": subscription.start_date,
        #         "end_date": subscription.end_date,
        #         "is_active": subscription.is_active
        #     }

        #     subscriptions_data.append(data)

        # if len(subscriptions_data) >= 2:
        #     upgrade_subscription = subscriptions_data[1]

        # is_upgrade_plan = (
        #     upgrade_subscription is not None
        # )
        subscriptions_data = []

        for subscription in active_subscriptions:

            subscriptions_data.append({

                "subscription_id": str(subscription.id),

                "plan_name": subscription.plan_name,

                "property_limit": subscription.property_limit,

                "used_listings": subscription.used_listings,

                "remaining_listings": (
                    subscription.property_limit -
                    subscription.used_listings
                ),

                "start_date": subscription.start_date,

                "end_date": subscription.end_date,

                "is_active": subscription.is_active

            })

        current_subscription = (
            subscriptions_data[0]
            if len(subscriptions_data) >= 1
            else None
        )

        upgrade_subscription = (
            subscriptions_data[1]
            if len(subscriptions_data) >= 2
            else None
        )

        is_upgrade_plan = (
            upgrade_subscription is not None
        )
        # ================= PLAN RESPONSE =================

        plans_response = []

        if getattr(agent, "elite_plan", None):

            plans_response.append({
                "id": "elite",
                "name": "Elite Agent",
                "plans": elite_plans
            })

        elif getattr(agent, "plan", None):

            plans_response.append({
                "id": "premium",
                "name": "Premium Agent",
                "plans": premium_plans
            })

        else:

            plans_response = [
                {
                    "id": "premium",
                    "name": "Premium Agent",
                    "plans": premium_plans
                },
                {
                    "id": "elite",
                    "name": "Elite Agent",
                    "plans": elite_plans
                }
            ]

        # current_subscription = None
        # upgrade_subscription = None

        # if len(subscriptions_data) >= 1:
        #     current_subscription = subscriptions_data[0]

        # if len(subscriptions_data) >= 2:
        #     upgrade_subscription = subscriptions_data[1]

        return Response({

            "is_upgrade_plan": (
                upgrade_subscription is not None
            ),

            "current_plan": current_plan,

            "current_active_subscriptions": {
                "current_plan": current_subscription,
                "upgrade_plan": upgrade_subscription
            },

            "plans": plans_response,

            "advertisement_packages": formatted_ads,

            "reel_packages": formatted_reels

        })      

        # # ================= FINAL RESPONSE =================

        # return Response({
        #     "is_upgrade_plan": is_upgrade_plan,

        #     "current_plan": current_plan,

        #     "upgrade_plan": upgrade_subscription,

        #     "current_active_subscriptions":
        #         subscriptions_data,


        #     # "plans": [

        #     #     {
        #     #         "id": "premium",
        #     #         # "plan_type": "premium",
        #     #         "name": "Premium Agent",
        #     #         "plans": premium_plans
        #     #     },

        #     #     {
        #     #         "id": "elite",
        #     #         # "plan_type": "elite",
        #     #         "name": "Elite Agent",
        #     #         "plans": elite_plans
        #     #     }
        #     # ],

        #     "advertisement_packages": formatted_ads,

        #     "reel_packages": formatted_reels

        # })

class AgentUpgradePlanAPIView(APIView):
    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        agent = request.user

        plan_type = request.data.get("plan_type")   # premium / elite
        plan_key = request.data.get("plan_key")     # starter / growth / pro / silver etc

        if not plan_type or not plan_key:
            return Response({
                "status": False,
                "message": "plan_type and plan_key are required"
            }, status=400)

        # ================= PREMIUM =================
        if plan_type == "premium":

            plan_map = {
                "starter": 90,
                "growth": 180,
                "pro": 365
            }

            validity = plan_map.get(plan_key)

            if not validity:
                return Response({"status": False, "message": "Invalid premium plan"}, status=400)

            try:
                plan = PremiumPlan.objects.get(validity=validity)
            except PremiumPlan.DoesNotExist:
                return Response({"status": False, "message": "Plan not found"}, status=404)

            agent.activate_premium_plan(plan)

            # 🔔 Notification
            create_notification(
                agent,
                "Plan Upgraded",
                f"You have successfully upgraded to {plan.name}",
                "system"
            )

        # ================= ELITE =================
        elif plan_type == "elite":

            plan_map = {
                "silver": 90,
                "gold": 180,
                "platinum": 365
            }

            days = plan_map.get(plan_key)

            if not days:
                return Response({"status": False, "message": "Invalid elite plan"}, status=400)

            try:
                plan = ElitePlan.objects.get(plan_validity_days=days)
            except ElitePlan.DoesNotExist:
                return Response({"status": False, "message": "Plan not found"}, status=404)

            agent.activate_elite_plan(plan)

            # 🔔 Notification
            create_notification(
                agent,
                "Plan Upgraded",
                f"You have successfully upgraded to {plan.name}",
                "system"
            )

        else:
            return Response({
                "status": False,
                "message": "Invalid plan type"
            }, status=400)

        # ================= RESPONSE =================
        return Response({
            "status": True,
            "message": "Plan upgraded successfully",
            "plan_type": plan_type,
            "plan_name": plan.name,
            "expiry_date": agent.plan_expiry_date
        })






class AgentUsageSummaryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        agent = request.user

        properties = agent.properties.all()

        total_used = properties.count()

        total_limit, residential_limit, commercial_limit = agent.get_plan_limits()

        residential_used = properties.filter(category__name__iexact="residential").count()
        commercial_used = properties.filter(category__name__iexact="commercial").count()

        return Response({
            "total": {
                "used": total_used,
                "limit": total_limit,
                "remaining": max(total_limit - total_used, 0)
            },
            "residential": {
                "used": residential_used,
                "limit": residential_limit,
                "remaining": max(residential_limit - residential_used, 0)
            },
            "commercial": {
                "used": commercial_used,
                "limit": commercial_limit,
                "remaining": max(commercial_limit - commercial_used, 0)
            }
        })


def check_plan_expiry_notifications():
    agents = AgentUserProfile.objects.all()

    for agent in agents:
        if not agent.plan_expiry_date:
            continue

        days_left = (agent.plan_expiry_date - timezone.now()).days

        # 🔔 Expiring soon (3 days before)
        if 0 < days_left <= 3:
            if not Notification.objects.filter(
                agent=agent,
                type="expiry",
                title="Plan Expiring Soon"
            ).exists():

                Notification.objects.create(
                    agent=agent,
                    title="Plan Expiring Soon",
                    message=f"Your plan will expire in {days_left} day(s)",
                    type="expiry"
                )

        # 🔔 Expired
        if days_left < 0:
            if not Notification.objects.filter(
                agent=agent,
                type="expiry",
                title="Plan Expired"
            ).exists():

                Notification.objects.create(
                    agent=agent,
                    title="Plan Expired",
                    message="Your plan has expired. Please renew.",
                    type="expiry"
                )
class AgentNotificationListAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AgentJWTAuthentication]

    def get(self, request):

        # 🔥 CHECK PLAN NOTIFICATIONS
        check_plan_notifications(request.user)

        notifications = Notification.objects.filter(
            agent_id=request.user.id
        ).order_by('-created_at')

        data = [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "type": n.type,
                "is_read": n.is_read,
                "created_at": n.created_at
            }
            for n in notifications
        ]

        return Response(data)

# ================= MARK AS READ =================
class MarkNotificationReadAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AgentJWTAuthentication]

    def post(self, request, id):
        try:
            notification = Notification.objects.get(
                id=id,
                agent_id=request.user.id   # ✅ FIXED
            )

            notification.is_read = True
            notification.save()

            return Response({"message": "Marked as read"}, status=200)

        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=404)


# ================= UNREAD COUNT =================
class UnreadNotificationCountAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AgentJWTAuthentication]

    def get(self, request):
        count = Notification.objects.filter(
            agent_id=request.user.id,   # ✅ FIXED
            is_read=False
        ).count()

        return Response({"unread_count": count})



# class AgentPlanCombinedAPIView(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def get(self, request):
#         from developer.models import PremiumPlan, ElitePlan

#         # ✅ Define agent types manually (IDs for frontend mapping)
#         agent_types = [
#             {"id": 1, "name": "elite agent"},
#             {"id": 2, "name": "premium agent"},
#         ]

#         plans = []

#         # ✅ Elite plans → agent_type = 1
#         for plan in ElitePlan.objects.all():
#             plans.append({
#                 "id": plan.id,
#                 "name": plan.name,
#                 "agent_type": 1
#             })

#         # ✅ Premium plans → agent_type = 2
#         for plan in PremiumPlan.objects.all():
#             plans.append({
#                 "id": plan.id,
#                 "name": plan.name,
#                 "agent_type": 2
#             })

#         return Response({
#             "agent_types": agent_types,
#             "plans": plans
#         })

class AgentPlanCombinedAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        from developer.models import PremiumPlan, ElitePlan,AgentPlan
        # from .models import AgentPlan   # ✅ import your basic plan

        # ✅ Add BASIC agent type
        agent_types = [
            {"id": 1, "name": "elite agent"},
            {"id": 2, "name": "premium agent"},
            {"id": 3, "name": "basic agent"},   # ✅ NEW
        ]

        plans = []

        # ✅ Elite plans → agent_type = 1
        for plan in ElitePlan.objects.all():
            plans.append({
                "id": plan.id,
                "name": plan.name,
                "agent_type": 1
            })

        # ✅ Premium plans → agent_type = 2
        for plan in PremiumPlan.objects.all():
            plans.append({
                "id": plan.id,
                "name": plan.name,
                "agent_type": 2
            })

        # ✅ Basic plans → agent_type = 3
        for plan in AgentPlan.objects.all():
            plans.append({
                "id": plan.id,
                "name": plan.name,
                "agent_type": 3
            })

        return Response({
            "agent_types": agent_types,
            "plans": plans
        })


class AgentPlanListAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        plans = AgentPlan.objects.all()
        serializer = AgentPlanSerializer(plans, many=True)
        return Response(serializer.data)
    
class PremiumPlanListAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        plans = PremiumPlan.objects.all()
        serializer = PremiumPlanSerializer(plans, many=True)
        return Response(serializer.data)
    
class ElitePlanListAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        plans = ElitePlan.objects.all()
        serializer = ElitePlanSerializer(plans, many=True)
        return Response(serializer.data)

class AgentPlansAPIView(APIView):

    def get(self, request):

        plan_type = request.GET.get("plan_type")
        plan_key = request.GET.get("plan_key")

        response_data = []

        # =====================================================
        # BASIC PLANS
        # =====================================================

        if not plan_type or plan_type.lower() == "basic":

            basic_queryset = AgentPlan.objects.all()

            if plan_key:
                basic_queryset = basic_queryset.filter(
                    name__iexact=plan_key
                )

            basic_serializer = AgentPlanSerializer(
                basic_queryset,
                many=True
            )

            basic_plans = []

            for item in basic_serializer.data:

                basic_plans.append({
                    "plan_id": item["id"],
                    "plan_type": item["plan_type"],
                    "plan_key": item["name"].lower().replace(" ", "_"),
                    "label": item["name"],
                    "duration": f'{item["validity"]} Days',
                    "price": item["price"],
                    "savings": f'{item["validity"]} Days',
                    "features": [
                        f'Agent Badge: {item["agent_badge"]}',
                        f'Priority Search: {item["priority_search"]}',
                        f'Meta Ads: {item["meta_ads"]}',
                        f'Bulk Whatsapp: {item["bulk_whatsapp"]}',
                        f'Poster: {item["poster"]}',
                        f'Social Media: {item["social_media"]}',
                        f'{item["validity"]} Days Validity'
                    ]
                })

            response_data.append({
                "id": "basic",
                "name": "Basic Agent",
                "plans": basic_plans
            })

        # =====================================================
        # PREMIUM PLANS
        # =====================================================

        if not plan_type or plan_type.lower() == "premium":

            premium_queryset = PremiumPlan.objects.all()

            if plan_key:
                premium_queryset = premium_queryset.filter(
                    name__iexact=plan_key
                )

            premium_serializer = PremiumPlanSerializer(
                premium_queryset,
                many=True
            )

            premium_plans = []

            for item in premium_serializer.data:

                premium_plans.append({
                    "plan_id": item["id"],
                    "plan_type": item["plan_type"],
                    "plan_key": item["name"].lower(),
                    "label": item["name"],
                    "duration": f'{item["validity"]} Days',
                    "price": item["price"],
                    "savings": f'{item["validity"]} Days',
                    "features": [
                        f'{item["total_listing"]} Property Listings',
                        f'{item["residential_limit"]} Residential Listings',
                        f'{item["commercial_limit"]} Commercial Listings',
                        f'Edit: {item["edit"]}',
                        f'Enquiries: {item["enquiries"]}',
                        f'{item["priority_search"]}',
                        f'{item["meta_ads"]}',
                        f'{item["bulk_whatsapp"]}',
                        f'{item["poster"]}',
                        f'{item["social_media"]}',
                        f'Lead Follow: {item["lead_follow"]}',
                        f'{item["lead_management"]}',
                        f'{item["validity"]} Days Validity'
                    ]
                })

            response_data.append({
                "id": "premium",
                "name": "Premium Agent",
                "plans": premium_plans
            })

        # =====================================================
        # ELITE PLANS
        # =====================================================

        if not plan_type or plan_type.lower() == "elite":

            elite_queryset = ElitePlan.objects.all()

            if plan_key:
                elite_queryset = elite_queryset.filter(
                    name__iexact=plan_key
                )

            elite_serializer = ElitePlanSerializer(
                elite_queryset,
                many=True
            )

            elite_plans = []

            for item in elite_serializer.data:

                elite_plans.append({
                    "plan_id": item["id"],
                    "plan_type": item["plan_type"],
                    "plan_key": item["name"].lower(),
                    "label": item["name"],
                    "duration": f'{item["plan_validity_days"]} Days',
                    "price": item["price"],
                    "savings": f'{item["plan_validity_days"]} Days',
                    "features": [
                        f'{item["total_property_listings"]} Property Listings',
                        f'{item["featured_listings_limit"]} featured Listings',
                        f'{item["priority_search"]}',
                        f'{item["meta_ads_promotion"]}',
                        f'{item["bulk_whatsapp_messages"]}',
                        f'{item["poster_creation"]}',
                        f'{item["social_media_marketing"]}',
                        f'{item["lead_followup_support"]}',
                        f'{item["lead_management"]}',
                        f'{item["plan_validity_days"]} Days Validity'
                    ]
                })

            response_data.append({
                "id": "elite",
                "name": "Elite Agent",
                "plans": elite_plans
            })

        return Response({
            "status": True,
            "message": "Plans fetched successfully",
            "plans": response_data
        }, status=status.HTTP_200_OK)

import jwt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import InvalidToken

class AllPlansAPIView(APIView):

    authentication_classes = []   # ✅ IMPORTANT FIX
    permission_classes = [AllowAny]

    def get(self, request):

        try:

            user = None
            agent = None

            # =====================================================
            # SAFE TOKEN PARSE (NO AUTH CLASS USED)
            # =====================================================

            auth_header = request.headers.get("Authorization")

            if auth_header:

                try:
                    token = auth_header.split(" ")[1]

                    decoded = jwt.decode(
                        token,
                        settings.SECRET_KEY,
                        algorithms=["HS256"]
                    )

                    user_id = decoded.get("user_id")
                    username = decoded.get("username")

                    # ================= USER =================
                    if user_id:
                        user = UserProfile.objects.filter(user_id=user_id).first()

                    # ================= AGENT =================
                    if not user and username:
                        agent = AgentUserProfile.objects.filter(username=username).first()

                except Exception:
                    user = None
                    agent = None

            normal = AgentPlan.objects.all()
            premium = PremiumPlan.objects.all()
            elite = ElitePlan.objects.all()
            userplans = Userplan.objects.all()

            if not user and not agent:
                return Response({
                    "user_plans": UserplanSerializer(userplans, many=True).data,
                    "normal_plans": AgentPlanSerializer(normal, many=True).data,
                    "premium_plans": PremiumPlanSerializer(premium, many=True).data,
                    "elite_plans": ElitePlanSerializer(elite, many=True).data,
                })

            if agent:
                return Response({
                    "user_plans": UserplanSerializer(userplans, many=True).data,
                    "normal_plans": AgentPlanSerializer(normal, many=True).data,
                    "premium_plans": PremiumPlanSerializer(premium, many=True).data,
                    "elite_plans": ElitePlanSerializer(elite, many=True).data,
                })


            property_count = Property.objects.filter(user=user.user).count()
            active_subscriptions = UserPlanSubscription.objects.filter(
                user=user.user,
                is_active=True
            ).order_by("purchased_at")

            is_upgrade_plan = active_subscriptions.count() > 1

            upgrade_plan = None

            if is_upgrade_plan:

                upgrade_subscription = active_subscriptions.last()

                upgrade_plan = {
                    # "subscription_id": str(upgrade_subscription.id),
                    "plan_name": upgrade_subscription.plan.name,
                    "start_date": upgrade_subscription.purchased_at,
                    "expiry_date": upgrade_subscription.expiry_date,
                    "is_active": upgrade_subscription.is_active
                }

            return Response({
                "property_count": property_count,
                "is_upgrade_plan": is_upgrade_plan,
                "user_plans": UserplanSerializer(userplans, many=True).data,
                "normal_plans": AgentPlanSerializer(normal, many=True).data,
                "premium_plans": PremiumPlanSerializer(premium, many=True).data,
                "elite_plans": ElitePlanSerializer(elite, many=True).data,
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=500)


class AgentContactCreateAPIView(APIView):
    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        if isinstance(exc, NotAuthenticated):
            return Response(
                {"error": "Please login to contact agent"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().handle_exception(exc)

    def post(self, request, agent_id):
        try:
            agent = AgentUserProfile.objects.get(id=agent_id)
        except AgentUserProfile.DoesNotExist:
            return Response({"error": "Agent not found"}, status=404)

        serializer = AgentContactSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            # ✅ take from request OR fallback
            email = request.data.get("email") or getattr(user, "email", "")
            first_name = request.data.get("first_name") or getattr(user, "name", "Guest")
            last_name = request.data.get("last_name")  # optional

            serializer.save(
                agent=agent,
                user=user,
                email=email,
                first_name=first_name,
                last_name=last_name  # can be None or ""
            )

            return Response({
                "status": True,
                "message": "Message sent successfully"
            })

        return Response(serializer.errors, status=400)


class AgentContactListAPIView(APIView):
    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # ✅ request.user is AgentUserProfile here
        agent = request.user  

        contacts = AgentContact.objects.filter(agent=agent).order_by('-created_at')
        serializer = AgentContactSerializer(contacts, many=True)

        return Response(serializer.data)


class AgentContactDeleteAPIView(APIView):
    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            contact = AgentContact.objects.get(id=id, agent=request.user)
        except AgentContact.DoesNotExist:
            return Response({
                "status": False,
                "message": "Contact message not found"
            }, status=404)

        contact.delete()

        return Response({
            "status": True,
            "message": "Contact message deleted successfully"
        })

        
class ChangePasswordAPIView(APIView):
    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            agent = request.user
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']

            # Check current password
            if not agent.check_password(current_password):
                return Response({
                    "error": "Current password is incorrect"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            agent.set_password(new_password)
            agent.save()

            return Response({
                "message": "Password updated successfully"
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import json


class AmenitiesAPIView(View):
    def get(self, request):
        try:
            subcategory_id = request.GET.get("subcategory_id")
            amenities = Amenities.objects.all()
            if subcategory_id:
                amenities = amenities.filter(subcategory_id=subcategory_id)
            amenities = amenities.order_by("name")

            data = [
                {"id": a.id, "name": a.name, "icon": a.icon.url if a.icon else None}
                for a in amenities
            ]

            return JsonResponse({"status": True, "message": "Amenities fetched successfully", "data": data})
        except Exception as e:
            return JsonResponse({"status": False, "message": str(e), "data": []})


class CategoryListAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all().order_by("name")
        data = [{"id": c.id, "name": c.name, "icon": c.icon.url if c.icon else None} for c in categories]
        return Response({"status": True, "data": data})


class SubcategoryListAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        category_id = request.GET.get("category_id")
        subcategories = Subcategory.objects.all()
        if category_id:
            subcategories = subcategories.filter(category_id=category_id)
        data = [
            {"id": s.id, "name": s.name, "image": s.image.url if s.image else None, "category_id": s.category_id}
            for s in subcategories
        ]
        return Response({"status": True, "data": data})

class SubcategoryFieldListAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        subcategory_id = request.GET.get("subcategory_id")

        if not subcategory_id:
            return Response({
                "status": False,
                "message": "subcategory_id is required"
            })

        fields = SubcategoryField.objects.filter(
            subcategory_id=subcategory_id
        ).prefetch_related("options") 

        data = []

        for f in fields:
            opts = f.options.all()
            if f.field_type in ["select", "countable"]:
                options = [opt.name for opt in opts]

            elif f.field_type == "multi_select":
                options = [
                    {
                        "name": opt.name,
                        "icon": opt.icon.url if opt.icon else None
                    }
                    for opt in opts
                ]
            else:
                options = []

            field_dict = {
                "id": f.id,
                "field_name": f.field_name,
                "field_type": f.field_type,
                "required": f.required,
                "icon": f.icon.url if f.icon else None
            }

            if options:
                field_dict["options"] = options

            data.append(field_dict)

        return Response({
            "status": True,
            "data": data
        })
    

class PurposeListAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        purposes = Purpose.objects.all().order_by("name")
        data = [{"id": p.id, "name": p.name} for p in purposes]
        return Response({"status": True, "data": data})


class PropertyMetaAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            category_id = request.GET.get("category_id")

            # ================== CATEGORIES ==================
            categories = Category.objects.all().order_by("name")
            category_data = [
                {
                    "id": c.id,
                    "name": c.name,
                    "icon": c.icon.url if c.icon else None
                }
                for c in categories
            ]

            # ================== SUBCATEGORIES ==================
            subcategories = Subcategory.objects.all().order_by("name")

            if category_id:
                subcategories = subcategories.filter(category_id=category_id)

            # ✅ Prefetch fields + options
            subcategories = subcategories.prefetch_related(
                "subcategoryfield_set__options"
            )

            subcategory_data = []

            for s in subcategories:
                field_list = []

                for f in s.subcategoryfield_set.all():
                    opts = f.options.all()

                    # ✅ Build options properly
                    if f.field_type in ["select", "countable"]:
                        options = [opt.name for opt in opts]

                    elif f.field_type == "multi_select":
                        options = [
                            {
                                "name": opt.name,
                                "icon": opt.icon.url if opt.icon else None
                            }
                            for opt in opts
                        ]
                    else:
                        options = []

                    # ✅ FULL field data (FIXED)
                    field_dict = {
                        "id": f.id,
                        "field_name": f.field_name,
                        "field_type": f.field_type,
                        "required": f.required,
                        "icon": f.icon.url if f.icon else None
                    }

                    # ✅ Add options only if present
                    if options:
                        field_dict["options"] = options

                    field_list.append(field_dict)

                subcategory_data.append({
                    "id": s.id,
                    "name": s.name,
                    "category_id": s.category_id,
                    "fields": field_list
                })

            # ================== PURPOSES ==================
            purposes = Purpose.objects.all().order_by("name")
            purpose_data = [{"id": p.id, "name": p.name} for p in purposes]

            # ================== AMENITIES ==================
            amenities = Amenities.objects.all().order_by("name")
            amenities_data = [
                {
                    "id": a.id,
                    "name": a.name,
                    "icon": a.icon.url if a.icon else None
                }
                for a in amenities
            ]

            return Response({
                "status": True,
                # "message": "Property meta fetched successfully",
                "data": {
                    "categories": category_data,
                    "subcategories": subcategory_data,
                    "purposes": purpose_data,
                    "amenities": amenities_data
                }
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": str(e),
                "data": {}
            })

class AgentPropertyListAPIView(APIView):

    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        properties = AgentProperty.objects.filter(
            agent=user
        ).select_related(
            "category",
            "subcategory",
            "purpose"
        ).prefetch_related(
            "amenities",
            "images",
            "selling_points",
            "landmarks",
            "field_values"
        ).order_by('-created_at')

        serializer = AgentPropertySerializer(
            properties,
            many=True,
            context={'request': request}
        )

        # =====================================================
        # PLAN LIMIT
        # =====================================================

        # total_properties = properties.count()

        # total_limit, residential_limit, commercial_limit = user.get_plan_limits()

        # remaining_listings = max(
        #     total_limit - total_properties,
        #     0
        # )
        # =====================================================
        # PLAN LIMIT
        # =====================================================

        total_properties = properties.count()

        active_subscriptions = Subscription.objects.filter(
            agent=user,
            is_active=True
        )

        total_limit = sum(
            sub.property_limit
            for sub in active_subscriptions
        )

        total_used = sum(
            sub.used_listings
            for sub in active_subscriptions
        )

        remaining_listings = max(
            total_limit - total_used,
            0
        )

        subscription_details = []

        for subscription in active_subscriptions:

            subscription_details.append({

                "subscription_id": str(
                    subscription.id
                ),

                "plan_name":
                    subscription.plan_name,

                "property_limit":
                    subscription.property_limit,

                "used_listings":
                    subscription.used_listings,

                "remaining_listings":
                    max(
                        subscription.property_limit -
                        subscription.used_listings,
                        0
                    ),

                "start_date":
                    subscription.start_date,

                "end_date":
                    subscription.end_date,

                "is_active":
                    subscription.is_active
            })

        # =====================================================
        # EDIT LIMIT
        # =====================================================

        # total_edit_limit = 0

        # for sub in active_subscriptions:

        #     premium = PremiumPlan.objects.filter(
        #         name=sub.plan_name
        #     ).first()

        #     elite = ElitePlan.objects.filter(
        #         name=sub.plan_name
        #     ).first()

        #     edit_value = None

        #     if premium:
        #         edit_value = premium.edit
        #     elif elite:
        #         edit_value = elite.edit

        #     if not edit_value:
        #         continue

        #     match = re.search(r"\d+", str(edit_value))

        #     if match:
        #         total_edit_limit += int(match.group())
        total_edit_limit = 0

        for sub in active_subscriptions:

            edit_value = None

            if sub.plan_type == "premium":

                premium = PremiumPlan.objects.filter(
                    name=sub.plan_name
                ).first()

                if premium:
                    edit_value = premium.edit

            elif sub.plan_type == "elite":

                elite = ElitePlan.objects.filter(
                    name=sub.plan_name
                ).first()

                if elite:
                    edit_value = elite.edit

            if not edit_value:
                continue

            match = re.search(r"\d+", str(edit_value))

            if match:
                total_edit_limit += int(match.group())

        # =====================================================
        # EDIT USED (FIXED LOGIC)
        # =====================================================

        # IMPORTANT:
        # If edit tracking is not per-property, you must store it somewhere.
        # Best simple approach: count edits field in property

        total_used_edits = sum(
            s.edit_used for s in active_subscriptions
        )

        remaining_edits = max(total_edit_limit - total_used_edits, 0)


        return Response({
            "status": True,

            "remaining_property": remaining_listings,
            "remaining_edit_count": remaining_edits,

            # "total_limit": total_limit,

            # "used_properties": total_properties,

            "data": serializer.data
        })


class AgentPropertyLimitAPIView(APIView):
    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        agent = request.user
        total_limit, residential_limit, commercial_limit = agent.get_plan_limits()

        total_used = AgentProperty.objects.filter(agent_id=agent.id).count()
        residential_used = AgentProperty.objects.filter(agent_id=agent.id, category__name__iexact="Residential").count()
        commercial_used = AgentProperty.objects.filter(agent_id=agent.id, category__name__iexact="Commercial").count()

        data = {
            "agent_name": agent.username,
            "agent_type": agent.agent_type,
            "plan_active": agent.is_plan_active(),
            "plan_expiry_date": agent.plan_expiry_date,
            "total_limit": total_limit,
            "total_used": total_used,
            "total_remaining": max(total_limit - total_used, 0),
        }

        if agent.plan:
            data.update({
                "residential_limit": residential_limit,
                "residential_used": residential_used,
                "residential_remaining": max(residential_limit - residential_used, 0),
                "commercial_limit": commercial_limit,
                "commercial_used": commercial_used,
                "commercial_remaining": max(commercial_limit - commercial_used, 0),
            })

        return Response(data)

class AgentPropertyAPIView(APIView):
    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    # ================= FIXED PARSER =================
    def parse_list_field(self, request, field_name):
        raw_values = request.data.getlist(field_name)

        if not raw_values:
            value = request.data.get(field_name)
            if value:
                raw_values = [value]

        parsed = []

        for v in raw_values:
            if not v:
                continue

            if isinstance(v, str):
                try:
                    decoded = json.loads(v)
                except Exception as e:
                    print(f"{field_name} JSON PARSE ERROR:", e)
                    continue
            else:
                decoded = v

            if isinstance(decoded, list):
                parsed.extend(decoded)
            elif isinstance(decoded, dict):
                parsed.append(decoded)

        return parsed

    # ================= POST =================
    def post(self, request):

        agent = request.user
        category_id = request.data.get("category")

        if not category_id:

            return Response({
                "status": False,
                "message": "Category is required"
            }, status=400)

        try:

            category = Category.objects.get(
                id=category_id
            )

        except Category.DoesNotExist:

            return Response({
                "status": False,
                "message": "Invalid category"
            }, status=400)

        category_name = category.name.lower().strip()

        # =====================================================
        # ACTIVE SUBSCRIPTIONS
        # =====================================================

        active_subscriptions = Subscription.objects.filter(
            agent=agent,
            is_active=True
        )

        if not active_subscriptions.exists():

            return Response({
                "status": False,
                "message": "No active subscription found"
            }, status=400)

        # =====================================================
        # TOTAL PROPERTY LIMIT
        # =====================================================

        total_limit = sum(
            subscription.property_limit
            for subscription in active_subscriptions
        )

        # total_limit = 0
        # total_used = 0

        # for subscription in active_subscriptions:

        #     total_limit += subscription.property_limit

        #     used = AgentProperty.objects.filter(
        #         subscription=subscription
        #     ).count()

        #     total_used += used
        total_used = sum(
            sub.used_listings
            for sub in active_subscriptions
        )


        remaining_property = max(
            total_limit - total_used,
            0
        )

        # DEBUG
        print("TOTAL LIMIT:", total_limit)
        print("TOTAL USED:", total_used)
        print("REMAINING:", remaining_property)

        if remaining_property <= 0:

            create_notification(
                agent,
                "Listing Limit Reached",
                "You have reached your property listing limit.",
                "usage"
            )

            return Response({
                "status": False,
                "message": "Property limit reached. Please upgrade your plan.",
                "remaining_property": 0
            }, status=400)

        # =====================================================
        # PREMIUM RESIDENTIAL / COMMERCIAL LIMITS
        # =====================================================

        if getattr(agent, "plan", None):

            residential_limit = 0
            commercial_limit = 0

            for subscription in active_subscriptions:

                if subscription.plan_type == "elite":

                    # Elite plan logic
                    # used = AgentProperty.objects.filter(
                    #     subscription=subscription
                    # ).count()

                    # if used < subscription.property_limit:
                    #     selected_subscription = subscription
                    #     break
                    if subscription.used_listings < subscription.property_limit:
                        selected_subscription = subscription
                        break

                    continue

                # Premium plan

                premium = PremiumPlan.objects.filter(
                    name=subscription.plan_name
                ).first()

                if not premium:
                    continue

                if premium:
                    residential_limit += premium.residential_limit
                    commercial_limit += premium.commercial_limit

            residential_used = AgentProperty.objects.filter(
                agent=agent
            ).filter(
                Q(category__name__icontains="residential") |
                Q(category__name__icontains="plot/land") 
            ).count()

            # Commercial + Industrial
            commercial_used = AgentProperty.objects.filter(
                agent=agent
            ).filter(
                Q(category__name__icontains="commercial") |
                Q(category__name__icontains="industrial")
            ).count()

            residential_remaining = max(
                residential_limit - residential_used,
                0
            )

            commercial_remaining = max(
                commercial_limit - commercial_used,
                0
            )

            # =================================================
            # RESIDENTIAL CHECK
            # =================================================

            # if "residential" in category_name:
            if any(
                keyword in category_name
                for keyword in ["residential", "plot/land"]
            ):

                if residential_remaining <= 0:

                    return Response({

                        "status": False,

                        "message":
                        "Residential property limit reached",

                        "remaining_property":
                        remaining_property,

                        "residential_remaining":
                        residential_remaining,

                        "commercial_remaining":
                        commercial_remaining

                    }, status=400)

            # =================================================
            # COMMERCIAL CHECK
            # =================================================

            # if "commercial" in category_name:
            if any(
                keyword in category_name
                for keyword in ["commercial", "industrial"]
            ):

                if commercial_remaining <= 0:

                    return Response({

                        "status": False,

                        "message":
                        "Commercial property limit reached",

                        "remaining_property":
                        remaining_property,

                        "residential_remaining":
                        residential_remaining,

                        "commercial_remaining":
                        commercial_remaining

                    }, status=400)
        # ================= SERIALIZER =================
        serializer = AgentPropertySerializer(
            data=request.data,
            context={
                "request": request,
                "amenities_list": self.parse_list_field(request, "amenities"),
                "selling_points_list": self.parse_list_field(request, "selling_points"),
                "landmarks_list": self.parse_list_field(request, "landmarks"),
                "field_values": self.parse_list_field(request, "field_values"),
            }
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        active_subscriptions = Subscription.objects.filter(
            agent=agent,
            is_active=True
        )

        if not active_subscriptions.exists():

            return Response({
                "status": False,
                "message": "No active subscription found"
            }, status=400)

        selected_subscription = None

        for subscription in active_subscriptions.order_by("end_date"):

            # ===========================
            # ELITE PLAN
            # ===========================

            if subscription.plan_type == "elite":

                # used = AgentProperty.objects.filter(
                #     subscription=subscription
                # ).count()

                # if used < subscription.property_limit:
                #     selected_subscription = subscription
                #     break
                if subscription.used_listings < subscription.property_limit:
                    selected_subscription = subscription
                    break

                continue

            # ===========================
            # PREMIUM PLAN
            # ===========================

            premium = PremiumPlan.objects.filter(
                name=subscription.plan_name
            ).first()

            if not premium:
                continue

            residential_used = AgentProperty.objects.filter(
                subscription=subscription
            ).filter(
                Q(category__name__icontains="residential") |
                Q(category__name__icontains="plot/land")
            ).count()

            commercial_used = AgentProperty.objects.filter(
                subscription=subscription
            ).filter(
                Q(category__name__icontains="commercial") |
                Q(category__name__icontains="industrial")
            ).count()

            if any(
                keyword in category_name
                for keyword in ["residential", "plot/land"]
            ):

                if residential_used < premium.residential_limit:
                    selected_subscription = subscription
                    break

            elif any(
                keyword in category_name
                for keyword in ["commercial", "industrial"]
            ):

                if commercial_used < premium.commercial_limit:
                    selected_subscription = subscription
                    break

        print("FINAL SELECTED:", selected_subscription)
        print("SELECTED SUBSCRIPTION:", selected_subscription)
        with transaction.atomic():

            property_obj = serializer.save(
                subscription=selected_subscription,
                paid=True
            )

            selected_subscription.used_listings += 1
            selected_subscription.save(
                update_fields=["used_listings"]
            )

        # property_obj = serializer.save(
        #     subscription=selected_subscription,
        #     paid = True
        # )
        # selected_subscription.used_listings += 1

        # selected_subscription.save(
        #     update_fields=["used_listings"]
        # )
        # FEATURED LISTING

        selected_featured_subscription = None

        active_featured_subscriptions = (
            Subscription.objects.filter(
                agent=agent,
                is_active=True,
                featured_limit__gt=0
            )
            .order_by("end_date")
        )

        for subscription in active_featured_subscriptions:

            if subscription.featured_used < subscription.featured_limit:
                selected_featured_subscription = subscription
                break

        if selected_featured_subscription:

            property_obj.is_featured = True
            property_obj.save(update_fields=["is_featured"])

            selected_featured_subscription.featured_used += 1
            selected_featured_subscription.save(
                update_fields=["featured_used"]
            )

        else:

            property_obj.is_featured = False
            property_obj.save(update_fields=["is_featured"])

        # ================= IMAGES =================
        images = request.FILES.getlist("images")
        for img in images:
            AgentPropertyImage.objects.create(property=property_obj, image=img)

        # ================= MAIN IMAGE =================
        if not property_obj.image and property_obj.images.exists():
            property_obj.image = property_obj.images.first().image
            property_obj.save()

        active_subscriptions = Subscription.objects.filter(
            agent=agent,
            is_active=True
        )

        total_limit = sum(
            sub.property_limit
            for sub in active_subscriptions
        )

        # total_used = sum(
        #     AgentProperty.objects.filter(
        #         subscription=sub
        #     ).count()
        #     for sub in active_subscriptions
        # )
        total_used = sum(
            sub.used_listings
            for sub in active_subscriptions
        )

        remaining = max(
            total_limit - total_used,
            0
        )
        # 🔔 LOW REMAINING WARNING
        if remaining <= 2 and remaining > 0:
            create_notification(
                agent,
                "Listing Limit Warning",
                f"Only {remaining} property listings remaining.",
                "usage"
            )

        # ❌ LIMIT REACHED AFTER THIS ADD
        if remaining == 0:
            create_notification(
                agent,
                "Listing Limit Reached",
                "You have used all your property listings.",
                "usage"
            )

        # ================= RESPONSE =================
        return Response({
            "status": True,
            "message": "Property created successfully",
            "remaining_listings": remaining,
            "data": AgentPropertySerializer(
                property_obj,
                context={"request": request}
            ).data
        })

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

class PublicPropertyListAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):

        queryset = AgentProperty.objects.all()

        # =============================
        # 1. CATEGORY FILTER
        # =============================
        category = request.GET.get("category")

        if category:
            queryset = queryset.filter(
                category__name__icontains=category
            )

        # =============================
        # 2. SEARCH FILTER
        # (price + city + label)
        # =============================
        search = request.GET.get("search")

        if search:
            queryset = queryset.filter(
                Q(price__icontains=search) |
                Q(city__icontains=search) |
                Q(label__icontains=search)
            )

        queryset = queryset.distinct().order_by("-created_at")

        serializer = AgentPropertySerializer(
            queryset,
            many=True,
            context={"request": request}
        )

        return Response({
            # "status": True,
            # "count": queryset.count(),
            "data": serializer.data
        })


class PublicPropertyDetailAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, uuid):

        try:
            property_obj = AgentProperty.objects.select_related(
                "category",
                "subcategory",
                "purpose",
                "agent"
            ).prefetch_related(
                "amenities",
                "images",
                "selling_points",
                "landmarks",
                "field_values"
            ).get(uuid=uuid)   # ✅ FIXED HERE

        except AgentProperty.DoesNotExist:
            return Response(
                {"status": False, "error": "Property not found"},
                status=404
            )

        serializer = AgentPropertySerializer(
            property_obj,
            context={"request": request}
        )

        return Response({
            "status": True,
            "data": serializer.data
        })

class AgentPropertyDetailAPIView(APIView):

    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    # =========================================
    # GET OBJECT
    # =========================================

    def get_object(self, request, id):

        try:

            return AgentProperty.objects.get(
                id=id,
                agent=request.user
            )

        except AgentProperty.DoesNotExist:

            return None

    # =========================================
    # PARSE LIST FIELD
    # =========================================

    def parse_list_field(self, request, field_name):

        if hasattr(request.data, 'getlist'):

            values = request.data.getlist(field_name)

            if values:

                try:

                    if (
                        isinstance(values[0], str)
                        and (
                            values[0].startswith("[")
                            or values[0].startswith("{")
                        )
                    ):

                        return json.loads(values[0])

                except json.JSONDecodeError:
                    pass

            return values

        else:

            raw = request.data.get(field_name, "[]")

            try:
                return json.loads(raw)

            except json.JSONDecodeError:
                return []

    # =========================================
    # GET
    # =========================================

    def get(self, request, id):

        property_obj = self.get_object(
            request,
            id
        )

        if not property_obj:

            return Response({
                "error": "Property not found"
            }, status=404)

        serializer = AgentPropertySerializer(
            property_obj,
            context={'request': request}
        )

        return Response({
            "status": True,
            "data": serializer.data
        })

    # =========================================
    # UPDATE
    # =========================================

    def put(self, request, id):

        property_obj = self.get_object(
            request,
            id
        )
        agent = request.user

        # active_subscriptions = Subscription.objects.filter(
        #     agent=agent,
        #     is_active=True
        # ).order_by("start_date")

        # total_edit_limit = sum(
        #     subscription.edit_limit
        #     for subscription in active_subscriptions
        # )

        # total_used_edits = sum(
        #     subscription.edit_used
        #     for subscription in active_subscriptions
        # )

        # remaining_edits = (
        #     total_edit_limit -
        #     total_used_edits
        # )
        active_subscriptions = Subscription.objects.filter(
            agent=agent,
            is_active=True
        ).order_by("end_date")

        total_edit_limit = sum(
            subscription.edit_limit
            for subscription in active_subscriptions
        )

        total_used_edits = sum(
            subscription.edit_used
            for subscription in active_subscriptions
        )

        remaining_edits = max(
            total_edit_limit - total_used_edits,
            0
        )

        print("TOTAL EDIT LIMIT:", total_edit_limit)
        print("TOTAL USED EDITS:", total_used_edits)
        print("REMAINING EDITS:", remaining_edits)

        if remaining_edits <= 0:

            return Response({

                "status": False,

                "message":
                "Edit limit reached. Upgrade your plan.",

                "remaining_edits": 0

            }, status=400)

        if not property_obj:

            return Response({
                "error": "Property not found"
            }, status=404)

        old_category = property_obj.category.name.lower().strip()

        new_category_id = request.data.get("category")

        if new_category_id:

            try:

                new_category = Category.objects.get(
                    id=new_category_id
                )

                new_category_name = new_category.name.lower().strip()

            except Category.DoesNotExist:

                return Response({

                    "status": False,

                    "message": "Invalid category"

                }, status=400)

        else:

            new_category_name = old_category


        def get_group(category_name):

            if any(
                keyword in category_name
                for keyword in ["residential", "plot/land"]
            ):
                return "residential"

            if any(
                keyword in category_name
                for keyword in ["commercial", "industrial"]
            ):
                return "commercial"

            return None


        old_group = get_group(old_category)

        new_group = get_group(new_category_name)

        print("OLD GROUP:", old_group)
        print("NEW GROUP:", new_group)


        # ==========================================
        # CATEGORY CHANGE VALIDATION
        # ==========================================

        if old_group != new_group:

            residential_limit = 0
            commercial_limit = 0

            residential_used = 0
            commercial_used = 0

            for subscription in active_subscriptions:

                premium = PremiumPlan.objects.filter(
                    name=subscription.plan_name
                ).first()

                # Skip Elite plans
                if not premium:
                    continue

                residential_limit += premium.residential_limit
                commercial_limit += premium.commercial_limit

                residential_used += AgentProperty.objects.filter(

                    agent=agent

                ).filter(

                    Q(category__name__icontains="residential") |
                    Q(category__name__icontains="plot/land")

                ).exclude(

                    id=property_obj.id

                ).count()

                commercial_used += AgentProperty.objects.filter(

                    agent=agent

                ).filter(

                    Q(category__name__icontains="commercial") |
                    Q(category__name__icontains="industrial")

                ).exclude(

                    id=property_obj.id

                ).count()

            residential_remaining = max(

                residential_limit - residential_used,

                0

            )

            commercial_remaining = max(

                commercial_limit - commercial_used,

                0

            )

            print("Residential Remaining:", residential_remaining)
            print("Commercial Remaining:", commercial_remaining)

            if new_group == "residential":

                if residential_remaining <= 0:

                    return Response({

                        "status": False,

                        "message": "Residential property limit reached."

                    }, status=400)

            if new_group == "commercial":

                if commercial_remaining <= 0:

                    return Response({

                        "status": False,

                        "message": "Commercial property limit reached."

                    }, status=400)

        # amenities_list = request.data.getlist(
        #     'amenities'
        # )
        amenities_list = self.parse_list_field(
            request,
            'amenities'
        )

        selling_points_list = self.parse_list_field(
            request,
            'selling_points'
        )

        landmarks_list = self.parse_list_field(
            request,
            'landmarks'
        )

        field_values = self.parse_list_field(
            request,
            'field_values'
        )

        serializer = AgentPropertySerializer(
            property_obj,
            data=request.data,
            partial=True,
            context={
                'request': request,
                'amenities_list': amenities_list,
                'selling_points_list': selling_points_list,
                'landmarks_list': landmarks_list,
                'field_values': field_values
            }
        )

        if serializer.is_valid():

            property_obj = serializer.save()
            # subscription = Subscription.objects.filter(
            #     agent=request.user,
            #     is_active=True
            # ).first()

            # if subscription:
            #     subscription.edit_used += 1
            #     subscription.save()
            selected_subscription = None

            for subscription in active_subscriptions:

                print("======================")
                print("SUB:", subscription.id)
                print("EDIT LIMIT:", subscription.edit_limit)
                print("EDIT USED:", subscription.edit_used)

                if subscription.edit_used < subscription.edit_limit:

                    selected_subscription = subscription

                    print("SELECTED SUB:", subscription.id)

                    break

            if not selected_subscription:

                return Response({

                    "status": False,

                    "message": "No subscription has remaining edit limit."

                }, status=400)

            selected_subscription.edit_used += 1
            selected_subscription.save()

            print("UPDATED EDIT USED:", selected_subscription.edit_used)

            images = request.FILES.getlist('images')

            if images:

                property_obj.images.all().delete()

                for img in images:

                    AgentPropertyImage.objects.create(
                        property=property_obj,
                        image=img
                    )

                first_image = property_obj.images.first()

                if first_image:

                    property_obj.image = first_image.image
                    property_obj.save()

            return Response({

                "status": True,
                "message": "Property updated successfully",

                "data": AgentPropertySerializer(
                    property_obj,
                    context={'request': request}
                ).data
            })

        return Response(
            serializer.errors,
            status=400
        )

    # =========================================
    # DELETE
    # =========================================

    def delete(self, request, id):

        property_obj = self.get_object(
            request,
            id
        )

        if not property_obj:

            return Response({
                "error": "Property not found"
            }, status=404)

        agent = request.user

        property_obj.delete()

        if agent.properties_listed > 0:

            agent.properties_listed -= 1
            agent.save()

        return Response({

            "status": True,
            "message": "Property deleted successfully"

        })
    



from django.db.models.functions import ExtractMonth

class AgentPropertyEnquiryCreateAPI(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        print("URL ID:", id)
        print("USER ID:", request.user.id)
        print("DATA:", request.data)

        try:
            property_obj = AgentProperty.objects.get(id=int(id))
        except (AgentProperty.DoesNotExist, ValueError):
            return Response({"error": "Property not found"}, status=404)

        serializer = AgentPropertyEnquirySerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        serializer.save(
            user=request.user,
            agent_property=property_obj
        )

        return Response({
            "status": True,
            "message": "Enquiry submitted successfully",
            "data": serializer.data
        })


class AgentPropertyEnquiryListAPI(APIView):

    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        enquiries = AgentPropertyEnquiry.objects.filter(
            agent_property__agent=user
        ).order_by("-created_at")

        data = [
            {
                "id": e.id,
                "property": e.agent_property.label,
                "price": e.agent_property.price,   # ✅ ADD THIS LINE
                "name": e.name,
                "email": e.email,
                "phone": e.phone,
                "message": e.message,
                "date": e.created_at.strftime("%Y-%m-%d")
            }
            for e in enquiries
        ]

        return Response({
            "status": True,
            "count": len(data),
            "data": data
        })

class AgentPropertyEnquiryDetailAPI(APIView):

    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        try:
            enquiry = AgentPropertyEnquiry.objects.get(id=id)
        except AgentPropertyEnquiry.DoesNotExist:
            return Response({"error": "Enquiry not found"}, status=404)

        property_obj = enquiry.agent_property

        # Property Images
        images = [
            img.image.url for img in property_obj.images.all()
        ]

        # Amenities
        amenities = [
            amenity.name for amenity in property_obj.amenities.all()
        ]

        # Field Values
        field_values = [
            {
                "field": fv.field.field_name,
                "value": fv.value
            }
            for fv in property_obj.field_values.all()
        ]

        # Selling Points
        selling_points = [
            sp.point for sp in property_obj.selling_points.all()
        ]

        # Landmarks
        landmarks = [
            {
                "name": lm.name,
                "distance": lm.distance
            }
            for lm in property_obj.landmarks.all()
        ]

        data = {
            "enquiry": {
                "id": enquiry.id,
                "name": enquiry.name,
                "email": enquiry.email,
                "phone": enquiry.phone,
                "message": enquiry.message,
                "date": enquiry.created_at.strftime("%Y-%m-%d"),
            },
            "property": {
                "id": property_obj.id,
                "label": property_obj.label,
                "description": property_obj.description,
                "price": property_obj.price,
                "perprice": property_obj.perprice,
                "land_area": property_obj.land_area,
                "sq_ft": property_obj.sq_ft,
                "category": property_obj.category.name,
                "subcategory": property_obj.subcategory.name if property_obj.subcategory else None,
                "purpose": property_obj.purpose.name,
                "city": property_obj.city,
                "district": property_obj.district,
                "state": property_obj.state,
                "location": property_obj.location,
                "pincode": property_obj.pincode,
                "image": property_obj.image.url if property_obj.image else None,
                "screenshot": property_obj.screenshot.url if property_obj.screenshot else None,
                "images": images,
                "amenities": amenities,
                "field_values": field_values,
                "selling_points": selling_points,
                "landmarks": landmarks,
                "agent_phone": property_obj.phone,
                "agent_whatsapp": property_obj.whatsapp,
            }
        }

        return Response({
            "status": True,
            "data": data
        })

class DashboardAPIView(APIView):

    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        agent_properties = AgentProperty.objects.filter(agent=user)

        total_properties = agent_properties.count()

        # enquiries_qs = AgentPropertyEnquiry.objects.filter(
        #     agent_property__agent=user
        # )
        enquiries_qs = AgentPropertyEnquiry.objects.filter(
            property__agent=user
        )

        total_enquiries = enquiries_qs.count()

        # ================= PLAN LIMIT =================
        # total_limit, residential_limit, commercial_limit = user.get_plan_limits()

        # remaining_listings = max(total_limit - total_properties, 0)
        active_subscriptions = Subscription.objects.filter(
            agent=user,
            is_active=True
        )

        total_limit = 0
        total_used = 0

        # for subscription in active_subscriptions:

        #     total_limit += subscription.property_limit

        #     used = AgentProperty.objects.filter(
        #         subscription=subscription
        #     ).count()

        #     total_used += used

        # remaining_listings = max(
        #     total_limit - total_used,
        #     0
        # )
        # total_properties = properties.count()

        active_subscriptions = Subscription.objects.filter(
            agent=user,
            is_active=True
        )

        total_limit = sum(
            sub.property_limit
            for sub in active_subscriptions
        )

        total_used = sum(
            sub.used_listings
            for sub in active_subscriptions
        )

        remaining_listings = max(
            total_limit - total_used,
            0
        )

        # ================= MONTHLY =================
        current_year = timezone.now().year

        monthly = (
            enquiries_qs
            .filter(created_at__year=current_year)
            .annotate(month=ExtractMonth("created_at"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        month_map = {
            1: "Jan", 2: "Feb", 3: "Mar",
            4: "Apr", 5: "May", 6: "Jun",
            7: "Jul", 8: "Aug", 9: "Sep",
            10: "Oct", 11: "Nov", 12: "Dec"
        }

        month_counts = {m["month"]: m["count"] for m in monthly}

        monthly_data = [
            {"month": month_map[i], "count": month_counts.get(i, 0)}
            for i in range(1, 13)
        ]

        # ================= RECENT =================
        latest = enquiries_qs.order_by("-created_at")[:5]

        recent_data = [
            {
                # "property": e.agent_property.label,
                "property": e.property.label,
                "name": e.name,
                "email": e.email,
                "phone": e.phone,
                "message": e.message,
                "date": e.created_at.strftime("%Y-%m-%d")
            }
            for e in latest
        ]

        return Response({
            "status": True,
            "data": {
                "total_properties": total_properties,
                "total_enquiries": total_enquiries,
                "remaining_listings": remaining_listings,   # ✅ FIX ADDED
                "monthly_enquiries": monthly_data,
                "recent_enquiries": recent_data
            }
        })
    





class TestimonialListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        testimonials = Testimonial.objects.select_related("user").order_by("-id")

        data = [
            {
                "id": t.id,
                "name": t.user.name,
                "image": t.display_image,
                "rating": float(t.rating),
                "opinion": t.opinion,
                "description": t.description,
                "designation": t.designation,
            }
            for t in testimonials
        ]

        return Response({"data": data})

class PropertyListAPI(generics.ListAPIView):
            serializer_class = PropertyCardSerializer
            permission_classes = [AllowAny]

            def get_queryset(self):
                return (
                    Property.objects
                    .select_related("owner")
                    .prefetch_related("images")
                    .order_by("-created_at")
                )

            def get_serializer_context(self):
                context = super().get_serializer_context()
                request = self.request

                wishlist_ids = set()
                auth_header = request.headers.get("Authorization")

                if auth_header and auth_header.startswith("Bearer "):
                    try:
                        token = auth_header.split(" ")[1]

                        decoded = jwt.decode(
                            token,
                            settings.SECRET_KEY,
                            algorithms=["HS256"]
                        )

                        user_id = decoded.get("user_id")

                        if user_id:
                            wishlist_ids = set(
                                Wishlist.objects.filter(user_id=user_id)
                                .values_list("property_id", flat=True)
                            )

                    except Exception:
                        pass  # silently ignore for unauth users

                context["wishlist_ids"] = wishlist_ids
                return context

class WishlistView(APIView):
            authentication_classes = []
            permission_classes = [AllowAny]

            #  Get user from JWT
            def get_user_from_token(self, request):
                auth_header = request.headers.get("Authorization")

                if not auth_header:
                    return None, Response({"error": "Authorization header missing"}, status=401)

                try:
                    token = auth_header.split(" ")[1]

                    decoded = jwt.decode(
                        token,
                        settings.SECRET_KEY,
                        algorithms=["HS256"]
                    )

                    user_id = int(decoded.get("user_id"))
                    user = UserCreate.objects.get(id=user_id)

                    return user, None

                except jwt.ExpiredSignatureError:
                    return None, Response({"error": "Token expired"}, status=401)
                except jwt.InvalidTokenError:
                    return None, Response({"error": "Invalid token"}, status=401)
                except UserCreate.DoesNotExist:
                    return None, Response({"detail": "User not found"}, status=404)
                except Exception:
                    return None, Response({"error": "Something went wrong"}, status=400)

            #  GET wishlist
            def get(self, request):
                user, error = self.get_user_from_token(request)
                if error:
                    return error

                wishlist = Wishlist.objects.filter(user=user)

                #  Efficient query
                properties = Property.objects.filter(
                    id__in=wishlist.values_list("property_id", flat=True)
                ).select_related("owner").prefetch_related("images")

                serializer = WishlistSerializer(
                    properties,
                    many=True,
                    context={"wishlist_ids": set(properties.values_list("id", flat=True))}
                )

                return Response(serializer.data)

            # ➕ ADD to wishlist
            def post(self, request):
                user, error = self.get_user_from_token(request)
                if error:
                    return error

                masked_id = request.data.get("id")

                if not masked_id:
                    return Response({"error": "property id is required"}, status=400)

                #  Decode masked ID
                decoded = hashids.decode(masked_id)

                if not decoded:
                    return Response({"error": "Invalid property_id"}, status=400)

                real_id = decoded[0]

                try:
                    property_obj = Property.objects.get(id=real_id)
                except Property.DoesNotExist:
                    return Response({"error": "Property not found"}, status=404)

                wishlist, created = Wishlist.objects.get_or_create(
                    user=user,
                    property=property_obj
                )

                if not created:
                    return Response({"message": "Already in wishlist"})

                return Response({"message": "Added to wishlist"})

            # ❌ REMOVE from wishlist
            def delete(self, request):
                user, error = self.get_user_from_token(request)
                if error:
                    return error

                masked_id = request.data.get("property_id")

                if not masked_id:
                    return Response({"error": "property_id is required"}, status=400)

                # 🔓 Decode masked ID
                decoded = hashids.decode(masked_id)

                if not decoded:
                    return Response({"error": "Invalid property_id"}, status=400)

                real_id = decoded[0]

                try:
                    wishlist = Wishlist.objects.get(user=user, property_id=real_id)
                    wishlist.delete()
                    return Response({"message": "Removed from wishlist"})
                except Wishlist.DoesNotExist:
                    return Response({"error": "Not in wishlist"}, status=404)



from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.db.models import Q
import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

class PropertyListAPI(generics.ListAPIView):
    serializer_class = PropertyCardSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    # -----------------------------
    # SAFE INT CONVERTER
    # -----------------------------
    def safe_int(self, value):
        try:
            return int(str(value).replace(",", "").strip())
        except:
            return None

    # -----------------------------
    # QUERYSET FILTER
    # -----------------------------
    def get_queryset(self):

        queryset = Property.objects.select_related(
            "owner", "category", "purpose"
        ).prefetch_related("images").order_by("-created_at")

        request = self.request

        category = (request.GET.get("category") or "").strip()
        purpose = (request.GET.get("purpose") or "").strip()
        city = (request.GET.get("city") or "").strip()
        price_range = (request.GET.get("price_range") or "").strip()

        # -----------------------------
        # CATEGORY FILTER
        # -----------------------------
        if category and category.lower() != "all":
            queryset = queryset.filter(
                category__name__icontains=category
            )

        # -----------------------------
        # PURPOSE FILTER
        # -----------------------------
        if purpose and purpose.lower() != "all":
            queryset = queryset.filter(
                purpose__name__icontains=purpose
            )

        # -----------------------------
        # CITY FILTER
        # -----------------------------
        if city:
            queryset = queryset.filter(
                city__icontains=city
            )

        # -----------------------------
        # PRICE RANGE FILTER
        # (based on integer conversion)
        # -----------------------------
        if price_range:

            if price_range == "below_5":
                queryset = queryset.filter(price__lt="500000")

            elif price_range == "5_10":
                queryset = queryset.filter(price__gte="500000", price__lte="1000000")

            elif price_range == "10_25":
                queryset = queryset.filter(price__gte="1000000", price__lte="2500000")

            elif price_range == "25_50":
                queryset = queryset.filter(price__gte="2500000", price__lte="5000000")

            elif price_range == "above_50":
                queryset = queryset.filter(price__gt="5000000")

        return queryset

    # -----------------------------
    # WISHLIST CONTEXT
    # -----------------------------
    def get_serializer_context(self):
        context = super().get_serializer_context()
        request = self.request

        wishlist_ids = set()
        auth_header = request.headers.get("Authorization")

        if auth_header:
            parts = auth_header.strip().split()

            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]

                try:
                    decoded = jwt.decode(
                        token,
                        settings.SECRET_KEY,
                        algorithms=["HS256"]
                    )

                    user_id = decoded.get("user_id") or decoded.get("id")

                    if user_id:
                        wishlist_ids = set(
                            Wishlist.objects.filter(user_id=user_id)
                            .values_list("property_id", flat=True)
                        )

                except (ExpiredSignatureError, InvalidTokenError):
                    pass

        context["wishlist_ids"] = wishlist_ids
        return context



class WishlistView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    # -----------------------------
    # AUTH
    # -----------------------------
    def get_user_from_token(self, request):

        auth = request.headers.get(
            "Authorization"
        )

        if not auth:

            return None, Response({
                "error": "Authorization header missing"
            }, status=401)

        try:

            token = auth.split()[1]

            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            user = UserCreate.objects.get(
                id=decoded.get("user_id")
            )

            return user, None

        except Exception:

            return None, Response({
                "error": "Invalid token"
            }, status=401)

    # -----------------------------
    # GET WISHLIST
    # -----------------------------
    def get(self, request):

        user, error = self.get_user_from_token(
            request
        )

        if error:
            return error

        wishlist = Wishlist.objects.filter(
            user=user
        )

        serializer = WishlistSerializer(
            wishlist,
            many=True
        )

        return Response(
            serializer.data
        )

    # -----------------------------
    # ADD TO WISHLIST
    # -----------------------------
    def post(self, request):

        user, error = self.get_user_from_token(
            request
        )

        if error:
            return error

        property_id = request.data.get("id")

        if not property_id:

            return Response({
                "error": "id required"
            }, status=400)

        # ✅ UUID PROPERTY CHECK FIX
        exists = (

            Property.objects.filter(
                id=property_id
            ).exists()

            or

            AgentProperty.objects.filter(
                id=property_id
            ).exists()
        )

        if not exists:

            return Response({
                "error": "Property not found"
            }, status=404)

        obj, created = Wishlist.objects.get_or_create(

            user=user,

            property_uuid=property_id
        )

        if not created:

            return Response({
                "message": "Already in wishlist"
            })

        return Response({
            "message": "Added to wishlist"
        })

    # -----------------------------
    # REMOVE FROM WISHLIST
    # -----------------------------
    def delete(self, request):

        user, error = self.get_user_from_token(
            request
        )

        if error:
            return error

        property_id = request.data.get(
            "property_id"
        )

        if not property_id:

            return Response({
                "error": "id required"
            }, status=400)

        deleted, _ = Wishlist.objects.filter(

            user=user,

            property_uuid=property_id

        ).delete()

        if deleted:

            return Response({
                "message": "Removed from wishlist"
            })

        return Response({
            "error": "Not in wishlist"
        }, status=404)


from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

# from .models import Property, PropertyView
# from .serializers import PropertyDetailSerializer


class PropertyDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PropertyDetailSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    queryset = (
        Property.objects.select_related(
            "owner",
            "purpose",
            "category"
        ).prefetch_related(
            "amenities",
            "images"
        )
    )

    # =========================
    # UUID BASED LOOKUP
    # =========================
    def get_object(self):

        uuid_value = self.kwargs.get("uuid")

        if not uuid_value:
            raise NotFound("Property id not provided")

        try:
            property_obj = self.get_queryset().get(uuid=uuid_value)

            # =========================
            # TRACK VIEWS (SAFE)
            # =========================
            user = self.request.user if self.request.user.is_authenticated else None

            if user:
                PropertyView.objects.get_or_create(
                    user=user,
                    property=property_obj
                )

            return property_obj

        except Property.DoesNotExist:
            raise NotFound("Property not found")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed

from .models import Property, PropertyEnquiry
from .serializers import PropertyEnquirySerializer
from .authentication import UserJWTAuthentication
from .utils import hashids


class PropertyEnquiryCreateView(generics.CreateAPIView):
    queryset = PropertyEnquiry.objects.all()
    serializer_class = PropertyEnquirySerializer

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        user = request.user

        if not user or not user.is_authenticated:
            return Response(
                {"message": "User needs to login"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            property_hash = request.data.get("property_hash_id")

            if not property_hash:
                return Response(
                    {"error": "property_hash_id is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # -------------------------------
            # ✅ DECODE HASH → REAL ID
            # -------------------------------
            decoded = hashids.decode(property_hash)

            if not decoded:
                return Response(
                    {"error": "Invalid property ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            property_id = decoded[0]

            # -------------------------------
            # ✅ GET PROPERTY + OWNER
            # -------------------------------
            property_obj = Property.objects.select_related("owner").filter(id=property_id).first()

            if not property_obj:
                return Response(
                    {"error": "Property not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # -------------------------------
            # ✅ CREATE ENQUIRY
            # -------------------------------
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save(
                user=user,
                property=property_obj,
                owner=property_obj.owner,
                # property_hash_id=property_hash
            )

            return Response(
                {
                    "message": "Enquiry submitted successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        except AuthenticationFailed as e:
            return Response(
                {
                    "detail": str(e),
                    "code": "user_not_found"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

from uuid import UUID
from itertools import chain
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class RelatedPropertiesAPIView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, uuid_id):

        # =============================
        # VALIDATE UUID
        # =============================
        try:
            uuid_obj = UUID(str(uuid_id))
        except ValueError:
            return Response(
                {"error": "Invalid UUID"},
                status=400
            )

        current_property = None

        # =============================
        # TRY PROPERTY (FIXED: id not uuid)
        # =============================
        obj = Property.objects.select_related(
            "category",
            "purpose"
        ).filter(
            id=uuid_obj   # 🔥 FIX HERE
        ).first()

        if obj:
            current_property = obj

        # =============================
        # TRY AGENT PROPERTY (FIXED)
        # =============================
        if not current_property:

            obj = AgentProperty.objects.select_related(
                "category",
                "purpose"
            ).filter(
                id=uuid_obj   # 🔥 FIX HERE
            ).first()

            if obj:
                current_property = obj

        if not current_property:
            return Response(
                {"error": "Property not found"},
                status=404
            )

        # =============================
        # USER RELATED (FIXED)
        # =============================
        user_related = Property.objects.filter(
            category=current_property.category,
            purpose=current_property.purpose
        ).exclude(
            id=current_property.id   # 🔥 FIX HERE
        ).select_related(
            "user"
        ).prefetch_related(
            "images"
        ).filter(
            expiry_date__gte=timezone.now()
        )

        # =============================
        # AGENT RELATED (FIXED)
        # =============================
        agent_related = AgentProperty.objects.filter(
            category=current_property.category,
            purpose=current_property.purpose
        ).exclude(
            id=current_property.id   # 🔥 FIX HERE
        ).select_related(
            "agent"
        )

        # =============================
        # COMBINE
        # =============================
        combined = list(chain(user_related, agent_related))

        combined.sort(
            key=lambda x: x.created_at,
            reverse=True
        )

        combined = combined[:10]

        # =============================
        # SERIALIZER
        # =============================
        serializer = CombinedPropertyListSerializer(
            combined,
            many=True,
            context={
                "request": request,
                "wishlist_ids": set()
            }
        )

        return Response({
            "count": len(combined),
            "data": serializer.data
        })


class ContactCreateAPIView(APIView):

    def post(self,request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message":"Content submitted successfully",
                    "data":serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class BlogListingAPIView(APIView):

    authentication_classes = []     
    permission_classes = [AllowAny]

    def get(self,request):
        blogs = Blog.objects.all().order_by("-date")
        serializer = BlogListSerializer(
            blogs,
            many=True,
            context = {"request":request}
        )

        return Response(serializer.data,status=status.HTTP_200_OK)
    

from rest_framework.generics import RetrieveAPIView
from .models import Blog
from .serializers import SingleBlogSerializer


class SingleBlogAPIView(RetrieveAPIView):

    authentication_classes = []     
    permission_classes = [AllowAny]

    queryset = Blog.objects.all()
    serializer_class = SingleBlogSerializer
    lookup_field = "id"



from rest_framework.generics import ListAPIView
from .models import Blog
# from .serializers import BlogSerializer


class BlogByCategoryAPIView(ListAPIView):

    authentication_classes = []     #
    permission_classes = [AllowAny]

    serializer_class = BlogListSerializer

    def get_queryset(self):
        queryset = Blog.objects.select_related("category")

        category = self.request.query_params.get("category")

        if category:
            queryset = queryset.filter(
                category__name__iexact=category
            )

        return queryset
    


class BlogNameSearchAPIView(ListAPIView):

    authentication_classes = []     # ✅ allow without login
    permission_classes = [AllowAny]
    serializer_class = BlogListSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")

        if name:
            return Blog.objects.filter(
                blog_head__icontains=name
            )

        return Blog.objects.none()



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Wishlist
from .authentication import UserJWTAuthentication


class BulkWishlistDeleteAPIView(APIView):
    """
    Delete ALL wishlist items of logged-in user
    """

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):

        user = request.user   # authenticated user

        # delete all wishlist items of this user
        deleted_count, _ = Wishlist.objects.filter(user=user).delete()

        return Response(
            {
                "message": "Wishlist cleared successfully",
                "deleted_items": deleted_count
            },
            status=status.HTTP_200_OK
        )


class WishlistFilterAPIView(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        purpose_name = request.query_params.get("purpose")

        # -----------------------------------
        # STEP 1: GET WISHLIST IDS
        # -----------------------------------
        wishlist_qs = Wishlist.objects.filter(user_id=user.id)

        property_ids = list(
            wishlist_qs.values_list("property_uuid", flat=True)
        )

        property_ids = [pid for pid in property_ids if pid]

        wishlist_ids = set(str(pid) for pid in property_ids)

        # -----------------------------------
        # STEP 2: FETCH USER PROPERTIES
        # -----------------------------------
        user_properties = Property.objects.filter(
            id__in=property_ids
        ).select_related(
            "user",
            "purpose",
            "category"
        ).prefetch_related(
            "images"
        )

        # -----------------------------------
        # STEP 3: FETCH AGENT PROPERTIES
        # -----------------------------------
        agent_properties = AgentProperty.objects.filter(
            id__in=property_ids
        ).select_related(
            "agent",
            "purpose",
            "category"
        )

        # -----------------------------------
        # STEP 4: COMBINE
        # -----------------------------------
        combined = list(user_properties) + list(agent_properties)

        # -----------------------------------
        # STEP 5: PURPOSE FILTER
        # -----------------------------------
        if purpose_name and purpose_name.strip().lower() != "all":

            purpose_name = purpose_name.strip().lower()

            combined = [
                obj for obj in combined
                if obj.purpose and obj.purpose.name.lower() == purpose_name
            ]

        # -----------------------------------
        # STEP 6: BUILD RESPONSE (FULL FIELDS)
        # -----------------------------------
        results = []

        for obj in combined:

            results.append({

                "id": str(obj.id),
                "property_type": "user" if isinstance(obj, Property) else "agent",

                "label": obj.label,
                "city": obj.city,
                "perprice": getattr(obj, "perprice", None),
                "price": obj.price,
                "sq_ft": str(getattr(obj, "sq_ft", "")),
                "land_area": obj.land_area,

                # OWNER (different for both models)
                "owner": (
                    obj.owner if isinstance(obj, Property) and obj.owner
                    else getattr(obj, "user", None)
                ),

                "whatsapp": getattr(obj, "whatsapp", None),
                "phone": getattr(obj, "phone", None),
                "location": obj.location,

                # -----------------------------------
                # IMAGES SAFE HANDLING
                # -----------------------------------
                "images": (
                    [img.image.url for img in obj.images.all()]
                    if hasattr(obj, "images") and obj.images.exists()
                    else ([obj.image.url] if getattr(obj, "image", None) else [])
                ),

                # -----------------------------------
                # WISHLIST FLAG
                # -----------------------------------
                "is_wishlisted": str(obj.id) in wishlist_ids,
            })

        return Response(results, status=status.HTTP_200_OK)
    
    
class WishlistSortingAPIView(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        sort_by = request.query_params.get("sort", "default")

        # -----------------------------------
        # STEP 1: WISHLIST IDS
        # -----------------------------------
        wishlist_qs = Wishlist.objects.filter(user_id=user.id)

        wishlist_ids = set(
            str(i) for i in wishlist_qs.values_list("property_uuid", flat=True)
        )

        # -----------------------------------
        # STEP 2: GET BOTH MODELS
        # -----------------------------------
        user_properties = Property.objects.filter(
            id__in=wishlist_ids
        )

        agent_properties = AgentProperty.objects.filter(
            id__in=wishlist_ids
        )

        properties = list(user_properties) + list(agent_properties)

        # -----------------------------------
        # STEP 3: SORTING
        # -----------------------------------
        def safe_price(obj):
            try:
                return int(obj.price)
            except:
                return 0

        if sort_by == "latest":
            properties.sort(key=lambda x: x.created_at, reverse=True)

        elif sort_by == "price_low_to_high":
            properties.sort(key=safe_price)

        elif sort_by == "price_high_to_low":
            properties.sort(key=safe_price, reverse=True)

        # -----------------------------------
        # STEP 4: RESPONSE FORMAT (CLEAN)
        # -----------------------------------
        results = []

        for obj in properties:

            results.append({
                "id": str(obj.id),
                "property_type": "user" if isinstance(obj, Property) else "agent",
                "label": obj.label,
                "city": obj.city,
                "perprice": getattr(obj, "perprice", None),
                "price": obj.price,
                "sq_ft": str(getattr(obj, "sq_ft", "")),
                "land_area": obj.land_area,
                "owner": getattr(obj, "owner", "") if isinstance(obj, AgentProperty) else (obj.owner if obj.owner else None),
                "whatsapp": getattr(obj, "whatsapp", None),
                "phone": getattr(obj, "phone", None),
                "location": obj.location,

                # images safe handling
                "images": (
                    [img.image.url for img in obj.images.all()]
                    if hasattr(obj, "images") and obj.images.exists()
                    else ([obj.image.url] if getattr(obj, "image", None) else [])
                ),

                # 🔥 FIXED WISHLIST FLAG
                "is_wishlisted": str(obj.id) in wishlist_ids,
            })

        return Response(results, status=status.HTTP_200_OK)


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserProfileUpdateView(APIView):

    authentication_classes = [UserJWTAuthentication]  
    permission_classes = [IsAuthenticated]            
    def put(self, request):

        user = request.user   

        serializer = UserProfileUpdateSerializer(
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.update(user, serializer.validated_data)

        return Response(
            {"message": "Profile updated successfully"},
            status=200
        )




class MyActivityView(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        # ✅ Wishlist count
        wishlist_count = Wishlist.objects.filter(
            user=user
        ).count()

        # ✅ Enquiries count
        property_enquiries_count = PropertyEnquiry.objects.filter(
            user=user
        ).count()

        agent_property_enquiries_count = AgentPropertyEnquiry.objects.filter(
            user=user
        ).count()

        enquiries_count = (
            property_enquiries_count +
            agent_property_enquiries_count
        )


        # ✅ MATCH UserAdd USING EMAIL (NO RELATION NEEDED)
        user_add = UserCreate.objects.filter(
            email=user.email
        ).first()

        # ✅ Properties listed
        properties_listed_count = Property.objects.filter(
            user=user_add
        ).count() if user_add else 0

        # ✅ Viewed properties
        viewed_properties_count = PropertyView.objects.filter(
            user=user
        ).count()

        return Response({
            "wishlist_count": wishlist_count,
            "enquiries_count": enquiries_count,
            "properties_listed_count": properties_listed_count,
            "viewed_properties_count": viewed_properties_count,
        })

class UpdateAgentReviewAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]  # ✅ bypass default auth

    def get_user_from_token(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]

            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            user_id = decoded.get("user_id")

            if not user_id:
                return None

            # ✅ FIX: convert to UUID safely
            user_uuid = uuid.UUID(str(user_id))

            return UserCreate.objects.filter(id=user_uuid).first()

        except Exception:
            return None

    def put(self, request, review_id):

        user = self.get_user_from_token(request)

        if not user:
            return Response({"error": "User not found"}, status=401)

        try:
            review = AgentReview.objects.get(id=review_id)
        except AgentReview.DoesNotExist:
            return Response({"error": "Review not found"}, status=404)

        if review.user != user:
            return Response(
                {"error": "You can edit only your own review"},
                status=403
            )

        rating = request.data.get("rating")
        review_text = request.data.get("review")

        if rating is not None:
            review.rating = rating

        if review_text:
            review.review = review_text

        review.save()

        return Response({
            "message": "Review updated successfully",
            "data": {
                "id": str(review.id),
                "rating": review.rating,
                "review": review.review
            }
        }, status=200)



class DeleteAgentReviewAPIView(APIView):
    authentication_classes = []   # ❌ disable default JWT (important)
    permission_classes = []       # ❌ handle manually

    def get_user_from_token(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]

            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            user_id = decoded.get("user_id")

            # ✅ UUID SAFE QUERY
            return UserCreate.objects.filter(id=user_id).first()

        except Exception as e:
            return None

    def delete(self, request, review_id):

        user = self.get_user_from_token(request)

        if not user:
            return Response(
                {"error": "User not found"},
                status=401
            )

        try:
            review = AgentReview.objects.get(id=review_id)
        except AgentReview.DoesNotExist:
            return Response(
                {"error": "Review not found"},
                status=404
            )

        if review.user != user:
            return Response(
                {"error": "You can delete only your own review"},
                status=403
            )

        review.delete()

        return Response({
            "message": "Review deleted successfully"
        }, status=200)


class ActiveSliderAdsAPIView(ListAPIView):
    serializer_class = SliderAdSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        return SliderAd.objects.filter(is_active=True).order_by('-created_at')


class BannerAdsAPIView(ListAPIView):
    serializer_class = BannerAdSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        return BannerAd.objects.filter(is_active=True).order_by('-created_at')

class AgentDetailAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    # =====================================================
    # GET LOGGED USER
    # =====================================================

    def get_logged_user(self, request):

        auth_header = request.headers.get(
            "Authorization"
        )

        if not auth_header:
            return None

        try:

            token = auth_header.split(" ")[1]

            decoded = AccessToken(token)

            user_id = decoded.get("user_id")

            if not user_id:
                return None

            return UserCreate.objects.filter(
                id=user_id
            ).first()

        except Exception:
            return None

    # =====================================================
    # GET
    # =====================================================

    def get(self, request, agent_id):

        logged_user = self.get_logged_user(
            request
        )

        agent = None

        # =====================================================
        # UUID CHECK
        # =====================================================

        try:

            uuid_obj = uuid.UUID(agent_id)

            agent = AgentUserProfile.objects.filter(
                id=uuid_obj
            ).first()

        except ValueError:
            pass

        # =====================================================
        # AGENT CODE CHECK
        # =====================================================

        if not agent:

            agent = AgentUserProfile.objects.filter(
                agent_code=agent_id
            ).first()

        # =====================================================
        # NOT FOUND
        # =====================================================

        if not agent:

            return Response({
                "error": "Agent not found"
            }, status=404)

        # =====================================================
        # AGENT DATA
        # =====================================================

        agent_data = AgentDetailSerializer(
            agent,
            context={
                "request": request
            }
        ).data

        # =====================================================
        # PROPERTY QUERY
        # =====================================================

        queryset = AgentProperty.objects.filter(
            agent=agent
        )

        # =====================================================
        # CATEGORY FILTER
        # =====================================================

        category = request.GET.get(
            "category"
        )

        if category:

            queryset = queryset.filter(
                category__name__icontains=category
            )

        # =====================================================
        # SEARCH FILTER
        # =====================================================

        search = request.GET.get(
            "search"
        )

        if search:

            queryset = queryset.filter(

                Q(label__icontains=search) |

                Q(price__icontains=search) |

                Q(city__icontains=search)

            )

        queryset = queryset.distinct()

        total_properties = queryset.count()

        # =====================================================
        # PROPERTY SERIALIZER
        # =====================================================

        properties_data = []

        if agent.agent_type in [

            "premium",
            "elite"

        ]:

            queryset = queryset.order_by(
                "-created_at"
            )

            properties_data = AgentPropertySerializer(

                queryset,

                many=True,

                context={
                    "request": request
                }

            ).data
            wishlist_ids = []
            if logged_user:

                wishlist_ids = list(

                    Wishlist.objects.filter(
                        user=logged_user
                    ).values_list(
                        "property_uuid",
                        flat=True
                    )

                )

                wishlist_ids = [
                    str(i)
                    for i in wishlist_ids
                ]

                # wishlist_ids = [
                #     str(i)
                #     for i in wishlist_ids
                # ]

            for property_data in properties_data:

                property_data["is_wishlist"] = (

                    str(property_data["id"])
                    in wishlist_ids

                )

        # =====================================================
        # UPDATE REVIEW OWNER FIELD
        # =====================================================

        reviews = agent_data.get(
            "reviews",
            []
        )

        if logged_user:

            user_review_ids = list(

                AgentReview.objects.filter(

                    user=logged_user,
                    agent=agent

                ).values_list(
                    "id",
                    flat=True
                )
            )

            user_review_ids = [
                str(i)
                for i in user_review_ids
            ]

            for review in reviews:

                review["is_owner"] = (

                    str(review.get("id"))
                    in user_review_ids

                )

        # =====================================================
        # RESPONSE
        # =====================================================

        agent_data["properties_count"] = (
            total_properties
        )

        agent_data["properties"] = (
            properties_data
        )

        return Response(
            agent_data,
            status=200
        )


class PropertyFilterAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):

        queryset = Property.objects.all().order_by("-created_at")

        purpose = request.data.get("purpose")
        category = request.data.get("category")
        city = request.data.get("city")
        district = request.data.get("district")
        min_price = request.data.get("min_price")
        max_price = request.data.get("max_price")

        # -----------------------------
        # FILTERS
        # -----------------------------
        if purpose and purpose.lower() != "all":
            queryset = queryset.filter(purpose__name__icontains=purpose)

        if category and category.lower() != "all":
            queryset = queryset.filter(category__name__icontains=category)

        if city and city.lower() != "all":
            queryset = queryset.filter(city__icontains=city)

        if district and district.lower() != "all":
            queryset = queryset.filter(district__icontains=district)

        # -----------------------------
        # PRICE FILTER
        # -----------------------------
        if min_price or max_price:
            queryset = queryset.annotate(
                price_int=Cast("price", IntegerField())
            )

            if min_price:
                try:
                    queryset = queryset.filter(price_int__gte=int(min_price))
                except:
                    pass

            if max_price:
                try:
                    queryset = queryset.filter(price_int__lte=int(max_price))
                except:
                    pass

        serializer = PropertyCardSerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


import jwt
from itertools import chain

from django.conf import settings
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class PropertySearchAPIView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):

        raw_input = request.query_params.get(
            "label",
            ""
        ).strip().lower()

        user_properties = Property.objects.select_related(
            "user",
            "category",
            "purpose"
        ).prefetch_related("images")

        agent_properties = AgentProperty.objects.select_related(
            "agent",
            "category",
            "purpose"
        ).prefetch_related("images")


        price_prefix = None
        text_parts = []

        if raw_input:
            for part in raw_input.split():

                if part.isdigit():
                    price_prefix = part
                else:
                    text_parts.append(part)

        search_text = " ".join(text_parts)


        if search_text:

            user_properties = user_properties.filter(
                Q(label__icontains=search_text) |
                Q(city__icontains=search_text) |
                Q(district__icontains=search_text)
            )

            agent_properties = agent_properties.filter(
                Q(label__icontains=search_text) |
                Q(city__icontains=search_text) |
                Q(district__icontains=search_text)
            )


        if price_prefix:

            user_properties = user_properties.filter(
                price__startswith=price_prefix
            )

            agent_properties = agent_properties.filter(
                price__startswith=price_prefix
            )


        combined = list(
            chain(
                user_properties,
                agent_properties
            )
        )


        combined.sort(
            key=lambda x: x.created_at,
            reverse=True
        )


        # -------------------------
        # WISHLIST UUIDS
        # -------------------------
        wishlist_ids = set()

        auth = request.headers.get("Authorization")

        if auth:
            try:
                token = auth.split()[1]

                decoded = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )

                user_id = decoded.get("user_id")

                wishlist_ids = set(
                    str(x)
                    for x in Wishlist.objects.filter(
                        user_id=user_id
                    ).values_list(
                        "property_uuid",
                        flat=True
                    )
                )

            except Exception:
                pass


        serializer = CombinedPropertyListSerializer(
            combined,
            many=True,
            context={
                "request": request,
                "wishlist_ids": wishlist_ids
            }
        )


        return Response({
            "count": len(combined),
            "data": serializer.data
        })



class PropertyEnquiryByUserAPIView(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):

        user = request.user

        # enquiries received on properties owned by logged-in user
        enquiries = PropertyEnquiry.objects.filter(
            owner=user
        ).select_related(
            "user",
            "property"
        ).order_by("-created_at")


        serializer = PropertyEnquirySerializer(
            enquiries,
            many=True
        )

        return Response(
            {
                # "status": True,
                # "count": enquiries.count(),
                "data": serializer.data
            },
            status=200
        )

import re
from math import radians, sin, cos, sqrt, atan2

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Property
from .serializers import PropertySerializer


class NearbyPropertyAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    # ---------------------------
    # HAVERSINE FUNCTION
    # ---------------------------
    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371  # KM
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)

        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    # ---------------------------
    # EXTRACT LAT/LNG FROM URL
    # ---------------------------
    def extract_lat_lng(self, url):
        lat = lng = None

        if not url:
            return None, None

        # Pattern 1: @LAT,LNG
        match = re.search(r"@([0-9.\-]+),([0-9.\-]+)", url)
        if match:
            lat = float(match.group(1))
            lng = float(match.group(2))
            return lat, lng

        # Pattern 2: !2dLONG!3dLAT
        match = re.search(r"!2d([0-9.\-]+)!3d([0-9.\-]+)", url)
        if match:
            lng = float(match.group(1))
            lat = float(match.group(2))
            return lat, lng

        return None, None

    # ---------------------------
    # MAIN API
    # ---------------------------
    def get(self, request):

        # ✅ USER LOCATION
        try:
            user_lat = float(request.GET.get("lat"))
            user_lng = float(request.GET.get("lng"))
        except (TypeError, ValueError):
            return Response({"error": "lat & lng required"}, status=400)

        # ✅ OPTIONAL RADIUS (KM)
        radius = request.GET.get("radius")
        radius = float(radius) if radius else None

        properties = Property.objects.all()

        results = []

        for prop in properties:

            lat, lng = self.extract_lat_lng(prop.location)

            if lat is None or lng is None:
                continue

            distance = self.haversine(user_lat, user_lng, lat, lng)

            # ✅ APPLY RADIUS FILTER
            if radius and distance > radius:
                continue

            results.append((prop, distance))

        # ✅ SORT BY NEAREST
        results.sort(key=lambda x: x[1])

        results = results[:20]

        props = [item[0] for item in results]

        serializer = PropertySerializer(
            props,
            many=True,
            context={"request": request}
        ).data

        # ✅ ADD DISTANCE INTO RESPONSE
        final_data = []
        for i, item in enumerate(serializer):
            item["distance_km"] = round(results[i][1], 2)
            final_data.append(item)

        return Response({
            # "status": True,
            # "count": len(final_data),
            "data": final_data
        })

class AgentSearchAPIView(ListAPIView):
    serializer_class = AgentListFrontendSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        queryset = AgentUserProfile.objects.all()

        search = self.request.query_params.get("search", "").strip()
        username = self.request.query_params.get("username", "").strip()
        city = self.request.query_params.get("city", "").strip()
        agent_type = self.request.query_params.get("agent_type", "").strip()

        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(city__icontains=search) |
                Q(agent_type__icontains=search)
            )

        if username:
            queryset = queryset.filter(username__icontains=username)

        if city:
            queryset = queryset.filter(city__icontains=city)

        if agent_type:
            queryset = queryset.filter(agent_type__iexact=agent_type)

        return queryset.order_by("-created_at")


class AgentCityListAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):

        cities = (
            AgentUserProfile.objects
            .filter(is_agent=True, is_active=True)  # ✅ only active agents
            .exclude(city__isnull=True)
            .exclude(city__exact="")
            .values_list("city", flat=True)
            .distinct()
            .order_by("city")
        )

        return Response({
            "cities": list(cities)
        })

    def post(self, request):

        city = request.data.get("city")

        #  VALIDATION
        if not city or not str(city).strip():
            return Response({
                "count": 0,
                "data": [],
                "message": "City is required"
            })

        city = str(city).strip()

        # BASE QUERY (ONLY ACTIVE AGENTS)
        queryset = AgentUserProfile.objects.filter(
            is_agent=True,
            is_active=True
        )

        # SMART FILTER (CASE-INSENSITIVE + SAFE)
        queryset = queryset.filter(
            city__icontains=city
        )

        queryset = queryset.order_by("-created_at")

        #  NO RESULT HANDLING
        if not queryset.exists():
            return Response({
                "count": 0,
                "data": [],
                "message": "No agents found for this city"
            })

        # SERIALIZER
        serializer = AgentListFrontendSerializer(
            queryset,
            many=True,
            context={"request": request}
        )

        return Response({
            # "count": queryset.count(),
            "data": serializer.data
        })

class EnquiryDetailAPIView(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, enquiry_id):

        try:
            enquiry = PropertyEnquiry.objects.select_related(
                "property",
                "owner",
                "user"
            ).prefetch_related(
                "property__images"
            ).get(
                id=enquiry_id
            )

        except PropertyEnquiry.DoesNotExist:
            return Response(
                {"error": "Enquiry not found"},
                status=status.HTTP_404_NOT_FOUND
            )


        # ---------------------------------
        # only property owner can view
        # ---------------------------------
        if enquiry.owner != request.user:
            return Response(
                {
                    "error": "Unauthorized"
                },
                status=status.HTTP_403_FORBIDDEN
            )


        serializer = EnquiryDetailSerializer(
            enquiry,
            context={
                "request": request
            }
        )

        return Response({
            "status": True,
            "data": serializer.data
        })
    


from collections import defaultdict

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class PropertyFilterOptionsAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):

        # -------------------------
        # CATEGORY
        # -------------------------
        categories = list(
            Category.objects.values(
                "id",
                "name"
            ).order_by("name")
        )


        # -------------------------
        # PURPOSE
        # -------------------------
        purposes = list(
            Purpose.objects.values(
                "id",
                "name"
            ).order_by("name")
        )


        # -------------------------
        # DISTRICT -> CITIES
        # USER + AGENT PROPERTIES
        # -------------------------
        district_map = defaultdict(set)


        # user added properties
        user_properties = Property.objects.values(
            "district",
            "city"
        )


        # agent added properties
        agent_properties = AgentProperty.objects.values(
            "district",
            "city"
        )


        # combine both
        all_properties = list(user_properties) + list(agent_properties)


        for item in all_properties:

            district = (
                item.get("district", "")
                .strip()
            )

            city = (
                item.get("city", "")
                .strip()
            )


            if not district or not city:
                continue


            district_map[district].add(city)

        districts_data = []

        for district, cities in district_map.items():

            districts_data.append({
                "name": district,
                "cities": sorted(
                    list(cities)
                )
            })


        districts_data = sorted(
            districts_data,
            key=lambda x: x["name"].lower()
        )

        return Response({
            "categories": categories,
            "purposes": purposes,
            "districts": districts_data
        })


class CityDistrictFilterAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):

        city = request.GET.get("city")
        district = request.GET.get("district")

        queryset = Property.objects.all()

        if city:
            queryset = queryset.filter(city__iexact=city.strip())

        if district:
            queryset = queryset.filter(district__iexact=district.strip())

        cities = list(
            queryset.values_list("city", flat=True)
            .exclude(city__isnull=True)
            .exclude(city__exact="")
            .distinct()
        )

        districts = list(
            queryset.values_list("district", flat=True)
            .exclude(district__isnull=True)
            .exclude(district__exact="")
            .distinct()
        )

        return Response({
            # "status": True,
            "cities": cities,
            "districts": districts
        })

class RecentEnquiryAPIView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [UserJWTAuthentication]

    def get(self, request):
        user = request.user
        property_enquiries = (
            PropertyEnquiry.objects
            .select_related(
                "property",
                "property__user"
            )
            .filter(user=user)
            .order_by("-created_at")
        )
        agent_enquiries = (
            AgentPropertyEnquiry.objects
            .select_related(
                "property",
                "property__agent"
            )
            .filter(user=user)
            .order_by("-created_at")
        )
        property_data = RecentEnquirySerializer(
            property_enquiries,
            many=True
        ).data
        agent_data = RecentAgentEnquirySerializer(
            agent_enquiries,
            many=True
        ).data

        # =====================================================
        # ADD TYPE
        # =====================================================

        for item in property_data:

            item["enquiry_type"] = "property"

        for item in agent_data:

            item["enquiry_type"] = "agent_property"
        combined_data = list(
            chain(property_data, agent_data)
        )
        combined_data.sort(
            key=lambda x: x["created_at"],
            reverse=True
        )
        combined_data = combined_data[:10]

        return Response({

            "count": len(combined_data),

            "data": combined_data

        }, status=status.HTTP_200_OK)

class AgentPropertyLocationAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, agent_id):

        # -----------------------------
        # GET AGENT
        # -----------------------------
        agent = None

        try:
            uuid_obj = uuid.UUID(agent_id)
            agent = AgentUserProfile.objects.filter(id=uuid_obj).first()
        except ValueError:
            pass

        if not agent:
            agent = AgentUserProfile.objects.filter(agent_code=agent_id).first()

        if not agent:
            return Response({"error": "Agent not found"}, status=404)

        # -----------------------------
        # BASE QUERY
        # -----------------------------
        queryset = AgentProperty.objects.filter(agent=agent)

        # -----------------------------
        # GET CITY PARAM
        # -----------------------------
        city = request.GET.get("city")

        # -----------------------------
        # STEP 1 → RETURN CITIES
        # -----------------------------
        if not city:
            cities = list(
                queryset.exclude(city__isnull=True)
                .exclude(city__exact="")
                .values_list("city", flat=True)
                .distinct()
            )

            return Response({
                "agent_id": str(agent.id),
                "cities": cities
            })

        # -----------------------------
        # STEP 2 → FILTER BY CITY
        # -----------------------------
        queryset = queryset.filter(city__icontains=city)

        queryset = queryset.order_by("-created_at")

        serializer = AgentPropertySerializer(
            queryset,
            many=True,
            context={"request": request}
        )

        return Response({
            "agent_id": str(agent.id),
            "selected_city": city,
            "count": queryset.count(),
            "data": serializer.data
        })
    

import uuid

from django.db.models.functions import Lower, Trim

class AgentPropertyCityFilterAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, agent_id):

        agent = None

        try:
            uuid_obj = uuid.UUID(agent_id)
            agent = AgentUserProfile.objects.filter(
                id=uuid_obj
            ).first()
        except ValueError:
            pass

        if not agent:
            agent = AgentUserProfile.objects.filter(
                agent_code=agent_id
            ).first()


        if not agent:
            return Response(
                {"error": "Agent not found"},
                status=404
            )

        if agent.agent_type not in ["premium", "elite"]:
            return Response({
                "agent_type": agent.agent_type,
                "cities": [],
                "message": "City filters only available for premium/elite agents"
            })


        cities = (
            AgentProperty.objects.filter(
                agent=agent
            )
            .exclude(city__isnull=True)
            .exclude(city__exact="")
            .annotate(
                clean_city=Lower(Trim("city"))
            )
            .order_by("clean_city")
            .values_list("city", flat=True)
            .distinct()
        )


        return Response({
            "agent_id": str(agent.id),
            "agent_name": agent.username,
            "agent_type": agent.agent_type,
            "cities": list(cities)
        })

    def post(self, request, agent_id):

        city = request.data.get("city")

        if not city:
            return Response({
                "error":"city is required"
            }, status=400)


        agent = None

        try:
            uuid_obj = uuid.UUID(agent_id)
            agent = AgentUserProfile.objects.filter(
                id=uuid_obj
            ).first()

        except ValueError:
            pass


        if not agent:
            agent = AgentUserProfile.objects.filter(
                agent_code=agent_id
            ).first()


        if not agent:
            return Response(
                {"error":"Agent not found"},
                status=404
            )


        queryset = AgentProperty.objects.filter(
            agent=agent
        ).annotate(
            clean_city=Lower(Trim("city"))
        ).filter(
            clean_city=city.strip().lower()
        ).order_by("-created_at")


        serializer = AgentPropertySerializer(
            queryset,
            many=True,
            context={"request": request}
        )


        return Response({
            "agent_id": str(agent.id),
            "selected_city": city,
            "count": queryset.count(),
            "properties": serializer.data
        })
    

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import uuid


class AgentPropertySearchAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def get_agent(self, agent_id):

        agent = None
        try:

            uuid_obj = uuid.UUID(agent_id)

            agent = AgentUserProfile.objects.filter(
                id=uuid_obj
            ).first()

        except ValueError:
            pass

        if not agent:

            agent = AgentUserProfile.objects.filter(
                agent_code=agent_id
            ).first()

        return agent

    def get(self, request, agent_id):
        search = request.GET.get(
            "search",
            ""
        ).strip()

        category = request.GET.get(
            "category",
            ""
        ).strip()
        agent = self.get_agent(agent_id)

        if not agent:

            return Response({
                "error": "Agent not found"
            }, status=404)

        if agent.agent_type not in [
            "premium",
            "elite"
        ]:

            return Response({
                "agent_type": agent.agent_type,
                "properties": [],
                "message": "Search only available for premium/elite agents"
            })

        queryset = AgentProperty.objects.select_related(
            "category",
            "subcategory",
            "purpose",
            "agent"
        ).prefetch_related(
            "images"
        ).filter(
            agent=agent
        )
        if search:

            queryset = queryset.filter(

                Q(label__icontains=search)

                |

                Q(price__icontains=search)

            )

        if category:

            queryset = queryset.filter(
                category__name__icontains=category
            )
        queryset = queryset.distinct().order_by(
            "-created_at"
        )

        serializer = AgentPropertySerializer(
            queryset,
            many=True,
            context={
                "request": request
            }
        )
        return Response({

            "agent_id": str(agent.id),

            "agent_name": agent.username,

            "agent_type": agent.agent_type,

            # "search": search,

            # "category": category,

            "count": queryset.count(),

            "properties": serializer.data

        })

class CombinedPropertyListAPIView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):

        user_properties = Property.objects.select_related(
            "user",
            "category",
            "purpose"
        ).prefetch_related(
            "images"
        )

        agent_properties = AgentProperty.objects.select_related(
            "agent",
            "category",
            "purpose"
        ).prefetch_related(
            "images"
        )

        category = request.GET.get("category")
        purpose = request.GET.get("purpose")
        city = request.GET.get("city")
        search = request.GET.get("search")
        price_range = request.GET.get("price_range")

        if category:

            user_properties = user_properties.filter(
                category__name__icontains=category
            )

            agent_properties = agent_properties.filter(
                category__name__icontains=category
            )

        if purpose:

            user_properties = user_properties.filter(
                purpose__name__icontains=purpose
            )

            agent_properties = agent_properties.filter(
                purpose__name__icontains=purpose
            )

        if city:

            user_properties = user_properties.filter(
                city__icontains=city
            )

            agent_properties = agent_properties.filter(
                city__icontains=city
            )

        if search:

            user_properties = user_properties.filter(
                Q(label__icontains=search) |
                Q(city__icontains=search) |
                Q(price__icontains=search)
            )

            agent_properties = agent_properties.filter(
                Q(label__icontains=search) |
                Q(city__icontains=search) |
                Q(price__icontains=search)
            )

        user_properties = list(user_properties)
        agent_properties = list(agent_properties)

        if price_range:

            user_properties = [
                p for p in user_properties
                if self.check_price_range(
                    p.price,
                    price_range
                )
            ]

            agent_properties = [
                p for p in agent_properties
                if self.check_price_range(
                    p.price,
                    price_range
                )
            ]

        combined = user_properties + agent_properties
        combined.sort(
            key=lambda x: x.created_at,
            reverse=True
        )

        wishlist_ids = set()

        auth = request.headers.get(
            "Authorization"
        )

        if auth:

            try:

                token = auth.split()[1]

                decoded = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )

                user_id = (
                    decoded.get("user_id")
                    or decoded.get("id")
                )

                if user_id:

                    wishlist_ids = set(
                        str(x)
                        for x in Wishlist.objects.filter(
                            user_id=user_id
                        ).values_list(
                            "property_uuid",
                            flat=True
                        )
                    )

            except (
                ExpiredSignatureError,
                InvalidTokenError
            ):
                pass

        # --------------------------------
        # UUID FIX
        # --------------------------------

        for item in combined:

            # convert UUID into string safely
            item.id = str(item.id)

            # optional uuid field support
            if hasattr(item, "uuid") and item.uuid:
                item.uuid = str(item.uuid)

        serializer = CombinedPropertyListSerializer(
            combined,
            many=True,
            context={
                "request": request,
                "wishlist_ids": wishlist_ids
            }
        )

        return Response({
            "count": len(combined),
            "data": serializer.data
        })

    # --------------------------------
    # PRICE CONVERTER
    # --------------------------------

    def convert_price_to_number(self, price):

        try:

            if not price:
                return 0

            cleaned = str(price)

            cleaned = (
                cleaned
                .replace("₹", "")
                .replace(",", "")
                .replace("Lakhs+", "")
                .replace("Lakhs", "")
                .replace("Lakh+", "")
                .replace("Lakh", "")
                .strip()
            )

            return float(cleaned)

        except:
            return 0

    # --------------------------------
    # PRICE RANGE CHECKER
    # --------------------------------

    def check_price_range(self, price, price_range):

        amount = self.convert_price_to_number(
            price
        )

        # Below ₹5 Lakhs
        if price_range == "Below ₹5 Lakhs":
            return amount < 500000

        # ₹5 – 10 Lakhs
        elif price_range == "₹5 – 10 Lakhs":
            return 500000 <= amount <= 1000000

        # ₹10 – 25 Lakhs
        elif price_range == "₹10 – 25 Lakhs":
            return 1000000 <= amount <= 2500000

        # ₹25 – 50 Lakhs
        elif price_range == "₹25 – 50 Lakhs":
            return 2500000 <= amount <= 5000000

        # Above ₹50 Lakhs
        elif price_range == "Above ₹50 Lakhs":
            return amount > 5000000

        return True
        
from uuid import UUID

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import UserProfile

class UniversalPropertyDetailAPIView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]
    def get_logged_user(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:

            token = auth_header.split(" ")[1]

            decoded = AccessToken(token)

            user_id = decoded.get("user_id")

            if user_id:

                return UserCreate.objects.filter(
                    id=user_id
                ).first()

        except Exception:
            pass

        return None


    def get_logged_agent(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:

            token = auth_header.split(" ")[1]

            decoded = AccessToken(token)

            agent_id = decoded.get("agent_id")

            if agent_id:

                return AgentUserProfile.objects.filter(
                    id=agent_id
                ).first()

        except Exception:
            pass

        return None

    # =====================================================
    # GET PROFILE IMAGE
    # =====================================================

    def get_profile_image(self, person, request):

        if not person:
            return None

        # ===== USER PROFILE =====

        try:

            profile = UserProfile.objects.filter(
                user=person
            ).first()

            if profile:

                if profile.image:

                    try:

                        return request.build_absolute_uri(
                            profile.image.url
                        )

                    except:

                        return profile.image.url

                if hasattr(profile, "profile_image_url"):

                    return profile.profile_image_url

        except:
            pass

        # ===== AGENT PROFILE =====

        if getattr(person, "profile_image", None):

            try:

                return request.build_absolute_uri(
                    person.profile_image.url
                )

            except:

                return person.profile_image.url

        # ===== AGENT AVATAR =====

        if getattr(person, "avatar_url", None):

            return person.avatar_url

        return None

    # =====================================================
    # OWNER NAME
    # =====================================================

    def get_owner_name(self, owner_text, user_obj):

        # =========================================
        # MANUAL OWNER NAME
        # =========================================

        if owner_text and str(owner_text).strip():

            return str(owner_text).strip()

        # =========================================
        # FALLBACK USER NAME
        # =========================================

        if user_obj:

            if hasattr(user_obj, "name"):

                if user_obj.name:

                    return user_obj.name

            if hasattr(user_obj, "username"):

                if user_obj.username:

                    return user_obj.username

            if hasattr(user_obj, "email"):

                if user_obj.email:

                    return user_obj.email

        return ""

    # =====================================================
    # GET
    # =====================================================

    def get(self, request, uuid_id):
        logged_user = self.get_logged_user(request)

        logged_agent = self.get_logged_agent(request)

        # =========================================
        # VALIDATE UUID
        # =========================================

        try:

            uuid_obj = UUID(str(uuid_id))

        except ValueError:

            return Response({
                "error": "Invalid UUID format"
            }, status=400)
        
        obj = Property.objects.filter(
            id=uuid_obj
        ).first()

        if obj:

            is_wishlist = False

            # if request.user.is_authenticated:
            #     is_wishlist = Wishlist.objects.filter(
            #         user=request.user,
            #         property_uuid=obj.id
            #     ).exists()
            if logged_user:

                is_wishlist = Wishlist.objects.filter(
                    user=logged_user,
                    property_uuid=obj.id
                ).exists()

            serializer = UserPropertySerializer(
                obj,
                context={"request": request}
            )

            # data = serializer.data

            # return Response({
            #     ...
            #     "is_wishlist": is_wishlist,
            # })

        # =====================================================
        # USER PROPERTY
        # =====================================================

        obj = Property.objects.filter(
            id=uuid_obj
        ).first()

        if obj:

            serializer = UserPropertySerializer(
                obj,
                context={
                    "request": request
                }
            )

            data = serializer.data

            return Response({

                "id": str(obj.id),

                "property_code": (
                    obj.property_code
                ),

                "label": data.get("label"),

                "images": data.get(
                    "images",
                    []
                ),

                "purpose": (
                    obj.purpose.name
                    if obj.purpose else None
                ),

                "category": {

                    "id": obj.category.id,

                    "name": obj.category.name,

                    "image": None
                },

                "description": obj.description,

                "city": obj.city,

                "state": obj.state,

                "location": obj.location,

                "land_mark": data.get(
                    "landmarks",
                    []
                ),

                "created_at": obj.created_at.strftime(
                    "%Y-%m-%d"
                ),

                "property_features": data.get(
                    "features",
                    []
                ),

                "price_details": {

                    "price": obj.price,

                    "sq_ft": str(obj.sq_ft),

                    "land_area": obj.land_area,

                    "perprice": obj.perprice
                },

                # =================================================
                # CONTACT DETAILS
                # =================================================

                "contact_details": {

                    # OWNER FIELD
                    # if empty -> user.name

                    "owner": self.get_owner_name(
                        obj.owner,
                        obj.user
                    ),

                    "whatsapp": obj.whatsapp,

                    "phone": obj.phone,

                    # PROFILE IMAGE ALWAYS FROM USER

                    "owner_profile_image": (
                        self.get_profile_image(
                            obj.user,
                            request
                        )
                    )
                },

                "amenities": [

                    {
                        "name": a.name,

                        "icon": (
                            request.build_absolute_uri(
                                a.icon.url
                            )

                            if getattr(
                                a,
                                "icon",
                                None
                            )

                            else None
                        )
                    }

                    for a in obj.amenities.all()
                ],

                "key_selling_points": data.get(
                    "selling_points",
                    []
                ),

                "location_details": {

                    "village": obj.village,

                    "city": obj.city,

                    "state": obj.state,

                    "pincode": obj.pincode
                },
                "is_wishlist": is_wishlist
            })

        # =====================================================
        # AGENT PROPERTY
        # =====================================================

        obj = AgentProperty.objects.filter(
            id=uuid_obj
        ).first()

        if obj:

            is_wishlist = False

            # if request.user.is_authenticated:
            #     is_wishlist = Wishlist.objects.filter(
            #         user=request.user,
            #         property_uuid=obj.id
            #     ).exists()
            if logged_user:

                is_wishlist = Wishlist.objects.filter(
                    user=logged_user,
                    property_uuid=obj.id
                ).exists()

            serializer = AgentPropertySerializer(
                obj,
                context={"request": request}
            )

        if obj:

            serializer = AgentPropertySerializer(
                obj,
                context={
                    "request": request
                }
            )

            data = serializer.data

            agent_obj = obj.agent

            return Response({

                "id": str(obj.id),

                "property_code": f"AG-{obj.id}",

                "label": data.get("label"),

                "images": data.get(
                    "images",
                    []
                ),

                "purpose": (
                    obj.purpose.name
                    if obj.purpose else None
                ),

                "category": {

                    "id": obj.category.id,

                    "name": obj.category.name,

                    "image": None
                },

                "description": obj.description,

                "city": obj.city,

                "state": obj.state,

                "location": obj.location,

                "land_mark": data.get(
                    "landmarks",
                    []
                ),

                "created_at": obj.created_at.strftime(
                    "%Y-%m-%d"
                ),

                "property_features": data.get(
                    "features",
                    []
                ),

                "price_details": {

                    "price": obj.price,

                    "sq_ft": str(obj.sq_ft),

                    "land_area": obj.land_area,

                    "perprice": obj.perprice
                },

                "contact_details": {

                    "owner": self.get_owner_name(
                        obj.owner,
                        agent_obj
                    ),

                    "whatsapp": obj.whatsapp,

                    "phone": obj.phone,

                    "owner_profile_image": (
                        self.get_profile_image(
                            agent_obj,
                            request
                        )
                    )
                },

                "amenities": [

                    {
                        "name": a.name,

                        "icon": (
                            request.build_absolute_uri(
                                a.icon.url
                            )

                            if getattr(
                                a,
                                "icon",
                                None
                            )

                            else None
                        )
                    }

                    for a in obj.amenities.all()
                ],

                "key_selling_points": data.get(
                    "selling_points",
                    []
                ),

                "location_details": {

                    "village": obj.village,

                    "city": obj.city,

                    "state": obj.state,

                    "pincode": obj.pincode
                },
                "is_wishlist": is_wishlist
            })

        return Response({
            "error": "Property not found"
        }, status=404)



from uuid import UUID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class UniversalPropertyEnquiryAPI(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user
        uuid_id = request.data.get("property")

        if not uuid_id:
            return Response(
                {"error": "property id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ================= VALIDATE UUID =================
        try:
            uuid_obj = UUID(str(uuid_id))
        except ValueError:
            return Response(
                {"error": "Invalid UUID"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ================= USER PROPERTY =================
        prop = Property.objects.filter(id=uuid_obj).first()   # 🔥 FIX

        if prop:

            serializer = PropertyEnquirySerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=400)

            enquiry = serializer.save(
                user=user,
                property=prop
            )

            return Response({
                "status": True,
                "message": "Enquiry sent successfully",
                "type": "user_property",
                "data": PropertyEnquirySerializer(enquiry).data
            }, status=201)

        # ================= AGENT PROPERTY =================
        agent_prop = AgentProperty.objects.filter(id=uuid_obj).first()  # 🔥 FIX

        if agent_prop:

            serializer = AgentPropertyEnquirySerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=400)

            enquiry = serializer.save(
                user=user,
                property=agent_prop
            )

            return Response({
                "status": True,
                "message": "Enquiry sent successfully",
                "type": "agent_property",
                "data": AgentPropertyEnquirySerializer(enquiry).data
            }, status=201)

        return Response(
            {"error": "Property not found"},
            status=status.HTTP_404_NOT_FOUND
        )


import re
import jwt

from itertools import chain
from math import radians, sin, cos, sqrt, atan2

from django.conf import settings

from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError
)

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class NearbyPropertyAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    # --------------------------------
    # HAVERSINE
    # --------------------------------
    def haversine(
        self,
        lat1,
        lon1,
        lat2,
        lon2
    ):
        R = 6371

        dlat = radians(
            lat2 - lat1
        )

        dlon = radians(
            lon2 - lon1
        )

        a = (
            sin(dlat/2) ** 2
            +
            cos(radians(lat1))
            *
            cos(radians(lat2))
            *
            sin(dlon/2) ** 2
        )

        c = 2 * atan2(
            sqrt(a),
            sqrt(1-a)
        )

        return R * c


    # --------------------------------
    # EXTRACT LAT LNG
    # --------------------------------
    def extract_lat_lng(
        self,
        url
    ):

        if not url:
            return None, None

        url = str(url).strip()


        # @lat,lng
        match = re.search(
            r'@([0-9\-.]+),([0-9\-.]+)',
            url
        )

        if match:
            return (
                float(match.group(1)),
                float(match.group(2))
            )


        # !2dLONG!3dLAT
        match = re.search(
            r'!2d([0-9\-.]+)!3d([0-9\-.]+)',
            url
        )

        if match:
            return (
                float(match.group(2)),
                float(match.group(1))
            )


        # q=lat,lng
        match = re.search(
            r'q=([0-9\-.]+),([0-9\-.]+)',
            url
        )

        if match:
            return (
                float(match.group(1)),
                float(match.group(2))
            )

        return None, None


    # --------------------------------
    # GET
    # --------------------------------
    def get(self, request):

        try:
            user_lat = float(
                request.GET.get("lat")
            )

            user_lng = float(
                request.GET.get("lng")
            )

        except:
            return Response(
                {
                    "error": "lat & lng required"
                },
                status=400
            )


        radius = request.GET.get(
            "radius"
        )

        radius = (
            float(radius)
            if radius else None
        )


        # --------------------------------
        # USER PROPERTIES
        # --------------------------------
        user_properties = Property.objects.select_related(
            "user",
            "category",
            "purpose"
        ).prefetch_related(
            "images"
        )


        # --------------------------------
        # AGENT PROPERTIES
        # --------------------------------
        agent_properties = AgentProperty.objects.select_related(
            "agent",
            "category",
            "purpose"
        )


        all_properties = list(
            chain(
                user_properties,
                agent_properties
            )
        )


        # --------------------------------
        # AUTH USER WISHLIST
        # --------------------------------
        wishlist_ids = set()

        auth = request.headers.get(
            "Authorization"
        )

        if auth:
            try:
                token = auth.split()[1]

                decoded = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )

                user_id = (
                    decoded.get("user_id")
                    or decoded.get("id")
                )

                if user_id:

                    wishlist_ids = set(
                        str(x)
                        for x in
                        Wishlist.objects.filter(
                            user_id=user_id
                        ).values_list(
                            "property_uuid",
                            flat=True
                        )
                    )

            except (
                ExpiredSignatureError,
                InvalidTokenError
            ):
                pass


        # --------------------------------
        # DISTANCE FILTER
        # --------------------------------
        results = []

        for prop in all_properties:

            lat, lng = self.extract_lat_lng(
                prop.location
            )

            if lat is None:
                continue


            distance = self.haversine(
                user_lat,
                user_lng,
                lat,
                lng
            )


            if radius and distance > radius:
                continue


            results.append(
                (
                    prop,
                    distance
                )
            )


        # nearest first
        results.sort(
            key=lambda x: x[1]
        )

        results = results[:20]


        properties = [
            item[0]
            for item in results
        ]


        serialized = CombinedPropertyListSerializer(
            properties,
            many=True,
            context={
                "request": request,
                "wishlist_ids": wishlist_ids
            }
        ).data


        final = []

        for i, item in enumerate(serialized):

            item["distance_km"] = round(
                results[i][1],
                2
            )

            final.append(item)


        return Response({
            "count": len(final),
            "data": final
        })

import jwt

from itertools import chain

from django.conf import settings
from django.db.models import IntegerField
from django.db.models import Q
from django.db.models.functions import Cast

from jwt import (
    ExpiredSignatureError,
    InvalidTokenError
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status


class PropertiesFilterAPIView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []


    def post(self, request):

        # --------------------------------
        # QUERYSETS
        # --------------------------------
        user_queryset = Property.objects.select_related(
            "user",
            "category",
            "purpose"
        ).prefetch_related(
            "images"
        )


        agent_queryset = AgentProperty.objects.select_related(
            "agent",
            "category",
            "purpose"
        ).order_by("-created_at")


        purpose = request.data.get("purpose")
        category = request.data.get("category")
        city = request.data.get("city")
        district = request.data.get("district")
        min_price = request.data.get("min_price")
        max_price = request.data.get("max_price")


        # -------------------------
        # PURPOSE
        # -------------------------
        if purpose and purpose.lower() != "all":

            user_queryset = user_queryset.filter(
                purpose__name__icontains=purpose
            )

            agent_queryset = agent_queryset.filter(
                purpose__name__icontains=purpose
            )


        # -------------------------
        # CATEGORY
        # -------------------------
        if category and category.lower() != "all":

            user_queryset = user_queryset.filter(
                category__name__icontains=category
            )

            agent_queryset = agent_queryset.filter(
                category__name__icontains=category
            )


        # -------------------------
        # CITY
        # -------------------------
        if city and city.lower() != "all":

            user_queryset = user_queryset.filter(
                city__icontains=city
            )

            agent_queryset = agent_queryset.filter(
                city__icontains=city
            )


        # -------------------------
        # DISTRICT
        # -------------------------
        if district and district.lower() != "all":

            user_queryset = user_queryset.filter(
                district__icontains=district
            )

            agent_queryset = agent_queryset.filter(
                district__icontains=district
            )


        # -------------------------
        # PRICE FILTER
        # -------------------------
        if min_price or max_price:

            user_queryset = user_queryset.annotate(
                price_int=Cast(
                    "price",
                    IntegerField()
                )
            )

            agent_queryset = agent_queryset.annotate(
                price_int=Cast(
                    "price",
                    IntegerField()
                )
            )


            if min_price:
                try:
                    min_price = int(min_price)

                    user_queryset = user_queryset.filter(
                        price_int__gte=min_price
                    )

                    agent_queryset = agent_queryset.filter(
                        price_int__gte=min_price
                    )
                except:
                    pass


            if max_price:
                try:
                    max_price = int(max_price)

                    user_queryset = user_queryset.filter(
                        price_int__lte=max_price
                    )

                    agent_queryset = agent_queryset.filter(
                        price_int__lte=max_price
                    )
                except:
                    pass


        # -------------------------
        # COMBINE
        # -------------------------
        combined = list(
            chain(
                user_queryset,
                agent_queryset
            )
        )


        combined.sort(
            key=lambda x: x.created_at,
            reverse=True
        )


        # -------------------------
        # WISHLIST FIX
        # -------------------------
        wishlist_ids = set()

        auth = request.headers.get(
            "Authorization"
        )

        if auth:
            try:
                token = auth.split()[1]

                decoded = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )

                user_id = (
                    decoded.get("user_id")
                    or decoded.get("id")
                )


                if user_id:
                    wishlist_ids = set(
                        str(x)
                        for x in Wishlist.objects.filter(
                            user_id=user_id
                        ).values_list(
                            "property_uuid",
                            flat=True
                        )
                    )

            except (
                ExpiredSignatureError,
                InvalidTokenError
            ):
                pass


        serializer = CombinedPropertyListSerializer(
            combined,
            many=True,
            context={
                "request": request,
                "wishlist_ids": wishlist_ids
            }
        )


        return Response(
            {
                "count": len(combined),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt


class UnifiedJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        token = self.get_token(request)
        if not token:
            return None

        try:
            payload = jwt.decode(token, options={"verify_signature": False})
        except Exception:
            raise AuthenticationFailed("Invalid token")

        email = payload.get("email")

        if email:
            email = email.lower().strip()

            user = UserCreate.objects.filter(email=email).first()
            if user:
                return (user, token)

            agent = AgentUserProfile.objects.filter(email=email).first()
            if agent:
                return (agent, token)

        user_id = payload.get("user_id") or payload.get("id")

        if user_id:

            user = UserCreate.objects.filter(id=user_id).first()
            if user:
                return (user, token)

            agent = AgentUserProfile.objects.filter(id=user_id).first()
            if agent:
                return (agent, token)

        role = payload.get("role") or payload.get("type")

        if role == "agent":
            raise AuthenticationFailed("Agent token missing valid identity mapping")

        if role == "user":
            raise AuthenticationFailed("User token missing valid identity mapping")

        raise AuthenticationFailed("Invalid token payload")

    def get_token(self, request):
        auth = request.headers.get("Authorization")

        if not auth:
            return None

        parts = auth.split()
        if len(parts) != 2:
            return None

        return parts[1]

class UnifiedEnquiryListAPIView(APIView):

    authentication_classes = [UnifiedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        if not user or not hasattr(user, "id"):
            return Response(
                {"status": False, "message": "Invalid user"},
                status=401
            )

        result = []
        if isinstance(user, UserCreate):

            enquiries = PropertyEnquiry.objects.filter(
                property__user=user
            ).select_related("property")

            for e in enquiries:
                result.append({
                    "enquiry_id": str(e.id),
                    # "type": "user_property",
                    "name": e.name,
                    "email": e.email,
                    "phone": e.phone,
                    "property": e.property.label,
                    "price": e.property.price,
                    "time": e.created_at.strftime("%Y-%m-%d %H:%M:%S")
                })

        elif isinstance(user, AgentUserProfile):

            enquiries = AgentPropertyEnquiry.objects.filter(
                property__agent=user
            ).select_related("property")

            for e in enquiries:
                result.append({
                    "enquiry_id": str(e.id),
                    # "type": "agent_property",
                    "name": e.name,
                    "email": e.email,
                    "phone": e.phone,
                    "property": e.property.label,
                    "price": e.property.price,
                    "time": e.created_at.strftime("%Y-%m-%d %H:%M:%S")
                })

        return Response({
            # "status": True,
            # "role": user.__class__.__name__,
            # "count": len(result),
            "data": sorted(result, key=lambda x: x["time"], reverse=True)
        })

    def post(self, request):
        return Response(
            {"status": False, "message": "POST not allowed"},
            status=405
        )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class EnquiryDetailAPIView(APIView):

    authentication_classes = [UnifiedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        user = request.user
        if not user or not hasattr(user, "id"):
            return None
        return user

    def get(self, request, enquiry_id):

        user = self.get_user(request)

        if not user:
            return Response(
                {"status": False, "message": "Invalid user"},
                status=401
            )

        enquiry = PropertyEnquiry.objects.filter(id=enquiry_id).first()

        if enquiry:

            if not isinstance(user, UserCreate) or enquiry.property.user != user:
                return Response(
                    {"status": False, "message": "Not allowed"},
                    status=403
                )

            return Response({
                # "status": True,
                # "type": "user_property",
                "data": {
                    "enquiry_id": str(enquiry.id),
                    "name": enquiry.name,
                    "email": enquiry.email,
                    "phone": enquiry.phone,
                    "message": enquiry.message,

                    "created_at": enquiry.created_at.strftime("%B %d, %Y %I:%M %p"),

                    "property": {
                        "id": str(enquiry.property.id),
                        "label": enquiry.property.label,
                        "price": enquiry.property.price,
                        "description": enquiry.property.description,
                        # "image": enquiry.property.image.url if enquiry.property.image else None,
                        "image": (
                            enquiry.property.images.first().image.url
                            if enquiry.property.images.exists()
                            else None
                        ),
                        # "location": {
                        #     "city": enquiry.property.city,
                        #     "district": enquiry.property.district,
                        #     "state": enquiry.property.state
                        # }
                        "location": ", ".join(
                            filter(None, [
                                enquiry.property.city,
                                enquiry.property.district,
                                enquiry.property.state
                            ])
                        )
                    }
                }
            })

       
        enquiry = AgentPropertyEnquiry.objects.filter(id=enquiry_id).first()

        if enquiry:

            if not isinstance(user, AgentUserProfile) or enquiry.property.agent != user:
                return Response(
                    {"status": False, "message": "Not allowed"},
                    status=403
                )

            return Response({
                # "status": True,
                # "type": "user_property",
                "data": {
                    "enquiry_id": str(enquiry.id),
                    "name": enquiry.name,
                    "email": enquiry.email,
                    "phone": enquiry.phone,
                    "message": enquiry.message,

                    "created_at": enquiry.created_at.strftime("%B %d, %Y %I:%M %p"),

                    "property": {
                        "id": str(enquiry.property.id),
                        "label": enquiry.property.label,
                        "price": enquiry.property.price,
                        "description": enquiry.property.description,
                        "image": enquiry.property.image.url if enquiry.property.image else None,
                        "location": ", ".join(
                            filter(None, [
                                enquiry.property.city,
                                enquiry.property.district,
                                enquiry.property.state
                            ])
                        )
                    }
                }
            })

       
        return Response(
            {"status": False, "message": "Enquiry not found"},
            status=404
        )

class UserPropertyDetailAPIView(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, request, id):

        try:

            return Property.objects.filter(
                id=id,
                user=request.user
            ).select_related(
                "category",
                "subcategory",
                "purpose",
                "package"
            ).first()

        except Exception:
            return None

    # =========================================================
    # JSON PARSER
    # =========================================================

    def parse_json(self, value):

        if not value:
            return None

        if isinstance(value, list):
            return value

        if isinstance(value, dict):
            return value

        if isinstance(value, str):

            try:
                return json.loads(value)

            except Exception:
                return value

        return value

    # =========================================================
    # LIST PARSER
    # =========================================================

    def parse_list_field(self, request, field_name):

        raw_values = request.data.getlist(field_name)

        if not raw_values:

            single_value = request.data.get(field_name)

            if single_value:
                raw_values = [single_value]

        parsed = []

        for value in raw_values:

            if not value:
                continue

            if isinstance(value, str):

                try:
                    decoded = json.loads(value)

                except Exception:
                    decoded = value

            else:
                decoded = value

            if isinstance(decoded, list):

                parsed.extend(decoded)

            elif isinstance(decoded, dict):

                parsed.append(decoded)

            else:

                parsed.append(decoded)

        return parsed

    # =========================================================
    # GET
    # =========================================================

    def get(self, request, id):

        obj = self.get_object(
            request,
            id
        )

        if not obj:

            return Response({

                "status": False,
                "message": "Property not found"

            }, status=status.HTTP_404_NOT_FOUND)

        # =====================================================
        # PROPERTY LIMIT DATA
        # =====================================================

        # limit_data = get_property_remaining_counts(
        #     request.user
        # )
        # Only subscription properties need plan limit calculation
        # limit_data = None
        limit_data = get_property_remaining_counts(request.user)

        if obj.subscription:
            limit_data = get_property_remaining_counts(
                request.user
            )

        serializer = UserPropertySerializer(
            obj,
            context={
                "request": request
            }
        )

        return Response({

            "status": True,

            "remaining_property":
            limit_data["remaining_property"],

            "residential_remaining":
            limit_data["residential_remaining"],

            "commercial_remaining":
            limit_data["commercial_remaining"],

            "data":
            serializer.data

        }, status=status.HTTP_200_OK)

    # =========================================================
    # UPDATE
    # =========================================================

    def put(self, request, id):

        obj = self.get_object(
            request,
            id
        )

        if not obj:

            return Response({

                "status": False,
                "message": "Property not found"

            }, status=status.HTTP_404_NOT_FOUND)

        # =====================================================
        # PROPERTY LIMIT DATA
        # =====================================================

        limit_data = get_property_remaining_counts(
            request.user
        )
        subscription = obj.subscription

        use_subscription = None

        if subscription:

            if (
                subscription.is_active
                and
                subscription.expiry_date > timezone.now()
            ):

                if subscription.is_unlimited_edit:

                    use_subscription = subscription

                elif (
                    not subscription.has_no_edit
                    and
                    subscription.remaining_edit > 0
                ):

                    use_subscription = subscription
        else:

            if obj.single_property_edit_limit > 0:

                if (
                    obj.single_property_edit_used
                    >= obj.single_property_edit_limit
                ):

                    return Response({

                        "status": False,

                        "message": "Edit limit exceeded"

                    }, status=400)

        # -------------------------------------------------
        # Current plan exhausted
        # Find another active plan
        # -------------------------------------------------

        # if use_subscription is None:
        if subscription and use_subscription is None:

            use_subscription = get_available_edit_subscription(
                request.user
            )

            if use_subscription is None:

                return Response({

                    "status": False,

                    "message": "Edit limit exceeded"

                }, status=400)

            # Move property to new subscription

            obj.subscription = use_subscription

            obj.package = use_subscription.plan

            obj.save(
                update_fields=[
                    "subscription",
                    "package"
                ]
            )
        

        # if subscription:

        #     if subscription.has_no_edit:

        #         return Response({

        #             "status": False,

        #             "message":
        #             "Editing is not allowed in your plan"

        #         }, status=400)

        #     if (
        #         not subscription.is_unlimited_edit
        #         and
        #         subscription.remaining_edit <= 0
        #     ):

        #         return Response({

        #             "status": False,

        #             "message":
        #             "Edit limit exceeded"

        #         }, status=400)

        data = (
            request.data.dict()
            if hasattr(request.data, "dict")
            else request.data.copy()
        )

        # =====================================================
        # REMOVE READ ONLY FIELDS
        # =====================================================

        for field in [

            "id",
            "user",
            "property_code",
            "created_at",
            "updated_at"

        ]:

            data.pop(field, None)

        # =====================================================
        # CATEGORY VALIDATION
        # =====================================================

        new_category_id = data.get("category")

        if new_category_id and obj.subscription:

            try:

                new_category = Category.objects.get(
                    id=new_category_id
                )

            except Category.DoesNotExist:

                return Response({

                    "status": False,
                    "message": "Invalid category"

                }, status=status.HTTP_400_BAD_REQUEST)

            category_name = (
                new_category.name.lower()
            )

            # Residential categories
            is_residential = any(
                keyword in category_name
                for keyword in [
                    "residential",
                    "plot/land",
                    # "plot"
                ]
            )

            # Commercial categories
            is_commercial = any(
                keyword in category_name
                for keyword in [
                    "commercial",
                    "industrial"
                ]
            )

            # =================================================
            # OLD CATEGORY
            # =================================================

            old_category_name = (
                obj.category.name.lower()
                if obj.category else ""
            )

            old_is_residential = any(
                keyword in old_category_name
                for keyword in [
                    "residential",
                    "plot/land",
                    # "plot"
                ]
            )

            old_is_commercial = any(
                keyword in old_category_name
                for keyword in [
                    "commercial",
                    "industrial"
                ]
            )

            # =================================================
            # CATEGORY CHANGE VALIDATION
            # =================================================

            if (
                old_is_residential != is_residential
            ):

                if (
                    is_residential
                    and limit_data["residential_remaining"] <= 0
                ):

                    return Response({

                        "status": False,

                        "message":
                        "Residential property limit exceeded"

                    }, status=status.HTTP_400_BAD_REQUEST)

            if (
                old_is_commercial != is_commercial
            ):

                if (
                    is_commercial
                    and limit_data["commercial_remaining"] <= 0
                ):

                    return Response({

                        "status": False,

                        "message":
                        "Commercial property limit exceeded"

                    }, status=status.HTTP_400_BAD_REQUEST)

        # =====================================================
        # SERIALIZER CONTEXT
        # =====================================================

        context = {

            "request": request,

            "amenities_list":
            self.parse_list_field(
                request,
                "amenities"
            ),

            "selling_points_list":
            self.parse_list_field(
                request,
                "selling_points"
            ),

            "land_mark_list":
            self.parse_list_field(
                request,
                "landmarks"
            ),

            "features_list":
            self.parse_list_field(
                request,
                "field_values"
            ),
        }

        serializer = UserPropertySerializer(

            obj,
            data=data,
            # partial=True,
            partial = False,
            context=context

        )

        if not serializer.is_valid():

            return Response({

                "status": False,
                "errors": serializer.errors

            }, status=status.HTTP_400_BAD_REQUEST)
        old_category_name = obj.category.name if obj.category else ""

        instance = serializer.save()
        # instance = serializer.save()

        new_category_name = (
            instance.category.name.lower().strip()
            if instance.category else ""
        )

        if old_category_name != new_category_name:

            # Always update user profile counts
            request.user.profile.change_property_category(
                old_category_name,
                new_category_name
            )

            # Update subscription counts only if property belongs to a plan
            if instance.subscription:
                instance.subscription.change_property_category(
                    old_category_name,
                    new_category_name
                )

        property_subscription = instance.subscription

        if (
            property_subscription
            and property_subscription.is_active
        ):

            if (
                not property_subscription.has_no_edit
                and
                not property_subscription.is_unlimited_edit
            ):

                property_subscription.edit_used += 1

                property_subscription.save(
                    update_fields=["edit_used"]
                )
        elif instance.single_property_edit_limit > 0:

            instance.single_property_edit_used += 1

            instance.save(
                update_fields=[
                    "single_property_edit_used"
                ]
            )

        # if subscription:

        #     if (
        #         not subscription.has_no_edit
        #         and
        #         not subscription.is_unlimited_edit
        #     ):

        #         subscription.edit_used += 1

        #         subscription.save(
        #             update_fields=["edit_used"]
        #         )

        # =====================================================
        # MAIN IMAGE UPDATE
        # =====================================================

        # image = request.FILES.get("image")

        # if image:

        #     instance.image = image

        #     instance.save(
        #         update_fields=["image"]
        #     )

        # # =====================================================
        # # MULTIPLE IMAGES
        # # =====================================================

        # images = request.FILES.getlist("images")

        # if images:

        #     PropertyImage.objects.bulk_create([

        #         PropertyImage(
        #             property=instance,
        #             image=img
        #         )

        #         for img in images
        #     ])

        # =====================================================
        # REFRESH LIMITS
        # =====================================================

        limit_data = get_property_remaining_counts(
            request.user
        )

        return Response({

            "status": True,

            "message":
            "Property updated successfully",

            "remaining_property":
            limit_data["remaining_property"],

            "residential_remaining":
            limit_data["residential_remaining"],

            "commercial_remaining":
            limit_data["commercial_remaining"],

            "data":
            UserPropertySerializer(
                instance,
                context={
                    "request": request
                }
            ).data

        }, status=status.HTTP_200_OK)

    # =========================================================
    # DELETE
    # =========================================================

    def delete(self, request, id):

        obj = self.get_object(
            request,
            id
        )

        if not obj:

            return Response({

                "status": False,
                "message": "Property not found"

            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()

        # =====================================================
        # REFRESH LIMITS AFTER DELETE
        # =====================================================

        limit_data = get_property_remaining_counts(
            request.user
        )

        return Response({

            "status": True,

            "message":
            "Property deleted successfully",

            "remaining_property":
            limit_data["remaining_property"],

            "residential_remaining":
            limit_data["residential_remaining"],

            "commercial_remaining":
            limit_data["commercial_remaining"]

        }, status=status.HTTP_200_OK)


class AgentContactMessageCreateAPIView(APIView):

    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        name = request.data.get("name")
        message = request.data.get("message")

        if not name:
            return Response({
                "error": "name is required"
            }, status=400)

        if not message:
            return Response({
                "error": "message is required"
            }, status=400)

        contact_message = AgentContactMessage.objects.create(
            agent=request.user,
            name=name,
            message=message
        )

        serializer = AgentContactMessageSerializer(
            contact_message
        )

        return Response({

            "status": True,
            "message": "Message sent successfully",

            "data": serializer.data

        })



import uuid
import re

from datetime import timedelta

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from users.models import (
    Userplan,
    UserProfile,
    UserCreate
)

from users.serializers import (
    UserPlanActivateSerializer
)

from users.authentication import (
    UserJWTAuthentication
)


class ActivateUserPlanAPIView(APIView):

    # =====================================
    # CUSTOM JWT AUTH
    # =====================================

    authentication_classes = [
        UserJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = UserPlanActivateSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "status": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =====================================
        # PLAN UUID
        # =====================================

        try:

            plan_uuid = uuid.UUID(
                serializer.validated_data["plan_id"]
            )

        except Exception:

            return Response(
                {
                    "status": False,
                    "message": "Invalid plan UUID"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =====================================
        # PLAN
        # =====================================

        try:

            plan = Userplan.objects.get(
                id=plan_uuid
            )

        except Userplan.DoesNotExist:

            return Response(
                {
                    "status": False,
                    "message": "Plan not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # =====================================
        # AUTH USER
        # =====================================

        user = request.user

        # =====================================
        # PROFILE
        # =====================================

        profile = UserProfile.objects.filter(
            user_id=user.id
        ).first()

        if not profile:

            return Response(
                {
                    "status": False,
                    "message": "Profile not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # =====================================
        # VALIDITY DAYS
        # =====================================

        numbers = re.findall(
            r"\d+",
            str(plan.validity)
        )

        validity_days = (
            int(numbers[0])
            if numbers else 30
        )

        start_date = timezone.now()

        expiry_date = (
            start_date
            + timedelta(days=validity_days)
        )

        # =====================================
        # UPDATE USER
        # =====================================

        UserCreate.objects.filter(
            id=user.id
        ).update(
            role="owner",
            last_plan_expiry=expiry_date
        )

        # =====================================
        # UPDATE PROFILE
        # =====================================

        UserProfile.objects.filter(
            id=profile.id
        ).update(
            user_plan_id=plan.id,
            is_paid_user=True,
            user_role="owner",
            plan_start_date=start_date,
            plan_expiry_date=expiry_date
        )

        # =====================================
        # ADD PLAN
        # =====================================

        user.user_plans.add(plan)

        # =====================================
        # RESPONSE
        # =====================================

        return Response(
            {
                "status": True,
                "message": "Plan activated successfully",
                "data": {
                    "plan_id": str(plan.id),
                    "plan_name": plan.name,
                    "price": str(plan.price),
                    "validity": plan.validity,
                    "user_role": "owner",
                    # "is_paid_user": True,
                    "plan_start_date": start_date,
                    "plan_expiry_date": expiry_date
                }
            },
            status=status.HTTP_200_OK
        )




# class CurrentUserPlanAPIView(APIView):

#     authentication_classes = [
#         UserJWTAuthentication
#     ]

#     permission_classes = [
#         IsAuthenticated
#     ]

#     def get(self, request):

#         user = request.user

#         profile = UserProfile.objects.filter(
#             user_id=user.id
#         ).select_related(
#             "user_plan"
#         ).first()

#         if not profile:

#             return Response(
#                 {
#                     "status": False,
#                     "message": "Profile not found"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         if not profile.user_plan:

#             return Response(
#                 {
#                     "status": False,
#                     "message": "No active plan found"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = CurrentUserPlanSerializer(
#             profile
#         )

#         return Response(
#             {
#                 "status": True,
#                 "message": "Current plan fetched successfully",
#                 "data": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class CurrentUserPlanAPIView(APIView):

    authentication_classes = [
        UserJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        user = request.user

        profile = UserProfile.objects.filter(
            user=user
        ).first()

        if not profile:

            return Response(
                {
                    "status": False,
                    "message": "Profile not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # ==========================================
        # EXPIRE OLD PLANS
        # =========================================

        UserPlanSubscription.objects.filter(
            user=user,
            is_active=True,
            expiry_date__lt=timezone.now()
        ).update(
            is_active=False
        )

        # ==========================================
        # ACTIVE SUBSCRIPTIONS
        # ==========================================

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
        has_upgrade_plan = subscriptions.count() > 1

        # ==========================================
        # NO ACTIVE PLAN
        # ==========================================

        if not subscriptions.exists():

            return Response({
                "status": True,
                "message": "No active plan",
            }, 
            status= status.HTTP_404_NOT_FOUND
            )

        # ==========================================
        # HIGHEST PLAN
        # ==========================================

        highest_subscription = max(
            subscriptions,
            key=lambda x: (
                int(
                    "".join(
                        filter(
                            str.isdigit,
                            str(
                                x.plan.property_listing_limit
                            )
                        )
                    ) or 999999
                )
            )
        )

        total_properties = Property.objects.filter(
            user=user
        ).count()

        residential_properties = Property.objects.filter(
            user=user,
            category__name__iexact="Residential"
        ).count()

        commercial_properties = Property.objects.filter(
            user=user,
            category__name__iexact="Commercial"
        ).count()

        active_plan = highest_subscription.plan

        # ==========================================
        # PLAN LIMIT
        # ==========================================

        # ==========================================
        # TOTAL LIMIT FROM ALL ACTIVE PLANS
        # ==========================================

        total_property_limit = 0
        total_residential_limit = 0
        total_commercial_limit = 0

        for sub in subscriptions:

            plan = sub.plan

            # Property limit
            try:

                property_limit = int(
                    "".join(
                        filter(
                            str.isdigit,
                            str(plan.property_listing_limit)
                        )
                    ) or 0
                )

            except Exception:

                property_limit = 0

            total_property_limit += property_limit

            # Listing Type Example:
            # "6 Residential / 6 Commercial"

            listing_type = str(
                getattr(
                    plan,
                    "listing_type",
                    ""
                )
            )

            numbers = re.findall(
                r"\d+",
                listing_type
            )

            if len(numbers) >= 2:

                total_residential_limit += int(
                    numbers[0]
                )

                total_commercial_limit += int(
                    numbers[1]
                )

        # ==========================================
        # ACTIVE SUBSCRIPTIONS
        # ==========================================

        active_subscriptions = []

        for sub in subscriptions:

            active_subscriptions.append({

                "plan_id":
                str(sub.plan.id),

                "plan_name":
                sub.plan.name,

                "is_primary":
                sub.is_primary,

                "purchased_at":
                sub.purchased_at,

                "expiry_date":
                sub.expiry_date,

                "property_limit":
                sub.plan.property_listing_limit
            })

        # ==========================================
        # RESPONSE
        # ==========================================

        return Response({

            "status": True,

            "message":
            "Current plan fetched successfully",
            "is_upgrade_plan":
                has_upgrade_plan,

            "data": {

                # ======================================
                # ACTIVE PLAN
                # ======================================
                

                "plan_id":
                str(active_plan.id),

                "plan_type":
                "owner_plan",

                "name":
                active_plan.name,

                "validity":
                active_plan.validity,

                "price":
                str(active_plan.price),

                "features": {

                    "property_listing_limit":
                    getattr(
                        active_plan,
                        "property_listing_limit",
                        None
                    ),

                    "listing_type":
                    getattr(
                        active_plan,
                        "listing_type",
                        None
                    ),

                    "enquiry_limit":
                    getattr(
                        active_plan,
                        "enquiry_limit",
                        None
                    ),

                    "property_edit_option":
                    getattr(
                        active_plan,
                        "property_edit_option",
                        None
                    ),

                    "property_visibility":
                    getattr(
                        active_plan,
                        "property_visibility",
                        None
                    ),

                    "priority_search":
                    getattr(
                        active_plan,
                        "priority_search",
                        None
                    ),

                    "meta_ads_promotion":
                    getattr(
                        active_plan,
                        "meta_ads_promotion",
                        None
                    ),

                    "bulk_whatsapp_message":
                    getattr(
                        active_plan,
                        "bulk_whatsapp_message",
                        None
                    ),

                    "poster_creation":
                    getattr(
                        active_plan,
                        "poster_creation",
                        None
                    ),

                    "social_media_marketing":
                    getattr(
                        active_plan,
                        "social_media_marketing",
                        None
                    ),

                    "lead_follow_support":
                    getattr(
                        active_plan,
                        "lead_follow_support",
                        None
                    ),

                    "best_suited_for":
                    getattr(
                        active_plan,
                        "best_suited_for",
                        None
                    )
                },

                "plan_start_date":
                highest_subscription.purchased_at,

                "plan_expiry_date":
                highest_subscription.expiry_date,

                "is_paid_user":
                profile.is_paid_user,

                "user_role":
                profile.user_role,

                # ======================================
                # CURRENT PLAN LIMITS
                # ======================================

                "property_limit":
                total_property_limit,

                "residential_limit":
                total_residential_limit,

                "commercial_limit":
                total_commercial_limit,

                "remaining_property":
                max(
                    total_property_limit -
                    profile.total_property_used,
                    0
                ),

                "remaining_residential":
                max(
                    total_residential_limit -
                    profile.residential_property_used,
                    0
                ),

                "remaining_commercial":
                max(
                    total_commercial_limit -
                    profile.commercial_property_used,
                    0
                ),

                # ======================================
                # PROPERTY USAGE TRACKER
                # ======================================

                "property_used":
                profile.total_property_used,

                "residential_used":
                profile.residential_property_used,

                "commercial_used":
                profile.commercial_property_used,

                # ======================================
                # ACTUAL PROPERTY COUNTS
                # ======================================

                "total_properties":
                total_properties,

                "total_residential_properties":
                residential_properties,

                "total_commercial_properties":
                commercial_properties,

                # ======================================
                # EDIT OPTION
                # ======================================

                "property_edit_option":
                active_plan.property_edit_option,

                # ======================================
                # UPGRADE INFORMATION
                # ======================================

                "active_subscription_count":
                subscriptions.count(),

                "active_subscriptions":
                active_subscriptions,

                # ======================================
                # CURRENT ACTIVE SUBSCRIPTION
                # ======================================

                "current_active_subscription": {

                    "plan_id":
                    str(highest_subscription.plan.id),

                    "plan_name":
                    highest_subscription.plan.name,

                    "property_limit":
                    highest_subscription.plan.property_listing_limit,

                    "is_primary":
                    highest_subscription.is_primary,

                    "purchased_at":
                    highest_subscription.purchased_at,

                    "expiry_date":
                    highest_subscription.expiry_date
                },

                # ======================================
                # UPGRADE PLAN
                # ======================================

                "upgrade_plan": (

                    {
                        "plan_id":
                        str(
                            subscriptions.exclude(
                                id=highest_subscription.id
                            ).first().plan.id
                        ),

                        "plan_name":
                        subscriptions.exclude(
                            id=highest_subscription.id
                        ).first().plan.name,

                        "property_limit":
                        subscriptions.exclude(
                            id=highest_subscription.id
                        ).first().plan.property_listing_limit,

                        "expiry_date":
                        subscriptions.exclude(
                            id=highest_subscription.id
                        ).first().expiry_date
                    }

                    if subscriptions.count() > 1

                    else None
                )
            }

        })

class OwnerDashboardAPIView(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            user = request.user

            counts = get_property_remaining_counts(user)

            total_properties = counts["total_properties"]

            enquiries_qs = PropertyEnquiry.objects.filter(
                property__user=user
            )

            total_enquiries = enquiries_qs.count()

            current_year = timezone.now().year

            monthly = (
                enquiries_qs
                .filter(created_at__year=current_year)
                .annotate(
                    month=ExtractMonth("created_at")
                )
                .values("month")
                .annotate(
                    count=Count("id")
                )
                .order_by("month")
            )

            month_map = {
                1: "Jan",
                2: "Feb",
                3: "Mar",
                4: "Apr",
                5: "May",
                6: "Jun",
                7: "Jul",
                8: "Aug",
                9: "Sep",
                10: "Oct",
                11: "Nov",
                12: "Dec"
            }

            month_counts = {
                item["month"]: item["count"]
                for item in monthly
            }

            monthly_data = [
                {
                    "month": month_map[i],
                    "count": month_counts.get(i, 0)
                }
                for i in range(1, 13)
            ]

            return Response({

                "status": True,

                "message":
                "Owner dashboard fetched successfully",

                "data": {

                    "property_listed":
                    total_properties,

                    "remaining_property":
                    counts["remaining_property"],

                    "residential_remaining":
                    counts["residential_remaining"],

                    "commercial_remaining":
                    counts["commercial_remaining"],

                    "total_enquiries":
                    total_enquiries,

                    "monthly_enquiries":
                    monthly_data
                }

            }, status=status.HTTP_200_OK)

        except Exception as e:

            return Response({

                "status": False,
                "message": str(e)

            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.utils import timezone

class UserPropertyListAPIView(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        properties = (
            Property.objects
            .filter(user=user)
            .select_related(
                "category",
                "subcategory",
                "purpose",
                "package"
            )
            .prefetch_related("amenities")
            .order_by("-created_at")
        )

        counts = get_property_remaining_counts(user)

        edit_data = get_edit_remaining_count(user)

        # ==========================================
        # ACTIVE PLANS
        # ==========================================

        active_subscriptions = (
            UserPlanSubscription.objects
            .filter(
                user=user,
                is_active=True,
                expiry_date__gt=timezone.now()
            )
            .select_related("plan")
        )

        has_active_plan = active_subscriptions.exists()

        serializer = UserPropertySerializer(
            properties,
            many=True,
            context={
                "request": request
            }
        )
        property_edit_data = []

        for prop in properties:

            if prop.single_property_package:

                remaining = max(
                    prop.single_property_edit_limit -
                    prop.single_property_edit_used,
                    0
                )

            else:
                remaining = None

            property_edit_data.append({
                "property_id": prop.id,
                "remaining_edit": remaining
            })

        return Response({

            "status": True,

            "message":
            "Properties fetched successfully",

            # ======================================
            # PLAN STATUS
            # ======================================

            "is_plan_chosen":
            has_active_plan,

            # ======================================
            # PROPERTY LIMITS
            # ======================================

            "remaining_property":
            counts["remaining_property"],

            "residential_remaining":
            counts["residential_remaining"],

            "commercial_remaining":
            counts["commercial_remaining"],

            "remaining_edit_count":
            edit_data["remaining_edit"],

            # ======================================
            # PROPERTY DATA
            # ======================================
            "single_property_edit": property_edit_data,

            "data":
            serializer.data

        }, status=status.HTTP_200_OK)




class UserPropertyCreateAPIView(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    # =====================================================
    # PARSE LIST FIELD
    # =====================================================

    def parse_list_field(self, request, field_name):

        raw_values = request.data.getlist(field_name)

        if not raw_values:

            value = request.data.get(field_name)

            if value:
                raw_values = [value]

        parsed = []

        for v in raw_values:

            if not v:
                continue

            if isinstance(v, str):

                try:
                    decoded = json.loads(v)

                except:
                    decoded = v

            else:
                decoded = v

            if isinstance(decoded, list):

                parsed.extend(decoded)

            elif isinstance(decoded, dict):

                parsed.append(decoded)

            else:

                parsed.append(decoded)

        return parsed

    # =====================================================
    # POST
    # =====================================================

    def post(self, request):

        user = request.user

        # =================================================
        # GET REMAINING COUNTS
        # =================================================

        counts = get_property_remaining_counts(user)

        remaining_property = counts[
            "remaining_property"
        ]

        residential_remaining = counts[
            "residential_remaining"
        ]

        commercial_remaining = counts[
            "commercial_remaining"
        ]

        # =================================================
        # CATEGORY VALIDATION
        # =================================================

        category_id = request.data.get("category")

        if not category_id:

            return Response({

                "status": False,
                "message": "Category is required"

            }, status=400)

        try:

            category = Category.objects.get(
                id=category_id
            )

        except Category.DoesNotExist:

            return Response({

                "status": False,
                "message": "Invalid category"

            }, status=400)

        category_name = (
            category.name.lower().strip()
        )
        print("\n================ CATEGORY DEBUG ================")
        print("Category ID:", category.id)
        print("Category Name:", category.name)
        print("Category Name (lower):", category_name)
        print("Remaining Property:", remaining_property)
        print("Residential Remaining:", residential_remaining)
        print("Commercial Remaining:", commercial_remaining)
        print("================================================\n")

        if remaining_property <= 0:

            return Response({

                "status": False,

                "message":
                "Property limit exceeded",

                "remaining_property":
                remaining_property,

                "residential_remaining":
                residential_remaining,

                "commercial_remaining":
                commercial_remaining

            }, status=400)

        print("DEBUG: Checking Residential Condition")
        print("DEBUG:", category_name, "in", ["residential", "plot/land"], "=", category_name in ["residential", "plot/land"])

        if category_name in ["residential", "plot/land"]:
            print("DEBUG: Residential category matched")

            if residential_remaining <= 0:
                print("DEBUG: Residential limit exceeded")


                return Response({

                    "status": False,
                    "message": "Residential property limit exceeded",

                    "remaining_property": remaining_property,
                    "residential_remaining": residential_remaining,
                    "commercial_remaining": commercial_remaining

                }, status=400)
            else:

                print("DEBUG: Residential property can be created")

        print("DEBUG: Checking Commercial Condition")
        print("DEBUG:", category_name, "in", ["commercial", "industrial"], "=", category_name in ["commercial", "industrial"])
        if category_name in ["commercial", "industrial"]:
            print("DEBUG: Commercial category matched")
            if commercial_remaining <= 0:
                print("DEBUG: Commercial limit exceeded")
                return Response({

                    "status": False,
                    "message": "Commercial property limit exceeded",

                    "remaining_property": remaining_property,
                    "residential_remaining": residential_remaining,
                    "commercial_remaining": commercial_remaining

                }, status=400)
            else:
                print("DEBUG: Commercial property can be created")
        print("DEBUG: Passed all limit checks")

        # =================================================
        # SERIALIZER
        # =================================================

        serializer = UserPropertySerializer(

            data=request.data,

            context={

                "request": request,

                "amenities_list":
                self.parse_list_field(
                    request,
                    "amenities"
                ),

                "selling_points_list":
                self.parse_list_field(
                    request,
                    "selling_points"
                ),

                "land_mark_list":
                self.parse_list_field(
                    request,
                    # "land_mark"
                    "landmarks"
                ),

                "features_list":
                self.parse_list_field(
                    request,
                    "field_values"
                ),
            }
        )

        # =================================================
        # VALIDATION
        # =================================================

        if not serializer.is_valid():

            return Response({

                "status": False,
                "errors": serializer.errors

            }, status=400)

        active_subscription = get_available_subscription(
            user,
            category_name
        )
        profile = user.profile

        if not active_subscription:

            if profile.total_property_used >= 2:

                return Response({
                    "status": False,
                    "message": "Your without plan limit reached. Please purchase a plan to continue."
                }, status=400)

        # IF USER HAS NO SUBSCRIPTION
        # STORE PROPERTY IN REDIS

        if not active_subscription:

            cache_key = (
                f"pending_property_{user.id}_{uuid.uuid4()}"
            )

            image = request.FILES.get("image")

            images = request.FILES.getlist("images")

            property_data = serializer.validated_data.copy()

            # ---------------------------------------------

            # property_data["category"] = str(
            #     property_data["category"].id
            # )

            # property_data["purpose"] = str(
            #     property_data["purpose"].id
            # )

            # if property_data.get("subcategory"):

            #     property_data["subcategory"] = str(
            #         property_data["subcategory"].id
            #     )

            # property_data["user"] = str(user.id)
            # ---------------------------------------------
            # CONVERT MODEL / UUID / STRING SAFELY
            # ---------------------------------------------

            category = property_data.get("category")

            if category:

                property_data["category"] = str(

                    category.id

                    if hasattr(category, "id")

                    else category

                )

            purpose = property_data.get("purpose")

            if purpose:

                property_data["purpose"] = str(

                    purpose.id

                    if hasattr(purpose, "id")

                    else purpose

                )

            subcategory = property_data.get("subcategory")

            if subcategory:

                property_data["subcategory"] = str(

                    subcategory.id

                    if hasattr(subcategory, "id")

                    else subcategory

                )

            property_data["user"] = str(user.id)

            # ---------------------------------------------

            property_data["amenities"] = [

                str(x.id)

                for x in serializer.context[
                    "amenities_list"
                ]

                if hasattr(x, "id")
            ]

            property_data["selling_points"] = (
                serializer.context["selling_points_list"]
            )

            property_data["landmarks"] = (
                serializer.context["land_mark_list"]
            )

            property_data["field_values"] = (
                serializer.context["features_list"]
            )

            # ---------------------------------------------
            # STORE IMAGES
            # ---------------------------------------------

            if image:

                property_data["main_image"] = base64.b64encode(

                    image.read()

                ).decode()

                property_data["main_image_name"] = image.name

            multiple_images = []

            for img in images:

                multiple_images.append({

                    "name": img.name,

                    "content": base64.b64encode(

                        img.read()

                    ).decode()

                })

            property_data["multiple_images"] = multiple_images

            # ---------------------------------------------
            single_plan = SinglePropertyPackage.objects.filter(
                is_active=True
            ).first()

            if not single_plan:

                return Response({

                    "status": False,

                    "message": "Single Property Package not available"

                }, status=400)

            cache.set(

                cache_key,

                property_data,

                timeout=60 * 30

            )

            return Response({

                "status": True,
                "payment_required": True,
                "message": "Property validated successfully",
                "plan_id": str(single_plan.id),
                "plan_name": single_plan.name,
                "cache_key": cache_key,
                "amount": 5000

            })

        # =================================================
        # SAVE PROPERTY
        # =================================================

        property_obj = serializer.save(
            package=(
                active_subscription.plan
                if active_subscription
                else None
            ),
              
            subscription=active_subscription,
            paid="yes" if active_subscription else "no"
        )
        request.user.profile.increase_property_usage(
            property_obj.category.name
        )
        if active_subscription:
            active_subscription.increase_property_usage(
                property_obj.category.name
            )
        print("\n=========== PROPERTY DEBUG ===========")

        print("Property ID :", property_obj.id)

        print(
            "Package :",
            property_obj.package.name
            if property_obj.package
            else None
        )

        print(
            "Subscription :",
            property_obj.subscription.id
            if property_obj.subscription
            else None
        )

        print("======================================\n")

        # =================================================
        # SINGLE IMAGE
        # =================================================

        image = request.FILES.get("image")

        if image:

            property_obj.image = image
            property_obj.save()

        # =================================================
        # MULTIPLE IMAGES
        # =================================================

        images = request.FILES.getlist("images")

        if images:

            PropertyImage.objects.bulk_create([

                PropertyImage(
                    property=property_obj,
                    image=img
                )

                for img in images
            ])

        # =================================================
        # REFRESH COUNTS
        # =================================================

        updated_counts = (
            get_property_remaining_counts(user)
        )

        # =================================================
        # RESPONSE
        # =================================================

        return Response({

            "status": True,

            "message":
            "Property created successfully",

            "remaining_property":
            updated_counts["remaining_property"],

            "residential_remaining":
            updated_counts["residential_remaining"],

            "commercial_remaining":
            updated_counts["commercial_remaining"],

            "data":
            UserPropertySerializer(

                property_obj,

                context={
                    "request": request
                }

            ).data

        }, status=201)

        
import uuid
import razorpay

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class CreatePaymentAPIView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def get_auth_user(self, request):

        auth_header = request.headers.get(
            "Authorization"
        )

        if not auth_header:

            return None, None, None

        try:

            token = auth_header.split(" ")[1]

            decoded = AccessToken(token)

        except Exception:

            return None, None, None

        user = None
        agent = None

        user_id = decoded.get("user_id")

        username = decoded.get("username")

        # =================================================
        # USER
        # =================================================

        if user_id:

            user = UserCreate.objects.filter(
                id=user_id
            ).first()

        # =================================================
        # AGENT
        # =================================================

        if not user and username:

            agent = AgentUserProfile.objects.filter(
                username=username
            ).first()

        role = None

        if user:

            role = "user"

        elif agent:

            role = "agent"

        return user, agent, role

    # =====================================================
    # GET PLAN OBJECT USING ONLY plan_id
    # =====================================================

    def get_plan_object(self, plan_id):
        # =================================================
        # SINGLE PROPERTY PACKAGE
        # =================================================

        single_property = SinglePropertyPackage.objects.filter(
            id=plan_id,
            is_active=True
        ).first()

        if single_property:

            return single_property, "single_property"

        # =================================================
        # OWNER PLAN
        # =================================================

        owner_plan = Userplan.objects.filter(
            id=plan_id
        ).first()

        if owner_plan:

            return owner_plan, "owner_plan"

        # =================================================
        # PREMIUM PLAN
        # =================================================

        premium_plan = PremiumPlan.objects.filter(
            id=plan_id
        ).first()

        if premium_plan:

            return premium_plan, "premium"

        # =================================================
        # ELITE PLAN
        # =================================================

        elite_plan = ElitePlan.objects.filter(
            id=plan_id
        ).first()

        if elite_plan:

            return elite_plan, "elite"

        # =================================================
        # AGENT PLAN
        # =================================================

        agent_plan = AgentPlan.objects.filter(
            id=plan_id
        ).first()

        if agent_plan:

            return agent_plan, "basic"

        # =================================================
        # SLIDER ADS
        # =================================================

        slider_plan = AdvertisementPackage.objects.filter(
            id=plan_id,
            ad_format="slider"
        ).first()

        if slider_plan:

            return slider_plan, "slider"

        # =================================================
        # BANNER ADS
        # =================================================

        banner_plan = AdvertisementPackage.objects.filter(
            id=plan_id,
            ad_format="banner"
        ).first()

        if banner_plan:

            return banner_plan, "banner"

        # =================================================
        # SHORT REEL
        # =================================================

        short_reel = ReelPackage.objects.filter(
            id=plan_id,
            reel_type="short_reel"
        ).first()

        if short_reel:

            return short_reel, "short_reel"

        # =================================================
        # CINEMATIC REEL
        # =================================================

        cinematic_reel = ReelPackage.objects.filter(
            id=plan_id,
            reel_type="cinematic_reel"
        ).first()

        if cinematic_reel:

            return cinematic_reel, "cinematic_reel"

        return None, None
    def get_plan_price(self, plan, plan_type):

        if plan_type in [
            "slider",
            "banner",
            "short_reel",
            "cinematic_reel"
        ]:

            return float(plan.price_per_day)

        return float(plan.price)

    # =====================================================
    # GET PLAN NAME
    # =====================================================

    def get_plan_name(self, plan):

        return plan.name

    # =====================================================
    # GET PLAN VALIDITY
    # =====================================================

    def get_plan_validity(self, plan, plan_type):

        # =================================================
        # OWNER PLAN
        # =================================================

        if plan_type == "owner_plan":

            return getattr(
                plan,
                "validity",
                None
            )

        # =================================================
        # PREMIUM PLAN
        # =================================================
        elif plan_type == "single_property":

            return None

        elif plan_type == "premium":

            return getattr(
                plan,
                "validity",
                None
            )

        # =================================================
        # ELITE PLAN
        # =================================================

        elif plan_type == "elite":

            return getattr(
                plan,
                "plan_validity_days",
                None
            )

        return None
    
    def deactivate_expired_plans(self, user):

        subscriptions = UserPlanSubscription.objects.filter(
            user=user,
            is_active=True
        )

        for sub in subscriptions:

            if (
                sub.expiry_date
                and timezone.now() > sub.expiry_date
            ):

                sub.is_active = False

                sub.save(
                    update_fields=["is_active"]
                )
            
    def deactivate_expired_agent_plans(self, agent):

        Subscription.objects.filter(
            agent=agent,
            is_active=True,
            end_date__lt=timezone.now().date()
        ).update(
            is_active=False
        )

    # =====================================================
    # POST
    # =====================================================

    def post(self, request):

        try:

            # =================================================
            # AUTH USER
            # =================================================

            user, agent, role = self.get_auth_user(
                request
            )

            if not role:

                return Response({
                    "status": False,
                    "message": "Invalid token"
                }, status=401)

            # =====================================================
            # PROPERTY LIMIT CHECK (ONLY FOR USER)
            # =====================================================

            # if role == "user":

            #     user_property_count = Property.objects.filter(
            #         user=user
            #     ).count()

            #     if user_property_count < 2:

            #         return Response({
            #             "status": False,
            #             "message": "You must add at least 2 properties before selecting a plan",
            #             "property_count": user_property_count,
            #             "required": 2
            #         }, status=400)
            # pending_registration = PendingAgentRegistration.objects.filter(
            #     email=user.email,
            #     status="pending"
            # ).first()
            pending_registration = None

            if role == "user" and user:

                # pending_registration = (
                #     PendingAgentRegistration.objects.filter(
                #         email=user.email,
                #         status="pending"
                #     ).first()
                # )
                pending_registration = (
                    PendingAgentRegistration.objects.filter(
                        submitted_by=user,
                        status="pending"
                    )
                    .order_by("-created_at")
                    .first()
                )

            plan_id = request.data.get("plan_id")
            plan, plan_type = self.get_plan_object(plan_id)
            

            if role == "user" and plan_type == "owner_plan":
                profile = user.profile
                # user_property_count = Property.objects.filter(
                #     user=user
                # ).count()

                if profile.total_property_used < 2:
                    return Response({
                        "status": False,
                        "message": "You must add at least 2 properties before selecting a plan",
                        "property_count": profile.total_property_used,
                        "required": 2
                    }, status=400)

            # if role == "user":

            #     # User is already becoming an agent
            #     if pending_registration:
            #         pass

            #     # Normal user -> require minimum properties
            #     else:
            #         user_property_count = Property.objects.filter(
            #             user=user
            #         ).count()

            #         if user_property_count < 2:
            #             return Response({
            #                 "status": False,
            #                 "message": "You must add at least 2 properties before selecting a plan",
            #                 "property_count": user_property_count,
            #                 "required": 2
            #             }, status=400)

            # =================================================
            # INPUT
            # =================================================

            plan_id = request.data.get(
                "plan_id"
            )

            if not plan_id:

                return Response({
                    "status": False,
                    "message": "plan_id required"
                }, status=400)
            try:

                plan_id = uuid.UUID(
                    str(plan_id)
                )

            except Exception:

                return Response({
                    "status": False,
                    "message":
                    "Invalid UUID plan_id"
                }, status=400)

            plan, plan_type = self.get_plan_object(
                plan_id
            )
            if role == "agent" and plan_type in [
                "slider",
                "banner"
            ]:

                AdvertisementRequestNotification.objects.create(

                    title="New Advertisement Request",

                    message=(
                        f"{agent.username} requested the "
                        f"{plan.name}. Please contact the agent "
                        f"to discuss the advertisement requirements."
                    ),

                    notification_type="advertisement_request",

                    advertisement_package=plan,

                    agent=agent
                )

                return Response({

                    "status": True,

                    "message": (
                        "Your advertisement request has been submitted successfully. "
                        "Our team will contact you shortly to discuss your advertisement requirements."
                    )

                }, status=201)
            # =================================================
            # AGENT PLAN LIMIT
            # =================================================

            if role == "agent" and plan_type not in [
                "short_reel",
                "cinematic_reel",
            ]:

                self.deactivate_expired_agent_plans(agent)

                active_agent_subscriptions = Subscription.objects.filter(
                    agent=agent,
                    is_active=True,
                    end_date__gt=timezone.now().date()
                )

                if active_agent_subscriptions.count() >= 2:

                    return Response({

                        "status": False,

                        "message": "Maximum 2 active agent plans allowed"

                    }, status=400)
            # =================================================
            # PENDING AGENT REGISTRATION CHECK
            # =================================================

            # pending_registration = None

            # if role == "user" and plan_type in [
            #     "basic",
            #     "premium",
            #     "elite"
            # ]:

            #     pending_registration = PendingAgentRegistration.objects.filter(
            #         email=user.email,
            #         status="pending"
            #     ).first()

            #     if not pending_registration:

            #         return Response({
            #             "status": False,
            #             "message": (
            #                 "Agent registration request not found. "
            #                 "Submit agent registration first."
            #             )
            #         }, status=400)

            # if role == "user" and plan_type == "owner_plan":

            #     subscription_count = UserPlanSubscription.objects.filter(
            #         user=user,
            #         is_active=True
            #     ).count()

            #     if subscription_count >= 2:

            #         return Response({
            #             "status": False,
            #             "message": "Your plan limit reached"
            #         }, status=400)

            # if not plan:

            #     return Response({
            #         "status": False,
            #         "message": "Plan not found"
            #     }, status=404)
            if role == "user" and plan_type == "owner_plan":

                # ==========================================
                # AUTO EXPIRE OLD PLANS
                # ==========================================

                self.deactivate_expired_plans(user)

                active_subscription_count = UserPlanSubscription.objects.filter(
                    user=user,
                    is_active=True,
                    expiry_date__gt=timezone.now()
                ).count()

                # ==========================================
                # MAX 2 ACTIVE PLANS
                # ==========================================

                if active_subscription_count >= 2:

                    return Response({
                        "status": False,
                        "message": "Maximum 2 active plans allowed"
                    }, status=400)

            # =================================================
            # PRICE
            # =================================================

            amount = self.get_plan_price(
                plan,
                plan_type
            )

            amount_paise = int(
                amount * 100
            )

            # =================================================
            # RAZORPAY
            # =================================================

            client = razorpay.Client(auth=(

                settings.RAZORPAY_KEY_ID,

                settings.RAZORPAY_KEY_SECRET
            ))

            razorpay_order = client.order.create({

                "amount": amount_paise,

                "currency": "INR",

                "payment_capture": 1
            })
            payment = Payment.objects.create(

                user=user if role == "user" else None,

                agent=agent if role == "agent" else None,
                pending_registration=pending_registration,

                plan_type=plan_type,

                amount=amount,

                razorpay_order_id=razorpay_order["id"],
                user_plan=(
                    plan if plan_type == "owner_plan"
                    else None
                ),
                premium_plan=(
                    plan if plan_type == "premium"
                    else None
                ),
                elite_plan=(
                    plan if plan_type == "elite"
                    else None
                ),
                agent_plan=(
                    plan if plan_type == "basic"
                    else None
                ),
                single_property_package=(
                    plan if plan_type == "single_property"
                    else None
                ),
                reel_package=(
                    plan if plan_type in [
                        "short_reel",
                        "cinematic_reel"
                    ] else None
                ),
                payment_status="created"
            )
            payment_data = {

                "payment_db_id":
                str(payment.id),

                "plan_id":
                str(plan.id),

                "plan_type":
                plan_type,

                "plan_name":
                self.get_plan_name(plan),

                "plan_price":
                str(amount),

                "plan_validity":
                self.get_plan_validity(
                    plan,
                    plan_type
                ),

                "razorpay_order_id":
                razorpay_order["id"],

                "amount":
                amount_paise,

                "currency":
                "INR",

                "payment_status":
                payment.payment_status,

                "created_at":
                payment.created_at
            }
            if payment.pending_registration:

                payment_data["agent"] = {

                    "agent_id":
                    str(payment.pending_registration.id),

                    "name":
                    payment.pending_registration.full_name,

                    "email":
                    payment.pending_registration.email,

                    "mobile":
                    payment.pending_registration.phone_number,

                    "agent_type":
                    payment.pending_registration.agent_type,

                    "status":
                    payment.pending_registration.status
                }
            elif role == "user" and user:

                payment_data["user"] = {

                    "user_id":
                    str(user.id),

                    "name":
                    user.name,

                    "email":
                    user.email,

                    "mobile":
                    user.mobile,

                    "role":
                    user.role
                }

            elif role == "agent" and agent:

                payment_data["agent"] = {

                    "agent_id":
                    str(agent.id),

                    "name":
                    agent.username,

                    "email":
                    agent.email,

                    "mobile":
                    agent.phone_number,

                    "agent_type":
                    agent.agent_type
                }
            return Response({

                "status": True,

                "message":
                "Order created successfully",

                "payment":
                payment_data

            }, status=201)

        except Exception as e:

            return Response({

                "status": False,

                "message":
                "Payment creation failed",

                "error":
                str(e)

            }, status=400)


import re
import hmac
import hashlib

from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from users.models import Payment, UserProfile


class VerifyPaymentAPIView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    # =================================================
    # VALIDITY HELPER
    # =================================================
    def get_validity_days(self, validity):

        if not validity:
            return 30

        try:
            nums = re.findall(r"\d+", str(validity))
            return int(nums[0]) if nums else int(validity)
        except Exception:
            return 30

    # =================================================
    # GET PLAN DETAILS
    # =================================================
    def get_plan_details(self, payment):

        plan_map = [
            "user_plan",
            "premium_plan",
            "elite_plan",
            "agent_plan",
            "single_property_package"
        ]

        for key in plan_map:
            plan = getattr(payment, key, None)
            if plan:
                return {
                    "name": plan.name,
                    "validity": getattr(plan, "validity", None),
                    "price": getattr(plan, "price", None)
                }

        if getattr(payment, "advertisement_package", None):
            return {
                "name": payment.advertisement_package.name,
                "validity": "1 Day",
                "price": payment.advertisement_package.price_per_day
            }

        if getattr(payment, "reel_package", None):
            return {
                "name": payment.reel_package.name,
                "validity": "1 Day",
                "price": payment.reel_package.price_per_day
            }

        return {
            "name": None,
            "validity": None,
            "price": None
        }
    # =================================================
    # DEACTIVATE EXPIRED AGENT PLANS
    # =================================================
    def deactivate_expired_agent_plans(self, agent):

        Subscription.objects.filter(
            agent=agent,
            is_active=True,
            end_date__lt=timezone.now().date()
        ).update(
            is_active=False
        )
    def post(self, request):

        try:

            payment_id = request.data.get("payment_id")
            razorpay_order_id = request.data.get("razorpay_order_id")
            razorpay_payment_id = request.data.get("razorpay_payment_id")
            razorpay_signature = request.data.get("razorpay_signature")

            if not all([payment_id, razorpay_order_id, razorpay_payment_id, razorpay_signature]):
                return Response({
                    "status": False,
                    "message": "All payment fields required"
                }, status=400)

            payment = Payment.objects.filter(
                id=payment_id,
                razorpay_order_id=razorpay_order_id
            ).first()

            if not payment:
                return Response({
                    "status": False,
                    "message": "Payment not found"
                }, status=404)

            if payment.payment_status == "success":
                return Response({
                    "status": True,
                    "message": "Payment already verified"
                })

            generated_signature = hmac.new(
                settings.RAZORPAY_KEY_SECRET.encode(),
                f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
                hashlib.sha256
            ).hexdigest()

            if generated_signature != razorpay_signature:
                return Response({
                    "status": False,
                    "message": "Invalid payment signature"
                }, status=400)

            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.payment_status = "success"
            payment.paid_at = timezone.now()
            payment.save()
            # ==========================================
            # REEL PURCHASE NOTIFICATION
            # ==========================================

            if payment.plan_type in [
                "short_reel",
                "cinematic_reel"
            ]:

                ReelPurchaseNotification.objects.create(

                    title="New Reel Package Purchased",

                    message=(
                        f"{payment.agent.username} "
                        f"purchased "
                        f"{payment.reel_package.name}"
                    ),

                    notification_type="reel_purchase",

                    payment=payment,

                    agent=payment.agent
                )
                plan_details = self.get_plan_details(payment)

                return Response({

                    "status": True,

                    "message": "Payment verified successfully. Our team will contact you shortly to discuss your reel requirements.",

                    "payment": {

                        "payment_db_id": str(payment.id),

                        "paid_by": payment.agent.username,

                        "paid_email": payment.agent.email,

                        "plan_type": payment.plan_type,

                        "plan_name": plan_details["name"],

                        "plan_price": plan_details["price"],

                        "payment_status": payment.payment_status,

                        "paid_at": payment.paid_at,

                        "created_at": payment.created_at,
                    }

                }, status=200)
            # =================================================
            # SINGLE PROPERTY PAYMENT
            # =================================================

            if payment.single_property_package:

                cache_key = request.data.get("cache_key")

                if not cache_key:

                    return Response({

                        "status": False,

                        "message": "cache_key required"

                    }, status=400)

                property_data = cache.get(cache_key)

                if not property_data:

                    return Response({

                        "status": False,

                        "message": "Property data expired"

                    }, status=400)

                from django.core.files.base import ContentFile

                import base64

                # Category
                category_value = property_data.get("category")

                if str(category_value).isdigit():
                    category = Category.objects.get(id=int(category_value))
                else:
                    category = Category.objects.get(name__iexact=category_value)

                # Purpose
                purpose_value = property_data.get("purpose")

                if str(purpose_value).isdigit():
                    purpose = Purpose.objects.get(id=int(purpose_value))
                else:
                    purpose = Purpose.objects.get(name__iexact=purpose_value)

                # Subcategory
                subcategory = None

                subcategory_value = property_data.get("subcategory")

                if subcategory_value:

                    if str(subcategory_value).isdigit():
                        subcategory = Subcategory.objects.get(
                            id=int(subcategory_value)
                        )

                    else:
                        subcategory = Subcategory.objects.get(
                            name__iexact=subcategory_value
                        )

                property_obj = Property.objects.create(

                    user=payment.user,

                    category=category,

                    subcategory=subcategory,

                    purpose=purpose,

                    label=property_data.get("label"),

                    description=property_data.get("description"),

                    price=property_data.get("price"),

                    perprice=property_data.get("perprice"),

                    deposit=property_data.get("deposit"),

                    phone=property_data.get("phone"),

                    whatsapp=property_data.get("whatsapp"),

                    city=property_data.get("city"),

                    district=property_data.get("district"),

                    state=property_data.get("state"),

                    taluk=property_data.get("taluk"),

                    village=property_data.get("village"),

                    pincode=property_data.get("pincode"),

                    location=property_data.get("location"),

                    selling_points=property_data.get("selling_points"),

                    land_mark=property_data.get("landmarks"),

                    paid="yes",

                    single_property_package=payment.single_property_package,

                    single_property_edit_limit=payment.single_property_package.edit_limit,

                    single_property_edit_used=0
                )
                # try:
                #     if property_data.get("main_image"):

                #         image_data = base64.b64decode(
                #             property_data["main_image"]
                #         )

                #         property_obj.image.save(
                #             property_data["main_image_name"],
                #             ContentFile(
                #                 image_data,
                #                 name=property_data["main_image_name"]
                #             ),
                #             save=True
                #         )

                # except Exception as e:
                #     print("MAIN IMAGE ERROR:", e)
                #     raise

                # try:

                #     for img in property_data.get("multiple_images", []):

                #         image_data = base64.b64decode(
                #             img["content"]
                #         )

                #         property_image = PropertyImage(
                #             property=property_obj
                #         )

                #         property_image.image.save(
                #             img["name"],
                #             ContentFile(image_data),
                #             save=False
                #         )

                #         property_image.save()

                # except Exception as e:

                #     print("MULTIPLE IMAGE ERROR:", str(e))
                

                for img in property_data.get("multiple_images", []):

                    try:

                        image_bytes = base64.b64decode(
                            img["content"]
                        )

                        suffix = os.path.splitext(
                            img["name"]
                        )[1]

                        with tempfile.NamedTemporaryFile(
                            suffix=suffix,
                            delete=False
                        ) as temp_file:

                            temp_file.write(image_bytes)

                            temp_path = temp_file.name

                        # Upload to Cloudinary
                        upload_result = cloudinary.uploader.upload(
                            temp_path,
                            folder="properties/multiple"
                        )

                        # Save only the public_id
                        PropertyImage.objects.create(

                            property=property_obj,

                            image=upload_result["public_id"]

                        )

                    except Exception as e:

                        print("MULTIPLE IMAGE ERROR:", str(e))

                    finally:

                        if os.path.exists(temp_path):
                            os.remove(temp_path)

                    # Don't stop payment verification if image upload fails
                    pass
                if property_data.get("amenities"):

                    amenities = Amenities.objects.filter(

                        id__in=property_data["amenities"]

                    )

                    property_obj.amenities.set(amenities)
                PropertyFeature.objects.filter(
                    property=property_obj
                ).delete()

                for feature in property_data.get("field_values", []):

                    if not isinstance(feature, dict):
                        continue

                    field_name = str(
                        feature.get("name", "")
                    ).strip()

                    if not field_name:
                        continue

                    field = SubcategoryField.objects.filter(

                        subcategory=property_obj.subcategory,

                        field_name__iexact=field_name

                    ).first()

                    if not field:
                        continue

                    PropertyFeature.objects.create(

                        property=property_obj,

                        field=field,

                        value=json.dumps({

                            "option": feature.get("option"),

                            "value": feature.get("value"),

                            "icon": feature.get("icon")

                        })

                    )
                profile = UserProfile.objects.get(user=payment.user)
                payment.user.profile.increase_property_usage(
                    property_obj.category.name
                )
                print("Calling increase_property_usage")
                print("Payment User:", payment.user.id)
                print("Property Category:", property_obj.category.name)
                print("Profile Exists:", hasattr(payment.user, "profile"))
                cache.delete(cache_key)
                return Response({

                    "status": True,

                    "message": "Payment verified successfully",

                    "property_id": str(property_obj.id),

                    "payment": {

                        "payment_db_id": str(payment.id),

                        "plan_type": payment.plan_type,

                        "plan_name": payment.single_property_package.name,

                        "amount_paid": str(payment.amount),

                        "payment_status": payment.payment_status,

                        "paid_at": payment.paid_at

                    }

                })

            if payment.agent:

                agent = payment.agent

                self.deactivate_expired_agent_plans(agent)

                active_subscriptions = Subscription.objects.filter(
                    agent=agent,
                    is_active=True,
                    end_date__gt=timezone.now().date()
                )

                if active_subscriptions.count() >= 2:

                    return Response({

                        "status": False,

                        "message": "Maximum 2 active agent plans allowed"

                    }, status=400)

                plan_name = ""

                validity_days = 30

                property_limit = 0
                featured_limit = 0

                if payment.premium_plan:
                    plan_type = "premium"
                    plan_name = payment.premium_plan.name

                    validity_days = payment.premium_plan.validity

                    property_limit = payment.premium_plan.total_listing

                elif payment.elite_plan:
                    plan_type = "elite"
                    plan_name = payment.elite_plan.name

                    validity_days = payment.elite_plan.plan_validity_days

                    property_limit = payment.elite_plan.total_property_listings
                    featured_limit = payment.elite_plan.featured_listings_limit

                elif payment.agent_plan:
                    plan_type = "basic"
                    plan_name = payment.agent_plan.name

                    validity_days = getattr(
                        payment.agent_plan,
                        "validity",
                        30
                    )

                    property_limit = getattr(
                        payment.agent_plan,
                        "property_limit",
                        0
                    )
                edit_limit = 0

                if payment.premium_plan and payment.premium_plan.edit:

                    match = re.search(
                        r"(\d+)",
                        str(payment.premium_plan.edit)
                    )

                    if match:
                        edit_limit = int(match.group(1))

                elif payment.elite_plan and payment.elite_plan.edit:

                    match = re.search(
                        r"(\d+)",
                        str(payment.elite_plan.edit)
                    )

                    if match:
                        edit_limit = int(match.group(1))

                Subscription.objects.create(
                    payment=payment,
                    agent=agent,
                    plan_type=plan_type,
                    plan_name=plan_name,
                    property_limit=property_limit,
                    used_listings=0,
                    edit_limit=edit_limit,
                    edit_used=0,
                    featured_limit=featured_limit,
                    featured_used=0,
                    start_date=timezone.now().date(),
                    end_date=timezone.now().date() + timedelta(days=int(validity_days)),
                    is_active=True
                )

            if payment.pending_registration:

                pending = payment.pending_registration

                if pending.status == "pending":

                    pending.status = "approved"

                    pending.save()
                    # agent = pending.agent
                    pending.refresh_from_db()

                    agent = AgentUserProfile.objects.filter(

                        email=pending.email

                    ).first()

                    if not agent:

                        return Response({

                            "status": False,

                            "message": "Agent profile creation failed"

                        }, status=400) 

                    self.deactivate_expired_agent_plans(agent)

                    active_subscriptions = Subscription.objects.filter(

                        agent=agent,

                        is_active=True,

                        end_date__gt=timezone.now().date()

                    )

                    if active_subscriptions.count() >= 2:

                        return Response({

                            "status": False,

                            "message": "Maximum 2 active agent plans allowed"

                        }, status=400)

                    plan_name = "Agent Plan"

                    validity_days = 30

                    property_limit = 0
                    featured_limit = 0

                    if pending.premium_plan:
                        plan_type = "premium"
                        plan_name = pending.premium_plan.name

                        validity_days = pending.premium_plan.validity

                        property_limit = pending.premium_plan.total_listing

                    elif pending.elite_plan:
                        plan_type = "elite"
                        plan_name = pending.elite_plan.name

                        validity_days = pending.elite_plan.plan_validity_days

                        property_limit = pending.elite_plan.total_property_listings
                        featured_limit = pending.elite_plan.featured_listings_limit

                    elif payment.agent_plan:
                        plan_type = "basic"
                        plan_name = payment.agent_plan.name

                        validity_days = getattr(

                            payment.agent_plan,

                            "validity",

                            30

                        )

                        property_limit = getattr(

                            payment.agent_plan,

                            "property_limit",

                            0

                        )
                    edit_limit = 0

                    if pending.premium_plan and pending.premium_plan.edit:

                        match = re.search(
                            r"(\d+)",
                            str(pending.premium_plan.edit)
                        )

                        if match:
                            edit_limit = int(match.group(1))

                    elif pending.elite_plan and pending.elite_plan.edit:

                        match = re.search(
                            r"(\d+)",
                            str(pending.elite_plan.edit)
                        )

                        if match:
                            edit_limit = int(match.group(1))

                    Subscription.objects.create(
                        payment=payment,
                        agent=agent,
                        plan_type=plan_type,
                        plan_name=plan_name,
                        property_limit=property_limit,
                        used_listings=0,
                        edit_limit=edit_limit,
                        edit_used=0,
                        featured_limit=featured_limit,
                        featured_used=0,
                        start_date=timezone.now().date(),
                        end_date=timezone.now().date() + timedelta(days=int(validity_days)),
                        is_active=True
                    )

            if payment.user and payment.user_plan:

                profile = UserProfile.objects.filter(
                    user=payment.user
                ).first()

                if profile:
                    expired_subscriptions = UserPlanSubscription.objects.filter(
                        user=payment.user,
                        is_active=True,
                        expiry_date__lt=timezone.now()
                    )

                    expired_subscriptions.update(
                        is_active=False
                    )

                    active_subscriptions = UserPlanSubscription.objects.filter(
                        user=payment.user,
                        is_active=True,
                        expiry_date__gt=timezone.now()
                    )

                    if active_subscriptions.count() >= 2:

                        return Response({
                            "status": False,
                            "message": "Maximum 2 active plans allowed"
                        }, status=400)

                    # ==========================================
                    # VALIDITY
                    # ==========================================

                    validity_days = self.get_validity_days(
                        payment.user_plan.validity
                    )

                    now = timezone.now()

                    expiry_date = (
                        now +
                        timedelta(days=validity_days)
                    )

                    # ==========================================
                    # CREATE SUBSCRIPTION
                    # ==========================================

                    subscription = UserPlanSubscription.objects.create(
                        user=payment.user,
                        plan=payment.user_plan,
                        is_active=True,
                        expiry_date=expiry_date
                    )

                    subscriptions = UserPlanSubscription.objects.filter(
                        user=payment.user,
                        is_active=True,
                        expiry_date__gt=timezone.now()
                    ).select_related("plan")

                    # ==========================================
                    # HIGHEST PLAN WINS
                    # ==========================================

                    highest_subscription = max(
                        subscriptions,
                        key=lambda x: (
                            int(
                                re.findall(
                                    r"\d+",
                                    str(x.plan.property_listing_limit)
                                )[0]
                            )
                            if re.findall(
                                r"\d+",
                                str(x.plan.property_listing_limit)
                            )
                            else 999999
                        )
                    )

                    UserPlanSubscription.objects.filter(
                        user=payment.user
                    ).update(
                        is_primary=False
                    )

                    highest_subscription.is_primary = True

                    highest_subscription.save(
                        update_fields=["is_primary"]
                    )

                    active_plan = highest_subscription.plan

                    # ==========================================
                    # PROFILE UPDATE
                    # ==========================================

                    profile.user_plan = active_plan

                    profile.is_paid_user = True

                    profile.user_role = "owner"

                    profile.plan_start_date = (
                        highest_subscription.purchased_at
                    )

                    profile.plan_expiry_date = (
                        highest_subscription.expiry_date
                    )

                    profile.save()

                    payment.user.role = "owner"

                    payment.user.last_plan_expiry = (
                        highest_subscription.expiry_date
                    )

                    payment.user.save()

                    if hasattr(payment.user, "user_plans"):

                        payment.user.user_plans.add(
                            payment.user_plan
                        )
            active_plan = None
            profile = None

            if payment.user:

                profile = UserProfile.objects.filter(
                    user=payment.user
                ).first()

                if profile:

                    profile.check_plan_expiry()

                    active_plan = profile.active_plan
            plan_details = self.get_plan_details(payment)

            return Response({
                "status": True,
                "message": "Payment verified successfully",
                "payment": {
                    "payment_db_id": str(payment.id),
                    "paid_by": payment.user.name if payment.user else payment.agent.username,
                    "paid_email": payment.user.email if payment.user else payment.agent.email,
                    "plan_type": payment.plan_type,
                    "plan_name": plan_details["name"],
                    "plan_validity": plan_details["validity"],
                    "plan_price": plan_details["price"],
                    "amount_paid": str(payment.amount),
                    "payment_status": payment.payment_status,
                    "paid_at": payment.paid_at,
                    "created_at": payment.created_at
                },
            })

        except Exception as e:
            return Response({
                "status": False,
                "message": "Payment verification failed",
                "error": str(e)
            }, status=400)

class AdvertisementRequestAPIView(APIView):

    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        plan_id = request.data.get("plan_id")

        if not plan_id:
            return Response({
                "status": False,
                "message": "plan_id is required"
            }, status=400)

        plan = AdvertisementPackage.objects.filter(
            id=plan_id
        ).first()

        if not plan:
            return Response({
                "status": False,
                "message": "Advertisement package not found"
            }, status=404)

        if plan.ad_format not in ["slider", "banner"]:
            return Response({
                "status": False,
                "message": "Invalid advertisement package."
            }, status=400)

        agent = request.user

        AdvertisementRequestNotification.objects.create(

            title="New Advertisement Request",

            message=(
                f"{agent.username} requested the "
                f"{plan.name}. Please contact the agent "
                f"to discuss the advertisement requirements."
            ),

            notification_type="advertisement_request",

            advertisement_package=plan,

            agent=agent
        )
        
        return Response({

            "status": True,

            "message": "Advertisement request sent successfully."

        }, status=201)

class AgentReelPurchaseNotificationAPIView(APIView):

    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        agent = request.user

        notifications = (
            ReelPurchaseNotification.objects.filter(
                agent=agent
            )
            .select_related(
                "payment",
                "payment__reel_package"
            )
            .order_by("-created_at")
        )

        serializer = ReelPurchaseNotificationSerializer(
            notifications,
            many=True
        )

        return Response({

            "status": True,

            "count": notifications.count(),

            "notifications": serializer.data

        })

class AgentPurchaseHistoryAPIView(APIView):

    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        agent = request.user
        purchase_history = []

        subscriptions = Subscription.objects.filter(
            agent=request.user
        ).order_by("-start_date")

        for subscription in subscriptions:
            payment = subscription.payment

            price = None

            if subscription.plan_type == "premium":
                plan = PremiumPlan.objects.filter(
                    name=subscription.plan_name
                ).first()

            elif subscription.plan_type == "elite":
                plan = ElitePlan.objects.filter(
                    name=subscription.plan_name
                ).first()

            else:
                plan = AgentPlan.objects.filter(
                    name=subscription.plan_name
                ).first()

            if plan:
                price = plan.price

            purchase_history.append({
                "plan_type": "Subscription",
                "plan_name": subscription.plan_name,
                "price": price,
                "purchase_date": subscription.start_date,
                "status": "Active" if subscription.is_active else "Expired",
                "order_id": payment.razorpay_order_id if payment else None,
                "payment_id": payment.razorpay_payment_id if payment else None,
            })
        reels = ReelPurchaseNotification.objects.filter(
                agent=request.user
            ).select_related(
                "payment",
                "payment__reel_package"
            )

        for reel in reels:

            package = reel.payment.reel_package

            purchase_history.append({

                "plan_type": "Reel",

                "plan_name": package.name,

                "price": package.price_per_day,

                "purchase_date": reel.created_at.date(),

                "status": reel.status.title(),
                "order_id": reel.payment.razorpay_order_id if reel.payment else None,
                "payment_id": reel.payment.razorpay_payment_id if reel.payment else None,

            })

        ads = AdvertisementRequestNotification.objects.filter(
                agent=request.user
            ).select_related(
                "advertisement_package"
            )

        for ad in ads:

            package = ad.advertisement_package

            purchase_history.append({

                "plan_type": "Advertisement",

                "plan_name": package.name,

                "price": package.price_per_day,

                "purchase_date": ad.created_at.date(),

                "status": ad.status.title(),
                # "order_id": ad.payment.razorpay_order_id if ad.payment else None,
                # "payment_id": ad.payment.razorpay_payment_id if ad.payment else None,

            })

        purchase_history.sort(
            key=lambda x: x["purchase_date"],
            reverse=True
        )

        serializer = PurchaseHistorySerializer(
            purchase_history,
            many=True
        )

        return Response({
            "status": True,
            "count": len(serializer.data),
            "plans": serializer.data
        })
 

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
import os


class DebugDB(APIView):
    def get(self, request):
        return Response({
            "db_path": settings.DATABASES["default"]["NAME"],
            "exists": os.path.exists(settings.DATABASES["default"]["NAME"]),
            "size": os.path.getsize(settings.DATABASES["default"]["NAME"])
            if os.path.exists(settings.DATABASES["default"]["NAME"])
            else 0,
        })

        