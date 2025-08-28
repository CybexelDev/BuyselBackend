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




def base(request):
    return render(request, 'base.html')


def base(request):
    return render(request, 'more.html')



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


# def propertice(request):
#     model1_objects = House.objects.all()
#     model2_objects = Land.objects.all()
#     model3_objects = Commercial.objects.all()
#     model4_objects = OffPlan.objects.all()
#     model5_objects = AgentHouse.objects.all()
#     model6_objects = AgentLand.objects.all()
#     model7_objects = AgentOffPlan.objects.all()
#     model8_objects = AgentCommercial.objects.all()
#     return render(request,'properties.html',{
#                 'model1_objects': model1_objects,
#                 'model2_objects': model2_objects,
#                 'model3_objects': model3_objects,
#                 'model4_objects': model4_objects,
#                 'model5_objects': model5_objects,
#                 'model6_objects': model6_objects,
#                 'model7_objects': model7_objects,
#                 'model8_objects': model8_objects,
#                 }
#                 )




# import requests
# import os
# from django.http import JsonResponse
# from django.conf import settings

# IMGUR_CLIENT_ID = "1ca46e37be674f5"

# def upload_to_imgur(image_path):
#     headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
#     with open(image_path, "rb") as f:
#         response = requests.post("https://api.imgur.com/3/image", headers=headers, files={"image": f})
#     return response.json().get("data", {}).get("link")

# def share_property(request):
#     if request.method == "POST" and request.FILES.get("image"):
#         image = request.FILES["image"]

#         filename = f"property.png"
#         save_path = os.path.join(settings.MEDIA_ROOT, "shared_properties", filename)

#         # Save the image locally
#         with open(save_path, "wb") as f:
#             for chunk in image.chunks():
#                 f.write(chunk)

#         # Upload to Imgur
#         imgur_url = upload_to_imgur(save_path)

#         return JsonResponse({"success": True, "image_url": imgur_url})

#     return JsonResponse({"success": False, "error": "Invalid request"})

# @csrf_exempt
# def save_screenshot(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)  # Convert JSON request to Python dict
            
#             model_name = data.get("model_name")
#             object_id = data.get("object_id")

#             if not model_name or not object_id:
#                 return JsonResponse({"error": "Missing model_name or object_id"}, status=400)

#             # Add screenshot saving logic here

#             return JsonResponse({"success": "Screenshot saved successfully!"})

#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON format"}, status=400)

#     return JsonResponse({"error": "Invalid request"}, status=400)






def index(request):
    purposes = Purpose.objects.all()
    properties = Property.objects.all()

    if request.method == 'POST':
        # ------------------- Inbox form -------------------
        if "messages_text" in request.POST:  
            name = request.POST.get("name")
            pin_code = request.POST.get("pin_code")
            contact = request.POST.get("contact")
            messages_text = request.POST.get("messages_text")

            Inbox.objects.create(
                name=name,
                pin_code=pin_code,
                contact=contact,
                messages_text=messages_text
            )
            return redirect("index")

        # ------------------- Agent form -------------------
        elif "Dealings" in request.POST and "image" in request.FILES:
            name = request.POST.get("name")
            email = request.POST.get("email")
            address = request.POST.get("address")
            phone_number = request.POST.get("phone_number")
            Dealings = request.POST.get("Dealings")
            image = request.FILES.get("image")

            AgentForm.objects.create(
                name=name,
                email=email,
                address=address,
                phone_number=phone_number,
                Dealings=Dealings,
                image=image
            )
            return redirect("index")

        # ------------------- Property form -------------------
        elif "about_the_property" in request.POST and "image" in request.FILES:
            categories = request.POST.get("categories")
            purposes = request.POST.get("purposes")
            label = request.POST.get("label")
            land_area = request.POST.get("land_area")
            sq_ft = request.POST.get("sq_ft")
            about_the_property = request.POST.get("about_the_property")
            amenities = request.POST.get("amenities")
            image = request.FILES.get("image")
            price = request.POST.get("price")
            owner = request.POST.get("owner")
            phone = request.POST.get("phone")
            locations = request.POST.get("locations")
            pin_code = request.POST.get("pin_code")
            land_mark = request.POST.get("land_mark")
            duration = request.POST.get("duration")
            total_price = request.POST.get("total_price")
            whatsapp = request.POST.get("whatsapp")
            city = request.POST.get("city")
            District = request.POST.get("District")


            Propertylist.objects.create(
                categories=categories,
                purposes=purposes,
                label=label,
                land_area=land_area,
                sq_ft=sq_ft,
                about_the_property=about_the_property,
                amenities=amenities,
                image=image,
                price=price,
                owner=owner,
                phone=phone,
                locations=locations,
                pin_code=pin_code,
                land_mark=land_mark,
                total_price=total_price,
                duration=duration,
                whatsapp=whatsapp,
                city=city,
                District=District,
           
            )
            return redirect("index")

    return render(request, 'index.html', {
        "purposes": purposes,
        "properties": properties,
    })


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        return redirect("contact")  # reload page after submit (or redirect somewhere else)

    return render(request, "contact.html")


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











