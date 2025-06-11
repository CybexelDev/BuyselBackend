from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import SuperuserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from . models import *
from agents.models import *
from django.shortcuts import render, redirect, get_object_or_404, redirect
from . forms import *
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponse

# Create your views here.
# def admin_page(request):

#     return render(request, 'admin.html')

def base(request):
    agenthouse = agenthouse.objects.all()

    context ={
        'agenthouse': agenthouse
    }
    return render(request,'base2.html',context)




@user_passes_test(lambda u: u.is_superuser)
def admin_page(request):
    house = House.objects.all()
    land = Land.objects.all()
    com = Commercial.objects.all()
    offplan = OffPlan.objects.all()
    agents_register = AgentForm.objects.all()
    propertyregister =Propertylist.objects.all()
    blog = Blog.objects.all()
    agenthouse = AgentHouse.objects.all()
    agentland = AgentLand.objects.all()
    agentcom = AgentCommercial.objects.all()
    agentoffplan = AgentOffPlan.objects.all()
    login = Login.objects.all()
    inbox  = Inbox.objects.all()
    profile = UserProfile.objects.all()

    context ={
        'house': house,
        'land':land,
        'com':com,
        'offplan':offplan,
        'agents_register': agents_register,
        'propertyregister': propertyregister,
        'blog':blog,
        'agenthouse':agenthouse,
        'agentland' : agentland,
        'agentcom':agentcom,
        'agentoffplan':agentoffplan,
        'login' : login,
        'inbox': inbox,
        'profile':profile,

    }
    return render(request, 'admin.html',context)

from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
def superuser_login_view(request):
    User = get_user_model()
    if request.method == 'POST':
        form = SuperuserLoginForm(request.POST)
        holder = User.objects.filter(is_superuser=True).first()
        if holder.rate_limit >= 5 and timezone.now() < holder.last_failed_login + timedelta(minutes=2):
            print('the login is limited')
        else:
            holder = User.objects.filter(is_superuser=True).first()
            if holder.rate_limit >= 5:
                holder.rate_limit = 0
                holder.save()
            else:
                if form.is_valid():
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    user = authenticate(request, username=username, password=password)
                    if user is not None and user.is_superuser:
                        holder = User.objects.filter(is_superuser=True).first()
                        if holder:
                            holder.rate_limit = 0
                            holder.save()
                        login(request, user)
                        return redirect(reverse('admin_panel') + '#dashboard')  # custom redirect
                    else:
                        holder = User.objects.filter(is_superuser=True).first()
                        if holder:
                            holder.rate_limit += 1
                            holder.last_failed_login = timezone.now()
                            holder.save()
                            print('Rate limit incremented:', holder.rate_limit)
                        messages.error(request, 'Invalid credentials or not a superuser.')
    else:
        form = SuperuserLoginForm()
    return render(request, 'login.html', {'form': form})


from django.contrib.auth import logout

# def superuser_logout_view(request):
#     logout(request)
#     messages.success(request, "You have been logged out successfully.")
#     return render(request, 'login.html')
def superuser_logout_view(request):
    logout(request)
    return redirect('superuser_login_view')  

def houses_create(request):
    categories = MainCategory.objects.all()

    if request.method == 'POST':
        house = House(
            Caption=request.POST.get('Caption'),
            category_id=request.POST.get('category'),
            total_land=request.POST.get('total_land'),
            price=request.POST.get('price'),
            house_area=request.POST.get('house_area'),
            address=request.POST.get('address'),
            description=request.POST.get('description'),
            furnished=bool(request.POST.get('furnished')),
            land_mark=request.POST.get('land_mark'),
            Bedroom=request.POST.get('Bedroom'),
            Bathroom=request.POST.get('Bathroom'),
            Kitchen=bool(request.POST.get('Kitchen')),
            allowed_persons=request.POST.get('allowed_persons') or None,
            sequrity_deposit=request.POST.get('sequrity_deposit'),
            Time_perioud=request.POST.get('Time_perioud'),
            gender=request.POST.get('gender'),
            location=request.POST.get('location'),
            username=request.POST.get('username'),
            contact=request.POST.get('contact'),
            status=request.POST.get('status'),
            disabled=bool(request.POST.get('disabled')),
            image=request.FILES.get('image'),
            screenshot=request.FILES.get('screenshot'),
        )
        house.save()

        # ✅ Save additional images using HouseImage
        images = request.FILES.getlist('house_images')
        for img in images:
            HouseImage.objects.create(house=house, image=img)

        messages.success(request, "House created successfully!")
        return redirect('house_create')  # You can change this to 'house_list' or detail view

    return render(request, 'createhouses.html', {'categories': categories})

from uuid import UUID
from django.contrib import messages

def houseupdate(request, pk: UUID):
    house = get_object_or_404(House, pk=pk)
    categories = MainCategory.objects.all()

    if request.method == 'POST':
        house.Caption = request.POST.get('Caption')
        category_id = request.POST.get('category')
        if category_id:
            try:
                house.category = MainCategory.objects.get(id=category_id)
            except MainCategory.DoesNotExist:
                pass

        house.total_land = request.POST.get('total_land')
        house.price = request.POST.get('price')
        house.house_area = request.POST.get('house_area')
        house.address = request.POST.get('address')
        house.description = request.POST.get('description')
        house.furnished = bool(request.POST.get('furnished'))
        house.land_mark = request.POST.get('land_mark')
        house.Bedroom = request.POST.get('Bedroom')
        house.Bathroom = request.POST.get('Bathroom')
        house.Kitchen = bool(request.POST.get('Kitchen'))
        house.allowed_persons = request.POST.get('allowed_persons') or None
        house.sequrity_deposit = request.POST.get('sequrity_deposit')
        house.Time_perioud = request.POST.get('Time_perioud')
        house.gender = request.POST.get('gender')
        house.location = request.POST.get('location')
        house.username = request.POST.get('username')
        house.contact = request.POST.get('contact')
        house.status = request.POST.get('status')
        house.disabled = bool(request.POST.get('disabled'))

        if request.FILES.get('image'):
            house.image = request.FILES.get('image')
        if request.FILES.get('screenshot'):
            house.screenshot = request.FILES.get('screenshot')

        house.save()

        # Save new additional house images
        new_images = request.FILES.getlist('house_images')
        for img in new_images:
            HouseImage.objects.create(house=house, image=img)

        # ✅ Show popup message using alert
        messages.success(request, "House updated successfully!")
        return redirect('house_update', pk=pk)

    return render(request, 'houseupdate.html', {'house': house, 'categories': categories})

from django.urls import reverse
def housedelete(request, pk):
    house = get_object_or_404(House, pk=pk)
    house.delete()
    messages.success(request, "House deleted successfully.")
    return redirect(reverse('admin_panel') + '#house')


def lands_create(request):
    categories = MainCategory.objects.all()

    if request.method == 'POST':
        land = Land(
            Caption=request.POST.get('Caption'),
            category_id=request.POST.get('category'),
            total_land=request.POST.get('total_land'),
            price=request.POST.get('price'),
            space_area=request.POST.get('space_area'),
            address=request.POST.get('address'),
            description=request.POST.get('description'),
            land_mark=request.POST.get('land_mark'),
            sequrity_deposit=request.POST.get('sequrity_deposit'),
            Time_perioud=request.POST.get('Time_perioud'),
            location=request.POST.get('location'),
            username=request.POST.get('username'),
            contact=request.POST.get('contact'),
            status=request.POST.get('status'),
            disabled=bool(request.POST.get('disabled')),
            image=request.FILES.get('image'),
            screenshot=request.FILES.get('screenshot'),
        )
        land.save()

        # ✅ Save multiple LandImage instances
        images = request.FILES.getlist('land_images')
        for img in images:
            LandImage.objects.create(land=land, image=img)

        messages.success(request, "Land created successfully!")
        return redirect(reverse('admin_panel') + '#land') # Or wherever you want to go

    return render(request, 'createlands.html', {'categories': categories})



def land_update(request, pk: UUID):
    land = get_object_or_404(Land, pk=pk)
    categories = MainCategory.objects.all()

    if request.method == 'POST':
        land.Caption = request.POST.get('Caption')
        land.category = MainCategory.objects.get(id=request.POST.get('category'))
        land.total_land = request.POST.get('total_land')
        land.price = request.POST.get('price')
        land.space_area = request.POST.get('space_area')
        land.address = request.POST.get('address')
        land.description = request.POST.get('description')
        
        land.land_mark = request.POST.get('land_mark')
        land.sequrity_deposit = request.POST.get('sequrity_deposit')
        land.Time_perioud = request.POST.get('Time_perioud')
        land.location = request.POST.get('location')
        land.username = request.POST.get('username')
        land.contact = request.POST.get('contact')
        land.status = request.POST.get('status')
        land.disabled = bool(request.POST.get('disabled'))

        if request.FILES.get('image'):
            land.image = request.FILES.get('image')
        if request.FILES.get('screenshot'):
            land.screenshot = request.FILES.get('screenshot')

        land.save()

        for img in request.FILES.getlist('land_images'):
            LandImage.objects.create(land=land, image=img)

        return redirect(reverse('admin_panel') + '#land')

    return render(request, 'updateland.html', {'land': land, 'categories': categories})


def land_delete(request, pk: UUID):
    land = get_object_or_404(Land, pk=pk)
    if request.method == 'POST':
        land.delete()
        return redirect(reverse('admin_panel') + '#land')
    return render(request, 'land_confirm_delete.html', {'land': land})

def commercial_create(request):
    categories = MainCategory.objects.all()

    if request.method == 'POST':
        commercial = Commercial(
            Caption=request.POST.get('Caption'),
            category_id=request.POST.get('category'),
            total_land=request.POST.get('total_land'),
            price=request.POST.get('price'),
            address=request.POST.get('address'),
            description=request.POST.get('description'),
            land_mark=request.POST.get('land_mark'),
            sequrity_deposit=request.POST.get('sequrity_deposit'),
            Time_perioud=request.POST.get('Time_perioud'),
            location=request.POST.get('location'),
            username=request.POST.get('username'),
            contact=request.POST.get('contact'),
            status=request.POST.get('status'),
            disabled=bool(request.POST.get('disabled')),
            amenities=request.POST.get('amenities'),
            image=request.FILES.get('image'),
            screenshot=request.FILES.get('screenshot'),
        )
        commercial.save()

        # ✅ Save additional commercial images
        for img in request.FILES.getlist('commercial_images'):
            CommercialImage.objects.create(commercial=commercial, image=img)

        messages.success(request, "Commercial property created successfully!")
        return redirect(reverse('admin_panel') + '#commercial')

    return render(request, 'createcoms.html', {'categories': categories})

def commercial_update(request, pk):
    commercial = get_object_or_404(Commercial, pk=pk)
    categories = MainCategory.objects.all()

    if request.method == 'POST':
        commercial.Caption = request.POST.get('Caption')
        commercial.category_id = request.POST.get('category')
        commercial.total_land = request.POST.get('total_land')
        commercial.price = request.POST.get('price')
        commercial.address = request.POST.get('address')
        commercial.description = request.POST.get('description')
        commercial.land_mark = request.POST.get('land_mark')
        commercial.sequrity_deposit = request.POST.get('sequrity_deposit')
        commercial.Time_perioud = request.POST.get('Time_perioud')
        commercial.location = request.POST.get('location')
        commercial.username = request.POST.get('username')
        commercial.contact = request.POST.get('contact')
        commercial.status = request.POST.get('status')
        commercial.disabled = bool(request.POST.get('disabled'))
        commercial.amenities = request.POST.get('amenities')

        if request.FILES.get('image'):
            commercial.image = request.FILES.get('image')
        if request.FILES.get('screenshot'):
            commercial.screenshot = request.FILES.get('screenshot')

        commercial.save()

        # Save new images
        for img in request.FILES.getlist('commercial_images'):
            CommercialImage.objects.create(commercial=commercial, image=img)

        messages.success(request, "Commercial updated successfully!")
        return redirect('commercial_update', pk=pk)

    return render(request, 'update_com.html', {'commercial': commercial, 'categories': categories})

def commercial_delete(request, pk):
    commercial = get_object_or_404(Commercial, pk=pk)
    commercial.delete()
    return redirect(reverse('admin_panel') + '#commercial')
def offplan_create(request):
    categories = MainCategory.objects.all()

    if request.method == 'POST':
        offplan = OffPlan(
            Caption=request.POST.get('Caption'),
            category_id=request.POST.get('category'),
            total_land=request.POST.get('total_land'),
            price=request.POST.get('price'),
            address=request.POST.get('address'),
            description=request.POST.get('description'),
            rooms=request.POST.get('rooms'),
            land_mark=request.POST.get('land_mark'),
            location=request.POST.get('location'),
            username=request.POST.get('username'),
            contact=request.POST.get('contact'),
            status=request.POST.get('status'),
            disabled=bool(request.POST.get('disabled')),
            image=request.FILES.get('image'),
            screenshot=request.FILES.get('screenshot'),
        )
        offplan.save()

        # ✅ Save additional images
        for img in request.FILES.getlist('offplan_images'):
            OffplanImage.objects.create(offplan=offplan, image=img)

        messages.success(request, "OffPlan property created successfully!")
        return redirect(reverse('admin_panel') + '#offplan')

    return render(request, 'createoffs.html', {'categories': categories})


def offplan_update(request, pk):
    offplan = get_object_or_404(OffPlan, pk=pk)
    categories = MainCategory.objects.all()

    if request.method == 'POST':
        offplan.Caption = request.POST.get('Caption')
        offplan.category_id = request.POST.get('category')
        offplan.total_land = request.POST.get('total_land')
        offplan.price = request.POST.get('price')
        offplan.address = request.POST.get('address')
        offplan.description = request.POST.get('description')
        offplan.land_mark = request.POST.get('land_mark')
        offplan.rooms = request.POST.get('rooms')
        offplan.sequrity_deposit = request.POST.get('sequrity_deposit')
        offplan.Time_perioud = request.POST.get('Time_perioud')
        offplan.location = request.POST.get('location')
        offplan.username = request.POST.get('username')
        offplan.contact = request.POST.get('contact')
        offplan.status = request.POST.get('status')
        offplan.disabled = bool(request.POST.get('disabled'))

        # Updating image and screenshot if provided
        if request.FILES.get('image'):
            offplan.image = request.FILES.get('image')
        if request.FILES.get('screenshot'):
            offplan.screenshot = request.FILES.get('screenshot')

        offplan.save()

        # Handling additional images
        for img in request.FILES.getlist('offplan_images'):
            OffplanImage.objects.create(offplan=offplan, image=img)

        # Success message after update
        messages.success(request, "OffPlan updated successfully!")

        # Redirect to the same page to prevent resubmission on refresh
        return redirect('offplan_update', pk=pk)

    return render(request, 'updateoff.html', {'offplan': offplan, 'categories': categories})
def offplan_delete(request, pk):
    offplan = get_object_or_404(OffPlan, pk=pk)
    offplan.delete()
    return redirect(reverse('admin_panel') + '#offplan')










def create_blog(request):
    if request.method == "POST":
        blog_head = request.POST.get("blog_head")
        modal_head = request.POST.get("modal_head")
        date = request.POST.get("date")
        card_paragraph = request.POST.get("card_paragraph")
        modal_paragraph = request.POST.get("modal_paragraph")
        image = request.FILES.get("image")

        Blog.objects.create(
            blog_head=blog_head,
            modal_head=modal_head,
            date=date,
            card_paragraph=card_paragraph,
            modal_paragraph=modal_paragraph,
            image=image,
        )
        return redirect(reverse('admin_panel') + '#blog')
    return render(request, "blogcreate.html")

# views.py
def update_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        blog.blog_head = request.POST.get("blog_head")
        blog.modal_head = request.POST.get("modal_head")
        blog.date = request.POST.get("date")
        blog.card_paragraph = request.POST.get("card_paragraph")
        blog.modal_paragraph = request.POST.get("modal_paragraph")
        if request.FILES.get("image"):
            blog.image = request.FILES.get("image")
        blog.save()
        return redirect("admin_panel")
    return render(request, "blog_update.html", {"blog": blog})

def delete_blog(request, pk):
    # Retrieve the blog by its primary key (pk)
    blog = get_object_or_404(Blog, pk=pk)
    
    # Delete the blog instance
    blog.delete()
    
    # Redirect to the admin panel with the fragment identifier '#blog' to scroll to the blog section
    return redirect(reverse('admin_panel') + '#blog')


def inbox_delete(request, pk):
    inbox_item = get_object_or_404(Inbox, pk=pk)
    inbox_item.delete()
    return redirect(reverse('admin_panel') + '#inbox')





def agent_house_delete(request, pk):
    house = get_object_or_404(AgentHouse, pk=pk)
    house.delete()
    messages.success(request, "Agent House deleted successfully.")
    return redirect(reverse('admin_panel') + '#agenthouse')

def agenthouse_detail(request, pk):
    house = get_object_or_404(AgentHouse, pk=pk)
    context = {'house': house}
    return render(request, 'agenthouse_detail.html', context)


def agent_land_delete(request, pk):
    land = get_object_or_404(AgentLand, pk=pk)
    land.delete()
    messages.success(request, "Agent Land deleted successfully.")
    return redirect(reverse('admin_panel') + '#agentland')

def agentland_detail(request, pk):
    land = get_object_or_404(AgentLand, pk=pk)
    context = {'land': land}
    return render(request, 'agentland_detail.html', context)

def agent_com_delete(request, pk):
    com = get_object_or_404(AgentCommercial, pk=pk)
    com.delete()
    messages.success(request, "Agent Land deleted successfully.")
    return redirect(reverse('admin_panel') + '#agentcom')

def agentcom_detail(request, pk):
    com = get_object_or_404(AgentCommercial, pk=pk)
    context = {'com': com}
    return render(request, 'agentcom_detail.html', context)

def agent_offplan_delete(request, pk):
    offplan = get_object_or_404(AgentOffPlan, pk=pk)
    offplan.delete()
    messages.success(request, "Agent Land deleted successfully.")
    return redirect(reverse('admin_panel') + '#agentland')

def agentoffplan_detail(request, pk):
    offplan = get_object_or_404(AgentOffPlan, pk=pk)
    context = {'offplan': offplan}
    return render(request, 'agentoff_detail.html', context)


def agent_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Save the credentials (note: storing plain text passwords is insecure)
        login = Login(username=username, password=password)
        login.save()

        messages.success(request, 'Registration successful!')
        return redirect('agent_register')  # Redirect back to the form
    return render(request, 'createlogin.html')

def login_delete(request, id):
    login = get_object_or_404(Login, pk=id)
    login.delete()
    messages.success(request, "Login deleted successfully!")
    return redirect(reverse('admin_panel') + '#login')




def userprofile_create(request):
    logins = Login.objects.all()
    if request.method == 'POST':
        login_id = request.POST.get('login')
        login = get_object_or_404(Login, id=login_id)

        UserProfile.objects.create(
            login=login,
            phone_number=request.POST.get('phone_number'),
            address=request.POST.get('address'),
            profile_image=request.FILES.get('profile_image'),
            pin_code=request.POST.get('pin_code'),
            email=request.POST.get('email'),
            is_agent=bool(request.POST.get('is_agent')),
            paid=bool(request.POST.get('paid')),
        )
        messages.success(request, "Profile created successfully!")
        return redirect('admin_panel')

    return render(request, 'createprofile.html', {'logins': logins})


