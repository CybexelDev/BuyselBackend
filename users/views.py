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
import tempfile
from selenium import webdriver
from urllib.parse import quote
from django.http import JsonResponse
from django.db.models import Q
from .utils import send_otp_email



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





def agents(request):
    # Get all agent profiles
    agent_profile = UserProfile.objects.all()

    # Set up pagination (10 profiles per page)
    paginator = Paginator(agent_profile, 10)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    # Ensure UUIDs are correctly formatted and pass the profile picture URL
    profile_list = [
        {
            "id": str(profile.id), 
            "login": profile.login,  # Assuming 'login' is the username
            "image_url": profile.profile_image.url if profile.profile_image else None,
            "address": profile.address if hasattr(profile, "address") else "No Address Available",
        } 
        for profile in page_obj
    ]

    # Pass to template
    context = {
        'profiles': profile_list,
        'page_obj': page_obj  
    }

    return render(request, 'agents.html', context)






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

# def index(request):
#     purposes = Purpose.objects.all()
#     categories = Category.objects.all()
#     premium = Premium.objects.all()
#     districts = Property.objects.values_list("district", flat=True).distinct()
#     cities = Property.objects.values_list("city", flat=True).distinct()
#
#     District = taluk = village = state = ""
#
#     # Base queryset
#     properties = Property.objects.all().order_by('-created_at')[:20]
#
#     # ------------------- SEARCH -------------------
#     query = request.GET.get("q", "").strip()
#     if query:
#         properties = Property.objects.filter(
#             Q(label__icontains=query) |
#             Q(description__icontains=query) |
#             Q(city__icontains=query) |
#             Q(district__icontains=query) |
#             Q(category__name__icontains=query) |
#             Q(purpose__name__icontains=query) |
#             Q(state__icontains=query) |
#             Q(city__icontains=query) |
#             Q(price__icontains=query) |
#             Q(location__icontains=query)
#         ).order_by('-created_at')
#
#     # ------------------- POST REQUESTS -------------------
#     if request.method == 'POST':
#         # --- Inbox form ---
#         if "messages_text" in request.POST:
#             name = request.POST.get("name", "").strip()
#             pin_code = request.POST.get("pin_code", "").strip()
#             contact = request.POST.get("contact", "").strip()
#             messages_text = request.POST.get("messages_text", "").strip()
#
#             link_pattern = re.compile(r"(https?:\/\/|www\.)", re.IGNORECASE)
#             if (link_pattern.search(name) or link_pattern.search(contact) or
#                 link_pattern.search(pin_code) or link_pattern.search(messages_text)):
#                 return JsonResponse({"success": False, "error": "Links are not allowed."}, status=400)
#
#             Inbox.objects.create(
#                 name=name,
#                 pin_code=pin_code,
#                 contact=contact,
#                 messages_text=messages_text
#             )
#             return redirect("index")
#
#         # --- Dealings form ---
#         elif "Dealings" in request.POST and "image" in request.FILES:
#             name = request.POST.get("name", "").strip()
#             email = request.POST.get("email", "").strip()
#             address = request.POST.get("address", "").strip()
#             phone_number = request.POST.get("phone_number", "").strip()
#             Dealings = request.POST.get("Dealings", "").strip()
#
#             url_pattern = re.compile(r"(https?:\/\/|www\.|\b\S+\.(com|net|org|in|info|io|gov|co)\b)", re.IGNORECASE)
#             for field_value, field_name in [(name, "Name"), (address, "Address"), (phone_number, "Phone")]:
#                 if url_pattern.search(field_value):
#                     return render(request, 'index.html', {
#                         "agent_error": f"Links are not allowed in {field_name}.",
#                         "show_agent_modal": True,
#                         "purposes": purposes,
#                         "properties": properties,
#                         "categories": categories,
#                         "premium": premium,
#                         "districts": districts,
#                         "cities": cities,
#                     })
#
#             AgentForm.objects.create(
#                 name=name,
#                 email=email,
#                 address=address,
#                 phone_number=phone_number,
#                 Dealings=Dealings,
#                 image=request.FILES.get("image")
#             )
#             return redirect("index")
#
#         # --- Property form ---
#         elif "about_the_property" in request.POST and "image" in request.FILES:
#             category_name = request.POST.get("categories", "").strip()
#             purpose_name = request.POST.get("purposes", "").strip()
#             label = request.POST.get("label", "").strip()
#             land_area = request.POST.get("land_area", "").strip()
#             sq_ft = request.POST.get("sq_ft", "").strip()
#             description = request.POST.get("about_the_property", "").strip()
#             amenities = request.POST.get("amenities", "").strip()
#             owner = request.POST.get("owner", "").strip()
#             phone = request.POST.get("phone", "").strip()
#             whatsapp = request.POST.get("whatsapp", "").strip()
#             location = request.POST.get("locations", "").strip()
#             city = request.POST.get("city", "").strip()
#             District = request.POST.get("District", "").strip()
#             taluk = request.POST.get("taluk", "").strip()
#             village = request.POST.get("village", "").strip()
#             state = request.POST.get("state", "").strip()
#             pin_code = request.POST.get("pin_code", "").strip()
#             land_mark = request.POST.get("land_mark", "").strip()
#             duration = request.POST.get("duration", "").strip()
#             price = request.POST.get("price", "").strip()
#             total_price = request.POST.get("total_price", "").strip()
#
#             # 🚫 Link validation
#             url_pattern = re.compile(r"(https?:\/\/|www\.|\b\S+\.(com|net|org|in|info|io|gov|co)\b)", re.IGNORECASE)
#             for field_value, field_name in [
#                 (label, "Label"), (description, "Description"), (amenities, "Amenities"),
#                 (owner, "Owner"), (phone, "Phone"), (whatsapp, "WhatsApp"), (land_mark, "Landmark")
#             ]:
#                 if url_pattern.search(field_value):
#                     return render(request, "index.html", {
#                         "property_error": f"Links are not allowed in {field_name}.",
#                         "show_property_modal": True,
#                         "purposes": purposes,
#                         "properties": properties,
#                         "categories": categories,
#                         "premium": premium,
#                         "District": District,
#                         "taluk": taluk,
#                         "village": village,
#                         "state": state,
#                         "cities": cities,
#                     })
#
#             Propertylist.objects.create(
#                 categories=category_name,
#                 purposes=purpose_name,
#                 label=label,
#                 land_area=land_area,
#                 description=description,
#                 sq_ft=sq_ft,
#                 amenities=amenities,
#                 owner=owner,
#                 locations=location,
#                 price=price,
#                 about_the_property=description,
#                 pin_code=pin_code,
#                 land_mark=land_mark,
#                 phone=phone,
#                 image=request.FILES.get("image"),
#                 total_price=total_price,
#                 duration=duration,
#                 whatsapp=whatsapp,
#                 city=city,
#                 District=District,
#                 taluk=taluk,
#                 village=village,
#                 state=state,
#             )
#             messages.success(request, "Property added successfully!")
#             return redirect("index")
#
#     # ------------------- GET REQUEST -------------------
#     return render(request, 'index.html', {
#         "purposes": purposes,
#         "properties": properties,
#         "categories": categories,
#         "premium": premium,
#         "District": District,
#         "taluk": taluk,
#         "village": village,
#         "state": state,
#         "districts": districts,
#         "cities": cities,
#         "search_query": query,  # Pass current search term to template
#     })




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
from rest_framework_simplejwt.tokens import RefreshToken
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

class PremiumLoginAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and Password required"},
                status=400
            )

        try:
            premium = Premium.objects.get(username=username)

        except Premium.DoesNotExist:
            return Response({"error": "Invalid Username"}, status=400)

        if not check_password(password, premium.password):
            return Response({"error": "Invalid Password"}, status=400)

        refresh = RefreshToken()
        refresh["premium_id"] = premium.id
        refresh["username"] = premium.username

        response = Response({

            "message": "Login Success",
            "access": str(refresh.access_token),

            "premium": {
                "id": premium.id,
                "name": premium.name,
                "city": premium.city,
                "image": premium.image.url if premium.image else None
            }

        })

        # Store refresh token in cookie
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60
        )

        return response


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


# views.py
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
                    "email" : email
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

                response = Response({
                    "message": "Email verified successfully",
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "mobile": user.mobile
                    }
                })

                response.set_cookie(
                    key="refresh_token",
                    value=str(refresh),
                    httponly=True,
                    secure=False,
                    samesite="Lax",
                    max_age=7 * 24 * 60 * 60
                )

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

                    # ⭐ THIS TOKEN USE IN HEADER
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

            response = Response({
                "message": "Login successful",
                "access": str(refresh.access_token),
                "user": {
                    "email": user.email,
                    "name": user.name
                }
            })

            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=7 * 24 * 60 * 60
            )

            return response

        except UserCreate.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)

User = get_user_model()


class GoogleLoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        token = request.data.get("token")

        if not token:
            return Response({"error": "Token is required"}, status=400)

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            email = idinfo["email"]
            name = idinfo.get("name", "")

            user, _ = UserCreate.objects.get_or_create(
                email=email,
                defaults={"name": name, "is_verified": True}
            )

            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={"auth_provider": "google"}
            )

            refresh = RefreshToken.for_user(user)

            response = Response({

                "message": "Login successful",
                "access": str(refresh.access_token),

                "user": {
                    "email": user.email,
                    "name": user.name,
                    "username": profile.username,
                    "auth_provider": profile.auth_provider
                }

            })

            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=7 * 24 * 60 * 60
            )

            return response

        except ValueError:
            return Response({"error": "Invalid token"}, status=400)

class GoogleLoginRedirectView(APIView):
    """
    Redirect-based Google login (Web OAuth2)
    """
    def get(self, request):
        redirect_uri = "http://127.0.0.1:8000/auth/google/callback/"

        google_auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={settings.GOOGLE_CLIENT_ID}"
            "&response_type=code"
            "&scope=openid email profile"
            f"&redirect_uri={redirect_uri}"
        )

        return redirect(google_auth_url)


class GoogleCallbackView(APIView):
    """
    Callback endpoint for OAuth2 web login
    """
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response({"error": "No code provided"}, status=400)

        redirect_uri = "http://127.0.0.1:8000/auth/google/callback/"
        token_url = "https://oauth2.googleapis.com/token"

        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        token_response = requests.post(token_url, data=data)
        token_json = token_response.json()

        id_token_value = token_json.get("id_token")
        if not id_token_value:
            return Response(token_json, status=400)

        # Verify Google ID token
        idinfo = id_token.verify_oauth2_token(
            id_token_value,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        email = idinfo["email"]
        name = idinfo.get("name", "")

        # ✅ Use your UserCreate model, not default User
        user, _ = UserCreate.objects.get_or_create(
            email=email,
            defaults={"name": name, "is_verified": True}
        )

        # ✅ Ensure UserProfile exists
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={"auth_provider": "google"}
        )

        if profile.auth_provider != "google":
            profile.auth_provider = "google"
            profile.save()

        # ✅ Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "email": user.email,
                "name": user.name,
                "username": profile.username,
                "auth_provider": profile.auth_provider
            }
        })

class FacebookLoginRedirectView(APIView):

    def get(self, request):
        redirect_uri = "http://127.0.0.1:8000/auth/facebook/callback/"

        facebook_auth_url = (
            "https://www.facebook.com/v19.0/dialog/oauth?"
            f"client_id={settings.FACEBOOK_APP_ID}"
            f"&redirect_uri={redirect_uri}"
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
            partial=False   # 🔥 FULL update
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

        # ✅ Properly delete old Cloudinary image
        if profile.image and profile.image.public_id:
            cloudinary.uploader.destroy(profile.image.public_id)

        # Save new image
        profile.image = request.FILES["image"]
        profile.save()

        return Response({
            "message": "Profile image updated successfully",
            "image_url": profile.image.url
        })


class RefreshTokenView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token missing"},
                status=401
            )

        try:
            refresh = RefreshToken(refresh_token)

            return Response({
                "access": str(refresh.access_token)
            })

        except Exception:
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






