import json
from django.shortcuts import render, redirect, get_object_or_404, redirect
from developer.models import *
from . models import*
from . forms import *
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
# import requests
# from geopy.distance import geodesic
from users.views import*
from django.http import JsonResponse

# def agentslogin(request):
#     msg = ""
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         # Authenticate user with the username and password
#         user = Login.objects.filter(username=username, password=password)

#         if user:
#             # User found, start session and redirect
#             request.session["name"] = username

#             # Prevent caching the dashboard page
#             response = redirect('dashboard')
#             response['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
#             response['Pragma'] = 'no-cache'
#             response['Expires'] = '0'
#             return response  # Return the response to redirect to dashboard

#         else:
#             msg = "Username or Password is invalid"
#             return render(request, 'agentslogin.html', {'msg': msg})  # Render login page with error message

#     else:
#         # If the request is a GET request and the user is already logged in, redirect to dashboard
#         if "name" in request.session:
#             return redirect('dashboard')  # Redirect to dashboard if user is logged in
#         else:
#             # If not logged in, render the login page with no caching headers
#             response = render(request, 'agentslogin.html')
#             response['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
#             response['Pragma'] = 'no-cache'
#             response['Expires'] = '0'
#             return response  # Return the response her
        

def agentslogin(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            print('requeessttt',request.body)
            # data = json.loads(request.body)
            # username = data.get('username')
            # password = data.get('password')
            print("Raw request body:", request.body)
            data = json.loads(request.body.decode("utf-8"))
            username = data.get("username")
            password = data.get("password")
            print("Username:", username)
            print("Password:", password)


            # Authenticate user (replace with your logic)
            user = Login.objects.filter(username=username, password=password)

            if user:
                # Set session
                request.session["name"] = username
                print('the session user ',request.session["name"])
                # return redirect('dashboard')
                
                # Return success response
                return JsonResponse({
                    'status': 'success',
                    'message': 'Login successful',
                    'redirect_url': 'http://127.0.0.1:8000/agents/dashboard/'
                })
            else:
                # Return error response
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid username or password',
                }, status=400)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    else:
        if request.method == 'GET':
           return render(request,'agentslogin.html')



def logout_view(request):
    if "name" in request.session:
        request.session.pop("name")

        return redirect('agentslogin')  # Redirect the user to the login page


# views.py

from django.shortcuts import render, redirect
from .models import UserProfile

def dashboard(request):
     
    if "name" not in request.session:
        # No session found, redirect to the login page
        return redirect('agentslogin')  # Redirect to login if session is not present

    # Assuming that the session name corresponds to the username and it is related to UserProfile
    username = request.session["name"]
    try:
        # Retrieve the agent's profile (assuming agent is a UserProfile)
        agent = UserProfile.objects.get(login__username=username)  # You may need to adjust based on your models
    except UserProfile.DoesNotExist:
        return redirect('agentslogin')
  # Redirect if the agent doesn't exist

    # Pass agent info to the template
    response = render(request, 'dashboard.html', {'username': username, 'agent': agent})
    
    # Set cache control headers
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response



def category_list(request):
    categories = MainCategory.objects.all()
    return render(request, 'category_list.html', {'categories': categories})



def profile(request):
    if "name" not in request.session:
        return redirect('login')  # Redirect to login if the user is not authenticated

    username = request.session["name"]
    login_user = Login.objects.filter(username=username).first()

    if login_user:
        try:
            user_profile = UserProfile.objects.get(login=login_user)
        except UserProfile.DoesNotExist:
            user_profile = None
    else:
        user_profile = None

    return render(request, 'profile.html', {'user_profile': user_profile})

def update_profile(request):
    if "name" not in request.session:
        return redirect('login')

    username = request.session["name"]
    login_user = Login.objects.filter(username=username).first()

    if login_user:
        user_profile, created = UserProfile.objects.get_or_create(login=login_user)

        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
                return redirect('profile')  # Redirect to profile page after successful form submission
        else:
            form = UserProfileForm(instance=user_profile)

        return render(request, 'update_profile.html', {'form': form})
    else:
        return redirect('login')

def agent_house_create(request):
    categories = MainCategory.objects.all()  # Fetch all categories from the MainCategory model
    username = request.session.get("name")  # Get the username from the session
    
    if not username:
        return redirect('login')  # Redirect to login if user is not logged in
    
    # Fetch user profile to get phone contact (assuming login is linked to user profile)
    user_profile = UserProfile.objects.filter(login__username=username).first()
    contact = user_profile.phone_number if user_profile else None
    if request.method == 'POST':
        # Create a new AgentHouse object and populate fields from the POST data
        house = AgentHouse(
            Caption=request.POST['Caption'],
            category_id=request.POST['category'],  # Use category_id to link to the MainCategory model
            total_land=request.POST.get('total_land', ''),
            house_area=request.POST['house_area'],
            price=request.POST['price'],
            address=request.POST['address'],
            description=request.POST['description'],
            furnished='furnished' in request.POST,
            land_mark=request.POST['land_mark'],
            Bedroom=request.POST['Bedroom'],
            Bathroom=request.POST['Bathroom'],
            Kitchen='Kitchen' in request.POST,
            allowed_persons=request.POST['allowed_persons'],
            sequrity_deposit=request.POST['sequrity_deposit'],
            Time_perioud=request.POST['Time_perioud'],
            gender=request.POST['gender'],
            location=request.POST['location'],
            agent_name=request.POST['agent_name'],
            contact=request.POST['contact'],
            status=request.POST['status'],
            disabled='disabled' in request.POST,
        )
        house.save()  
        uploaded_images = request.FILES.getlist('images')
        
        # Check if the contact of images is not 4
        if len(uploaded_images) != 4:
            # Use messages.error to show the validation error message
            messages.error(request, "Exactly 4 images must be uploaded.")
            return render(request, 'createhouse.html', {'categories': categories, 'username': username, 'contact': contact})  # Re-render the form

        # Save images
        for image in uploaded_images:
            AgentHouseImage.objects.create(house=house, image=image)
        
        return redirect('house-list')  # Redirect after successful creation

    return render(request, 'createhouse.html', {'categories': categories, 'username': username,'contact':contact})  # Pass categories to the template  # Pass categories to the template




def house_list(request):
    username = request.session.get("name")

    if not username:
        return redirect('login')

    user_profile = UserProfile.objects.filter(login__username=username).first()
    if not user_profile:
        return redirect('login')

    house = AgentHouse.objects.filter(agent_name=username)

    # If you want to paginate the results
    paginator = Paginator(house, 10)  # Show 10 houses per page
    page_contact = request.GET.get('page')
    page_obj = paginator.get_page(page_contact)

    # Get the first image for each house (assuming each house has at least one image)
    for house in page_obj:
        house.first_image = AgentHouseImage.objects.filter(house=house).first()  # Get the first image

    return render(request, 'houselist.html', {'houselist': page_obj})


def agent_house_detail(request, pk):
    house = get_object_or_404(AgentHouse, pk=pk)
    return render(request, 'housedetail.html', {'house': house})

def agent_house_update(request, pk):
    categories = MainCategory.objects.all()  # Fetch all categories from the MainCategory model
    house = get_object_or_404(AgentHouse, pk=pk)

    if request.method == 'POST':
        # Get all the fields from POST data
        agent_name = request.POST.get('agent_name')
        if not agent_name:
            messages.error(request, "'Agent Name' is required.")
            return render(request, 'updatehouse.html', {'house': house, 'categories': categories})

        house.Caption = request.POST['Caption']
        category_id = request.POST['category']
        category = MainCategory.objects.get(id=category_id)
        house.category = category
        
        house.total_land = request.POST.get('total_land', '')
        house.house_area = request.POST['house_area']
        house.price = request.POST['price']
        house.address = request.POST['address']
        house.description = request.POST['description']
        house.furnished = 'furnished' in request.POST
        house.land_mark = request.POST['land_mark']
        house.Bedroom = request.POST['Bedroom']
        house.Bathroom = request.POST['Bathroom']
        house.Kitchen = 'Kitchen' in request.POST
        house.allowed_persons = request.POST['allowed_persons']
        house.sequrity_deposit = request.POST['sequrity_deposit']
        house.Time_perioud = request.POST['Time_perioud']
        house.gender = request.POST['gender']
        house.location = request.POST['location']
        house.agent_name = request.POST['agent_name'] # Now use the value from POST data
        house.contact = request.POST.get('contact', '')  # D
        house.status = request.POST.get('status', '')  
        house.disabled = 'disabled' in request.POST

        # Handle images
        uploaded_images = request.FILES.getlist('images')
        if uploaded_images:
            if len(uploaded_images) != 4:
                messages.error(request, "Exactly 4 images must be uploaded.")
                return render(request, 'updatehouse.html', {'house': house, 'categories': categories})

            house.images.all().delete()  # Delete old images
            for image in uploaded_images:
                AgentHouseImage.objects.create(house=house, image=image)

        house.save()  # Save the updated house data
        return redirect('house-detail', pk=house.pk)  # Redirect to the house details page

    return render(request, 'updatehouse.html', {'house': house, 'categories': categories})





def agent_land_create(request):
    categories = MainCategory.objects.all()
    username = request.session.get("name")  
    user_profile = UserProfile.objects.filter(login__username=username).first()
    contact = user_profile.phone_number if user_profile else None  

    if request.method == 'POST':
        land = AgentLand(
            Caption=request.POST['Caption'],
            category_id=request.POST['category'],
            total_land=request.POST.get('total_land', ''),
            price=request.POST['price'],
            address=request.POST['address'],
            description=request.POST['description'],
            furnished='furnished' in request.POST,
            land_mark=request.POST['land_mark'],
            sequrity_deposit=request.POST['sequrity_deposit'],
            Time_perioud=request.POST['Time_perioud'],
            location=request.POST['location'],
            agent_name=request.POST['agent_name'],
            contact=request.POST['contact'],
            status=request.POST['status'],
            disabled='disabled' in request.POST,
        )
        land.save()  

        uploaded_images = request.FILES.getlist('images')
        
        if not (4 <= len(uploaded_images) <= 20):
            messages.error(request, "You must upload at least 4 images and at most 20 images.")
            return render(request, 'createland.html', {'categories': categories, 'username': username, 'contact': contact})

        for image in uploaded_images:
            AgentLandImage.objects.create(land=land, image=image)

        return redirect('land-list')

    return render(request, 'createland.html', {'categories': categories, 'username': username, 'contact': contact})

def land_list(request):
    username = request.session.get("name")
    if not username:
        return redirect('login')

    user_profile = UserProfile.objects.filter(login__username=username).first()
    if not user_profile:
        return redirect('login')

    land_qs = AgentLand.objects.filter(agent_name=username)
    
    paginator = Paginator(land_qs, 10)
    page_contact = request.GET.get('page')
    page_obj = paginator.get_page(page_contact)

    for land in page_obj.object_list:
        land.first_image = AgentLandImage.objects.filter(land=land).first()

    return render(request, 'landlist.html', {'landlist': page_obj})

def agent_land_detail(request, pk):
    land = get_object_or_404(AgentLand, pk=pk)
    return render(request, 'landdetail.html', {'land': land})

def agent_land_update(request, pk):
    categories = MainCategory.objects.all()
    land = get_object_or_404(AgentLand, pk=pk)

    if request.method == 'POST':
        land.Caption = request.POST['Caption']
        
        category_id = request.POST['category']
        category = MainCategory.objects.get(id=category_id)
        land.category = category  

        land.total_land = request.POST.get('total_land', '')
        land.price = request.POST['price']
        land.address = request.POST['address']
        land.description = request.POST['description']
        land.land_mark = request.POST['land_mark']
        land.sequrity_deposit = request.POST['sequrity_deposit']
        land.Time_perioud = request.POST['Time_perioud']
        land.location = request.POST['location']
        land.agent_name = request.POST['agent_name']
        land.contact = request.POST['contact']
        land.status = request.POST['status']
        land.disabled = 'disabled' in request.POST

        uploaded_images = request.FILES.getlist('images')
        
        if uploaded_images:
            if not (4 <= len(uploaded_images) <= 20):
                messages.error(request, "You must upload at least 4 images and at most 20 images.")
                return render(request, 'updateland.html', {'land': land, 'categories': categories})

            AgentLandImage.objects.filter(land=land).delete()

            for image in uploaded_images:
                AgentLandImage.objects.create(land=land, image=image)

        land.save()
        return redirect('land-detail', pk=land.pk)

    return render(request, 'updateland.html', {'land': land, 'categories': categories})






def agent_offplan_create(request):
    categories = MainCategory.objects.all()  # Fetch all categories from the MainCategory model
    username = request.session.get("name")  # Get the username from the session

    if not username:
        return redirect('login')  # Redirect to login if user is not logged in
    
    # Fetch user profile to get phone contact (assuming login is linked to user profile)
    user_profile = UserProfile.objects.filter(login__username=username).first()
    contact = user_profile.phone_number if user_profile else None

    if request.method == 'POST':
        # Safely retrieve fields with .get() to avoid MultiValueDictKeyError
        rooms = request.POST.get('rooms', None)
        house_area = request.POST.get('house_area', None)
        Caption = request.POST.get('Caption', None)
        category = request.POST.get('category', None)
        price = request.POST.get('price', None)
        address = request.POST.get('address', None)
        description = request.POST.get('description', None)
        total_land = request.POST.get('total_land', None)
        land_mark = request.POST.get('land_mark', None)
        bedroom = request.POST.get('Bedroom', None)
        bathroom = request.POST.get('Bathroom', None)
        allowed_persons = request.POST.get('allowed_persons', None)
        sequrity_deposit = request.POST.get('sequrity_deposit', None)
        time_perioud = request.POST.get('Time_perioud', None)
        gender = request.POST.get('gender', None)
        location = request.POST.get('location', None)
        agent_name = request.POST.get('agent_name', None)
        contact = request.POST.get('contact', None)
        status = request.POST.get('status', None)
        furnished = 'furnished' in request.POST
        kitchen = 'Kitchen' in request.POST
        disabled = 'disabled' in request.POST

        # Validate required fields (including 'house_area')
        if not Caption or not category or not price or not house_area or not rooms:
            messages.error(request, "Caption, category, price, house area, and rooms are required.")
            return render(request, 'createoff.html', {
                'categories': categories,
                'username': username,
                'contact': contact
            })

        # Create the new OffPlanHouse object
        off_plan_house = AgentOffPlan(
            Caption=Caption,
            category_id=category,
            total_land=total_land,
            house_area=house_area,
            price=price,
            address=address,
            description=description,
            furnished=furnished,
            land_mark=land_mark,
            Bedroom=bedroom,
            Bathroom=bathroom,
            Kitchen=kitchen,
            allowed_persons=allowed_persons,
            sequrity_deposit=sequrity_deposit,
            Time_perioud=time_perioud,
            gender=gender,
            location=location,
            agent_name=agent_name,
            contact=contact,
            status=status,
            disabled=disabled,
            rooms=rooms  # Add rooms to the OffPlanHouse
        )
        off_plan_house.save()

        # Handle image uploads (validate that exactly 4 images are uploaded)
        uploaded_images = request.FILES.getlist('images')
        if len(uploaded_images) != 4:
            messages.error(request, "Exactly 4 images must be uploaded.")
            return render(request, 'createoff.html', {
                'categories': categories,
                'username': username,
                'contact': contact
            })

        # Save the images to the database
        for image in uploaded_images:
            AgentCommercialImage.objects.create(off_plan_house=off_plan_house, image=image)

        # Redirect after successful creation
        messages.success(request, "Off-plan house successfully created!")
        return redirect('off_list')

    return render(request, 'createoff.html', {
        'categories': categories,
        'username': username,
        'contact': contact
    })



def off_list(request):
    # Get the logged-in user's username from the session
    username = request.session.get("name")
    
    if not username:
        return redirect('login')

    user_profile = UserProfile.objects.filter(login__username=username).first()
    if not user_profile:
        return redirect('login')

    offs = AgentOffPlan.objects.filter(agent_name=username)

    # If you want to paginate the results
    paginator = Paginator(offs, 10)  # Show 10 lands per page
    page_contact = request.GET.get('page')
    page_obj = paginator.get_page(page_contact)

    # Get the first image for each land (assuming each land has at least one image)
    for offplan in page_obj:
        offplan.first_image = AgentOffPlanImage.objects.filter(offplan=offplan).first()

    return render(request, 'offlist.html', {'offlist': page_obj})


def agent_off_detail(request, pk):
    off = get_object_or_404(AgentOffPlan, pk=pk)
    return render(request, 'offdetail.html', {'off': off})

def agent_off_update(request, pk):
    categories = MainCategory.objects.all()  # Fetch all categories from the MainCategory model
    offplan = get_object_or_404(AgentOffPlan, pk=pk)

    if request.method == 'POST':
        offplan.Caption = request.POST['Caption']
        
        # Get the category from the form and fetch the corresponding MainCategory instance
        category_id = request.POST['category']
        category = MainCategory.objects.get(id=category_id)
        offplan.category = category  # Assign the MainCategory instance to the offplan's category

        offplan.total_land = request.POST.get('total_land', '')
        offplan.price = request.POST['price']
        offplan.rooms = request.POST['rooms']
        offplan.land_mark = request.POST['land_mark']
        offplan.address = request.POST['address']
        offplan.description = request.POST['description']
        offplan.location = request.POST['location']
        offplan.agent_name = request.POST['agent_name']
        offplan.contact = request.POST['contact']
        offplan.status = request.POST['status']
        offplan.disabled = 'disabled' in request.POST

        # Image Handling
        uploaded_images = request.FILES.getlist('images')
        
        if uploaded_images:
            if len(uploaded_images) != 4:
                # If not exactly 4 images, use messages.error() to display an error
                messages.error(request, "Exactly 4 images must be uploaded.")
                return render(request, 'updateoff.html', {'offplan': offplan, 'categories': categories})  # Re-render the form

            # Delete old images before adding new ones
            offplan.images.all().delete()  # Delete all old images associated with this offplan

            # Save new images
            for image in uploaded_images:
                AgentOffPlanImage.objects.create(offplan=offplan, image=image)

        offplan.save()  # Save the updated offplan data
        return redirect('off-detail', pk=offplan.pk)  # Redirect to the offplan details page

    return render(request, 'updateoff.html', {'offplan': offplan, 'categories': categories})




def agent_com_create(request):
    categories = MainCategory.objects.all()  # Fetch all categories from the MainCategory model
    username = request.session["name"] 
    user_profile = UserProfile.objects.filter(login__username=username).first()  # Assuming login is linked to user profile
    contact = user_profile.phone_number if user_profile else None 
    if request.method == 'POST':
        # Create a new Agentcom object and populate fields from the POST data
        com = AgentCommercial(
            Caption=request.POST['Caption'],
            category_id=request.POST['category'],  # Use category_id to link to the MainCategory model
            total_land=request.POST.get('total_land', ''),
           
            price=request.POST['price'],
            address=request.POST['address'],
            description=request.POST['description'],
           
            land_mark=request.POST['land_mark'],
           
            
            
            sequrity_deposit=request.POST['sequrity_deposit'],
            Time_perioud=request.POST['Time_perioud'],
            
            location=request.POST['location'],
            agent_name=request.POST['agent_name'],
            contact=request.POST['contact'],
            status=request.POST['status'],
            disabled='disabled' in request.POST,
        )
        com.save()  
        uploaded_images = request.FILES.getlist('images')
        if len(uploaded_images) != 4:
            # If not exactly 4 images, raise a validation error
            raise ValidationError("Exactly 4 images must be uploaded.")

        # Save images
        for image in uploaded_images:
            AgentCommercialImage.objects.create(com=com, image=image)
        
        return redirect('com-list') 

    return render(request, 'createcom.html', {'categories': categories, 'username': username,'contact':contact})  # Pass categories to the template




def com_list(request):
    # Get the logged-in user's username from the session
    username = request.session.get("name")
    
  
    
    if not username:
        return redirect('login')

    user_profile = UserProfile.objects.filter(login__username=username).first()
    if not user_profile:
        return redirect('login')

    comms = AgentCommercial.objects.filter(agent_name=username)

    # If you want to paginate the results
    paginator = Paginator(comms, 10)  # Show 10 lands per page
    page_contact = request.GET.get('page')
    page_obj = paginator.get_page(page_contact)

    # Get the first image for each land (assuming each land has at least one image)
    for com in page_obj:
        com.first_image = AgentCommercialImage.objects.filter(com=com).first()

    return render(request, 'comlist.html', {'comlist': page_obj})

def agent_com_detail(request, pk):
    com = get_object_or_404(AgentCommercial, pk=pk)
    return render(request, 'comdetail.html', {'com': com})

def agent_com_update(request, pk):
    categories = MainCategory.objects.all()  # Fetch all categories from the MainCategory model
    com = get_object_or_404(AgentCommercial, pk=pk)

    if request.method == 'POST':
        com.Caption = request.POST['Caption']
        
        # Get the category from the form and fetch the corresponding MainCategory instance
        category_id = request.POST['category']
        category = MainCategory.objects.get(id=category_id)
        com.category = category  # Assign the MainCategory instance to the com's category
        com.price = request.POST['price']
        com.address = request.POST['address']
        com.description = request.POST['description']
        com.land_mark = request.POST['land_mark']
        com.sequrity_deposit = request.POST['sequrity_deposit']
        com.Time_perioud = request.POST['Time_perioud']  
        com.location = request.POST['location']
        com.agent_name = request.POST['agent_name']
        com.contact = request.POST['contact']
        com.status = request.POST['status']
        com.disabled = 'disabled' in request.POST

        # Image Handling
        uploaded_images = request.FILES.getlist('images')
        
        if uploaded_images:
            if len(uploaded_images) != 4:
                # If not exactly 4 images, use messages.error() to display an error
                messages.error(request, "Exactly 4 images must be uploaded.")
                return render(request, 'updatecom.html', {'com': com, 'categories': categories})  # Re-render the form

            # Delete old images before adding new ones
            com.images.all().delete()  # Delete all old images associated with this com

            # Save new images
            for image in uploaded_images:
                AgentCommercialImage.objects.create(com=com, image=image)

        com.save()  # Save the updated com data
        return redirect('com-detail', pk=com.pk)  # Redirect to the com details page

    return render(request, 'updatecom.html', {'com': com, 'categories': categories})



# def agent_messages(request, agent_id):
#     """
#     View to display the messages for a specific agent on their page.
#     """
#     # Get the agent profile by ID
#     try:
#         agent = UserProfile.objects.get(id=agent_id)
#     except UserProfile.DoesNotExist:
#         # If no agent is found, redirect or handle as needed
#         return redirect('dashboard')

#     # Get all the messages related to this agent (assuming ManyToMany relationship with Inbox)
#     messages = agent.messages.all()  # Get all related messages
#     print("messages",messages)

#     # Pass agent and messages to the template
#     return render(request, 'notification.html', {'agent': agent, 'messages': messages})


# def inbox_view(request, agent_id):
#     # Count the contact of messages for the specific agent
#     total_messages = Inbox.objects.filter(agent_id=agent_id).count()
    
#     # Retrieve the messages for that specific agent
#     messages = Inbox.objects.filter(agent_id=agent_id)
    
#     return render(request, 'base1.html', {
#         'messages': messages,
#         'total_messages': total_messages,
#         'agent_id': agent_id
#     })

def check_pin_code_messages(request):
    if "name" not in request.session:
        return redirect('login')

    username = request.session["name"]
    try:
        user_profile = UserProfile.objects.get(login__username=username)
    except UserProfile.DoesNotExist:
        return redirect('login')

    inbox_messages = Inbox.objects.all()
    matching_messages = []
    non_matching_messages = []

    # Loop through inbox messages and separate them based on pin code match
    for message in inbox_messages:
        if user_profile.pin_code == int(message.pin_code):
            matching_messages.append(message)
            # Mark message as read when it's viewed
            message.is_read = True
            message.save()
        else:
            non_matching_messages.append(message)

    return render(
        request,
        'notification.html',
        {'matching_messages': matching_messages, 'non_matching_messages': non_matching_messages}
    )

def base1(request):
    if "name" not in request.session:
        return redirect('login')  # Redirect to login if session is not found

    username = request.session["name"]
    try:
        agent = UserProfile.objects.get(login__username=username)
    except UserProfile.DoesNotExist:
        return redirect('login')  # Redirect if no agent profile exists

    # Count unread messages (assuming 'is_read' is a boolean field in your Inbox model)
    unread_messages_count = Inbox.objects.filter(is_read=False).count()  # Count unread messages

    return render(
        request,
        'base1.html',
        {'username': username, 'agent': agent, 'unread_messages_count': unread_messages_count}
    )

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



def category_count(request):
    # Fetch the current user's profile (assuming the agent is logged in)
    username = request.session.get("name")
    
    if not username:
        return redirect('login')  # Redirect to login if the user is not logged in
    
    # Get the user's profile or related data
    user_profile = UserProfile.objects.filter(login__username=username).first()
    contact = user_profile.phone_contact if user_profile else None

    # Fetch categories and count listings for each category type (Sale, Rent, Lease, Resell)
    categories = MainCategory.objects.all()

    # Initialize dictionaries for counts
    sale_count = 0
    rent_count = 0
    lease_count = 0
    resell_count = 0
    
    # Iterate over each category type
    for category in categories:
        if category.catgory == 'Sale':
            sale_count += AgentHouse.objects.filter(category=category).count()
            sale_count += AgentLand.objects.filter(category=category).count()
            sale_count += AgentCommercial.objects.filter(category=category).count()
            sale_count += AgentOffPlan.objects.filter(category=category).count()
        
        elif category.catgory == 'Rent':
            rent_count += AgentHouse.objects.filter(category=category).count()
            rent_count += AgentLand.objects.filter(category=category).count()
            rent_count += AgentCommercial.objects.filter(category=category).count()
            rent_count += AgentOffPlan.objects.filter(category=category).count()
        
        elif category.catgory == 'Lease':
            lease_count += AgentHouse.objects.filter(category=category).count()
            lease_count += AgentLand.objects.filter(category=category).count()
            lease_count += AgentCommercial.objects.filter(category=category).count()
            lease_count += AgentOffPlan.objects.filter(category=category).count()
        
        elif category.catgory == 'Resell':
            resell_count += AgentHouse.objects.filter(category=category).count()
            resell_count += AgentLand.objects.filter(category=category).count()
            resell_count += AgentCommercial.objects.filter(category=category).count()
            resell_count += AgentOffPlan.objects.filter(category=category).count()
    
    # Pass these counts to the template
    return render(request, 'dashboard.html', {
        'username': username,
        'contact': contact,
        'sale_count': sale_count,
        'rent_count': rent_count,
        'lease_count': lease_count,
        'resell_count': resell_count,
    })