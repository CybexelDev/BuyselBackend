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
from agents.utils import check_plan_notifications
from agents.utils import create_notification


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

from rest_framework.permissions import AllowAny
import jwt
from django.conf import settings

class FeaturedPropertyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PropertyCardSerializer
    authentication_classes = []   # 🔥 VERY IMPORTANT
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Property.objects.filter(
            is_featured=True
        ).prefetch_related(
            "images",
            "category",
            "purpose"
        ).order_by("-id")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        request = self.request

        wishlist_ids = set()
        user = None

        # ✅ MANUAL TOKEN HANDLING (same as your wishlist API)
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

                # ✅ YOUR REAL USER MODEL
                user = UserCreate.objects.filter(id=user_id).first()

                if user:
                    wishlist_ids = set(
                        Wishlist.objects.filter(user=user)
                        .values_list("property_id", flat=True)
                    )

            except jwt.ExpiredSignatureError:
                print("Token expired")
            except jwt.InvalidTokenError:
                print("Invalid token")
            except Exception as e:
                print("Error:", str(e))

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

            if not user.is_verified:
                return Response(
                    {"error": "Email not verified"},
                    status=400
                )

            if not check_password(
                password,
                user.password
            ):
                return Response(
                    {"error": "Invalid credentials"},
                    status=400
                )


            # ------------------------
            # UUID SAFE JWT
            # ------------------------
            refresh = RefreshToken.for_user(user)

            # important after UUID migration
            refresh["user_id"] = str(user.id)


            profile, created = UserProfile.objects.get_or_create(
                user=user
            )

            profile_image = profile.profile_image_url


            return Response({
                "message": "Login successful",

                "access": str(
                    refresh.access_token
                ),

                "refresh": str(
                    refresh
                ),

                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "name": user.name,
                    "image": profile_image
                }
            })


        except UserCreate.DoesNotExist:
            return Response(
                {
                    "error": "Invalid credentials"
                },
                status=400
            )



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
            # image_url = getattr(profile.image, 'url', None)
            # uploaded image or initials avatar
            image_url = profile.profile_image_url

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


# class UserProfileView(APIView):

#     authentication_classes = []
#     permission_classes = [AllowAny]

#     # 🔹 Common method to extract user from token
#     def get_user_from_token(self, request):
#         auth_header = request.headers.get("Authorization")

#         if not auth_header:
#             return None, Response({"error": "Authorization header missing"}, status=401)

#         try:
#             token = auth_header.split(" ")[1]

#             decoded = jwt.decode(
#                 token,
#                 settings.SECRET_KEY,
#                 algorithms=["HS256"]
#             )

#             user_id = int(decoded.get("user_id"))
#             user = UserCreate.objects.get(id=user_id)

#             return user, None

#         except jwt.ExpiredSignatureError:
#             return None, Response({"error": "Token expired"}, status=401)
#         except jwt.InvalidTokenError:
#             return None, Response({"error": "Invalid token"}, status=401)
#         except UserCreate.DoesNotExist:
#             return None, Response(
#                 {"detail": "User not found", "code": "user_not_found"},
#                 status=404
#             )
#         except Exception:
#             return None, Response({"error": "Something went wrong"}, status=400)

#     # 🔹 GET Profile
#     def get(self, request):
#         user, error = self.get_user_from_token(request)
#         if error:
#             return error

#         profile, _ = UserProfile.objects.get_or_create(user=user)
#         serializer = UserProfileSerializer(profile)
#         data = serializer.data
#         data["image"] = profile.profile_image_url
#         return Response(serializer.data)

#     # 🔹 PUT Profile (Full Update)
#     def put(self, request):
#         user, error = self.get_user_from_token(request)
#         if error:
#             return error

#         profile, _ = UserProfile.objects.get_or_create(user=user)

#         serializer = UserProfileSerializer(
#             profile,
#             data=request.data,
#             partial=False   #  FULL update
#         )

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors, status=400)


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

# class AgentPendingRegisterAPIView(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def clean_optional(self, value):
#         if value is None:
#             return None
#         value = str(value).strip()
#         return value if value else None

#     def post(self, request):
#         data = request.data

#         email = data.get("email", "").strip().lower()
#         password = data.get("password", "").strip()
#         agent_type = data.get("agent_type", "")
#         plan_id = data.get("plan_id")

#         # ✅ Required fields
#         if not email or not password or not agent_type:
#             return Response({
#                 "status": False,
#                 "message": "Email, password, and agent type are required."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ Validate email
#         try:
#             validate_email(email)
#         except ValidationError:
#             return Response({
#                 "status": False,
#                 "message": "Invalid email format."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ Duplicate check
#         if PendingAgentRegistration.objects.filter(email=email, status='pending').exists():
#             return Response({
#                 "status": False,
#                 "message": "You have already submitted a registration request."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         from agents.models import AgentUserProfile
#         if AgentUserProfile.objects.filter(email=email).exists():
#             return Response({
#                 "status": False,
#                 "message": "Account already exists. Please login."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ Plan handling
#         premium_plan = None
#         elite_plan = None

#         if agent_type == "premium":
#             if not plan_id:
#                 return Response({"status": False, "message": "Premium plan is required."}, status=400)

#             premium_plan = PremiumPlan.objects.filter(id=plan_id).first()
#             if not premium_plan:
#                 return Response({"status": False, "message": "Invalid premium plan."}, status=400)

#         elif agent_type == "elite":
#             if not plan_id:
#                 return Response({"status": False, "message": "Elite plan is required."}, status=400)

#             elite_plan = ElitePlan.objects.filter(id=plan_id).first()
#             if not elite_plan:
#                 return Response({"status": False, "message": "Invalid elite plan."}, status=400)

#         elif agent_type != "basic":
#             return Response({"status": False, "message": "Invalid agent type."}, status=400)

#         # ✅ FIX: FIRST get values
#         full_name = self.clean_optional(data.get("full_name"))
#         phone_number = self.clean_optional(data.get("phone_number"))
#         city = self.clean_optional(data.get("city"))
#         pin_code = self.clean_optional(data.get("pin_code"))
#         address = self.clean_optional(data.get("address"))

#         # ✅ THEN apply defaults (important order)
#         full_name = full_name or "Guest User"
#         phone_number = phone_number or "0000000000"
#         city = city or "Unknown"
#         pin_code = pin_code or "000000"
#         address = address or "N/A"

#         # ✅ Create object
#         PendingAgentRegistration.objects.create(
#             full_name=full_name,
#             email=email,
#             phone_number=phone_number,
#             password=password,
#             city=city,
#             pin_code=pin_code,
#             address=address,
#             agent_type=agent_type,
#             premium_plan=premium_plan,
#             elite_plan=elite_plan,
#             status="pending"
#         )

#         return Response({
#             "status": True,
#             "message": "Registration request submitted successfully. Waiting for admin approval."
#         }, status=status.HTTP_201_CREATED)

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

        token = request.headers.get("Authorization")

        if not token:
            return Response({"error": "Reset token missing"}, status=400)

        try:
            token = token.split(" ")[1]
        except:
            return Response({"error": "Invalid token format"}, status=400)

        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or not confirm_password:
            return Response({"error": "Both passwords required"}, status=400)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)

        try:
            agent = AgentUserProfile.objects.get(reset_token=token)

            agent.set_password(new_password)

            # clear token
            agent.reset_token = None
            agent.save(update_fields=["password", "reset_token"])

            return Response({"message": "Password changed successfully"})

        except AgentUserProfile.DoesNotExist:
            return Response({"error": "Invalid or expired token"}, status=400)

class AgentPendingRegisterAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data

        email = str(data.get("email", "")).strip().lower()
        password = str(data.get("password", "")).strip()
        agent_type = data.get("agent_type")   # NUMBER (1/2/3)
        plan_id = data.get("plan_id")

        full_name = str(data.get("full_name", "")).strip()
        phone_number = str(data.get("phone_number", "")).strip()
        city = str(data.get("city", "")).strip()
        pin_code = str(data.get("pin_code", "")).strip()
        address = str(data.get("address", "")).strip()

        # ✅ Required validation
        if not all([email, password, agent_type, full_name, phone_number, city, pin_code, address]):
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

        if PendingAgentRegistration.objects.filter(email=email, status='pending').exists():
            return Response({
                "status": False,
                "message": "You have already submitted a request."
            }, status=400)

        if AgentUserProfile.objects.filter(email=email).exists():
            return Response({
                "status": False,
                "message": "Account already exists. Please login."
            }, status=400)

        # ✅ Map agent type
        agent_type_map = {
            1: "elite",
            2: "premium",
            3: "basic"
        }

        try:
            agent_type = int(agent_type)
        except:
            return Response({
                "status": False,
                "message": "Invalid agent type."
            }, status=400)

        if agent_type not in agent_type_map:
            return Response({
                "status": False,
                "message": "Invalid agent type."
            }, status=400)

        agent_type_str = agent_type_map[agent_type]

        premium_plan = None
        elite_plan = None

        # ✅ Plan handling
        if agent_type_str == "elite":
            if not plan_id:
                return Response({"status": False, "message": "Elite plan required"}, status=400)

            elite_plan = ElitePlan.objects.filter(id=plan_id).first()
            if not elite_plan:
                return Response({"status": False, "message": "Invalid elite plan"}, status=400)

        elif agent_type_str == "premium":
            if not plan_id:
                return Response({"status": False, "message": "Premium plan required"}, status=400)

            premium_plan = PremiumPlan.objects.filter(id=plan_id).first()
            if not premium_plan:
                return Response({"status": False, "message": "Invalid premium plan"}, status=400)

        # ✅ BASIC → NO PLAN NEEDED
        # do nothing for basic

        PendingAgentRegistration.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=password,
            city=city,
            pin_code=pin_code,
            address=address,
            agent_type=agent_type_str,
            premium_plan=premium_plan,
            elite_plan=elite_plan,
            status="pending"
        )

        return Response({
            "status": True,
            "message": "Registration submitted. Waiting for admin approval."
        }, status=201)

# class AgentPendingRegisterAPIView(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def clean_optional(self, value):
#         if value is None:
#             return None
#         value = str(value).strip()
#         return value if value else None


#     def post(self, request):
#         data = request.data

#         email = data.get("email", "").strip().lower()
#         password = data.get("password", "").strip()
#         agent_type = data.get("agent_type", "").strip()
#         plan_id = data.get("plan_id")

#         # ✅ Required fields validation
#         if not email or not password or not agent_type:
#             return Response({
#                 "status": False,
#                 "message": "Email, password, and agent type are required."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ Validate email format
#         try:
#             validate_email(email)
#         except ValidationError:
#             return Response({
#                 "status": False,
#                 "message": "Invalid email format."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ Prevent duplicate pending OR approved users
#         if PendingAgentRegistration.objects.filter(email=email, status='pending').exists():
#             return Response({
#                 "status": False,
#                 "message": "You have already submitted a registration request."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # (Optional but recommended)
#         from agents.models import AgentUserProfile
#         if AgentUserProfile.objects.filter(email=email).exists():
#             return Response({
#                 "status": False,
#                 "message": "Account already exists. Please login."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ Initialize plans
#         premium_plan = None
#         elite_plan = None

#         # ✅ Validate plan selection
#         if agent_type == "premium":
#             if not plan_id:
#                 return Response({
#                     "status": False,
#                     "message": "Premium plan is required."
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             premium_plan = PremiumPlan.objects.filter(id=plan_id).first()
#             if not premium_plan:
#                 return Response({
#                     "status": False,
#                     "message": "Invalid premium plan."
#                 }, status=status.HTTP_400_BAD_REQUEST)

#         elif agent_type == "elite":
#             if not plan_id:
#                 return Response({
#                     "status": False,
#                     "message": "Elite plan is required."
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             elite_plan = ElitePlan.objects.filter(id=plan_id).first()
#             if not elite_plan:
#                 return Response({
#                     "status": False,
#                     "message": "Invalid elite plan."
#                 }, status=status.HTTP_400_BAD_REQUEST)

#         elif agent_type == "basic":
#             # ✅ No plan required
#             premium_plan = None
#             elite_plan = None

#         else:
#             return Response({
#                 "status": False,
#                 "message": "Invalid agent type."
#             }, status=status.HTTP_400_BAD_REQUEST)
        

#         ✅ Optional fields
#         full_name = data.get("full_name", "").strip()
#         phone_number = data.get("phone_number", "").strip()
#         city = data.get("city", "").strip()
#         pin_code = data.get("pin_code", "").strip()
#         address = data.get("address", "").strip() or "N/A"

#         # ✅ Create Pending Agent
#         PendingAgentRegistration.objects.create(
#             full_name=full_name,
#             email=email,
#             phone_number=phone_number,
#             password=password,  # will be hashed in model
#             city=city,
#             pin_code=pin_code,
#             address=address,
#             agent_type=agent_type,
#             premium_plan=premium_plan,
#             elite_plan=elite_plan,
#             status="pending"
#         )

#         return Response({
#             "status": True,
#             "message": "Registration request submitted successfully. Waiting for admin approval."
#         }, status=status.HTTP_201_CREATED)  


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

# class SubmitAgentReviewAPIView(APIView):
#     # permission_classes = [AllowAny]
#     # authentication_classes = []
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def post(self, request, agent_id):
#         # Get agent
#         try:
#             try:
#                 agent = AgentUserProfile.objects.get(id=uuid.UUID(agent_id))
#             except ValueError:
#                 agent = AgentUserProfile.objects.get(agent_code=agent_id)
#         except AgentUserProfile.DoesNotExist:
#             return Response({"error": "Agent not found"}, status=404)

#         serializer = AgentReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(agent=agent, user=request.user if request.user.is_authenticated else None)
#             return Response({"message": "Review submitted"}, status=201)

#         return Response(serializer.errors, status=400)




# class SubmitAgentReviewAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def get_user_safely(self, request):
#         """
#         🔥 Handles both:
#         - Normal login (request.user works)
#         - Google/Facebook (fallback to JWT decode)
#         """

#         # ✅ STEP 1: Try normal way
#         try:
#             user = UserCreate.objects.get(id=request.user.id)
#             return user, None
#         except Exception:
#             pass

#         # 🔥 STEP 2: Fallback → decode JWT manually
#         auth_header = request.headers.get("Authorization")

#         if not auth_header:
#             return None, Response({"error": "Authorization header missing"}, status=401)

#         try:
#             token = auth_header.split(" ")[1]

#             decoded = jwt.decode(
#                 token,
#                 settings.SECRET_KEY,
#                 algorithms=["HS256"]
#             )

#             user_id = decoded.get("user_id")

#             if not user_id:
#                 return None, Response({"error": "Invalid token payload"}, status=401)

#             user = UserCreate.objects.filter(id=user_id).first()

#             if not user:
#                 return None, Response({"error": "User not found"}, status=404)

#             return user, None

#         except jwt.ExpiredSignatureError:
#             return None, Response({"error": "Token expired"}, status=401)

#         except jwt.InvalidTokenError:
#             return None, Response({"error": "Invalid token"}, status=401)

#         except Exception as e:
#             return None, Response({"error": str(e)}, status=400)

#     def post(self, request, agent_id):

#         # ✅ STEP 1: Get correct user (ALL LOGIN TYPES)
#         user, error = self.get_user_safely(request)
#         if error:
#             return error

#         # ✅ STEP 2: Ensure profile exists
#         profile, created = UserProfile.objects.get_or_create(
#             user=user,
#             defaults={
#                 "full_name": user.name,
#                 "auth_provider": "mobile"  # fallback
#             }
#         )

#         # 🔥 OPTIONAL: Update provider if missing
#         if not profile.auth_provider:
#             profile.auth_provider = "mobile"
#             profile.save()

#         # 🔥 STEP 3: Get agent
#         try:
#             try:
#                 agent = AgentUserProfile.objects.get(id=uuid.UUID(agent_id))
#             except ValueError:
#                 agent = AgentUserProfile.objects.get(agent_code=agent_id)
#         except AgentUserProfile.DoesNotExist:
#             return Response({"error": "Agent not found"}, status=404)

#         # 🔥 STEP 4: Prevent duplicate review
#         if AgentReview.objects.filter(agent=agent, user=user).exists():
#             return Response(
#                 {"error": "You already reviewed this agent"},
#                 status=400
#             )

#         # 🔥 STEP 5: Save review
#         serializer = AgentReviewSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save(
#                 agent=agent,
#                 user=user
#             )

#             return Response({
#                 "message": "Review submitted successfully",
#                 # "user": {
#                 #     "id": user.id,
#                 #     "email": user.email,
#                 #     "profile_id": profile.id,
#                 #     "provider": profile.auth_provider
#                 # }
#             }, status=201)

#         return Response(serializer.errors, status=400)


class SubmitAgentReviewAPIView(APIView):
    permission_classes = []   # 🔥 disable DRF permission
    authentication_classes = []  # 🔥 disable DRF auth

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

            # ✅ IMPORTANT: use filter().first() (no crash)
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

    def post(self, request, agent_id):

        # ✅ STEP 1: Get logged-in user
        user, error = self.get_user_from_token(request)
        if error:
            return error

        # ✅ STEP 2: Ensure profile exists (NO ERROR)
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "full_name": user.name or "",
                "auth_provider": "mobile"
            }
        )

        # ✅ STEP 3: Get agent (UUID or code)
        try:
            try:
                agent = AgentUserProfile.objects.get(id=uuid.UUID(agent_id))
            except ValueError:
                agent = AgentUserProfile.objects.get(agent_code=agent_id)
        except AgentUserProfile.DoesNotExist:
            return Response({"error": "Agent not found"}, status=404)

        # ✅ STEP 4: Prevent duplicate review
        if AgentReview.objects.filter(agent=agent, user=user).exists():
            return Response(
                {"message": "You already reviewed this agent"},
                status=400
            )

        # ✅ STEP 5: Save review
        serializer = AgentReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(agent=agent, user=user)

            return Response({
                "message": "Review submitted successfully"
            }, status=201)

        return Response(serializer.errors, status=400)
    


# class ToggleReviewLikeAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, review_id):
#         try:
#             review = AgentReview.objects.get(id=review_id)
#         except AgentReview.DoesNotExist:
#             return Response({"error": "Review not found"}, status=404)

#         if request.user in review.likes.all():
#             review.likes.remove(request.user)
#             liked = False
#         else:
#             review.likes.add(request.user)
#             liked = True

#         return Response({
#             "liked": liked,
#             "total_likes": review.likes.count()
#         })

# from developer.models import UserCreate, UserProfile

# class ToggleReviewLikeAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, review_id):

#         # ✅ Step 1: Get Review (UUID supported)
#         try:
#             review = AgentReview.objects.get(id=review_id)
#         except AgentReview.DoesNotExist:
#             return Response({"error": "Review not found"}, status=404)

#         # ✅ Step 2: Get logged-in user → UserProfile → UserCreate
#         try:
#             # request.user = CustomUser
#             user_profile = UserProfile.objects.get(user__id=request.user.id)

#             # actual user for your model
#             user = user_profile.user   # this is UserCreate

#         except UserProfile.DoesNotExist:
#             return Response({"error": "User profile not found"}, status=404)

#         # ✅ Step 3: Toggle Like
#         if review.likes.filter(id=user.id).exists():
#             review.likes.remove(user)
#             liked = False
#         else:
#             review.likes.add(user)
#             liked = True

#         return Response({
#             "liked": liked,
#             "total_likes": review.likes.count()
#         })

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

# class AgentListFrontendAPIView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     def get(self, request):
#         agent_type = request.GET.get("type")  # all / basic / premium / elite

#         agents = AgentUserProfile.objects.filter(is_active=True)

#         if agent_type and agent_type != "all":
#             agents = agents.filter(agent_type=agent_type)

#         serializer = AgentListFrontendSerializer(agents, many=True)
#         return Response(serializer.data)

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




from developer.models import PremiumPlan, ElitePlan
from .serializers import PremiumPlanSerializer, ElitePlanSerializer
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
            f"{plan.Bulk_whatsapp}",
            f"{plan.Poster} Posters",
            f"{plan.social_media.strip()}",
            f"Lead Follow: {plan.lead_follow}",
            f"{plan.lead_management.strip()}",
            f"{plan.validity} Days Validity"
        ]

    def build_elite_features(self, plan):
        return [
            f"{plan.total_property_listings} Property Listings",
            f"{plan.sale_listings_limit} Sale Listings",
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
        current_plan = None

        if getattr(agent, "plan", None):
            plan = agent.plan
            current_plan = {
                "type": "premium",
                "plan_key": self.get_premium_key(plan.validity),
                "name": plan.name,
                "start_date": getattr(agent, "plan_start_date", None),
                "expiry_date": getattr(agent, "plan_expiry_date", None),
                "is_active": agent.is_plan_active()
            }

        elif getattr(agent, "elite_plan", None):
            elite = agent.elite_plan
            current_plan = {
                "type": "elite",
                "plan_key": self.get_elite_key(elite.plan_validity_days),
                "name": elite.name,
                "start_date": getattr(agent, "plan_start_date", None),
                "expiry_date": getattr(agent, "plan_expiry_date", None),
                "is_active": agent.is_plan_active()
            }

        # ================= PREMIUM =================
        premium_plans = []
        for plan in premium_plans_qs:
            premium_plans.append({
                "id": self.get_premium_key(plan.validity),
                "label": plan.name,
                "duration": self.format_duration(plan.validity),
                "price": plan.price,
                "savings": self.format_duration(plan.validity),
                "features": self.build_premium_features(plan)
            })

        # ================= ELITE =================
        elite_plans = []
        for plan in elite_plans_qs:
            elite_plans.append({
                "id": self.get_elite_key(plan.plan_validity_days),
                "label": plan.name,
                "duration": self.format_duration(plan.plan_validity_days),
                "price": plan.price,
                "savings": self.format_duration(plan.plan_validity_days),
                "features": self.build_elite_features(plan)
            })

        # ================= GROUPED ADS =================
        ads_grouped = defaultdict(lambda: {
            "id": None,
            "name": "",
            "plans": []
        })

        for ad in ad_packages:
            group = ads_grouped[ad.name]

            group["id"] = group["id"] or ad.id
            group["name"] = ad.name

            group["plans"].append({
                "type": ad.ad_format,
                "price_per_day": ad.price_per_day,
                "features": self.build_ad_features(ad)
            })

        formatted_ads = list(ads_grouped.values())

        # ================= GROUPED REELS =================
        reels_grouped = defaultdict(lambda: {
            "id": None,
            "name": "",
            "plans": []
        })

        for reel in reel_packages:
            group = reels_grouped[reel.name]

            group["id"] = group["id"] or reel.id
            group["name"] = reel.name

            group["plans"].append({
                "type": reel.reel_type,
                "price_per_day": reel.price_per_day,
                "features": self.build_reel_features(reel)
            })

        formatted_reels = list(reels_grouped.values())

        # ================= FINAL RESPONSE =================
        return Response({
            "current_plan": current_plan,
            "plans": [
                {
                    "id": 1,
                    "name": "Premium Agent",
                    "plans": premium_plans
                },
                {
                    "id": 2,
                    "name": "Elite Agent",
                    "plans": elite_plans
                }
            ],
            "advertisement_packages": formatted_ads,
            "reel_packages": formatted_reels
        })





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
    
class AllPlansAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        normal = AgentPlan.objects.all()
        premium = PremiumPlan.objects.all()
        elite = ElitePlan.objects.all()
        userplans = Userplan.objects.all()   # ✅ added

        return Response({
            "user_plans": UserplanSerializer(userplans, many=True).data,   # ✅ added
            "normal_plans": AgentPlanSerializer(normal, many=True).data,
            "premium_plans": PremiumPlanSerializer(premium, many=True).data,
            "elite_plans": ElitePlanSerializer(elite, many=True).data
        })
# class AgentContactCreateAPIView(APIView):
#     authentication_classes = [UserJWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def handle_exception(self, exc):
#         if isinstance(exc, NotAuthenticated):
#             return Response(
#                 {"error": "Please login to contact agent"},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
#         return super().handle_exception(exc)

#     def post(self, request, agent_code):
#         try:
#             agent = AgentUserProfile.objects.get(agent_code=agent_code)
#         except AgentUserProfile.DoesNotExist:
#             return Response({"error": "Agent not found"}, status=404)

#         serializer = AgentContactSerializer(data=request.data)

#         if serializer.is_valid():
#             user = request.user  # ✅ this is UserCreate

#             serializer.save(
#                 agent=agent,
#                 user=user,  # ✅ IMPORTANT (link user)
#                 email=getattr(user, "email", "guest@example.com"),
#                 first_name=getattr(user, "name", "Guest"),
#                 last_name=""
#             )

#             return Response({
#                 "status": True,
#                 "message": "Message sent successfully"
#             })

#         return Response(serializer.errors, status=400)

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


# class SubcategoryFieldListAPIView(APIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     def get(self, request):
#         subcategory_id = request.GET.get("subcategory_id")
#         fields = SubcategoryField.objects.filter(subcategory_id=subcategory_id)
#         data = [
#             {
#                 "id": f.id,
#                 "field_name": f.field_name,
#                 "field_type": f.field_type,
#                 "required": f.required,
#                 "icon": f.icon.url if f.icon else None
#             }
#             for f in fields
#         ]
#         return Response({"status": True, "data": data})


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

# class PropertyMetaAPIView(APIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     def get(self, request):
#         try:
#             category_id = request.GET.get("category_id")

#             # ================== CATEGORIES ==================
#             categories = Category.objects.all().order_by("name")
#             category_data = [
#                 {
#                     "id": c.id,
#                     "name": c.name,
#                     "icon": c.icon.url if c.icon else None
#                 }
#                 for c in categories
#             ]

#             # ================== SUBCATEGORIES ==================
#             subcategories = Subcategory.objects.all().order_by("name")

#             if category_id:
#                 subcategories = subcategories.filter(category_id=category_id)

#             # ✅ Prefetch options (IMPORTANT)
#             subcategories = subcategories.prefetch_related(
#                 "subcategoryfield_set__options"
#             )

#             subcategory_data = []

#             for s in subcategories:
#                 fields = s.subcategoryfield_set.all()

#                 field_list = []
#                 for f in fields:

#                     # ✅ Get options
#                     option_list = [
#                         {
#                             "id": opt.id,
#                             "name": opt.name,
#                             "icon": opt.icon.url if opt.icon else None
#                         }
#                         for opt in f.options.all()
#                     ]

#                     # ✅ Field data
#                     # field_dict = {
#                     #     "id": f.id,
#                     #     "field_name": f.field_name,
#                     #     "field_type": f.field_type,
#                     #     "required": f.required,
#                     #     "icon": f.icon.url if f.icon else None,
#                     #     "field_ui": f.field_ui,

#                     #     # ✅ Show options only for these types
#                     #     "options": option_list if f.field_type in ["select", "multi_select", "countable"] else []
#                     # }
#                     # Decide option format
#                     if f.field_type in ["select", "countable"]:
#                         options = [opt.name for opt in f.options.all()]

#                     elif f.field_type == "multi_select":
#                         options = [
#                             {
#                                 "name": opt.name,
#                                 "icon": opt.icon.url if opt.icon else None
#                             }
#                             for opt in f.options.all()
#                         ]
#                     else:
#                         options = []

#                     field_dict = {
#                         "id": f.id,
#                         "field_name": f.field_name,
#                         # "options": options
#                     }

#                     if options:
#                         field_dict["options"] = options

#                     field_list.append(field_dict)

#                 subcategory_data.append({
#                     "id": s.id,
#                     "name": s.name,
#                     "category_id": s.category_id,
#                     "fields": field_list
#                 })

#             # ================== PURPOSES ==================
#             purposes = Purpose.objects.all().order_by("name")
#             purpose_data = [{"id": p.id, "name": p.name} for p in purposes]

#             # ================== AMENITIES ==================
#             amenities = Amenities.objects.all().order_by("name")
#             amenities_data = [
#                 {
#                     "id": a.id,
#                     "name": a.name,
#                     "icon": a.icon.url if a.icon else None
#                 }
#                 for a in amenities
#             ]

#             return Response({
#                 "status": True,
#                 "message": "Property meta fetched successfully",
#                 "data": {
#                     "categories": category_data,
#                     "subcategories": subcategory_data,
#                     "purposes": purpose_data,
#                     "amenities": amenities_data
#                 }
#             })

#         except Exception as e:
#             return Response({
#                 "status": False,
#                 "message": str(e),
#                 "data": {}
#             })

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

# class AgentPropertyListAPIView(APIView):
#     authentication_classes = [AgentJWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         properties = AgentProperty.objects.filter(agent=request.user).select_related(
#             "category", "subcategory", "purpose"
#         ).prefetch_related(
#             "amenities", "images", "selling_points", "landmarks", "field_values"
#         ).order_by('-created_at')

#         serializer = AgentPropertySerializer(properties, many=True, context={'request': request})
#         return Response({"status": True, "data": serializer.data})


# class AgentPropertyLimitAPIView(APIView):
#     authentication_classes = [AgentJWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         agent = request.user
#         total_limit, residential_limit, commercial_limit = agent.get_plan_limits()

#         total_used = AgentProperty.objects.filter(agent_id=agent.id).count()
#         residential_used = AgentProperty.objects.filter(agent_id=agent.id, category__name__iexact="Residential").count()
#         commercial_used = AgentProperty.objects.filter(agent_id=agent.id, category__name__iexact="Commercial").count()

#         data = {
#             "agent_name": agent.username,
#             "agent_type": agent.agent_type,
#             "plan_active": agent.is_plan_active(),
#             "plan_expiry_date": agent.plan_expiry_date,
#             "total_limit": total_limit,
#             "total_used": total_used,
#             "total_remaining": max(total_limit - total_used, 0),
#         }

#         if agent.plan:
#             data.update({
#                 "residential_limit": residential_limit,
#                 "residential_used": residential_used,
#                 "residential_remaining": max(residential_limit - residential_used, 0),
#                 "commercial_limit": commercial_limit,
#                 "commercial_used": commercial_used,
#                 "commercial_remaining": max(commercial_limit - commercial_used, 0),
#             })

#         return Response(data)


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

        # ================= LIMIT CHECK BEFORE SAVE =================
        total_limit, _, _ = agent.get_plan_limits()
        total_used = AgentProperty.objects.filter(agent=agent).count()

        if total_used >= total_limit:
            create_notification(
                agent,
                "Listing Limit Reached",
                "You have reached your property listing limit.",
                "usage"
            )

            return Response({
                "status": False,
                "message": "Property limit reached. Please upgrade your plan."
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

        property_obj = serializer.save()

        # ================= IMAGES =================
        images = request.FILES.getlist("images")
        for img in images:
            AgentPropertyImage.objects.create(property=property_obj, image=img)

        # ================= MAIN IMAGE =================
        if not property_obj.image and property_obj.images.exists():
            property_obj.image = property_obj.images.first().image
            property_obj.save()

        # ================= AFTER SAVE LIMIT CHECK =================
        total_used = AgentProperty.objects.filter(agent=agent).count()
        remaining = total_limit - total_used

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

# class PublicPropertyListAPIView(APIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     def get(self, request):
#         properties = AgentProperty.objects.all()

#         print("COUNT:", properties.count())  # debug

#         return Response(
#             AgentPropertySerializer(properties, many=True, context={'request': request}).data
#         )

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


# class PublicPropertyDetailAPIView(APIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     def get(self, request, id):
#         try:
#             property_obj = AgentProperty.objects.select_related(
#                 "category", "subcategory", "purpose"
#             ).prefetch_related(
#                 "amenities", "images", "selling_points", "landmarks", "field_values"
#             ).get(id=id)

#         except AgentProperty.DoesNotExist:
#             return Response({"error": "Property not found"}, status=404)

#         serializer = AgentPropertySerializer(
#             property_obj,
#             context={'request': request}
#         )

#         return Response({
#             "status": True,
#             "data": serializer.data
#         })

# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response

# from .models import AgentProperty
# from .serializers import AgentPropertySerializer
# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response

# from .models import AgentProperty
# from .serializers import AgentPropertySerializer


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

        # def get_object(self, request, id):
        #     try:
        #         return AgentProperty.objects.get(id=id, agent=request.user)
        #     except AgentProperty.DoesNotExist:
        #         return None

        def get_object(self, request, id):
            try:
                return AgentProperty.objects.get(uuid=id, agent=request.user)
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
        total_limit, residential_limit, commercial_limit = user.get_plan_limits()

        remaining_listings = max(total_limit - total_properties, 0)

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

# class PropertyListAPI(generics.ListAPIView):
#     serializer_class = PropertyCardSerializer
#     permission_classes = [AllowAny]

#     authentication_classes = []

#     def get_queryset(self):
#         queryset = (
#             Property.objects
#             .select_related("owner")
#             .prefetch_related("images")
#             .order_by("-created_at")
#         )
#         category = self.request.query_params.get("category")
#         purpose = self.request.query_params.get("purpose")

#         if category:
#             queryset = queryset.filter(category__name__iexact=category)

#         if purpose:
#             queryset = queryset.filter(purpose__name__iexact=purpose)

#         return queryset

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         request = self.request

#         wishlist_ids = set()
#         auth_header = request.headers.get("Authorization")

#         if auth_header:
#             parts = auth_header.strip().split()

#             # ✅ Robust Bearer parsing
#             if len(parts) == 2 and parts[0].lower() == "bearer":
#                 token = parts[1].strip()

#                 try:
#                     decoded = jwt.decode(
#                         token,
#                         settings.SECRET_KEY,
#                         algorithms=["HS256"]
#                     )

#                     # ✅ Handle multiple possible payload keys
#                     user_id = decoded.get("user_id") or decoded.get("id")

#                     if user_id:
#                         wishlist_ids = set(
#                             Wishlist.objects.filter(user_id=user_id)
#                             .values_list("property_id", flat=True)
#                         )

#                 # ✅ Explicit error handling (no silent failures)
#                 except ExpiredSignatureError:
#                     print("❌ Token expired")

#                 except InvalidTokenError:
#                     print("❌ Invalid token")

#                 except Exception as e:
#                     print("❌ JWT error:", str(e))

#         context["wishlist_ids"] = wishlist_ids
#         return context



# from rest_framework import generics
# from rest_framework.permissions import AllowAny
# import jwt
# from django.conf import settings
# from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# class PropertyListAPI(generics.ListAPIView):
#     serializer_class = PropertyCardSerializer
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     def get_queryset(self):
#         queryset = (
#             Property.objects
#             .select_related("owner", "category", "purpose")
#             .prefetch_related("images")
#             .order_by("-created_at")
#         )

        

#         # ✅ GET PARAMS
#         category = self.request.query_params.get("category")
#         purpose = self.request.query_params.get("purpose")


#         # ✅ CLEAN INPUT
#         if category:
#             category = category.strip()
#         if purpose:
#             purpose = purpose.strip()

#         # ✅ HANDLE "all"
#         if category and category.lower() == "all":
#             category = None
#         if purpose and purpose.lower() == "all":
#             purpose = None

#         # # 🔥 DEBUG: DB VALUES
#         # print("DB Categories:",
#         #       list(Property.objects.values_list("category__name", flat=True)))
#         # print("DB Purposes:",
#         #       list(Property.objects.values_list("purpose__name", flat=True)))

#         # ✅ APPLY FILTER
#         if category:
#             queryset = queryset.filter(
#                 category__name__icontains=category
#             )

#         if purpose:
#             queryset = queryset.filter(
#                 purpose__name__icontains=purpose
#             )
            
#         return queryset

#     # --------------------------------------------------
#     # ✅ WISHLIST CONTEXT
#     # --------------------------------------------------
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         request = self.request

#         wishlist_ids = set()
#         auth_header = request.headers.get("Authorization")

#         if auth_header:
#             parts = auth_header.strip().split()

#             if len(parts) == 2 and parts[0].lower() == "bearer":
#                 token = parts[1].strip()

#                 try:
#                     decoded = jwt.decode(
#                         token,
#                         settings.SECRET_KEY,
#                         algorithms=["HS256"]
#                     )

#                     user_id = decoded.get("user_id") or decoded.get("id")

#                     if user_id:
#                         wishlist_ids = set(
#                             Wishlist.objects.filter(user_id=user_id)
#                             .values_list("property_id", flat=True)
#                         )

#                 except ExpiredSignatureError:
#                     print("❌ Token expired")

#                 except InvalidTokenError:
#                     print("❌ Invalid token")

#                 except Exception as e:
#                     print("❌ JWT error:", str(e))

#         context["wishlist_ids"] = wishlist_ids
#         return context


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


# class WishlistView(APIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     #  Get user from JWT
#     def get_user_from_token(self, request):
#         auth_header = request.headers.get("Authorization")

#         if not auth_header:
#             return None, Response({"error": "Authorization header missing"}, status=401)

#         try:
#             token = auth_header.split(" ")[1]

#             decoded = jwt.decode(
#                 token,
#                 settings.SECRET_KEY,
#                 algorithms=["HS256"]
#             )

#             user_id = int(decoded.get("user_id"))
#             user = UserCreate.objects.get(id=user_id)

#             return user, None

#         except jwt.ExpiredSignatureError:
#             return None, Response({"error": "Token expired"}, status=401)
#         except jwt.InvalidTokenError:
#             return None, Response({"error": "Invalid token"}, status=401)
#         except UserCreate.DoesNotExist:
#             return None, Response({"detail": "User not found"}, status=404)
#         except Exception:
#             return None, Response({"error": "Something went wrong"}, status=400)

#     #  GET wishlist
#     def get(self, request):
#         user, error = self.get_user_from_token(request)
#         if error:
#             return error

#         wishlist = Wishlist.objects.filter(user=user)

#         #  Efficient query
#         properties = Property.objects.filter(
#             id__in=wishlist.values_list("property_id", flat=True)
#         ).select_related("owner").prefetch_related("images")

#         serializer = WishlistSerializer(
#             properties,
#             many=True,
#             context={"wishlist_ids": set(properties.values_list("id", flat=True))}
#         )

#         return Response(serializer.data)

#     # ➕ ADD to wishlist
#     def post(self, request):
#         user, error = self.get_user_from_token(request)
#         if error:
#             return error

#         masked_id = request.data.get("id")

#         if not masked_id:
#             return Response({"error": "property id is required"}, status=400)

#         #  Decode masked ID
#         decoded = hashids.decode(masked_id)

#         if not decoded:
#             return Response({"error": "Invalid property_id"}, status=400)

#         real_id = decoded[0]

#         try:
#             property_obj = Property.objects.get(id=real_id)
#         except Property.DoesNotExist:
#             return Response({"error": "Property not found"}, status=404)

#         wishlist, created = Wishlist.objects.get_or_create(
#             user=user,
#             property=property_obj
#         )

#         if not created:
#             return Response({"message": "Already in wishlist"})

#         return Response({"message": "Added to wishlist"})

#     # ❌ REMOVE from wishlist
#     def delete(self, request):
#         user, error = self.get_user_from_token(request)
#         if error:
#             return error

#         masked_id = request.data.get("property_id")

#         if not masked_id:
#             return Response({"error": "property_id is required"}, status=400)

#         # 🔓 Decode masked ID
#         decoded = hashids.decode(masked_id)

#         if not decoded:
#             return Response({"error": "Invalid property_id"}, status=400)

#         real_id = decoded[0]

#         try:
#             wishlist = Wishlist.objects.get(user=user, property_id=real_id)
#             wishlist.delete()
#             return Response({"message": "Removed from wishlist"})
#         except Wishlist.DoesNotExist:
#             return Response({"error": "Not in wishlist"}, status=404)


import jwt
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from jwt import ExpiredSignatureError, InvalidTokenError



class WishlistView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    # -----------------------------
    # AUTH
    # -----------------------------
    def get_user_from_token(self, request):
        auth = request.headers.get("Authorization")

        if not auth:
            return None, Response({"error": "Authorization header missing"}, status=401)

        try:
            token = auth.split()[1]

            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            user = UserCreate.objects.get(id=decoded.get("user_id"))

            return user, None

        except Exception:
            return None, Response({"error": "Invalid token"}, status=401)

    # -----------------------------
    # GET WISHLIST
    # -----------------------------
    def get(self, request):
        user, error = self.get_user_from_token(request)
        if error:
            return error

        wishlist = Wishlist.objects.filter(user=user)

        serializer = WishlistSerializer(wishlist, many=True)

        return Response(serializer.data)

    # -----------------------------
    # ADD TO WISHLIST
    # -----------------------------
    def post(self, request):
        user, error = self.get_user_from_token(request)
        if error:
            return error

        property_id = request.data.get("id")

        if not property_id:
            return Response({"error": "id required"}, status=400)

        # validate existence in both models
        exists = (
            Property.objects.filter(uuid=property_id).exists()
            or AgentProperty.objects.filter(uuid=property_id).exists()
        )

        if not exists:
            return Response({"error": "Property not found"}, status=404)

        obj, created = Wishlist.objects.get_or_create(
            user=user,
            property_uuid=property_id
        )

        if not created:
            return Response({"message": "Already in wishlist"})

        return Response({"message": "Added to wishlist"})

    # -----------------------------
    # REMOVE FROM WISHLIST
    # -----------------------------
    def delete(self, request):
        user, error = self.get_user_from_token(request)
        if error:
            return error

        property_id = request.data.get("property_id")

        if not property_id:
            return Response({"error": "id required"}, status=400)

        deleted, _ = Wishlist.objects.filter(
            user=user,
            property_uuid=property_id
        ).delete()

        if deleted:
            return Response({"message": "Removed from wishlist"})

        return Response({"error": "Not in wishlist"}, status=404)



from rest_framework import generics
from rest_framework.exceptions import NotFound

from .models import Property
from .serializers import PropertyDetailSerializer
from .utils import hashids


# class PropertyDetailAPIView(generics.RetrieveAPIView):
#     """
#     Retrieve property using HASHED ID
#     """

#     serializer_class = PropertyDetailSerializer

#     authentication_classes = [UserJWTAuthentication]
#     permission_classes = [IsAuthenticated]


#     #  OPTIMIZED QUERY
#     queryset = (
#         Property.objects
#         .select_related(
#             "owner",
#             "purpose",
#             "category",
#             # "subcategory",
#         )
#         .prefetch_related(
#             "amenities",
#             "images",                 # ✅ multiple property images
#             # "subcategory__fields",    # ✅ subcategory icons
#         )
#     )

#     def get(self, request, pk):

#         try:
#             property_obj = Property.objects.get(id=pk)

#             # ✅ TRACK VIEW HERE (no separate API)
#             PropertyView.objects.get_or_create(
#                 user=request.user,
#                 property=property_obj
#             )

#             serializer = PropertyCardSerializer(property_obj)

#             return Response(serializer.data)

#         except Property.DoesNotExist:
#             return Response({"error": "Not found"}, status=404)

#     def initial(self, request, *args, **kwargs):
#         try:
#             super().initial(request, *args, **kwargs)
#         except AuthenticationFailed as e:
#             # keeps "User not found" if already raised
#             raise e
#         except Exception:
#             raise AuthenticationFailed(
#                 {"detail": "User needs to login"}
#             )


#     # --------------------------------------------------
#     # HASHED ID LOOKUP
#     # --------------------------------------------------
#     def get_object(self):

#         hash_id = self.kwargs.get("hash_id")

#         if not hash_id:
#             raise NotFound("Property id not provided")

#         decoded = hashids.decode(hash_id)

#         if not decoded:
#             raise NotFound("Invalid property id")

#         real_id = decoded[0]

#         try:
#             return self.get_queryset().get(id=real_id)
#         except Property.DoesNotExist:
#             raise NotFound("Property not found")

#     # --------------------------------------------------
#     # PASS REQUEST TO SERIALIZER
#     # --------------------------------------------------
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["request"] = self.request
#         return context


# class PropertyDetailAPIView(generics.RetrieveAPIView):
    
#     serializer_class = PropertyDetailSerializer
#     authentication_classes = [UserJWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     queryset = (
#         Property.objects
#         .select_related("owner", "purpose", "category")
#         .prefetch_related("amenities", "images")
#     )

#     def get_object(self):

#         hash_id = self.kwargs.get("hash_id")

#         if not hash_id:
#             raise NotFound("Property id not provided")

#         decoded = hashids.decode(hash_id)

#         if not decoded:
#             raise NotFound("Invalid property id")

#         real_id = decoded[0]

#         try:
#             property_obj = self.get_queryset().get(id=real_id)

#             # ✅ TRACK VIEW HERE
#             PropertyView.objects.get_or_create(
#                 user=self.request.user,
#                 property=property_obj
#             )

#             return property_obj

#         except Property.DoesNotExist:
#             raise NotFound("Property not found")

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["request"] = self.request
#         return context

    # def initial(self, request, *args, **kwargs):
    #     try:
    #         super().initial(request, *args, **kwargs)
    #     except AuthenticationFailed as e:
    #         raise e
    #     except Exception:
    #         raise AuthenticationFailed(
    #             {"detail": "User needs to login"}
    #         )


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
    
    

# class PropertyEnquiryCreateView(generics.CreateAPIView):
#     queryset = PropertyEnquiry.objects.all()
#     serializer_class = PropertyEnquirySerializer

#     authentication_classes = [UserJWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     # --------------------------------------------------
#     # CUSTOM CREATE RESPONSE
#     # --------------------------------------------------
#     def create(self, request, *args, **kwargs):

#         # ✅ Check authenticated user
#         user = request.user

#         if not user or not user.is_authenticated:
#             return Response(
#                 {"message": "User needs to login"},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )

#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save(user=request.user)
#             serializer.save(user=request.user)

#             return Response(
#                 {
#                     "message": "Enquiry submitted successfully",
#                     "data": serializer.data
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         # ✅ catches "User not found" from your authentication.py
#         except AuthenticationFailed as e:
#             return Response(
#                 {
#                     "detail": str(e),
#                     "code": "user_not_found"
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED
#             )

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

# from .serializers import RelatedPropertySerializer

# class RelatedPropertiesAPIView(APIView):

#     authentication_classes = [UserJWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self,request,hash_id):
        
#         #decode hashed_id
#         property_id = decode_id(hash_id)

#         if not property_id:
#             return Response(
#                 {"error":"Invalid property id"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         if isinstance(property_id, (list, tuple)):
#             property_id = property_id[0]

#         try:
#             property_obj = Property.objects.select_related(
#                 "category","purpose"
#             ).get(id=property_id)

#         except Property.DoesNotExist:
#             return Response(
#                 {"error":"Property not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         related_properties = (
#             Property.objects.filter(
#                 category=property_obj.category,
#                 purpose=property_obj.purpose,
#                 expiry_date__gte=property_obj.created_at
#             )
#             .exclude(id=property_obj.id)
#             .select_related("owner")
#             .prefetch_related("images")
#             .order_by("-created_at")[:10]
#         )

#         serializer = RelatedPropertySerializer(
#             related_properties,
#             many=True,
#             context={"request":request}
#         )

#         return Response(serializer.data)

# from django.utils import timezone

# class RelatedPropertiesAPIView(APIView):

#     authentication_classes = [UserJWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, hash_id):

#         # decode hashed_id
#         property_id = decode_id(hash_id)

#         if not property_id:
#             return Response(
#                 {"error": "Invalid property id"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if isinstance(property_id, (list, tuple)):
#             property_id = property_id[0]

#         try:
#             property_obj = Property.objects.select_related(
#                 "category", "purpose"
#             ).get(id=property_id)

#         except Property.DoesNotExist:
#             return Response(
#                 {"error": "Property not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         # ✅ FIXED FILTER
#         related_properties = (
#             Property.objects.filter(
#                 category=property_obj.category,
#                 purpose=property_obj.purpose,
#                 expiry_date__gte=timezone.now()   # ✅ FIX HERE
#             )
#             .exclude(id=property_obj.id)
#             .select_related("owner")
#             .prefetch_related("images")
#             .order_by("-created_at")[:10]
#         )

#         serializer = RelatedPropertySerializer(
#             related_properties,
#             many=True,
#             context={"request": request}
#         )

#         return Response(serializer.data)

from itertools import chain
from uuid import UUID

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import CombinedPropertyListSerializer


class RelatedPropertiesAPIView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]


    def get(self, request, uuid_id):

        # ----------------------------
        # VALIDATE UUID
        # ----------------------------
        try:
            uuid_obj = UUID(
                str(uuid_id)
            )

        except ValueError:
            return Response(
                {
                    "error":"Invalid UUID"
                },
                status=400
            )


        current_property = None


        # ---------------------------------
        # TRY USER PROPERTY
        # ---------------------------------
        obj = Property.objects.select_related(
            "category",
            "purpose"
        ).filter(
            uuid=uuid_obj
        ).first()


        if obj:
            current_property = obj


        # ---------------------------------
        # TRY AGENT PROPERTY
        # ---------------------------------
        if not current_property:

            obj = AgentProperty.objects.select_related(
                "category",
                "purpose"
            ).filter(
                uuid=uuid_obj
            ).first()


            if obj:
                current_property = obj


        if not current_property:
            return Response(
                {
                    "error":"Property not found"
                },
                status=404
            )


        # ---------------------------------
        # USER RELATED
        # ---------------------------------
        user_related = Property.objects.filter(
            category=current_property.category,
            purpose=current_property.purpose
        ).exclude(
            uuid=current_property.uuid
        ).select_related(
            "owner"
        ).prefetch_related(
            "images"
        ).filter(
            expiry_date__gte=timezone.now()
        )


        # ---------------------------------
        # AGENT RELATED
        # ---------------------------------
        agent_related = AgentProperty.objects.filter(
            category=current_property.category,
            purpose=current_property.purpose
        ).exclude(
            uuid=current_property.uuid
        ).select_related(
            "agent"
        )


        # ---------------------------------
        # COMBINE BOTH
        # ---------------------------------
        combined = list(
            chain(
                user_related,
                agent_related
            )
        )


        combined.sort(
            key=lambda x:x.created_at,
            reverse=True
        )


        combined = combined[:10]


        serializer = CombinedPropertyListSerializer(
            combined,
            many=True,
            context={
                "request":request,
                "wishlist_ids":set()
            }
        )


        return Response({
            "count":len(combined),
            "data":serializer.data
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

        purpose_name = request.query_params.get("purpose")

        wishlist_qs = Wishlist.objects.filter(user=user)

        if purpose_name and purpose_name.strip() and purpose_name.strip().lower() != "all":
            wishlist_qs = wishlist_qs.filter(
                property__purpose__name__iexact=purpose_name
            )

        properties = Property.objects.filter(
            id__in=wishlist_qs.values_list("property_id", flat=True)
        ).select_related(
            "owner",
            "purpose",
            "category"
        ).prefetch_related(
            "images"
        ).order_by("-created_at")

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
    


# class UserProfileUpdateView(APIView):

#     authentication_classes = []
#     permission_classes = []

#     def get_user_from_token(self, request):

#         auth_header = request.headers.get("Authorization")

#         if not auth_header:
#             return None, Response(
#                 {"error": "Authorization header missing"},
#                 status=401
#             )

#         try:
#             token = auth_header.split(" ")[1]

#             decoded = jwt.decode(
#                 token,
#                 settings.SECRET_KEY,
#                 algorithms=["HS256"]
#             )

#             user_id = decoded.get("user_id")

#             user = UserCreate.objects.get(id=user_id)

#             return user, None

#         except Exception:
#             return None, Response(
#                 {"error": "Invalid or expired token"},
#                 status=401
#             )

#     # UPDATE PROFILE
    
#     def put(self, request):

#         user, error = self.get_user_from_token(request)

#         if error:
#             return error

#         serializer = UserProfileUpdateSerializer(
#             data=request.data
#         )

#         if not serializer.is_valid():
#             return Response(serializer.errors, status=400)

#         serializer.update(user, serializer.validated_data)

#         return Response(
#             {"message": "Profile updated successfully"},
#             status=200
#         )


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
        enquiries_count = PropertyEnquiry.objects.filter(
            user=user
        ).count()

        # ✅ MATCH UserAdd USING EMAIL (NO RELATION NEEDED)
        user_add = UserCreate.objects.filter(
            email=user.email
        ).first()

        # ✅ Properties listed
        properties_listed_count = Property.objects.filter(
            owner=user_add
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



# class UpdateAgentReviewAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_user_safely(self, request):
        
#         try:
#             return UserCreate.objects.get(id=request.user.id)
#         except:
#             pass

#         auth_header = request.headers.get("Authorization")

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
#             return UserCreate.objects.filter(id=user_id).first()

#         except:
#             return None

#     def put(self, request, review_id):

#         user = self.get_user_safely(request)

#         if not user:
#             return Response({"error": "User not found"}, status=401)

#         try:
#             review = AgentReview.objects.get(id=review_id)
#         except AgentReview.DoesNotExist:
#             return Response({"error": "Review not found"}, status=404)

#         if review.user != user:
#             return Response(
#                 {"error": "You can edit only your own review"},
#                 status=403
#             )

#         rating = request.data.get("rating")
#         review_text = request.data.get("review")

#         if rating is not None:
#             review.rating = rating

#         if review_text:
#             review.review = review_text

#         review.save()

#         return Response({
#             "message": "Review updated successfully",
#             "data": {
#                 "id": str(review.id),
#                 "rating": review.rating,
#                 "review": review.review
#             }
#         }, status=200)

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



# class DeleteAgentReviewAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_user_safely(self, request):
       
#         try:
#             return UserCreate.objects.get(id=request.user.id)
#         except:
#             pass

#         auth_header = request.headers.get("Authorization")

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
#             return UserCreate.objects.filter(id=user_id).first()

#         except:
#             return None

#     def delete(self, request, review_id):

#         # Get logged-in user
#         user = self.get_user_safely(request)

#         if not user:
#             return Response({"error": "User not found"}, status=401)

#         #  Get review
#         try:
#             review = AgentReview.objects.get(id=review_id)
#         except AgentReview.DoesNotExist:
#             return Response({"error": "Review not found"}, status=404)

#         # Check ownership
#         if review.user != user:
#             return Response(
#                 {"error": "You can delete only your own review"},
#                 status=403
#             )

#         #  Delete
#         review.delete()

#         return Response({
#             "message": "Review deleted successfully"
#         }, status=200)


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
    serializer_class = SliderBannerSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        return SliderBannerAd.objects.filter(is_active=True).order_by('-created_at')


class BannerAdsAPIView(ListAPIView):
    serializer_class = HeroImageSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        return HeroImage.objects.filter(is_active=True).order_by('-created_at')



# class AgentDetailAPIView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     def get(self, request, identifier):

#         try:
           
#             agent = AgentUserProfile.objects.get(agent_id=identifier)

#         except AgentUserProfile.DoesNotExist:
#             return Response({
#                 "status": False,
#                 "message": "Agent not found"
#             }, status=404)

#         serializer = AgentSerializer(agent)

#         return Response({
#             "status": True,
#             "data": serializer.data
#         })



# class AgentDetailAPIView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     def get(self, request, agent_id):

#         agent = None

#         try:
#             uuid_obj = uuid.UUID(agent_id)
#             agent = AgentUserProfile.objects.filter(id=uuid_obj).first()
#         except ValueError:
#             pass

#         if not agent:
#             agent = AgentUserProfile.objects.filter(agent_code=agent_id).first()

#         if not agent:
#             return Response({"error": "Agent not found"}, status=404)

#         agent_data = AgentDetailSerializer(agent).data

#         queryset = AgentProperty.objects.filter(agent=agent)

#         # CATEGORY FILTER
#         category = request.GET.get("category")
#         if category:
#             queryset = queryset.filter(category__name__icontains=category)

#         queryset = queryset.distinct()

#         total_properties = queryset.count()

#         properties_data = []

#         if agent.agent_type in ["premium", "elite"]:
#             queryset = queryset.order_by("-created_at")

#             properties_data = PremiumElitePropertySerializer(
#                 queryset,
#                 many=True,
#                 context={"request": request}
#             ).data

#         agent_data["properties_count"] = total_properties
#         agent_data["properties"] = properties_data

#         return Response(agent_data, status=200)

class AgentDetailAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, agent_id):

        agent = None

        # ================= UUID CHECK =================
        try:
            uuid_obj = uuid.UUID(agent_id)
            agent = AgentUserProfile.objects.filter(id=uuid_obj).first()
        except ValueError:
            pass

        # ================= AGENT CODE CHECK =================
        if not agent:
            agent = AgentUserProfile.objects.filter(agent_code=agent_id).first()

        # ================= NOT FOUND =================
        if not agent:
            return Response({"error": "Agent not found"}, status=404)

        # ================= AGENT DATA =================
        agent_data = AgentDetailSerializer(agent).data

        # ================= PROPERTY QUERY =================
        queryset = AgentProperty.objects.filter(agent=agent)

        # ================= FILTER =================
        category = request.GET.get("category")
        if category:
            queryset = queryset.filter(category__name__icontains=category)

        search = request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(label__icontains=search) |
                Q(price__icontains=search) |
                Q(city__icontains=search)
            )


        queryset = queryset.distinct()

        total_properties = queryset.count()

        # ================= PROPERTY SERIALIZER =================
        properties_data = []

        if agent.agent_type in ["premium", "elite"]:
            queryset = queryset.order_by("-created_at")

            properties_data = AgentPropertySerializer(
                queryset,
                many=True,
                context={"request": request}
            ).data

        # ================= RESPONSE =================
        agent_data["properties_count"] = total_properties
        agent_data["properties"] = properties_data

        return Response(agent_data, status=200)



# class PropertyFilterAPIView(APIView):

#     authentication_classes = [UserJWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         user = request.user
#         if not user or not user.is_authenticated:
#             return Response(
#                 {"error": "Authentication failed"},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )

        
#         queryset = Property.objects.all().order_by("-created_at")

#         purpose = request.GET.get("purpose")
#         category = request.GET.get("category")
#         city = request.GET.get("city")
#         district = request.GET.get("district")
#         min_price = request.GET.get("min_price")
#         max_price = request.GET.get("max_price")

        
#         if purpose and purpose.lower() != "all":
#             queryset = queryset.filter(purpose__name__icontains=purpose)

#         if category and category.lower() != "all":
#             queryset = queryset.filter(category__name__icontains=category)

#         if city and city.lower() != "all":
#             queryset = queryset.filter(city__icontains=city)

#         if district and district.lower() != "all":
#             queryset = queryset.filter(district__icontains=district)

   
#         if min_price or max_price:
#             queryset = queryset.annotate(price_int=Cast("price", IntegerField()))

#             if min_price:
#                 try:
#                     queryset = queryset.filter(price_int__gte=int(min_price))
#                 except:
#                     pass

#             if max_price:
#                 try:
#                     queryset = queryset.filter(price_int__lte=int(max_price))
#                 except:
#                     pass

#         serializer = PropertyCardSerializer(queryset, many=True)

#         return Response({
#             "count": queryset.count(),
#             "data": serializer.data
#         }, status=status.HTTP_200_OK)


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



# class PropertyEnquiryListAPIView(APIView):

#     authentication_classes = [UserJWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         user = request.user

#         # 🔥 Get enquiries for properties owned by this user
#         enquiries = PropertyEnquiry.objects.filter(
#             property__owner=user
#         ).select_related("user", "property").order_by("-created_at")

#         serializer = PropertyEnquirySerializer(enquiries, many=True)

#         return Response({
#             "count": enquiries.count(),
#             "data": serializer.data
#         }, status=status.HTTP_200_OK)




# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from django.db.models import Q

# from .models import Property
# from .serializers import PropertyCardSerializer


# class PropertySearchAPIView(APIView):

#     authentication_classes = []
#     permission_classes = [AllowAny]

#     def get(self, request):

#         raw_input = request.query_params.get("label", "").strip().lower()

#         queryset = Property.objects.all().order_by("-created_at")

#         price_prefix = None
#         text_parts = []

#         if raw_input:
#             for part in raw_input.split():

#                 if part.isdigit():
#                     price_prefix = part
#                 else:
#                     text_parts.append(part)

#         search_text = " ".join(text_parts)

#         if search_text:
#             queryset = queryset.filter(
#                 Q(label__icontains=search_text) |
#                 Q(city__icontains=search_text) |
#                 Q(district__icontains=search_text)
#             )

#         if price_prefix:
#             queryset = queryset.filter(
#                 price__startswith=price_prefix
#             )

#         queryset = queryset.distinct()

#         serializer = PropertyCardSerializer(
#             queryset,
#             many=True,
#             context={"wishlist_ids": set()}
#         )

#         return Response({
#             "count": queryset.count(),
#             "data": serializer.data
#         }, status=200)

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
            "owner",
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
    

# from django.db.models import Q, IntegerField
# from django.db.models.functions import Cast
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny

# class PropertyListAPIView(APIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     def get(self, request):

#         queryset = Property.objects.all()

#         # =========================
#         # CATEGORY FILTER
#         # =========================
#         category = request.GET.get("category")
#         if category:
#             queryset = queryset.filter(
#                 category__name__icontains=category
#             )

#         # =========================
#         # PURPOSE FILTER
#         # =========================
#         purpose = request.GET.get("purpose")
#         if purpose:
#             queryset = queryset.filter(
#                 purpose__name__icontains=purpose
#             )

#         # =========================
#         # CITY FILTER
#         # =========================
#         city = request.GET.get("city")
#         if city:
#             queryset = queryset.filter(
#                 city__icontains=city
#             )

#         # =========================
#         # SEARCH FILTER
#         # =========================
#         # search = request.GET.get("search")
#         # if search:
#         #     queryset = queryset.filter(
#         #         Q(label__icontains=search) |
#         #         Q(city__icontains=search) |
#         #         Q(price__icontains=search)
#         #     )

#         # =========================
#         # PRICE RANGE (FIXED PROPERLY)
#         # =========================

#         queryset = queryset.annotate(
#             price_int=Cast("price", IntegerField())
#         )

#         price_range = request.GET.get("price_range")

#         if price_range:

#             if price_range == "below_5":
#                 queryset = queryset.filter(price_int__lte=500000)

#             elif price_range == "5_10":
#                 queryset = queryset.filter(
#                     price_int__gte=500000,
#                     price_int__lte=1000000
#                 )

#             elif price_range == "10_25":
#                 queryset = queryset.filter(
#                     price_int__gte=1000000,
#                     price_int__lte=2500000
#                 )

#             elif price_range == "25_50":
#                 queryset = queryset.filter(
#                     price_int__gte=2500000,
#                     price_int__lte=5000000
#                 )

#             elif price_range == "above_50":
#                 queryset = queryset.filter(
#                     price_int__gte=5000000
#                 )

#         # =========================
#         # FINAL OUTPUT
#         # =========================
#         queryset = queryset.distinct().order_by("-created_at")

#         return Response({
#             "status": True,
#             "count": queryset.count(),
#             "data": PropertyDetailSerializer(
#                 queryset,
#                 many=True,
#                 context={"request": request}
#             ).data
#         })


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



# from django.db.models import Q, Avg
# from rest_framework.generics import ListAPIView
# from rest_framework.permissions import AllowAny

# from .models import AgentUserProfile
# from .serializers import AgentListFrontendSerializer


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

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status

# from .models import PropertyEnquiry
# from .serializers import EnquiryDetailSerializer


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
    

# class PropertyFilterOptionsAPIView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     def get(self, request):

#         categories = list(
#             Category.objects.values("name").order_by("name")
#         )

#         purposes = list(
#             Purpose.objects.values("name").order_by("name")
#         )

#         cities = list(
#             Property.objects.values_list("city", flat=True)
#             .exclude(city__isnull=True)
#             .exclude(city__exact="")
#             .distinct()
#         )

#         districts = list(
#             Property.objects.values_list("district", flat=True)
#             .exclude(district__isnull=True)
#             .exclude(district__exact="")
#             .distinct()
#         )

#         # ✅ PRICE RANGES (STATIC - YOU CONTROL THIS)
#         # price_ranges = [
#         #     {"key": "below_5", "label": "Below ₹5 Lakhs"},
#         #     {"key": "5_10", "label": "₹5 – 10 Lakhs"},
#         #     {"key": "10_25", "label": "₹10 – 25 Lakhs"},
#         #     {"key": "25_50", "label": "₹25 – 50 Lakhs"},
#         #     {"key": "above_50", "label": "Above ₹50 Lakhs"},
#         # ]

#         return Response({
#             # "status": True,
#             "data": {
#                 "categories": categories,
#                 "purposes": purposes,
#                 "cities": cities,
#                 "districts": districts,
#                 # "price_ranges": price_ranges
#             }
#         })


# from collections import defaultdict

# class PropertyFilterOptionsAPIView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     def get(self, request):

#         # -------------------------
#         # CATEGORY & PURPOSE
#         # -------------------------
#         categories = list(
#             Category.objects.values("name").order_by("name")
#         )

#         purposes = list(
#             Purpose.objects.values("name").order_by("name")
#         )

#         # -------------------------
#         # DISTRICT -> CITIES GROUPING
#         # -------------------------
#         district_map = defaultdict(set)

#         properties = Property.objects.values("district", "city")

#         for item in properties:
#             district = item.get("district")
#             city = item.get("city")

#             if not district or not city:
#                 continue

#             district_map[district].add(city)

#         # convert to required format
#         districts_data = []
#         for district, cities in district_map.items():
#             districts_data.append({
#                 "name": district,
#                 "cities": sorted(list(cities))
#             })

#         # optional: sort districts
#         districts_data = sorted(districts_data, key=lambda x: x["name"])

#         # -------------------------
#         # RESPONSE
#         # -------------------------
#         return Response({
#             # "data": {
#                 "categories": categories,
#                 "purposes": purposes,
#                 "districts": districts_data
#             # }
#         })

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


        # -------------------------
        # FORMAT DISTRICTS
        # -------------------------
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


        # -------------------------
        # RESPONSE
        # -------------------------
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

        enquiries = PropertyEnquiry.objects.select_related(
            "property", "property__owner"
        ).filter(
            user=user
        ).order_by("-created_at")[:10]

        serializer = RecentEnquirySerializer(enquiries, many=True)

        return Response({
            "count": enquiries.count(),
            "data": serializer.data
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
from django.conf import settings
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# from .models import (
#     Property,
#     AgentProperty,
#     Wishlist
# )

# from .serializers import (
#     PropertyCardSerializer,
#     AgentPropertySerializer
# )


from itertools import chain

# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response

# from django.db.models import Q

# import jwt
# from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
# # from django.conf import settings

# from .models import (
#     Property,
#     AgentProperty,
#     Wishlist
# )

# from .serializers import CombinedPropertyListSerializer


import jwt

from itertools import chain

from django.conf import settings
from django.db.models import Q

from jwt import (
    ExpiredSignatureError,
    InvalidTokenError
)

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class CombinedPropertyListAPIView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]


    def get(self, request):

        user_properties = Property.objects.select_related(
            "owner",
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


        # -----------------------------
        # COMBINE BOTH
        # -----------------------------
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


        # -----------------------------
        # USER WISHLIST
        # -----------------------------
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

                    # convert UUIDs -> strings
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


        return Response({
            "count": len(combined),
            "data": serializer.data
        })

from uuid import UUID
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import UserProfile


class UniversalPropertyDetailAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    # ✅ GET PROFILE IMAGE (USER + AGENT)
    def get_profile_image(self, person, request):
        if not person:
            return None

        # ===== USER PROFILE IMAGE =====
        try:
            profile = UserProfile.objects.filter(user=person).first()
            if profile:
                if profile.image:
                    try:
                        return request.build_absolute_uri(profile.image.url)
                    except:
                        return profile.image.url

                # fallback avatar from model
                return profile.profile_image_url
        except:
            pass

        # ===== AGENT PROFILE IMAGE =====
        if getattr(person, "profile_image", None):
            try:
                return request.build_absolute_uri(person.profile_image.url)
            except:
                return person.profile_image.url

        # ===== AGENT AVATAR =====
        if getattr(person, "avatar_url", None):
            return person.avatar_url

        return None

    # ✅ CLEAN OWNER NAME (NO UUID)
    def get_owner_name(self, person, fallback):
        if not person:
            return fallback or ""

        if hasattr(person, "name") and person.name:
            return person.name

        if hasattr(person, "username") and person.username:
            return person.username

        if hasattr(person, "email") and person.email:
            return person.email

        return fallback or ""

    def get(self, request, uuid_id):

        # ===== VALIDATE UUID =====
        try:
            uuid_obj = UUID(str(uuid_id))
        except ValueError:
            return Response({"error": "Invalid UUID format"}, status=400)

        # =====================================================
        # USER PROPERTY
        # =====================================================
        obj = Property.objects.filter(uuid=uuid_obj).first()

        if obj:
            serializer = PropertyDetailSerializer(obj, context={"request": request})
            data = serializer.data

            user_obj = obj.owner   # ✅ IMPORTANT FIX (NOT obj.user)

            return Response({
                "id": str(obj.uuid),
                "property_code": f"TA-L-{obj.id}",
                "label": data.get("label"),
                "images": data.get("images", []),
                "purpose": obj.purpose.name if obj.purpose else None,

                "category": {
                    "id": obj.category.id,
                    "name": obj.category.name,
                    "image": None
                },

                "description": obj.description,
                "city": obj.city,
                "state": obj.state,
                "location": obj.location,

                "land_mark": data.get("landmarks", []),

                "created_at": obj.created_at.strftime("%Y-%m-%d"),

                "property_features": data.get("features", []),

                "price_details": {
                    "price": obj.price,
                    "sq_ft": str(obj.sq_ft),
                    "land_area": obj.land_area,
                    "perprice": obj.perprice
                },

                # ✅ FINAL CORRECT OUTPUT
                "contact_details": {
                    "owner": self.get_owner_name(user_obj, ""),
                    "whatsapp": obj.whatsapp,
                    "phone": obj.phone,
                    "owner_profile_image": self.get_profile_image(user_obj, request)
                },

                "amenities": [
                    {
                        "name": a.name,
                        "icon": request.build_absolute_uri(a.icon.url)
                        if getattr(a, "icon", None) else None
                    }
                    for a in obj.amenities.all()
                ],

                "key_selling_points": data.get("selling_points", []),

                "location_details": {
                    "village": obj.village,
                    "city": obj.city,
                    "state": obj.state,
                    "pincode": obj.pincode
                }
            })

        # =====================================================
        # AGENT PROPERTY
        # =====================================================
        obj = AgentProperty.objects.filter(uuid=uuid_obj).first()

        if obj:
            serializer = AgentPropertySerializer(obj, context={"request": request})
            data = serializer.data

            agent_obj = obj.agent

            return Response({
                "id": str(obj.uuid),
                "property_code": f"AG-{obj.id}",
                "label": data.get("label"),
                "images": data.get("images", []),
                "purpose": obj.purpose.name if obj.purpose else None,

                "category": {
                    "id": obj.category.id,
                    "name": obj.category.name,
                    "image": None
                },

                "description": obj.description,
                "city": obj.city,
                "state": obj.state,
                "location": obj.location,

                "land_mark": data.get("landmarks", []),

                "created_at": obj.created_at.strftime("%Y-%m-%d"),

                "property_features": data.get("features", []),

                "price_details": {
                    "price": obj.price,
                    "sq_ft": str(obj.sq_ft),
                    "land_area": obj.land_area,
                    "perprice": obj.perprice
                },

                # ✅ FINAL CORRECT OUTPUT
                "contact_details": {
                    "owner": self.get_owner_name(agent_obj, obj.owner),
                    "whatsapp": obj.whatsapp,
                    "phone": obj.phone,
                    "owner_profile_image": self.get_profile_image(agent_obj, request)
                },

                "amenities": [
                    {
                        "name": a.name,
                        "icon": request.build_absolute_uri(a.icon.url)
                        if getattr(a, "icon", None) else None
                    }
                    for a in obj.amenities.all()
                ],

                "key_selling_points": data.get("selling_points", []),

                "location_details": {
                    "village": obj.village,
                    "city": obj.city,
                    "state": obj.state,
                    "pincode": obj.pincode
                }
            })

        return Response({"error": "Property not found"}, status=404)

# from uuid import UUID
# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response

# # from .models import Property, AgentProperty


# class UniversalPropertyDetailAPIView(APIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     def get(self, request, uuid_id):

#         # ============================
#         # VALIDATE UUID
#         # ============================
#         try:
#             uuid_obj = UUID(str(uuid_id))
#         except ValueError:
#             return Response(
#                 {"error": "Invalid UUID format"},
#                 status=400
#             )

#         # =====================================
#         # TRY USER PROPERTY FIRST
#         # =====================================
#         # obj = Property.objects.filter(uuid=uuid_obj).first()

#         # if obj:

#         #     serializer = PropertyDetailSerializer(
#         #         obj,
#         #         context={"request": request}
#         #     )

#         #     return Response(serializer.data)

#         # # =====================================
#         # # THEN TRY AGENT PROPERTY
#         # # =====================================
#         # obj = AgentProperty.objects.filter(uuid=uuid_obj).first()

#         # if obj:

#         #     serializer = AgentPropertySerializer(
#         #         obj,
#         #         context={"request": request}
#         #     )

#         #     profile_image = None

#         #     if obj.agent and getattr(obj.agent, "profile_image", None):
#         #         try:
#         #             profile_image = request.build_absolute_uri(obj.agent.profile_image.url)
#         #         except:
#         #             profile_image = obj.agent.profile_image.url
#         #     else:
#         #         # fallback avatar
#         #         name = getattr(obj.agent, "name", "AG")
#         #         initials = name[:2].upper() if name else "AG"

#         #         profile_image = (
#         #             f"https://ui-avatars.com/api/?name={initials}"
#         #             "&background=8bc83f"
#         #             "&color=ffffff"
#         #             "&size=256"
#         #             "&bold=true"
#         #         )

#             data = serializer.data

#             formatted = {
#                 "id": str(obj.uuid),
#                 "property_code": f"AG-{obj.id}",
#                 "label": data["label"],
#                 "images": data["images"],
#                 "purpose": obj.purpose.name if obj.purpose else None,

#                 "category": {
#                     "id": obj.category.id,
#                     "name": obj.category.name,
#                     "image": None
#                 },

#                 "description": obj.description,
#                 "city": obj.city,
#                 "state": obj.state,
#                 "location": obj.location,

#                 "land_mark": data.get("landmarks", []),

#                 "created_at": obj.created_at.strftime("%Y-%m-%d"),

#                 "property_features": data.get("features", []),

#                 "price_details": {
#                     "price": obj.price,
#                     "sq_ft": str(obj.sq_ft),
#                     "land_area": obj.land_area,
#                     "perprice": obj.perprice
#                 },

#                 "contact_details": {
#                     "owner": getattr(obj.agent, "name", obj.owner),
#                     "whatsapp": obj.whatsapp,
#                     "phone": obj.phone,
#                     "owner_profile_image": profile_image
#                 },

#                 # "owner_profile_image": (
#                 #     f"https://ui-avatars.com/api/?name="
#                 #     f"{(obj.agent.name[:2] if hasattr(obj.agent,'name') else 'AG').upper()}"
#                 #     "&background=8bc83f"
#                 #     "&color=ffffff"
#                 #     "&size=256"
#                 #     "&bold=true"
#                 # ),

#                 "amenities": [
#                     {
#                         "name": a.name,
#                         "icon": (
#                             request.build_absolute_uri(a.icon.url)
#                             if getattr(a, "icon", None)
#                             else None
#                         )
#                     }
#                     for a in obj.amenities.all()
#                 ],

#                 "key_selling_points": data.get("selling_points", []),

#                 "location_details": {
#                     "village": obj.village,
#                     "city": obj.city,
#                     "state": obj.state,
#                     "pincode": obj.pincode
#                 }
#             }

#             return Response(formatted)

#         return Response(
#             {"error": "Property not found"},
#             status=404
#         )

# from uuid import UUID
# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response


# class UniversalPropertyDetailAPIView(APIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     # ✅ COMMON PROFILE IMAGE HANDLER
#     def get_profile_image(self, person, request, default_prefix="US"):
#         if person and getattr(person, "profile_image", None):
#             try:
#                 return request.build_absolute_uri(person.profile_image.url)
#             except:
#                 return person.profile_image.url

#         name = getattr(person, "name", default_prefix)
#         initials = name[:2].upper() if name else default_prefix

#         return (
#             f"https://ui-avatars.com/api/?name={initials}"
#             "&background=8bc83f"
#             "&color=ffffff"
#             "&size=256"
#             "&bold=true"
#         )

#     def get(self, request, uuid_id):

#         # ============================
#         # VALIDATE UUID
#         # ============================
#         try:
#             uuid_obj = UUID(str(uuid_id))
#         except ValueError:
#             return Response({"error": "Invalid UUID format"}, status=400)

#         # =====================================
#         # USER PROPERTY
#         # =====================================
#         obj = Property.objects.filter(uuid=uuid_obj).first()

#         if obj:
#             serializer = PropertyDetailSerializer(
#                 obj,
#                 context={"request": request}
#             )
#             data = serializer.data

#             user_obj = getattr(obj, "user", None)
#             profile_image = self.get_profile_image(user_obj, request, "US")

#             formatted = {
#                 "id": str(obj.uuid),
#                 "property_code": f"TA-L-{obj.id}",
#                 "label": data.get("label"),
#                 "images": data.get("images", []),
#                 "purpose": obj.purpose.name if obj.purpose else None,

#                 "category": {
#                     "id": obj.category.id,
#                     "name": obj.category.name,
#                     "image": None
#                 },

#                 "description": obj.description,
#                 "city": obj.city,
#                 "state": obj.state,
#                 "location": obj.location,

#                 "land_mark": data.get("landmarks", []),

#                 "created_at": obj.created_at.strftime("%Y-%m-%d"),

#                 "property_features": data.get("features", []),

#                 "price_details": {
#                     "price": obj.price,
#                     "sq_ft": str(obj.sq_ft),
#                     "land_area": obj.land_area,
#                     "perprice": obj.perprice
#                 },

#                 # ✅ FIXED HERE
#                 "contact_details": {
#                     "owner": getattr(user_obj, "name", obj.owner),
#                     "whatsapp": obj.whatsapp,
#                     "phone": obj.phone,
#                     "owner_profile_image": profile_image
#                 },

#                 "amenities": [
#                     {
#                         "name": a.name,
#                         "icon": (
#                             request.build_absolute_uri(a.icon.url)
#                             if getattr(a, "icon", None)
#                             else None
#                         )
#                     }
#                     for a in obj.amenities.all()
#                 ],

#                 "key_selling_points": data.get("selling_points", []),

#                 "location_details": {
#                     "village": obj.village,
#                     "city": obj.city,
#                     "state": obj.state,
#                     "pincode": obj.pincode
#                 }
#             }

#             return Response(formatted)

#         # =====================================
#         # AGENT PROPERTY
#         # =====================================
#         obj = AgentProperty.objects.filter(uuid=uuid_obj).first()

#         if obj:
#             serializer = AgentPropertySerializer(
#                 obj,
#                 context={"request": request}
#             )
#             data = serializer.data

#             agent_obj = getattr(obj, "agent", None)
#             profile_image = self.get_profile_image(agent_obj, request, "AG")

#             formatted = {
#                 "id": str(obj.uuid),
#                 "property_code": f"AG-{obj.id}",
#                 "label": data.get("label"),
#                 "images": data.get("images", []),
#                 "purpose": obj.purpose.name if obj.purpose else None,

#                 "category": {
#                     "id": obj.category.id,
#                     "name": obj.category.name,
#                     "image": None
#                 },

#                 "description": obj.description,
#                 "city": obj.city,
#                 "state": obj.state,
#                 "location": obj.location,

#                 "land_mark": data.get("landmarks", []),

#                 "created_at": obj.created_at.strftime("%Y-%m-%d"),

#                 "property_features": data.get("features", []),

#                 "price_details": {
#                     "price": obj.price,
#                     "sq_ft": str(obj.sq_ft),
#                     "land_area": obj.land_area,
#                     "perprice": obj.perprice
#                 },

#                 # ✅ FIXED HERE ALSO
#                 "contact_details": {
#                     "owner": getattr(agent_obj, "name", obj.owner),
#                     "whatsapp": obj.whatsapp,
#                     "phone": obj.phone,
#                     "owner_profile_image": profile_image
#                 },

#                 "amenities": [
#                     {
#                         "name": a.name,
#                         "icon": (
#                             request.build_absolute_uri(a.icon.url)
#                             if getattr(a, "icon", None)
#                             else None
#                         )
#                     }
#                     for a in obj.amenities.all()
#                 ],

#                 "key_selling_points": data.get("selling_points", []),

#                 "location_details": {
#                     "village": obj.village,
#                     "city": obj.city,
#                     "state": obj.state,
#                     "pincode": obj.pincode
#                 }
#             }

#             return Response(formatted)

#         return Response({"error": "Property not found"}, status=404)





# class UniversalPropertyEnquiryAPI(APIView):

#     authentication_classes = [
#         UserJWTAuthentication
#     ]

#     permission_classes = [
#         IsAuthenticated
#     ]


#     def post(
#         self,
#         request,
#         uuid_id
#     ):

#         user = request.user


#         # --------------------------
#         # VALIDATE UUID
#         # --------------------------
#         try:
#             uuid_obj = UUID(
#                 str(uuid_id)
#             )

#         except ValueError:
#             return Response(
#                 {
#                     "error":"Invalid UUID"
#                 },
#                 status=400
#             )


#         # --------------------------
#         # USER PROPERTY
#         # --------------------------
#         prop = Property.objects.select_related(
#             "owner"
#         ).filter(
#             uuid=uuid_obj
#         ).first()


#         if prop:

#             serializer = PropertyEnquirySerializer(
#                 data=request.data
#             )

#             serializer.is_valid(
#                 raise_exception=True
#             )

#             serializer.save(
#                 user=user,
#                 property=prop,
#                 owner=prop.owner
#             )

#             return Response(
#                 {
#                     "status":True,
#                     "message":"Enquiry sent successfully",
#                     "property_type":"user",
#                     "data":serializer.data
#                 },
#                 status=201
#             )


#         # --------------------------
#         # AGENT PROPERTY
#         # --------------------------
#         agent_prop = AgentProperty.objects.filter(
#             uuid=uuid_obj
#         ).first()


#         if agent_prop:

#             serializer = AgentPropertyEnquirySerializer(
#                 data=request.data
#             )

#             serializer.is_valid(
#                 raise_exception=True
#             )

#             serializer.save(
#                 user=user,
#                 agent_property=agent_prop
#             )

#             return Response(
#                 {
#                     "status":True,
#                     "message":"Enquiry sent successfully",
#                     "property_type":"agent",
#                     "data":serializer.data
#                 },
#                 status=201
#             )


#         return Response(
#             {
#                 "error":"Property not found"
#             },
#             status=404
#         )


class UniversalPropertyEnquiryAPI(APIView):

    authentication_classes = [UserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user
        uuid_id = request.data.get("property")

        if not uuid_id:
            return Response(
                {"error": "property uuid is required"},
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
        prop = Property.objects.filter(uuid=uuid_obj).first()

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
        agent_prop = AgentProperty.objects.filter(uuid=uuid_obj).first()

        if agent_prop:
            serializer = AgentPropertyEnquirySerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=400)

            enquiry = serializer.save(
                user=user,
                property=agent_prop   # ✅ IMPORTANT FIX (matches model field name)
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

# models
# from .models import Property, AgentProperty, Wishlist
# from .serializers import CombinedPropertyListSerializer


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
            "owner",
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
            "owner",
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
                property__owner=user
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

            if not isinstance(user, UserCreate) or enquiry.property.owner != user:
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

