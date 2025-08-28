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
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.hashers import make_password 

from django.http import JsonResponse













# Create your views here.
# def admin_page(request):

#     return render(request, 'admin.html')

def base(request):
    agenthouse = agenthouse.objects.all()

    context ={
        'agenthouse': agenthouse
    }
    return render(request,'base2.html',context)




from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
def superuser_login_view(request):
    User = get_user_model()
    if request.method == 'POST':
        form = SuperuserLoginForm(request.POST)
        holder = User.objects.filter(is_superuser=True).first()
        if holder.rate_limit >= 5 and timezone.now() < holder.last_failed_login + timedelta(hours=5):
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



from uuid import UUID
from django.contrib import messages

from django.urls import reverse









def create_blog(request):
    blog = Blog.objects.all()
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
        return redirect(reverse('create_blog') )
    return render(request, "admin_blogs.html",{'blog':blog})


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
        return redirect("create_blog")
    return redirect("create_blog")


@require_POST
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return redirect("create_blog")


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










def categories(request):
    categories = Category.objects.all()
    purposes = Purpose.objects.all()

    if request.method == 'POST':
        # Handle Category Add/Delete
        if 'add' in request.POST and 'name' in request.POST:
            name = request.POST.get('name')
            if name:
                Category.objects.create(name=name)
            return redirect('categories')

        if 'delete' in request.POST and 'category_id' in request.POST:
            category_id = request.POST.get('category_id')
            Category.objects.filter(id=category_id).delete()
            return redirect('categories')

        # Handle Purpose Add/Delete
        if 'add' in request.POST and 'purposename' in request.POST:
            name = request.POST.get('purposename')
            if name:
                Purpose.objects.create(name=name)
            return redirect('categories')

        if 'delete' in request.POST and 'purpose_id' in request.POST:
            purpose_id = request.POST.get('purpose_id')
            Purpose.objects.filter(id=purpose_id).delete()
            return redirect('categories')

    return render(request, 'admin_categories.html', {
        'categories': categories,
        'purposes': purposes
    })



def add_property(request):
    categories = Category.objects.all()
    purposes = Purpose.objects.all()
    properties = Property.objects.all()

    if request.method == "POST":
        category_id = request.POST.get("category")
        purpose_id = request.POST.get("purpose")

        amenities = request.POST.getlist('amenities')
        amenities_str = ", ".join([a.strip() for a in amenities if a.strip()])


        uploaded_images = request.FILES.getlist("images")
        main_image = uploaded_images[0] if uploaded_images else None  

        property_obj = Property.objects.create(
            category_id=category_id,
            purpose_id=purpose_id,
            label=request.POST.get("label"),
            land_area=request.POST.get("land_area"),
            sq_ft=request.POST.get("sq_ft"),
            description=request.POST.get("description"),
            amenities=amenities_str,
            image=main_image,
            perprice=request.POST.get("perprice"),
            price=request.POST.get("price"),
            owner=request.POST.get("owner"),
            whatsapp=request.POST.get("whatsapp"),
            phone=request.POST.get("phone"),
            location=request.POST.get("location"),
            city=request.POST.get("city"),
            pincode=request.POST.get("pincode"),
            district=request.POST.get("district"),
            land_mark=request.POST.get("land_mark"),
            paid=request.POST.get("paid"),
            added_by=request.POST.get("added_by"),
            # ✅ Ensure integer
            duration_days=int(request.POST.get("duration_days") or 30),
        )


        # ✅ Save extra images
        for extra_img in uploaded_images[1:]:
            PropertyImage.objects.create(property=property_obj, image=extra_img)

        return redirect("add_property")

    return render(request, "admin_propertylistings.html", {
        "categories": categories,
        "purposes": purposes,
        "properties": properties,
    })


@require_POST
def edit_property(request, property_id):
    prop = get_object_or_404(Property, id=property_id)

    category_id = request.POST.get("category")
    purpose_id = request.POST.get("purpose")
    prop.label = request.POST.get('label')
    prop.land_area = request.POST.get("land_area")
    prop.sq_ft = request.POST.get("sq_ft")
    prop.description = request.POST.get("description")
    amenities = request.POST.get("amenities")
    prop.amenities = amenities
    prop.perprice = request.POST.get("perprice")
    prop.price = request.POST.get("price")
    prop.owner = request.POST.get("owner")
    prop.whatsapp = request.POST.get("whatsapp")
    prop.phone = request.POST.get("phone")
    prop.location = request.POST.get("location")
    prop.city = request.POST.get("city")
    prop.pincode = request.POST.get("pincode")
    prop.land_mark = request.POST.get("land_mark")
    prop.paid = request.POST.get("paid") == "Yes"
    prop.added_by = request.POST.get("added_by")

    # 🔥 Cast to int to avoid TypeError
    duration_days = request.POST.get("duration_days")
    if duration_days:
        try:
            prop.duration_days = int(duration_days)
        except ValueError:
            prop.duration_days = 0  # fallback if bad input

    if category_id:
        prop.category = get_object_or_404(Category, id=category_id)
    if purpose_id:
        prop.purpose = get_object_or_404(Purpose, id=purpose_id)

    prop.save()

    # ✅ Handle multiple new images
    images = request.FILES.getlist("images")
    if images:
        for img in images:
            PropertyImage.objects.create(property=prop, image=img)

    # ✅ Handle image deletions
    delete_images = request.POST.getlist("delete_images")  # comes from checkboxes/hidden inputs
    if delete_images:
        for img_id in delete_images:
            try:
                image_obj = PropertyImage.objects.get(id=img_id, property=prop)
                image_obj.delete()
            except PropertyImage.DoesNotExist:
                pass

    messages.success(request, "Property updated successfully.")
    return redirect('add_property')




@require_POST
def delete_property(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    prop.delete()
    return redirect('add_property')



# def agents_login(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         speacialised = request.POST.get("speacialised")
#         phone = request.POST.get("phone")
#         whatsapp = request.POST.get("whatsapp")
#         email = request.POST.get("email")
#         location = request.POST.get("location")
#         city = request.POST.get("city")
#         pincode = request.POST.get("pincode")
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         image = request.FILES.get("image")  # ✅ file comes from request.FILES

#         Premium.objects.create(
#             name=name,
#             speacialised=speacialised,
#             phone=phone,
#             whatsapp=whatsapp,
#             email=email,
#             location=location,
#             city=city,
#             pincode=pincode,
#             username=username,
#             password=make_password(password),  # ✅ store securely
#             image=image  # ✅ CloudinaryField can take this directly
#         )

#         messages.success(request, "Premium Agent created successfully!")
#         return redirect("agents_login")

#     return render(request, "admin_agentlogin.html")



def agents_login(request):
    if request.method == "POST":
        if "username" in request.POST:   # Premium Agent Login form
            name = request.POST.get("name")
            speacialised = request.POST.get("speacialised")
            phone = request.POST.get("phone")
            whatsapp = request.POST.get("whatsapp")
            email = request.POST.get("email")
            location = request.POST.get("location")
            city = request.POST.get("city")
            pincode = request.POST.get("pincode")
            username = request.POST.get("username")
            password = request.POST.get("password")
            image = request.FILES.get("image")
            duration_days = request.POST.get("duration_days")  # ✅ from POST, not FILES

            # optional: check duplicate username
            if Premium.objects.filter(username=username).exists():
                messages.error(request, "❌ This username is already registered.")
                return redirect("agents_login")

            Premium.objects.create(
                name=name,
                speacialised=speacialised,
                phone=phone,
                whatsapp=whatsapp,
                email=email,
                location=location,
                city=city,
                pincode=pincode,
                username=username,
                password=make_password(password),
                image=image,
                duration_days=duration_days,
                created_at=timezone.now()
            )
            messages.success(request, "✅ Premium Agent created successfully!")

        elif "agentname" in request.POST:   # ✅ Normal Agent form
            agentsname = request.POST.get("agentname")
            agentsspeacialised = request.POST.get("agentspeacialised")
            agentsphone = request.POST.get("agentphone")
            agentswhatsapp = request.POST.get("agentwhatsapp")
            agentsemail = request.POST.get("agentemail")
            agentslocation = request.POST.get("agentlocation")
            agentsimage = request.FILES.get("agentsimage")  # ✅ file input

            # optional: avoid duplicate phone numbers
            if Agents.objects.filter(agentsphone=agentsphone).exists():
                messages.error(request, "❌ This phone number is already registered.")
                return redirect("agents_login")

            Agents.objects.create(
                agentsname=agentsname,
                agentsspeacialised=agentsspeacialised,
                agentsphone=agentsphone,
                agentswhatsapp=agentswhatsapp,
                agentsemail=agentsemail,
                agentslocation=agentslocation,
                agentsimage=agentsimage   # ✅ matches your model
            )
            messages.success(request, "✅ Agent added successfully!")

    return render(request, "admin_agentlogin.html")



def admin_premiumagents(request):
    premium = Premium.objects.all()
    return render(request, 'admin_premiumagents.html',{'premium':premium})

def admin_agents(request):
    premium = Premium.objects.all()
    agents = Agents.objects.all()
    return render(request, 'admin_agents.html',{'premium':premium, 'agents':agents})




def edit_premium(request, pk):
    premium = get_object_or_404(Premium, pk=pk)

    if request.method == "POST":
        premium.name = request.POST.get("name", premium.name)
        premium.speacialised = request.POST.get("speacialised", premium.speacialised)
        premium.phone = request.POST.get("phone", premium.phone)
        premium.whatsapp = request.POST.get("whatsapp", premium.whatsapp)
        premium.email = request.POST.get("email", premium.email)
        premium.location = request.POST.get("location", premium.location)
        premium.city = request.POST.get("city", premium.city)

        if "image" in request.FILES:
            premium.image = request.FILES["image"]

        premium.save()

        return redirect("admin_premiumagents")  # redirect back to list page

    return render(request, "admin_premiumagents.html", {"premium": premium})


# ✨ Delete Premium Agent
def delete_premium(request, pk):
    premium = get_object_or_404(Premium, pk=pk)
    premium.delete()
    messages.success(request, "🗑️ Premium Agent deleted successfully!")
    return redirect("admin_premiumagents")



def edit_agent(request, pk):
    agent = get_object_or_404(Agents, pk=pk)
    if request.method == "POST":
        agent.agentsname = request.POST.get("name")
        agent.agentsspeacialised = request.POST.get("specialised")
        agent.agentsphone = request.POST.get("phone")
        agent.agentswhatsapp = request.POST.get("whatsapp")
        agent.agentsemail = request.POST.get("email")
        agent.agentslocation = request.POST.get("location")

        if request.FILES.get("image"):
            agent.agentsimage = request.FILES.get("image")

        agent.save()
        messages.success(request, "✅ Agent updated successfully!")
        return redirect("admin_agents")  # adjust to your listing page

    return redirect("admin_agents")


def delete_agent(request, pk):
    agent = get_object_or_404(Agents, pk=pk)
    agent.delete()
    messages.success(request, "🗑️ Agent deleted successfully!")
    return redirect("admin_agents")


def admin_contact(request):
    contact_list = Contact.objects.all().order_by("-created_at")  # latest first
    
    # pagination: 10 contacts per page
    paginator = Paginator(contact_list, 1)
    page_number = request.GET.get("page")
    contacts = paginator.get_page(page_number)

    return render(request, 'admin_contact.html', {'contacts': contacts})



def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    messages.success(request, "🗑️ Contact deleted successfully!")
    return redirect("admin_contact")



def admin_message(request):
    message_list = Inbox.objects.all().order_by("-created_at")  # latest first
    
    # pagination: 10 per page
    paginator = Paginator(message_list, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  

    return render(request, 'admin_messagebox.html', {'page_obj': page_obj})


def delete_message(request, pk):
    message = get_object_or_404(Inbox, pk=pk)
    message.delete()
    messages.success(request, "🗑️ Message deleted successfully!")  # flash message
    return redirect("admin_message")



def admin_agent_reg(request):
    agent_list = AgentForm.objects.all().order_by("-created_at")  # latest first
    
    paginator = Paginator(agent_list, 1)  # paginate (2 per page for testing)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  

    return render(request, 'admin_agentsregisterations.html', {'page_obj': page_obj})


def delete_agent_reg(request, pk):
    agent = get_object_or_404(AgentForm, pk=pk)
    agent.delete()
    messages.success(request, "🗑️ Agent deleted successfully!")
    return redirect("agent_reg")



def admin_property_list(request):
    property_list = Propertylist.objects.all().order_by("-created_at")  # latest first
    
    paginator = Paginator(property_list, 1)  # paginate (2 per page for testing)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  

    return render(request, 'admin_propertyregisterations.html', {'page_obj': page_obj})


def delete_property_list(request, pk):
    property_list = get_object_or_404(Propertylist, pk=pk)
    property_list.delete()
    messages.success(request, "🗑️ Property deleted successfully!")
    return redirect("admin_property_list")


def admin_request(request):
    requestforms = Request.objects.all().order_by("-created_at")  # latest first
    
    paginator = Paginator(requestforms, 1)  # paginate (2 per page for testing)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  

    return render(request, 'admin_requestform.html', {'page_obj': page_obj})


def delete_requestforms(request, pk):
    requestforms = get_object_or_404(Request, pk=pk)
    requestforms.delete()
    messages.success(request, "🗑️ Property deleted successfully!")
    return redirect("requestforms")


def expired_property(request):
    expired = ExpiredProperty.objects.all()
    category = Category.objects.all()
    purpose = Purpose.objects.all()
    return render(request, 'admin_expiredproperties.html',{
        'property': expired,
        'category': category,
        'purpose':purpose
        })


@require_POST
def edit_exproperty(request, property_id):
    prop = get_object_or_404(ExpiredProperty, id=property_id)

    category_id = request.POST.get("category")
    purpose_id = request.POST.get("purpose")
    prop.label = request.POST.get('label')
    prop.land_area = request.POST.get("land_area")
    prop.sq_ft = request.POST.get("sq_ft")
    prop.description = request.POST.get("description")
    prop.amenities = request.POST.get("amenities")
    prop.perprice = request.POST.get("perprice")
    prop.price = request.POST.get("price")
    prop.owner = request.POST.get("owner")
    prop.whatsapp = request.POST.get("whatsapp")
    prop.phone = request.POST.get("phone")
    prop.location = request.POST.get("location")
    prop.city = request.POST.get("city")
    prop.pincode = request.POST.get("pincode")
    prop.land_mark = request.POST.get("land_mark")
    prop.paid = request.POST.get("paid") == "Yes"
    prop.added_by = request.POST.get("added_by")

    # Duration
    duration_days = request.POST.get("duration_days")
    if duration_days:
        try:
            prop.duration_days = int(duration_days)
        except ValueError:
            prop.duration_days = 0

    if category_id:
        prop.category = get_object_or_404(Category, id=category_id)
    if purpose_id:
        prop.purpose = get_object_or_404(Purpose, id=purpose_id)

    prop.save()

    # Handle new images
    for img in request.FILES.getlist("images"):
        PropertyImage.objects.create(expired_property=prop, image=img)

    # Handle image deletions
    for img_id in request.POST.getlist("delete_images"):
        try:
            image_obj = PropertyImage.objects.get(id=img_id, expired_property=prop)
            image_obj.delete()
        except PropertyImage.DoesNotExist:
            pass

    messages.success(request, "Property updated successfully.")
    return redirect('expired_property')



@require_POST
def delete_property(request, pk):
    prop = get_object_or_404(ExpiredProperty, pk=pk)
    prop.delete()
    return redirect('expired_property')











