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




def base(request):
    return render(request, 'base.html')


def base(request):
    return render(request, 'more.html')

def properties(request):
    model1_objects = House.objects.all()
    model2_objects = Land.objects.all()
    model3_objects = Commercial.objects.all()
    model4_objects = OffPlan.objects.all()
    model5_objects = AgentHouse.objects.all()
    model6_objects = AgentLand.objects.all()
    model7_objects = AgentOffPlan.objects.all()
    model8_objects = AgentCommercial.objects.all()

    return render(request, 'properties.html',{
            'model1_objects': model1_objects,
            'model2_objects': model2_objects,
            'model3_objects': model3_objects,
            'model4_objects': model4_objects,
            'model5_objects': model5_objects,
            'model6_objects': model6_objects,
            'model7_objects': model7_objects,
            'model8_objects': model8_objects,
    })


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


def index(request):
    try:
        model1_objects = House.objects.prefetch_related(
            Prefetch('images', queryset=HouseImage.objects.all())
        ).order_by('-id')

        model2_objects = list(Land.objects.filter(id__isnull=False).order_by('-id'))
        model3_objects = list(Commercial.objects.all().order_by('-id')[:2])
        model4_objects = list(OffPlan.objects.all().order_by('-id')[:2])

        model5_objects = AgentHouse.objects.prefetch_related(
            Prefetch('images', queryset=AgentHouseImage.objects.all())
        ).order_by('-id')[:2]

        model6_objects = AgentLand.objects.prefetch_related(
            Prefetch('images', queryset=AgentLandImage.objects.all())
        ).order_by('-id')[:2]

        model7_objects = AgentOffPlan.objects.prefetch_related(
            Prefetch('images', queryset=AgentOffPlanImage.objects.all())
        ).order_by('-id')[:2]

        model8_objects = AgentCommercial.objects.prefetch_related(
            Prefetch('images', queryset=AgentCommercialImage.objects.all())
        ).order_by('-id')[:2]

        msgs = list(Inbox.objects.all().order_by('-id')[:15])

        # Debugging output
        for obj in model1_objects:
            print(f"Model1 Object ID: {obj.id} (Type: {type(obj.id)})")

    except Exception as e:
        print(f"Error fetching objects: {e}")
        model1_objects = model2_objects = model3_objects = model4_objects = []
        model5_objects = model6_objects = model7_objects = model8_objects = []
        msgs = []

    if request.method == 'POST':
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        pin_code = request.POST.get("pin_code")
        messages = request.POST.get("messages")

        if name and contact and messages:
            msg = Inbox(name=name, contact=contact, pin_code=pin_code, messages_text=messages)
            msg.save()

    return render(request, 'index.html', {
        'model1_objects': model1_objects,
        'model2_objects': model2_objects,
        'model3_objects': model3_objects,
        'model4_objects': model4_objects,
        'model5_objects': model5_objects,
        'model6_objects': model6_objects,
        'model7_objects': model7_objects,
        'model8_objects': model8_objects,
        'msgs': msgs,
    })





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

MODEL_MAPPING = {
    'model1': House,
    'model2': Land,
    'model3': Commercial,
    'model4': OffPlan,
    'model5': AgentHouse,
    'model6': AgentLand,
    'model7': AgentCommercial,
    'model8': AgentOffPlan,
    'houseimg': HouseImage,
}


def get_model_class(model_name):
    """
    Helper function to get the model class based on the model name.
    """
    model_classes = {
        'house': House,
        'land': Land,
        'commercial': Commercial,
        'offplan': OffPlan,
        'agenthouse': AgentHouse,
        'agentland': AgentLand,
        'agentoffplan': AgentOffPlan,
        'agentcommercial': AgentCommercial,
        'houseimg': HouseImage,
    }
    return model_classes.get(model_name.lower())

def validate_uuid(object_id):
    """
    Helper function to validate if the given object_id is a valid UUID.
    """
    try:
        return uuid.UUID(object_id)
    except ValueError:
        return None



def detail_view(request, model_name, object_id):
    model_classes = {
        'house': House,
        'land': Land,
        'commercial': Commercial,
        'offplan': OffPlan,
        'agenthouse': AgentHouse,
        'agentland': AgentLand,
        'agentoffplan': AgentOffPlan,
        'agentcommercial': AgentCommercial,
    }

    model_class = model_classes.get(model_name.lower())

    if not model_class:
        raise Http404("Invalid model name")

    # Fetch the object
    obj = get_object_or_404(model_class, id=object_id)

    # Fetch related images
    images = obj.images.all() if hasattr(obj, 'images') else []

    return render(request, 'detail.html', {'object': obj, 'images': images, 'object_id':object_id})



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



def agents_view(request, profile_id):
    # Get the user profile by ID
    profile = get_object_or_404(UserProfile, id=profile_id)

    # Get the listings related to this profile
    agent_houses = AgentHouse.objects.filter(agent_name=profile)
    agent_lands = AgentLand.objects.filter(agent_name=profile)
    agent_commercials = AgentCommercial.objects.filter(agent_name=profile)
    agent_offplans = AgentOffPlan.objects.filter(agent_name=profile)

    # Pass everything to the template
    context = {
        'profile': profile,
        'agent_houses': agent_houses,
        'agent_lands': agent_lands,
        'agent_commercials': agent_commercials,
        'agent_offplans': agent_offplans,
    }

    return render(request, 'agents_view.html', context)




def faq(request):
    return render(request,'faq.html')

def sitemap_view(request):
     return render(request, 'sitemap.xml', content_type='application/xml')












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


def agents_detail(request, model_name, object_id):
    # Define the model classes for agent listings
    model_classes = {
        'agenthouse': AgentHouse,
        'agentland': AgentLand,
        'agentcommercial': AgentCommercial,
        'agentoffplan': AgentOffPlan,
    }

    # Get the model class dynamically
    model_class = model_classes.get(model_name.lower())

    if not model_class:
        raise Http404("Invalid model name")

    # Fetch the object
    obj = get_object_or_404(model_class, id=object_id)

    # Fetch related images
    images = obj.images.all() if hasattr(obj, 'images') else []

    # Debugging: Print images in the console
    print(f"\nImages for {model_name} (ID: {object_id}):")

    if images:
        for img in images:
            print(f" - Image URL: {img.image.url}")
    else:
        print("No images found")

    return render(request, 'agent_detail.html', {'object': obj, 'images': images})


def agent_form(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        dealings = request.POST['Dealings']
        image = request.FILES['image']

        # Create and save the new agent instance
        agent = AgentForm(
            name=name,
            email=email,
            address=address,
            phone_number=phone_number,
            Dealings=dealings,
            image=image
        )
        
        try:
            agent.save()
            messages.success(request, "Agent created successfully!")
            return redirect('index')  # Redirect to agent list page
        except ValidationError as e:
            messages.error(request, f"Error: {e}")
            return render(request, 'agent_form.html')
    
    return render(request, 'agent_form.html')

def property_form(request):
    if request.method == 'POST':
        # Get form data from the request
        property_name = request.POST.get('property_name')
        locations = request.POST.get('locations')
        price = request.POST.get('price')
        about_the_property = request.POST.get('about_the_property')
        image = request.FILES.get('image')  # Get the uploaded image

        if not property_name or not locations or not price or not about_the_property or not image:
            messages.error(request, "All fields are required!")
            return redirect('property_form')  # Redirect back to the form if data is missing

        # Create a new Propertylist object and save it
        property = Propertylist(
            property_name=property_name,
            locations=locations,
            price=price,
            about_the_property=about_the_property,
            image=image
        )
        property.save()
        
        messages.success(request, "Property has been created successfully.")
        return redirect('index')  # Redirect to the property list view

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



def propertice(request):
    model1_objects = House.objects.all().order_by('-id')
    model2_objects = Land.objects.all().order_by('-id')
    model3_objects = Commercial.objects.all().order_by('-id')
    model4_objects = OffPlan.objects.all().order_by('-id')
    model5_objects = AgentHouse.objects.all().order_by('-id')
    model6_objects = AgentLand.objects.all().order_by('-id')
    model7_objects = AgentOffPlan.objects.all().order_by('-id')
    model8_objects = AgentCommercial.objects.all().order_by('-id')

    return render(request, 'properties.html', {
        'model1_objects': model1_objects,
        'model2_objects': model2_objects,
        'model3_objects': model3_objects,
        'model4_objects': model4_objects,
        'model5_objects': model5_objects,
        'model6_objects': model6_objects,
        'model7_objects': model7_objects,
        'model8_objects': model8_objects,
    })



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