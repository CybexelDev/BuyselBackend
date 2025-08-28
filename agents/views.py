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


