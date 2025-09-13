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

def base(request):
    return render(request, 'base.html')


def base(request):
    return render(request, 'more.html')

def about(request):
    return render(request, 'about.html')



# def index(request):
#     try:
#         model1_objects = House.objects.prefetch_related(Prefetch('images', queryset=HouseImage.objects.all()))
#         model2_objects = list(Land.objects.filter(id__isnull=False))
#         model3_objects = list(Commercial.objects.all()[:2])
#         model4_objects = list(OffPlan.objects.all()[:2])
#         model5_objects = AgentHouse.objects.prefetch_related(Prefetch('images', queryset=AgentHouseImage.objects.all()))[:2]
#         model6_objects = AgentLand.objects.prefetch_related(Prefetch('images', queryset=AgentLandImage.objects.all()))[:2]
#         model7_objects = AgentOffPlan.objects.prefetch_related(Prefetch('images', queryset=AgentOffPlanImage.objects.all()))[:2]
#         model8_objects = AgentCommercial.objects.prefetch_related(Prefetch('images', queryset=AgentCommercialImage.objects.all()))[:2]

#         msgs = list(Inbox.objects.all().order_by('-id')[:15])
    
#         # Debugging output
#         for obj in model1_objects:
#             print(f"Model1 Object ID: {obj.id} (Type: {type(obj.id)})")
    
#     except Exception as e:
#         print(f"Error fetching objects: {e}")
#         model1_objects = model2_objects = model3_objects = model4_objects = []
#         model5_objects = model6_objects = model7_objects = model8_objects = []
#         msgs = []

#     if request.method == 'POST':
#         name = request.POST.get("name")
#         contact = request.POST.get("contact")
#         pin_code = request.POST.get("pin_code")
#         messages = request.POST.get("messages")

#         if name and contact and messages:
#             msg = Inbox(name=name, contact=contact, pin_code=pin_code, messages_text=messages)
#             msg.save()

    

#     return render(request, 'index.html', {
#         'model1_objects': model1_objects,
#         'model2_objects': model2_objects,
#         'model3_objects': model3_objects,
#         'model4_objects': model4_objects, 
#         'model5_objects': model5_objects,
#         'model6_objects': model6_objects,
#         'model7_objects': model7_objects,
#         'model8_objects': model8_objects,
#         'msgs': msgs,
       
#     })

from .forms import InboxMessages

# def index(request):
#     try:
#         model1_objects = House.objects.prefetch_related(
#             Prefetch('images', queryset=HouseImage.objects.all())
#         ).order_by('-id')

#         model2_objects = list(Land.objects.filter(id__isnull=False).order_by('-id'))
#         model3_objects = list(Commercial.objects.all().order_by('-id')[:2])
#         model4_objects = list(OffPlan.objects.all().order_by('-id')[:2])

#         model5_objects = AgentHouse.objects.prefetch_related(
#             Prefetch('images', queryset=AgentHouseImage.objects.all())
#         ).order_by('-id')[:2]

#         model6_objects = AgentLand.objects.prefetch_related(
#             Prefetch('images', queryset=AgentLandImage.objects.all())
#         ).order_by('-id')[:2]

#         model7_objects = AgentOffPlan.objects.prefetch_related(
#             Prefetch('images', queryset=AgentOffPlanImage.objects.all())
#         ).order_by('-id')[:2]

#         model8_objects = AgentCommercial.objects.prefetch_related(
#             Prefetch('images', queryset=AgentCommercialImage.objects.all())
#         ).order_by('-id')[:2]

#         msgs = list(Inbox.objects.all().order_by('-id'))
#         form = InboxMessages

#         if request.method == 'POST':
#             form = InboxMessages(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return render(request, 'index.html', {
#                     'form': InboxMessages(),  # Empty form after save
#                     'success': True,
#                     'message': 'Message submitted successfully!'
#                 })
#             else:
#                 return render(request, 'index.html', {
#                     'form': form,
#                     'success': False
#                 })
#         else:
#             form = InboxMessages()
#             return render(request, 'index.html', {'form': form})


#     except Exception as e:
#         print(f"Error fetching objects: {e}")
#         model1_objects = model2_objects = model3_objects = model4_objects = []
#         model5_objects = model6_objects = model7_objects = model8_objects = []
#         msgs = []

#     # For initial page render (GET request)
#     form = InboxMessages()
#     return render(request, 'index.html', {
#         'form': form,
#         'model1_objects': model1_objects,
#         'model2_objects': model2_objects,
#         'model3_objects': model3_objects,
#         'model4_objects': model4_objects,
#         'model5_objects': model5_objects,
#         'model6_objects': model6_objects,
#         'model7_objects': model7_objects,
#         'model8_objects': model8_objects,
#         'msgs': msgs,
#     })



def more(request):
    return render(request,'more.html')



# def blog(request):
#     blogs = Blog.objects.all()
    
   
#     paginator = Paginator(blogs, 10) 
#     page_number = request.GET.get('page') 
#     page_obj = paginator.get_page(page_number)  

#     return render(request, 'blog.html', {'page_obj': page_obj})

def blog(request):
    blogs = Blog.objects.all().order_by('-date')  # change 'created_at' to your actual date field name

    paginator = Paginator(blogs, 10)
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

def index(request):
    purposes = Purpose.objects.all()
    properties = Property.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    premium = Premium.objects.all()
    districts = Property.objects.values_list("district", flat=True).distinct()
    cities = Property.objects.values_list("city", flat=True).distinct()

    if request.method == 'POST':

        # ------------------- Inbox form -------------------
        if "messages_text" in request.POST:
            name = request.POST.get("name", "").strip()
            pin_code = request.POST.get("pin_code", "").strip()
            contact = request.POST.get("contact", "").strip()
            messages_text = request.POST.get("messages_text", "").strip()

            # ✅ Basic validation: disallow links
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



        elif "Dealings" in request.POST and "image" in request.FILES:

            name = request.POST.get("name", "").strip()

            email = request.POST.get("email", "").strip()

            address = request.POST.get("address", "").strip()

            phone_number = request.POST.get("phone_number", "").strip()

            Dealings = request.POST.get("Dealings", "").strip()

            url_pattern = re.compile(r"(https?:\/\/|www\.|\b\S+\.(com|net|org|in|info|io|gov|co)\b)", re.IGNORECASE)

            error_message = None

            for field_value, field_name in [(name, "Name"), (address, "Address"), (phone_number, "Phone")]:

                if url_pattern.search(field_value):
                    error_message = f"Links are not allowed in {field_name}."

                    break

            if error_message:
                # Pass error back to template

                return render(request, 'index.html', {

                    "agent_error": error_message,

                    "show_agent_modal": True,  # flag to open modal

                    # include other context data

                    "purposes": Purpose.objects.all(),

                    "properties": Property.objects.all(),

                    "categories": Category.objects.all(),

                    "premium": Premium.objects.all(),

                    "districts": Property.objects.values_list("district", flat=True).distinct(),

                    "cities": Property.objects.values_list("city", flat=True).distinct(),

                })

            # Save agent

            AgentForm.objects.create(
                name=name,
                email=email,
                address=address,
                phone_number=phone_number,
                Dealings=Dealings,
                image=request.FILES.get("image")

            )

            return redirect("index")

        # ------------------- Property form -------------------
        elif "about_the_property" in request.POST and "image" in request.FILES:
            # Get all fields directly as strings (no FK lookup needed)
            category_name = request.POST.get("categories", "").strip()
            purpose_name = request.POST.get("purposes", "").strip()
            label = request.POST.get("label", "").strip()
            land_area = request.POST.get("land_area")
            sq_ft = request.POST.get("sq_ft")
            description = request.POST.get("about_the_property", "").strip()
            amenities = request.POST.get("amenities", "").strip()
            owner = request.POST.get("owner", "").strip()
            phone = request.POST.get("phone", "").strip()
            whatsapp = request.POST.get("whatsapp", "").strip()
            location = request.POST.get("locations", "").strip()
            city = request.POST.get("city", "").strip()
            district = request.POST.get("District", "").strip()
            pin_code = request.POST.get("pin_code", "").strip()
            land_mark = request.POST.get("land_mark", "").strip()
            duration = request.POST.get("duration", "").strip()
            price = request.POST.get("price")
            total_price = request.POST.get("total_price")

            # ❌ Backend link validation (prevent links in text fields)
            url_pattern = re.compile(r"(https?:\/\/|www\.|\b\S+\.(com|net|org|in|info|io|gov|co)\b)", re.IGNORECASE)
            fields_to_check = [
                (label, "Label"),
                (description, "Description"),
                (amenities, "Amenities"),
                (owner, "Owner"),
                (phone, "Phone"),
                (whatsapp, "WhatsApp"),
                (land_mark, "Landmark")
            ]
            for field_value, field_name in fields_to_check:
                if url_pattern.search(field_value):
                    return render(request, "index.html", {
                        "property_error": f"Links are not allowed in {field_name}.",
                        "show_property_modal": True,
                        "purposes": Purpose.objects.all(),
                        "properties": Propertylist.objects.all(),
                        "categories": Category.objects.all(),
                        "premium": Premium.objects.all(),
                        "districts": Propertylist.objects.values_list("District", flat=True).distinct(),
                        "cities": Propertylist.objects.values_list("city", flat=True).distinct(),
                    })

            # ✅ Save directly into Propertylist (no ForeignKeys)
            Propertylist.objects.create(
                categories=category_name,
                purposes=purpose_name,
                label=label,
                land_area=land_area,
                sq_ft=sq_ft,
                about_the_property=description,
                amenities=amenities,
                image=request.FILES.get("image"),
                price=price,
                total_price=total_price,
                owner=owner,
                phone=phone,
                whatsapp=whatsapp,
                locations=location,
                city=city,
                District=district,
                pin_code=pin_code,
                land_mark=land_mark,
                duration=duration
            )

            messages.success(request, "Property added successfully!")
            return redirect("index")

    return render(request, 'index.html', {
        "purposes": purposes,
        "properties": properties,
        "categories": categories,
        "premium": premium,
        "districts": districts,
        "cities": cities,
        "property": properties.first(),
    })



def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius (km)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def nearest_property(request):
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
        lat, lng = None, None

        if prop.location:
            # Case 1: embed link with !2d / !3d
            match = re.search(r"!2d([0-9.\-]+)!3d([0-9.\-]+)", prop.location)
            if match:
                lng = float(match.group(1))
                lat = float(match.group(2))

            # Case 2: place/share link with @lat,lng
            match2 = re.search(r"@([0-9.\-]+),([0-9.\-]+)", prop.location)
            if match2:
                lat = float(match2.group(1))
                lng = float(match2.group(2))

        if lat and lng:
            dist = haversine(user_lat, user_lng, lat, lng)

            # Get all images as absolute URLs
            images = []
            if prop.images.exists():
                images = [request.build_absolute_uri(img.image.url) for img in prop.images.all()]
            else:
                images = [request.build_absolute_uri("/static/images/demo.png")]

            results.append({
                "id": prop.id,
                "label": prop.label,
                "land_area": prop.land_area,
                "price": str(prop.price),
                "perprice": str(prop.perprice) if prop.perprice else "",
                "description": prop.description or "",   # ✅ Add description here
                "sq_ft": prop.sq_ft or "",
                "latitude": lat,
                "longitude": lng,
                "distance": round(dist, 2),
                "purpose_name": prop.purpose.name if prop.purpose else "For Sale",
                "images": images,
                "location": prop.location or "",
                "phone": prop.phone or "",
            })

    results.sort(key=lambda x: x["distance"])

    if not results:
        return JsonResponse({"error": "No properties with valid coordinates"}, status=404)

    return JsonResponse(results, safe=False)


def properties(request):
    properties = Property.objects.all().order_by('-created_at')
    purposes = Purpose.objects.all()
    categories = Category.objects.all()
    districts = Property.objects.values_list("district", flat=True).distinct()  # ✅ lowercase
    cities = Property.objects.values_list("city", flat=True).distinct()  # ✅ correct

    return render(request,'properties.html',{
        "properties": properties,
        "districts": districts,
        "cities": cities,
        "purposes": purposes,
        "categories": categories,
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

    # Fetch related properties (same category, purpose, and location)
    related_properties = Property.objects.filter(
        category=property_obj.category,
        purpose=property_obj.purpose,
        location__iexact=property_obj.location
    ).exclude(id=property_obj.id)[:6]  # Exclude current property, limit 6

    return render(request, "detail_properties.html", {
        'property': property_obj,
        'extra_images': extra_images,
        'amenities': amenities,
        'related_properties': related_properties,
    })



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

        ContactRequest.objects.create(
            first_name=first_name,
            last_name=last_name,
            contact_method=contact_method,
            email=email,
            phone=phone,
            message=message,
        )

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
    property_obj = get_object_or_404(AgentProperty, pk=pk)  # or your actual model name
    extra_images = AgentPropertyImage.objects.filter(property=property_obj)

    return render(request, "propertygallery.html", {
        'property': property_obj,
        'extra_images': extra_images
    })

def property_gallery(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)  # or your actual model name
    extra_images = PropertyImage.objects.filter(property=property_obj)

    return render(request, "gallery.html", {
        'property': property_obj,
        'extra_images': extra_images
    })


@csrf_exempt
def upload_property_screenshot(request):
    if request.method == "POST":
        property_id = request.POST.get("property_id")
        screenshot_file = request.FILES.get("screenshot")
        if not screenshot_file:
            return JsonResponse({"status": "error", "message": "No screenshot received"}, status=400)
        try:
            prop = Property.objects.get(id=property_id)
            prop.screenshot = screenshot_file
            prop.save()
            return JsonResponse({"status": "success", "screenshot_url": prop.screenshot.url})
        except Property.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Property not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)




