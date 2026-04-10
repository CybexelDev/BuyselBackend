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

from django.db.models import Prefetch
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from cloudinary.uploader import upload

from django.http import FileResponse
import os
from django.conf import settings

from developer.models import Premium
from django.core.validators import validate_email

import tempfile
from selenium import webdriver
from urllib.parse import quote
from django.http import JsonResponse
from django.db.models import Q
from .utils import send_otp_email
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import NotAuthenticated
from .authentication import UserJWTAuthentication
from rest_framework import generics


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


class BudgetListAPIView(APIView):

    def get(self, request):

        budget = Budget.objects.all().order_by("id")

        serializer = BudgetSerializer(
            budget,
            many=True
        )

        return Response({
            "budget": serializer.data
        })


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


class FeaturedPropertyViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = PropertySerializer

    def get_queryset(self):

        return Property.objects.filter(
            is_featured=True   # ✅ only featured
        ).prefetch_related(
            "images",
            "category",
            "purpose"
        ).order_by("-id")


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
                if profile.image:
                    if hasattr(profile.image, "url"):
                        image_url = profile.image.url
                    else:
                        image_url, _ = cloudinary_url(profile.image)
                else:
                    image_url, _ = cloudinary_url("Vector_te4oj7")

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


class ChangePasswordAPI(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ChangePasswordSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(serializer.errors, status=400)

        # ✅ Get Authorization Header
        auth_header = request.headers.get("Authorization")

        if not auth_header:

            return Response(
                {"error": "Reset token missing"},
                status=400
            )

        # ✅ Remove Bearer
        try:

            reset_token = auth_header.split(" ")[1]

        except IndexError:

            return Response(
                {"error": "Invalid Authorization header"},
                status=400
            )

        try:

            reset = PasswordResetToken.objects.get(
                token=reset_token
            )

            # expiry check
            if reset.expires_at < timezone.now():

                return Response(
                    {"error": "Reset token expired"},
                    status=400
                )

            user = reset.user

            new_password = serializer.validated_data[
                "new_password"
            ]

            user.password = make_password(
                new_password
            )

            user.save(update_fields=["password"])

            # delete token after use
            reset.delete()

            return Response(
                {"message": "Password changed successfully"},
                status=200
            )

        except PasswordResetToken.DoesNotExist:

            return Response(
                {"error": "Invalid reset token"},
                status=400
            )


class UserLoginAPI(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = UserCreate.objects.get(email=email)

            if not user.is_verified:
                return Response({"error": "Email not verified"}, status=400)

            if not check_password(password, user.password):
                return Response({"error": "Invalid credentials"}, status=400)

            refresh = RefreshToken.for_user(user)

            #  Ensure profile exists
            profile, created = UserProfile.objects.get_or_create(user=user)

            #  Get image
            if profile.image:
                profile_image = profile.image.url
            else:
                # default cloudinary image
                profile_image, _ = cloudinary_url("Vector_te4oj7")

            response = Response({
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": uuid.uuid4().hex[:10],
                    "email": user.email,
                    "name": user.name,
                    "image": profile_image
                }
            })

            return response

        except UserCreate.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)



User = get_user_model()


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

class GoogleLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            access_token = request.data.get("access_token")
            if not access_token:
                return Response({"error": "Access token required"}, status=400)

            # 🔹 GET USER INFO FROM GOOGLE
            google_res = requests.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                params={"access_token": access_token},
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
                return Response({"error": "Email not found"}, status=400)

            # 🔹 CREATE OR GET USER
            user, profile = handle_google_user(email, name, picture)

            # 🔹 GENERATE JWT
            refresh = RefreshToken.for_user(user)

            # 🔹 SAFE IMAGE HANDLING
            image_url = getattr(profile.image, 'url', None)

            # 🔹 RESPONSE (NO COOKIES)
            return Response({
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "auth_provider": profile.auth_provider,
                    "image": image_url,
                    "is_profile_complete": profile.is_profile_complete
                }
            }, status=200)

        except requests.exceptions.Timeout:
            return Response({"error": "Google timeout"}, status=504)

        except Exception as e:
            print("GoogleLoginView ERROR:", str(e))
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


class UserProfileView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    # 🔹 Common method to extract user from token
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
            return None, Response(
                {"detail": "User not found", "code": "user_not_found"},
                status=404
            )
        except Exception:
            return None, Response({"error": "Something went wrong"}, status=400)

    # 🔹 GET Profile
    def get(self, request):
        user, error = self.get_user_from_token(request)
        if error:
            return error

        profile, _ = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    # 🔹 PUT Profile (Full Update)
    def put(self, request):
        user, error = self.get_user_from_token(request)
        if error:
            return error

        profile, _ = UserProfile.objects.get_or_create(user=user)

        serializer = UserProfileSerializer(
            profile,
            data=request.data,
            partial=False   #  FULL update
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)



class UserProfileImageUpdateView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

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

        except Exception:
            return None, Response({"error": "Invalid or expired token"}, status=401)

    def put(self, request):
        user, error = self.get_user_from_token(request)
        if error:
            return error

        if "image" not in request.FILES:
            return Response({"error": "Image file is required"}, status=400)

        profile, _ = UserProfile.objects.get_or_create(user=user)


        if profile.image and profile.image.public_id:
            cloudinary.uploader.destroy(profile.image.public_id)

        # Save new image
        profile.image = request.FILES["image"]
        profile.save()

        return Response({
            "message": "Profile image updated successfully",
            "image_url": profile.image.url
        })


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



class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        refresh_token = request.data.get("refresh") or request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token missing"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # ✅ Use SimpleJWT (same as agent)
            refresh = RefreshToken(refresh_token)

            new_access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)

            return Response({
                "access": new_access_token,
                "refresh": new_refresh_token
            })

        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
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
                "agent_details": agent_details
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

class AgentPendingRegisterAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data

        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()
        agent_type = data.get("agent_type", "").strip()
        plan_id = data.get("plan_id")

        # ✅ Required fields validation
        if not email or not password or not agent_type:
            return Response({
                "status": False,
                "message": "Email, password, and agent type are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return Response({
                "status": False,
                "message": "Invalid email format."
            }, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Prevent duplicate pending OR approved users
        if PendingAgentRegistration.objects.filter(email=email, status='pending').exists():
            return Response({
                "status": False,
                "message": "You have already submitted a registration request."
            }, status=status.HTTP_400_BAD_REQUEST)

        # (Optional but recommended)
        from agents.models import AgentUserProfile
        if AgentUserProfile.objects.filter(email=email).exists():
            return Response({
                "status": False,
                "message": "Account already exists. Please login."
            }, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Initialize plans
        premium_plan = None
        elite_plan = None

        # ✅ Validate plan selection
        if agent_type == "premium":
            if not plan_id:
                return Response({
                    "status": False,
                    "message": "Premium plan is required."
                }, status=status.HTTP_400_BAD_REQUEST)

            premium_plan = PremiumPlan.objects.filter(id=plan_id).first()
            if not premium_plan:
                return Response({
                    "status": False,
                    "message": "Invalid premium plan."
                }, status=status.HTTP_400_BAD_REQUEST)

        elif agent_type == "elite":
            if not plan_id:
                return Response({
                    "status": False,
                    "message": "Elite plan is required."
                }, status=status.HTTP_400_BAD_REQUEST)

            elite_plan = ElitePlan.objects.filter(id=plan_id).first()
            if not elite_plan:
                return Response({
                    "status": False,
                    "message": "Invalid elite plan."
                }, status=status.HTTP_400_BAD_REQUEST)

        elif agent_type == "basic":
            # ✅ No plan required
            premium_plan = None
            elite_plan = None

        else:
            return Response({
                "status": False,
                "message": "Invalid agent type."
            }, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Optional fields
        full_name = data.get("full_name", "").strip()
        phone_number = data.get("phone_number", "").strip()
        city = data.get("city", "").strip()
        pin_code = data.get("pin_code", "").strip()
        address = data.get("address", "").strip() or "N/A"

        # ✅ Create Pending Agent
        PendingAgentRegistration.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=password,  # will be hashed in model
            city=city,
            pin_code=pin_code,
            address=address,
            agent_type=agent_type,
            premium_plan=premium_plan,
            elite_plan=elite_plan,
            status="pending"
        )

        return Response({
            "status": True,
            "message": "Registration request submitted successfully. Waiting for admin approval."
        }, status=status.HTTP_201_CREATED)  


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
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, agent_id):
        # Get agent
        try:
            try:
                agent = AgentUserProfile.objects.get(id=uuid.UUID(agent_id))
            except ValueError:
                agent = AgentUserProfile.objects.get(agent_code=agent_id)
        except AgentUserProfile.DoesNotExist:
            return Response({"error": "Agent not found"}, status=404)

        serializer = AgentReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(agent=agent, user=request.user if request.user.is_authenticated else None)
            return Response({"message": "Review submitted"}, status=201)

        return Response(serializer.errors, status=400)

class ToggleReviewLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        try:
            review = AgentReview.objects.get(id=review_id)
        except AgentReview.DoesNotExist:
            return Response({"error": "Review not found"}, status=404)

        if request.user in review.likes.all():
            review.likes.remove(request.user)
            liked = False
        else:
            review.likes.add(request.user)
            liked = True

        return Response({
            "liked": liked,
            "total_likes": review.likes.count()
        })

class AgentListFrontendAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        agent_type = request.GET.get("type")  # all / basic / premium / elite

        agents = AgentUserProfile.objects.filter(is_active=True)

        if agent_type and agent_type != "all":
            agents = agents.filter(agent_type=agent_type)

        serializer = AgentListFrontendSerializer(agents, many=True)
        return Response(serializer.data)

class AgentReviewListAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, agent_id):

        # 🔥 Detect UUID or agent_code
        try:
            try:
                uuid_obj = uuid.UUID(agent_id)
                agent = AgentUserProfile.objects.get(id=uuid_obj)
            except ValueError:
                agent = AgentUserProfile.objects.get(agent_code=agent_id)

        except AgentUserProfile.DoesNotExist:
            return Response({"error": "Agent not found"}, status=404)

        reviews = AgentReview.objects.filter(agent=agent).order_by("-created_at")
        serializer = AgentReviewSerializer(reviews, many=True)

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

from rest_framework.exceptions import AuthenticationFailed


class AgentJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")

        if not user_id:
            raise AuthenticationFailed("Invalid token")

        try:
            user_uuid = uuid.UUID(user_id)
            user = AgentUserProfile.objects.get(id=user_uuid)
            return user
        except:
            raise AuthenticationFailed("User not found")


from developer.models import PremiumPlan, ElitePlan
from .serializers import PremiumPlanSerializer, ElitePlanSerializer


class PlanListAPIView(APIView):
    authentication_classes = [AgentJWTAuthentication]   # ✅ ADD THIS
    permission_classes = [IsAuthenticated]

    def get(self, request):
        premium_plans = PremiumPlan.objects.all()
        elite_plans = ElitePlan.objects.all()

        premium_serializer = PremiumPlanSerializer(premium_plans, many=True)
        elite_serializer = ElitePlanSerializer(elite_plans, many=True)

        return Response({
            "premium_plans": premium_serializer.data,
            "elite_plans": elite_serializer.data
        })
    
class AgentPlanCombinedAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        from developer.models import PremiumPlan, ElitePlan

        # ✅ Define agent types manually (IDs for frontend mapping)
        agent_types = [
            {"id": 1, "name": "elite agent"},
            {"id": 2, "name": "premium agent"},
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

        return Response({
            "agent_types": agent_types,
            "plans": plans
        })




class AgentContactCreateAPIView(APIView):
    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        from rest_framework.exceptions import NotAuthenticated
        if isinstance(exc, NotAuthenticated):
            return Response(
                {"error": "Please login to contact agent"},
                status=401
            )
        return super().handle_exception(exc)

    def post(self, request, agent_code):
        try:
            agent = AgentUserProfile.objects.get(agent_code=agent_code)
        except AgentUserProfile.DoesNotExist:
            return Response({"error": "Agent not found"}, status=404)

        serializer = AgentContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                agent=agent,
                email=request.user.email,
                first_name=request.user.name,
                last_name=""
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
        contacts = AgentContact.objects.filter(agent=request.user).order_by('-created_at')
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
        fields = SubcategoryField.objects.filter(subcategory_id=subcategory_id)
        data = [
            {
                "id": f.id,
                "field_name": f.field_name,
                "field_type": f.field_type,
                "required": f.required,
                "icon": f.icon.url if f.icon else None
            }
            for f in fields
        ]
        return Response({"status": True, "data": data})


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

            # ✅ Prefetch options (IMPORTANT)
            subcategories = subcategories.prefetch_related(
                "subcategoryfield_set__options"
            )

            subcategory_data = []

            for s in subcategories:
                fields = s.subcategoryfield_set.all()

                field_list = []
                for f in fields:

                    # ✅ Get options
                    option_list = [
                        {
                            "id": opt.id,
                            "name": opt.name,
                            "icon": opt.icon.url if opt.icon else None
                        }
                        for opt in f.options.all()
                    ]

                    # ✅ Field data
                    field_dict = {
                        "id": f.id,
                        "field_name": f.field_name,
                        "field_type": f.field_type,
                        "required": f.required,
                        "icon": f.icon.url if f.icon else None,
                        "field_ui": f.field_ui,

                        # ✅ Show options only for these types
                        "options": option_list if f.field_type in ["select", "multi_select", "countable"] else []
                    }

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
                "message": "Property meta fetched successfully",
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
# ==============================
# Agent Property APIs
# ==============================
class AgentPropertyListAPIView(APIView):
    authentication_classes = [AgentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        properties = AgentProperty.objects.filter(agent=request.user).select_related(
            "category", "subcategory", "purpose"
        ).prefetch_related(
            "amenities", "images", "selling_points", "landmarks", "field_values"
        ).order_by('-created_at')

        serializer = AgentPropertySerializer(properties, many=True, context={'request': request})
        return Response({"status": True, "data": serializer.data})


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

    # ================== HELPER ==================
    def parse_list_field(self, request, field_name):
        values = request.data.getlist(field_name) if hasattr(request.data, 'getlist') else [request.data.get(field_name, "[]")]
        parsed = []

        for v in values:
            try:
                decoded = json.loads(v) if isinstance(v, str) else v

                if isinstance(decoded, list):
                    parsed.extend(decoded)
                else:
                    parsed.append(decoded)

            except json.JSONDecodeError:
                continue

        return parsed

    # ================== POST ==================
    def post(self, request):
        agent = request.user

        # 🔒 PLAN CHECK
        if not agent.is_plan_active():
            return Response({"error": "Your plan has expired."}, status=403)

        # ================== PARSE INPUT ==================
        amenities_list = request.data.getlist('amenities')
        selling_points_list = self.parse_list_field(request, 'selling_points')
        landmarks_list = self.parse_list_field(request, 'landmarks')
        field_values = self.parse_list_field(request, 'field_values')

        # ================== PROCESS FIELD VALUES ==================
        cleaned_field_values = []

        for field in field_values:
            field_id = field.get("field_id")
            value = field.get("value")

            if not field_id:
                continue

            try:
                field_obj = SubcategoryField.objects.prefetch_related("options").get(id=field_id)
            except SubcategoryField.DoesNotExist:
                continue

            # ================== HANDLE TYPES ==================

            # BOOLEAN
            if field_obj.field_type == "boolean":
                value = bool(value)

            # NUMBER
            elif field_obj.field_type == "number":
                try:
                    value = int(value)
                except:
                    value = 0

            # SELECT (single)
            elif field_obj.field_type == "select":
                value = str(value) if value else ""

            # MULTI SELECT (list)
            elif field_obj.field_type == "multi_select":
                value = value if isinstance(value, list) else []

            # 🔥 COUNTABLE (IMPORTANT)
            elif field_obj.field_type == "countable":

                # ensure dict
                if not isinstance(value, dict):
                    value = {}

                formatted_value = {}

                # loop all options → set default 0
                for opt in field_obj.options.all():
                    try:
                        formatted_value[opt.name] = int(value.get(opt.name, 0))
                    except:
                        formatted_value[opt.name] = 0

                value = formatted_value

            # TEXT / DEFAULT
            else:
                value = str(value) if value else ""

            cleaned_field_values.append({
                "field_id": field_obj.id,
                "field_name": field_obj.field_name,
                "value": value
            })

        # ================== SERIALIZER ==================
        serializer = AgentPropertySerializer(
            data=request.data,
            context={
                'request': request,
                'amenities_list': amenities_list,
                'selling_points_list': selling_points_list,
                'landmarks_list': landmarks_list,
                'field_values': cleaned_field_values
            }
        )

        if serializer.is_valid():
            property_obj = serializer.save()

            # ================== SAVE IMAGES ==================
            images = request.FILES.getlist('images')
            for img in images:
                AgentPropertyImage.objects.create(property=property_obj, image=img)

            # AUTO SET MAIN IMAGE
            if not property_obj.image:
                first_image = property_obj.images.first()
                if first_image:
                    property_obj.image = first_image.image
                    property_obj.save()

            return Response({
                "status": True,
                "message": "Property added successfully",
                "data": AgentPropertySerializer(property_obj, context={'request': request}).data
            })

        return Response(serializer.errors, status=400)


class AgentPropertyDetailAPIView(APIView):
        authentication_classes = [AgentJWTAuthentication]
        permission_classes = [IsAuthenticated]
        parser_classes = [MultiPartParser, FormParser]

        def get_object(self, request, id):
            try:
                return AgentProperty.objects.get(id=id, agent=request.user)
            except AgentProperty.DoesNotExist:
                return None

        def parse_list_field(self, request, field_name):
            if hasattr(request.data, 'getlist'):
                values = request.data.getlist(field_name)
                if values:
                    try:
                        if isinstance(values[0], str) and (
                            values[0].startswith("[") or values[0].startswith("{")
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

        # GET
        def get(self, request, id):
            property_obj = self.get_object(request, id)
            if not property_obj:
                return Response({"error": "Property not found"}, status=404)

            serializer = AgentPropertySerializer(property_obj, context={'request': request})
            return Response({"status": True, "data": serializer.data})

        # ✅ UPDATE PROPERTY
        def put(self, request, id):
            property_obj = self.get_object(request, id)
            if not property_obj:
                return Response({"error": "Property not found"}, status=404)

            amenities_list = request.data.getlist('amenities')
            selling_points_list = self.parse_list_field(request, 'selling_points')
            landmarks_list = self.parse_list_field(request, 'landmarks')
            field_values = self.parse_list_field(request, 'field_values')

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

                images = request.FILES.getlist('images')
                if images:
                    property_obj.images.all().delete()
                    for img in images:
                        AgentPropertyImage.objects.create(property=property_obj, image=img)

                    first_image = property_obj.images.first()
                    if first_image:
                        property_obj.image = first_image.image
                        property_obj.save()

                return Response({
                    "status": True,
                    "message": "Property updated successfully",
                    "data": AgentPropertySerializer(property_obj, context={'request': request}).data
                })

            return Response(serializer.errors, status=400)

        # DELETE
        def delete(self, request, id):
            property_obj = self.get_object(request, id)
            if not property_obj:
                return Response({"error": "Property not found"}, status=404)

            agent = request.user
            property_obj.delete()

            if agent.properties_listed > 0:
                agent.properties_listed -= 1
                agent.save()

            return Response({
                "status": True,
                "message": "Property deleted successfully"
            })

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

class PropertyListAPI(generics.ListAPIView):
    serializer_class = PropertyCardSerializer
    permission_classes = [AllowAny]

    authentication_classes = []

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

        if auth_header:
            parts = auth_header.strip().split()

            # ✅ Robust Bearer parsing
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1].strip()

                try:
                    decoded = jwt.decode(
                        token,
                        settings.SECRET_KEY,
                        algorithms=["HS256"]
                    )

                    # ✅ Handle multiple possible payload keys
                    user_id = decoded.get("user_id") or decoded.get("id")

                    if user_id:
                        wishlist_ids = set(
                            Wishlist.objects.filter(user_id=user_id)
                            .values_list("property_id", flat=True)
                        )

                # ✅ Explicit error handling (no silent failures)
                except ExpiredSignatureError:
                    print("❌ Token expired")

                except InvalidTokenError:
                    print("❌ Invalid token")

                except Exception as e:
                    print("❌ JWT error:", str(e))

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




from rest_framework import generics
from rest_framework.exceptions import NotFound

from .models import Property
from .serializers import PropertyDetailSerializer
from .utils import hashids


class PropertyDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve property using HASHED ID
    """

    serializer_class = PropertyDetailSerializer

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]


    #  OPTIMIZED QUERY
    queryset = (
        Property.objects
        .select_related(
            "owner",
            "purpose",
            "category",
            # "subcategory",
        )
        .prefetch_related(
            "amenities",
            "images",                 # ✅ multiple property images
            # "subcategory__fields",    # ✅ subcategory icons
        )
    )

    def initial(self, request, *args, **kwargs):
        try:
            super().initial(request, *args, **kwargs)
        except AuthenticationFailed as e:
            # keeps "User not found" if already raised
            raise e
        except Exception:
            raise AuthenticationFailed(
                {"detail": "User needs to login"}
            )


    # --------------------------------------------------
    # HASHED ID LOOKUP
    # --------------------------------------------------
    def get_object(self):

        hash_id = self.kwargs.get("hash_id")

        if not hash_id:
            raise NotFound("Property id not provided")

        decoded = hashids.decode(hash_id)

        if not decoded:
            raise NotFound("Invalid property id")

        real_id = decoded[0]

        try:
            return self.get_queryset().get(id=real_id)
        except Property.DoesNotExist:
            raise NotFound("Property not found")

    # --------------------------------------------------
    # PASS REQUEST TO SERIALIZER
    # --------------------------------------------------
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context





class PropertyEnquiryCreateView(generics.CreateAPIView):
    queryset = PropertyEnquiry.objects.all()
    serializer_class = PropertyEnquirySerializer

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    # --------------------------------------------------
    # CUSTOM CREATE RESPONSE
    # --------------------------------------------------
    def create(self, request, *args, **kwargs):

        # ✅ Check authenticated user
        user = request.user

        if not user or not user.is_authenticated:
            return Response(
                {"message": "User needs to login"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {
                    "message": "Enquiry submitted successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        # ✅ catches "User not found" from your authentication.py
        except AuthenticationFailed as e:
            return Response(
                {
                    "detail": str(e),
                    "code": "user_not_found"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )



from .serializers import RelatedPropertySerializer

class RelatedPropertiesAPIView(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,hash_id):
        
        #decode hashed_id
        property_id = decode_id(hash_id)

        if not property_id:
            return Response(
                {"error":"Invalid property id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if isinstance(property_id, (list, tuple)):
            property_id = property_id[0]

        try:
            property_obj = Property.objects.select_related(
                "category","purpose"
            ).get(id=property_id)

        except Property.DoesNotExist:
            return Response(
                {"error":"Property not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        related_properties = (
            Property.objects.filter(
                category=property_obj.category,
                purpose=property_obj.purpose,
                expiry_date__gte=property_obj.created_at
            )
            .exclude(id=property_obj.id)
            .select_related("owner")
            .prefetch_related("images")
            .order_by("-created_at")[:10]
        )

        serializer = RelatedPropertySerializer(
            related_properties,
            many=True,
            context={"request":request}
        )

        return Response(serializer.data)




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



# import requests
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken

# User = get_user_model()


# class FacebookCallbackAPIView(APIView):

#     def get(self, request):

#         code = request.GET.get("code")

#         if not code:
#             return Response(
#                 {"error": "No code provided"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # ----------------------------------
#         # STEP 1: Exchange code for token
#         # ----------------------------------
#         token_url = "https://graph.facebook.com/v19.0/oauth/access_token"

#         token_params = {
#             "client_id": settings.FACEBOOK_APP_ID,
#             "redirect_uri": settings.FACEBOOK_REDIRECT_URI,
#             "client_secret": settings.FACEBOOK_APP_SECRET,
#             "code": code,
#         }

#         token_response = requests.get(token_url, params=token_params)
#         token_data = token_response.json()

#         access_token = token_data.get("access_token")

#         if not access_token:
#             return Response(
#                 {"error": "Failed to obtain access token"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # ----------------------------------
#         # STEP 2: Get Facebook user info
#         # ----------------------------------
#         user_info_url = "https://graph.facebook.com/me"

#         user_params = {
#             "fields": "id,name,email",
#             "access_token": access_token,
#         }

#         user_info = requests.get(user_info_url, params=user_params).json()

#         email = user_info.get("email")
#         name = user_info.get("name")

#         if not email:
#             return Response(
#                 {"error": "Email permission not granted"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # ----------------------------------
#         # STEP 3: Create or Get User
#         # ----------------------------------
#         user, created = User.objects.get_or_create(
#             email=email,
#             defaults={
#                 "username": email,
#                 "first_name": name,
#             },
#         )

#         # ----------------------------------
#         # STEP 4: Generate JWT Tokens
#         # ----------------------------------
#         refresh = RefreshToken.for_user(user)

#         return Response({
#             "message": "Facebook login successful",
#             "user": {
#                 "id": user.id,
#                 "email": user.email,
#                 "name": user.first_name,
#             },
#             "tokens": {
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#             },
#         })



# from django.http import JsonResponse

# def data_deletion(request):
#     return JsonResponse({
#         "message": "If you want to delete your data, contact support@buysel.com"
#     })


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

        # ✅ get purpose from query
        purpose_name = request.query_params.get("purpose")

        # ----------------------------------
        # STEP 1: user's wishlist
        # ----------------------------------
        wishlist_qs = Wishlist.objects.filter(user=user)

        # ----------------------------------
        # STEP 2: filter by purpose
        # ----------------------------------
        if purpose_name:
            wishlist_qs = wishlist_qs.filter(
                property__purpose__name__iexact=purpose_name
            )

        # ----------------------------------
        # STEP 3: get properties
        # ----------------------------------
        properties = Property.objects.filter(
            id__in=wishlist_qs.values_list("property_id", flat=True)
        ).select_related(
            "owner",
            "purpose",
            "category"
        ).prefetch_related(
            "images"
        ).order_by("-created_at")

        # ----------------------------------
        # STEP 4: serialize
        # ----------------------------------
        serializer = WishlistSerializer(
            properties,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


from django.db.models.functions import Cast
from django.db.models import IntegerField


class WishlistSortingAPIView(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        sort_by = request.query_params.get("sort", "default")

        # ----------------------------------
        # BASE QUERYSET (BEST PRACTICE)
        # ----------------------------------
        properties = Property.objects.filter(
            wishlist__user=user   # ✅ direct relation
        ).select_related(
            "owner", "purpose", "category"
        ).prefetch_related(
            "images"
        ).distinct()

        # ----------------------------------
        # SAFE PRICE CAST
        # ----------------------------------
        properties = properties.annotate(
            price_int=Cast("price", IntegerField())
        )

        # ----------------------------------
        # SORTING
        # ----------------------------------
        if sort_by == "latest":
            # latest property added
            properties = properties.order_by("-created_at")

        elif sort_by == "price_low_to_high":
            properties = properties.order_by("price_int")

        elif sort_by == "price_high_to_low":
            properties = properties.order_by("-price_int")

        else:
            # default wishlist view
            properties = properties.order_by("-wishlist__created_at")

        # ----------------------------------
        # SERIALIZER
        # ----------------------------------
        serializer = WishlistSerializer(
            properties,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UserProfileUpdateView(APIView):

    authentication_classes = []
    permission_classes = []

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

            user = UserCreate.objects.get(id=user_id)

            return user, None

        except Exception:
            return None, Response(
                {"error": "Invalid or expired token"},
                status=401
            )

    # UPDATE PROFILE
    
    def put(self, request):

        user, error = self.get_user_from_token(request)

        if error:
            return error

        serializer = UserProfileUpdateSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.update(user, serializer.validated_data)

        return Response(
            {"message": "Profile updated successfully"},
            status=200
        )


