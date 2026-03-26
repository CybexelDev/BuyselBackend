from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

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

from django.db.models import Count
from django.db.models import Q, CharField
from django.db.models.functions import Cast
from django.utils.timezone import make_aware
from datetime import datetime
from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache










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
    form = SuperuserLoginForm(request.POST or None)
    holder = User.objects.filter(is_superuser=True).first()

    if request.method == 'POST':
        if holder and holder.rate_limit >= 5 and timezone.now() < holder.last_failed_login + timedelta(hours=2):
            messages.error(request, "Too many failed attempts. Try again later.")
        else:
            if holder and holder.rate_limit >= 5:
                holder.rate_limit = 0
                holder.save()

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)

                if user and user.is_superuser:
                    if holder:
                        holder.rate_limit = 0
                        holder.save()
                    login(request, user)
                    return redirect(reverse('dashboard'))  # ✅ redirect to dashboard
                else:
                    if holder:
                        holder.rate_limit += 1
                        holder.last_failed_login = timezone.now()
                        holder.save()
                    messages.error(request, 'Invalid credentials or not a superuser.')

    return render(request, 'login.html', {'form': form})


# ✅ Dashboard view (only for logged-in superusers)
def superuser_required(user):
    return user.is_authenticated and user.is_superuser


@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def Dashboard(request):
    # ✅ Total properties
    total_active = Property.objects.count()
    total_expired = ExpiredProperty.objects.count()
    total_all = total_active + total_expired

    # ✅ Get list of all purposes (for dynamic table headers)
    all_purposes = list(Property.objects.values_list("purpose__name", flat=True).distinct())

    # ✅ Active properties by purpose
    active_by_purpose = (
        Property.objects.values("purpose__name")
        .annotate(total=Count("id"))
        .order_by("purpose__name")
    )

    # ✅ Premium agent report
    premium_report = []
    premiums = Premium.objects.annotate(total_properties=Count("properties"))
    for idx, premium in enumerate(premiums, start=1):
        # Build purpose → total mapping
        purpose_map = {p: 0 for p in all_purposes}
        purpose_counts = (
            AgentProperty.objects.filter(agent=premium)
            .values("purpose__name")
            .annotate(total=Count("id"))
        )
        for pc in purpose_counts:
            purpose_map[pc["purpose__name"]] = pc["total"]

        premium_report.append({
            "sl_no": idx,
            "premium_name": premium.name,
            "total_properties": premium.total_properties,
            "purpose_map": purpose_map,
        })

    context = {
        "total_active": total_active,
        "total_expired": total_expired,
        "total_all": total_all,
        "all_purposes": all_purposes,      # ✅ purposes for table headers
        "premium_report": premium_report,  # ✅ agent data
        "active_by_purpose": active_by_purpose,
    }

    return render(request, "admin_dashboard.html", context)





from django.contrib.auth import logout

def superuser_logout_view(request):
    logout(request)
    return redirect('superuser_login_view')  



from uuid import UUID
from django.contrib import messages

from django.urls import reverse





@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
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
        return redirect(reverse('create_blog'))

    # ✅ Pagination
    blog_list = Blog.objects.all().order_by("-id")   # latest first
    paginator = Paginator(blog_list, 10)  # 5 blogs per page

    page_number = request.GET.get("page")
    blog_page = paginator.get_page(page_number)

    return render(request, "admin_blogs.html", {
        'blog': blog_page
    })

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
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

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
@require_POST
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return redirect("create_blog")







@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def categories(request):

    categories = Category.objects.all().order_by("-id")
    purposes = Purpose.objects.all().order_by("-id")
    subcategories = Subcategory.objects.select_related("category").all().order_by("-id")
    subcategory_fields = SubcategoryField.objects.select_related(
        "subcategory", "subcategory__category"
    ).all().order_by("-id")

    if request.method == 'POST':
        action = request.POST.get('action')

        # =========================
        # CATEGORY
        # =========================
        if action == 'add_category':
            name = request.POST.get('name')
            icon = request.FILES.get('icon')

            if name and icon:
                Category.objects.create(name=name, icon=icon)

        elif action == 'edit_category':
            category = get_object_or_404(Category, id=request.POST.get('category_id'))
            category.name = request.POST.get('name')

            if request.FILES.get('icon'):
                category.icon = request.FILES.get('icon')

            category.save()

        elif action == 'delete_category':
            Category.objects.filter(id=request.POST.get('category_id')).delete()

        # =========================
        # PURPOSE
        # =========================
        elif action == 'add_purpose':
            name = request.POST.get('name')
            if name:
                Purpose.objects.create(name=name)

        elif action == 'edit_purpose':
            purpose = get_object_or_404(Purpose, id=request.POST.get('purpose_id'))
            purpose.name = request.POST.get('name')
            purpose.save()

        elif action == 'delete_purpose':
            Purpose.objects.filter(id=request.POST.get('purpose_id')).delete()

        # =========================
        # SUBCATEGORY
        # =========================
        elif action == 'add_subcategory':
            name = request.POST.get('name')
            category_id = request.POST.get('category_id')
            image = request.FILES.get('image')

            if name and category_id:
                Subcategory.objects.create(
                    name=name,
                    category_id=category_id,
                    image=image
                )

        elif action == 'edit_subcategory':
            sub = get_object_or_404(Subcategory, id=request.POST.get('subcategory_id'))

            sub.name = request.POST.get('name')
            sub.category_id = request.POST.get('category_id')

            if request.FILES.get('image'):
                sub.image = request.FILES.get('image')

            sub.save()

        elif action == 'delete_subcategory':
            Subcategory.objects.filter(id=request.POST.get('subcategory_id')).delete()

        # =========================
        # SUBCATEGORY FIELDS
        # =========================
        elif action == "add_field":
            SubcategoryField.objects.create(
                subcategory_id=request.POST.get("subcategory_id"),
                field_name=request.POST.get("field_name"),
                field_type=request.POST.get("field_type"),
                required=request.POST.get("required") == "on",
                icon=request.FILES.get("icon")
            )

        elif action == "edit_field":
            field = get_object_or_404(SubcategoryField, id=request.POST.get("field_id"))

            field.subcategory_id = request.POST.get("subcategory_id")
            field.field_name = request.POST.get("field_name")
            field.field_type = request.POST.get("field_type")
            field.required = request.POST.get("required") == "on"

            if request.FILES.get("icon"):
                field.icon = request.FILES.get("icon")

            field.save()

        elif action == "delete_field":
            SubcategoryField.objects.filter(id=request.POST.get("field_id")).delete()

        return redirect('categories')

    return render(request, 'admin_categories.html', {
        'categories': categories,
        'purposes': purposes,
        'subcategories': subcategories,
        'subcategory_fields': subcategory_fields,
    })


from django.core.paginator import Paginator

import re

def parse_listing(listing_text):
    result = {}

    if not listing_text:
        return result

    parts = listing_text.split("/")

    for part in parts:
        part = part.strip()

        # ✅ FIXED REGEX (only words, no greedy capture)
        match = re.match(r'(\d+)\s+([a-zA-Z ]+)', part)

        if match:
            count = int(match.group(1))
            category = match.group(2).strip().lower()

            result[category] = count

    return result

def can_add_property(owner, category, purpose):

    # 🔥 UPGRADE PLAN
    if owner.upgrade_plan:

        listing_data = parse_listing(owner.upgrade_plan.listing)

        category_name = category.name.lower()

        # 🔥 FLEXIBLE MATCH (important fix)
        allowed_count = 0
        for key in listing_data:
            if key in category_name:
                allowed_count = listing_data[key]
                break

        current_count = Property.objects.filter(
            owner=owner,
            category__name__iexact=category.name
        ).count()

        print("DEBUG UPGRADE:", listing_data, allowed_count, current_count)

        if allowed_count == 0:
            return False, f"No listing allowed for {category.name}"

        if current_count >= allowed_count:
            return False, f"{category.name} limit reached"

        return True, None

    # 🔥 NORMAL PLAN
    if owner.user_plans.exists():

        plan = owner.user_plans.first()

        total = Property.objects.filter(owner=owner).count()

        print("DEBUG BASIC PLAN:", total)

        if total >= 2:
            return False, "Only 2 properties allowed for basic plan"

        return True, None

    return False, "No active plan found"


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.http import HttpResponse
import traceback


@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def add_property(request):

    categories = Category.objects.all()
    purposes = Purpose.objects.all()
    amenities_list = Amenities.objects.all()
    plans = Userplan.objects.all()
    users = UserAdd.objects.filter(is_active=True)

    properties = Property.objects.all().order_by('-created_at')

    paginator = Paginator(properties, 15)
    page_number = request.GET.get('page', 1)
    properties = paginator.get_page(page_number)

    if request.method == "POST":
        try:
            print("🔥 STARTING PROPERTY SAVE")

            category_id = request.POST.get("category")
            subcategory_id = request.POST.get("subcategory") or None
            purpose_id = request.POST.get("purpose")
            owner_id = request.POST.get("owner")

            # ✅ REQUIRED VALIDATION
            if not all([category_id, purpose_id, owner_id]):
                messages.error(request, "Missing required fields")
                return redirect("add_property")

            category = Category.objects.get(id=category_id)
            purpose = Purpose.objects.get(id=purpose_id)
            owner = UserAdd.objects.get(id=owner_id)

            # ✅ PLAN CHECK
            can_add, error = can_add_property(owner, category, purpose)
            if not can_add:
                messages.error(request, error)
                return redirect("add_property")

            # ✅ IMAGES
            uploaded_images = request.FILES.getlist("images")
            main_image = uploaded_images[0] if uploaded_images else None

            # 🔥 OPTIONAL: enforce image
            if not main_image:
                messages.error(request, "Main image is required")
                return redirect("add_property")

            # ✅ DYNAMIC FIELDS
            dynamic_fields = {}

            if subcategory_id:
                fields = SubcategoryField.objects.filter(subcategory_id=subcategory_id)

                for field in fields:
                    key = f"field_{field.id}"

                    if field.field_type == "boolean":
                        value = key in request.POST
                    else:
                        value = request.POST.get(key)

                    dynamic_fields[field.field_name] = {
                        "id": field.id,
                        "value": value
                    }

            # ✅ PACKAGE
            package = owner.user_plans.first() if owner.user_plans.exists() else None

            # ✅ DURATION
            duration_days = 30
            if owner.upgrade_plan:
                duration_days = owner.upgrade_plan.validity
            elif package:
                duration_days = package.validity

            # ✅ CREATE PROPERTY
            property_obj = Property.objects.create(
                category=category,
                subcategory_id=subcategory_id if subcategory_id else None,
                purpose=purpose,
                dynamic_fields=dynamic_fields,

                label=request.POST.get("label"),
                land_area=request.POST.get("land_area"),
                sq_ft=request.POST.get("sq_ft"),

                description=request.POST.get("description"),
                message=request.POST.get("message"),

                image=main_image,

                perprice=request.POST.get("perprice"),
                price=request.POST.get("price"),

                owner=owner,
                package=package,   # ✅ FIXED (removed plan)

                whatsapp=request.POST.get("whatsapp"),
                phone=request.POST.get("phone"),

                location=request.POST.get("location"),

                city=request.POST.get("city"),
                pincode=request.POST.get("pincode"),
                district=request.POST.get("district"),
                taluk=request.POST.get("taluk"),
                village=request.POST.get("village"),
                state=request.POST.get("state"),

                land_mark=request.POST.get("land_mark"),
                paid="no",

                added_by=request.POST.get("added_by"),
                market_staff=request.POST.get("market_staff"),

                duration_days=duration_days,
                note=request.POST.get("note") or "",
            )

            print("✅ PROPERTY SAVED:", property_obj.id)

            # ✅ AMENITIES
            amenities = request.POST.getlist("amenities")
            if amenities:
                property_obj.amenities.set(amenities)

            # ✅ MULTIPLE IMAGES
            for img in uploaded_images:
                PropertyImage.objects.create(
                    property=property_obj,
                    image=img
                )

            messages.success(request, "Property added successfully")

        except Exception as e:
            traceback.print_exc()
            return HttpResponse(f"ERROR: {str(e)}")  # 🔥 shows real error

        return redirect("add_property")

    return render(request, "admin_propertylistings.html", {
        "categories": categories,
        "purposes": purposes,
        "amenities": amenities_list,
        "properties": properties,
        "users": users,
        "plans": plans
    })


def get_subcategories(request, category_id):
    subs = Subcategory.objects.filter(category_id=category_id)
    return JsonResponse([{"id": s.id, "name": s.name} for s in subs], safe=False)


def get_subcategory_fields(request, subcategory_id):
    fields = SubcategoryField.objects.filter(subcategory_id=subcategory_id)

    return JsonResponse([
        {
            "id": f.id,
            "name": f.field_name,
            "type": f.field_type,
            "icon": f.icon.url if f.icon else ""
        } for f in fields
    ], safe=False)





@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
@require_POST
def edit_property(request, property_id):
    prop = get_object_or_404(Property, id=property_id)

    # --- Basic Fields ---
    prop.label = request.POST.get("label")
    prop.land_area = request.POST.get("land_area")
    prop.sq_ft = request.POST.get("sq_ft")
    prop.description = request.POST.get("description")
    prop.message = request.POST.get("message")  # ✅ ADDED
    prop.amenities = request.POST.get("amenities")
    prop.perprice = request.POST.get("perprice")
    prop.price = request.POST.get("price")
    prop.owner = request.POST.get("owner")
    prop.whatsapp = request.POST.get("whatsapp")
    prop.phone = request.POST.get("phone")
    prop.location = request.POST.get("location")
    prop.city = request.POST.get("city")
    prop.district = request.POST.get("district")
    prop.village = request.POST.get("village")
    prop.taluk = request.POST.get("taluk")
    prop.state = request.POST.get("state")
    prop.pincode = request.POST.get("pincode")
    prop.land_mark = request.POST.get("land_mark")
    prop.added_by = request.POST.get("added_by")
    prop.market_staff = request.POST.get("market_staff")

    # --- Paid (safe boolean handling) ---
    paid_value = request.POST.get("paid")
    prop.paid = True if paid_value in ["True", "Yes", "1"] else False

    # --- Category & Purpose ---
    category_id = request.POST.get("category")
    purpose_id = request.POST.get("purpose")

    if category_id:
        prop.category = get_object_or_404(Category, id=category_id)

    if purpose_id:
        prop.purpose = get_object_or_404(Purpose, id=purpose_id)

    # --- Duration Days ---
    duration_days = request.POST.get("duration_days")
    if duration_days:
        try:
            prop.duration_days = int(duration_days)
        except ValueError:
            pass

    # --- MANUAL SCREENSHOT UPLOAD ---
    screenshot_file = request.FILES.get("manual_screenshot")
    if screenshot_file:
        prop.screenshot = screenshot_file  # overwrite old screenshot

    # Save all updates BEFORE images
    prop.save()

    # --- ADD NEW IMAGES ---
    new_images = request.FILES.getlist("images")
    for img in new_images:
        PropertyImage.objects.create(property=prop, image=img)

    # --- DELETE SELECTED IMAGES ---
    delete_images = request.POST.getlist("delete_images")
    for img_id in delete_images:
        PropertyImage.objects.filter(id=img_id, property=prop).delete()

    messages.success(request, "Property updated successfully.")
    return redirect("add_property")



@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
@require_POST
def delete_property(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    prop.delete()
    return redirect('add_property')



@user_passes_test(superuser_required, login_url='superuser_login_view')
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

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_premiumagents(request):

    search_query = request.GET.get("search", "").strip()
    from_date = request.GET.get("from_date", "")
    to_date = request.GET.get("to_date", "")

    all_premium = Premium.objects.all()

    # -------------------------
    # 🔍 TEXT SEARCH
    # -------------------------
    if search_query:
        all_premium = all_premium.annotate(
            created_str=Cast("created_at", output_field=CharField()),
            duration_str=Cast("duration_days", output_field=CharField()),
        ).filter(
            Q(name__icontains=search_query) |
            Q(speacialised__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(whatsapp__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(pincode__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(created_str__icontains=search_query) |
            Q(duration_str__icontains=search_query)
        )

    # -------------------------
    # 📅 DATE RANGE FILTER
    # -------------------------
    if from_date:
        all_premium = all_premium.filter(created_at__date__gte=from_date)

    if to_date:
        all_premium = all_premium.filter(created_at__date__lte=to_date)

    # Sort latest first
    all_premium = all_premium.order_by("-created_at")

    # Pagination
    paginator = Paginator(all_premium, 20)
    premium = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'admin_premiumagents.html', {
        'premium': premium,
        'search_query': search_query,
        'from_date': from_date,
        'to_date': to_date,
    })


@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_agents(request):

    search_query = request.GET.get("search", "").strip()
    from_date = request.GET.get("from_date", "")
    to_date = request.GET.get("to_date", "")

    # Base Querysets
    all_premium = Premium.objects.all()
    all_agents = Agents.objects.all()

    # ------------------------------
    # 🔍 TEXT SEARCH (Both tables)
    # ------------------------------
    if search_query:

        # Premium search
        all_premium = all_premium.annotate(
            created_str=Cast("created_at", output_field=CharField()),
            duration_str=Cast("duration_days", output_field=CharField()),
        ).filter(
            Q(name__icontains=search_query) |
            Q(speacialised__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(whatsapp__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(pincode__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(created_str__icontains=search_query)
        )

        # Agents search
        all_agents = all_agents.annotate(
            created_str=Cast("created_at", output_field=CharField()),
            duration_str=Cast("duration_days", output_field=CharField()),
        ).filter(
            Q(agentsname__icontains=search_query) |
            Q(agentsspeacialised__icontains=search_query) |
            Q(agentsphone__icontains=search_query) |
            Q(agentswhatsapp__icontains=search_query) |
            Q(agentsemail__icontains=search_query) |
            Q(agentslocation__icontains=search_query) |
            Q(agentscity__icontains=search_query) |
            Q(agentspincode__icontains=search_query) |
            Q(created_str__icontains=search_query)
        )

    # ------------------------------
    # 📅 DATE RANGE FILTER
    # ------------------------------
    if from_date:
        all_premium = all_premium.filter(created_at__date__gte=from_date)
        all_agents = all_agents.filter(created_at__date__gte=from_date)

    if to_date:
        all_premium = all_premium.filter(created_at__date__lte=to_date)
        all_agents = all_agents.filter(created_at__date__lte=to_date)

    # Sort both by latest first
    all_premium = all_premium.order_by("-created_at")
    all_agents = all_agents.order_by("-created_at")

    # ------------------------------
    # 📄 Pagination
    # ------------------------------
    premium_paginator = Paginator(all_premium, 10)
    agents_paginator = Paginator(all_agents, 20)

    premium_page_number = request.GET.get('premium_page', 1)
    agents_page_number = request.GET.get('agents_page', 1)

    premium = premium_paginator.get_page(premium_page_number)
    agents = agents_paginator.get_page(agents_page_number)

    return render(request, 'admin_agents.html', {
        'premium': premium,
        'agents': agents,
        'search_query': search_query,
        'from_date': from_date,
        'to_date': to_date,
    })




@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
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

        # 🔥 Convert to int to avoid TypeError
        premium.duration_days = int(
            request.POST.get("duration_days") or premium.duration_days
        )

        if "image" in request.FILES:
            premium.image = request.FILES["image"]

        premium.save()  # triggers auto-move to ExpiredPremium if duration <= 0

        return redirect("admin_premiumagents")

    return render(request, "admin_premiumagents.html", {"premium": premium})

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_premium(request, pk):
    premium = get_object_or_404(Premium, pk=pk)
    premium.delete()
    messages.success(request, "🗑️ Premium Agent deleted successfully!")
    return redirect("admin_premiumagents")


@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def edit_agent(request, pk):
    agent = get_object_or_404(Agents, pk=pk)
    if request.method == "POST":
        agent.agentsname = request.POST.get("name")
        agent.agentsspeacialised = request.POST.get("specialised")
        agent.agentsphone = request.POST.get("phone")
        agent.agentswhatsapp = request.POST.get("whatsapp")
        agent.agentsemail = request.POST.get("email")
        agent.agentslocation = request.POST.get("location")
        agent.agentspincode = request.POST.get("pincode")
        agent.duration_days = request.POST.get("duration_days")


        if request.FILES.get("image"):
            agent.agentsimage = request.FILES.get("image")

        agent.save()
        messages.success(request, "✅ Agent updated successfully!")
        return redirect("admin_agents")  # adjust to your listing page

    return redirect("admin_agents")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_agent(request, pk):
    agent = get_object_or_404(Agents, pk=pk)
    agent.delete()
    messages.success(request, "🗑️ Agent deleted successfully!")
    return redirect("admin_agents")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_contact(request):
    contact_list = Contact.objects.all().order_by("-created_at")  # latest first
    
    # pagination: 10 contacts per page
    paginator = Paginator(contact_list, 20)
    page_number = request.GET.get("page")
    contacts = paginator.get_page(page_number)

    return render(request, 'admin_contact.html', {'contacts': contacts})

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    messages.success(request, "🗑️ Contact deleted successfully!")
    return redirect("admin_contact")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_message(request):
    message_list = Inbox.objects.all().order_by("-created_at")  # latest first
    
    # pagination: 10 per page
    paginator = Paginator(message_list, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  

    return render(request, 'admin_messagebox.html', {'page_obj': page_obj})

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_message(request, pk):
    message = get_object_or_404(Inbox, pk=pk)
    message.delete()
    messages.success(request, "🗑️ Message deleted successfully!")  # flash message
    return redirect("admin_message")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_agent_reg(request):

    search_query = request.GET.get("search", "").strip()
    from_date = request.GET.get("from_date", "")
    to_date = request.GET.get("to_date", "")

    # Base query
    agent_list = AgentForm.objects.all()

    # ---------------------------------------
    # 🔍 TEXT SEARCH
    # ---------------------------------------
    if search_query:
        agent_list = agent_list.annotate(
            created_str=Cast("created_at", output_field=CharField())
        ).filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(Dealings__icontains=search_query) |
            Q(created_str__icontains=search_query)
        )

    # ---------------------------------------
    # 📅 DATE RANGE FILTER (Calendar)
    # ---------------------------------------
    if from_date:
        agent_list = agent_list.filter(created_at__date__gte=from_date)

    if to_date:
        agent_list = agent_list.filter(created_at__date__lte=to_date)

    # Sort latest first
    agent_list = agent_list.order_by("-created_at")

    # Pagination
    paginator = Paginator(agent_list, 20)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "admin_agentsregisterations.html", {
        "page_obj": page_obj,
        "search_query": search_query,
        "from_date": from_date,
        "to_date": to_date,
    })

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_agent_reg(request, pk):
    agent = get_object_or_404(AgentForm, pk=pk)
    agent.delete()
    messages.success(request, "🗑️ Agent deleted successfully!")
    return redirect("agent_reg")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_property_list(request):
    search_query = request.GET.get("search", "")
    from_date = request.GET.get("from_date", "")
    to_date = request.GET.get("to_date", "")

    properties = Propertylist.objects.all().order_by("-created_at")

    # Search filter
    if search_query:
        properties = properties.filter(
            Q(categories__icontains=search_query) |
            Q(purposes__icontains=search_query) |
            Q(label__icontains=search_query) |
            Q(owner__icontains=search_query) |
            Q(locations__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(District__icontains=search_query)
        )

    # Date filter
    if from_date:
        properties = properties.filter(created_at__date__gte=from_date)

    if to_date:
        properties = properties.filter(created_at__date__lte=to_date)

    # Pagination
    paginator = Paginator(properties, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "admin_propertyregisterations.html", {
        "page_obj": page_obj,
        "search_query": search_query,
        "from_date": from_date,
        "to_date": to_date,
    })

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_property_list(request, pk):
    property_list = get_object_or_404(Propertylist, pk=pk)
    property_list.delete()
    messages.success(request, "🗑️ Property deleted successfully!")
    return redirect("admin_property_list")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_request(request):
    requestforms = Request.objects.all().order_by("-created_at")  # latest first
    
    paginator = Paginator(requestforms, 20)  # paginate (2 per page for testing)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  

    return render(request, 'admin_requestform.html', {'page_obj': page_obj})

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_requestforms(request, pk):
    requestforms = get_object_or_404(Request, pk=pk)
    requestforms.delete()
    messages.success(request, "🗑️ Property deleted successfully!")
    return redirect("requestforms")




@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def expired_property(request):

    search = request.GET.get("search", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    expired_list = ExpiredProperty.objects.all().order_by('-id')

    # 🔍 SEARCH (including property_code)
    if search:
        expired_list = expired_list.filter(
            Q(property_code__icontains=search) |   # ✅ added
            Q(label__icontains=search) |
            Q(purpose__name__icontains=search) |
            Q(category__name__icontains=search) |
            Q(city__icontains=search) |
            Q(village__icontains=search) |
            Q(district__icontains=search) |
            Q(owner__icontains=search) |
            Q(phone__icontains=search) |
            Q(price__icontains=search)
        )

    # 📅 DATE RANGE FILTER
    if start_date:
        expired_list = expired_list.filter(created_at__date__gte=start_date)

    if end_date:
        expired_list = expired_list.filter(created_at__date__lte=end_date)

    # Pagination
    paginator = Paginator(expired_list, 20)
    page_number = request.GET.get('page')
    expired = paginator.get_page(page_number)

    return render(request, 'admin_expiredproperties.html', {
        'property': expired,
        'search': search,
        'start_date': start_date,
        'end_date': end_date,
    })

@never_cache
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

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
@require_POST
def delete_property(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    prop.delete()
    return redirect('add_property')


@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
@require_POST
def expired_property_delete(request, pk):
    prop = get_object_or_404(ExpiredProperty, pk=pk)
    prop.delete()
    return redirect('expired_property')



@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def edit_expirepremium(request, pk):
    premium = get_object_or_404(ExpiredPremium, pk=pk)

    if request.method == "POST":
        premium.name = request.POST.get("name", premium.name)
        premium.speacialised = request.POST.get("speacialised", premium.speacialised)
        premium.phone = request.POST.get("phone", premium.phone)
        premium.whatsapp = request.POST.get("whatsapp", premium.whatsapp)
        premium.email = request.POST.get("email", premium.email)
        premium.location = request.POST.get("location", premium.location)
        premium.city = request.POST.get("city", premium.city)

        # 🔥 Convert to int safely
        premium.duration_days = int(
            request.POST.get("duration_days") or premium.duration_days
        )

        if "image" in request.FILES:
            premium.image = request.FILES["image"]

        premium.save()  # triggers auto-move back to Premium if duration >= 1

        return redirect("expired_agent")

    return render(request, "admin_expiredagents.html", {"premium": premium})


# -----------------------------
# Expired Premium List with search & filters
# -----------------------------
@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def expire_premium(request):
    # ===== AGENTS SEARCH & FILTER =====
    agents_search = request.GET.get("agents_search", "")
    agents_from = request.GET.get("agents_from", "")
    agents_to = request.GET.get("agents_to", "")

    agents_list = ExpireAgents.objects.all().order_by('-id')

    if agents_search:
        agents_list = agents_list.filter(
            Q(agentsname__icontains=agents_search) |
            Q(agentsspeacialised__icontains=agents_search) |
            Q(agentsphone__icontains=agents_search) |
            Q(agentslocation__icontains=agents_search) |
            Q(agentscity__icontains=agents_search)
        )
    if agents_from:
        agents_list = agents_list.filter(created_at__date__gte=agents_from)
    if agents_to:
        agents_list = agents_list.filter(created_at__date__lte=agents_to)

    agents_paginator = Paginator(agents_list, 15)
    agents_page_number = request.GET.get('agents_page')
    agents = agents_paginator.get_page(agents_page_number)

    # ===== PREMIUM AGENTS SEARCH & FILTER =====
    premium_search = request.GET.get("premium_search", "")
    premium_from = request.GET.get("premium_from", "")
    premium_to = request.GET.get("premium_to", "")

    premium_list = ExpiredPremium.objects.all().order_by('-id')

    if premium_search:
        premium_list = premium_list.filter(
            Q(name__icontains=premium_search) |
            Q(speacialised__icontains=premium_search) |
            Q(phone__icontains=premium_search) |
            Q(location__icontains=premium_search) |
            Q(city__icontains=premium_search)
        )
    if premium_from:
        premium_list = premium_list.filter(created_at__date__gte=premium_from)
    if premium_to:
        premium_list = premium_list.filter(created_at__date__lte=premium_to)

    premium_paginator = Paginator(premium_list, 15)
    premium_page_number = request.GET.get('premium_page')
    premium = premium_paginator.get_page(premium_page_number)

    return render(request, 'admin_expiredagents.html', {
        'premium': premium,
        'agents': agents,
        'agents_search': agents_search,
        'agents_from': agents_from,
        'agents_to': agents_to,
        'premium_search': premium_search,
        'premium_from': premium_from,
        'premium_to': premium_to,
    })
@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_premium_expire(request, pk):
    premium = get_object_or_404(ExpiredPremium, pk=pk)
    premium.delete()
    messages.success(request, "🗑️ Premium Agent deleted successfully!")
    return redirect("expired_agent")




@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def edit_expireagent(request, pk):
    agent = get_object_or_404(ExpireAgents, pk=pk)
    if request.method == "POST":
        agent.agentsname = request.POST.get("name")
        agent.agentsspeacialised = request.POST.get("specialised")
        agent.agentsphone = request.POST.get("phone")
        agent.agentswhatsapp = request.POST.get("whatsapp")
        agent.agentsemail = request.POST.get("email")
        agent.agentslocation = request.POST.get("location")
        agent.agentspincode = request.POST.get("pincode")
        agent.agentscity = request.POST.get("city")
        agent.duration_days = request.POST.get("duration_days")



        if request.FILES.get("image"):
            agent.agentsimage = request.FILES.get("image")

        agent.save()
        messages.success(request, "✅ Agent updated successfully!")
        return redirect("expired_agent")  # adjust to your listing page

    return redirect("expired_agent")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_agents_expire(request, pk):
    premium = get_object_or_404(ExpireAgents, pk=pk)
    premium.delete()
    messages.success(request, "🗑️ Premium Agent deleted successfully!")
    return redirect("expired_agent")

# def property_live_search(request):
#     query = request.GET.get('q', '')
#     results = []
#
#     if query:
#         properties = Property.objects.filter(
#             Q(label__icontains=query) |
#             Q(city__icontains=query) |
#             Q(owner__icontains=query)
#         )[:5]
#
#         for prop in properties:
#             results.append({
#                 'id': prop.id,
#                 'label': prop.label,
#                 'city': prop.city,
#             })
#
#     return JsonResponse({'results': results})
#

def property_live_search(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:

        # ---------------- ACTIVE PROPERTIES ----------------
        active = Property.objects.filter(
            Q(property_code__icontains=query) |
            Q(label__icontains=query) |
            Q(city__icontains=query) |
            Q(owner__icontains=query) |
            Q(district__icontains=query)
        ).values(
            "id", "property_code", "label", "city", "owner", "district"
        )

        for p in active:
            results.append({
                "id": p["id"],
                "property_code": p["property_code"],
                "label": p["label"],
                "city": p["city"],
                "owner": p["owner"],
                "district": p["district"],
                "type": "active"
            })

        # ---------------- EXPIRED PROPERTIES ----------------
        expired = ExpiredProperty.objects.filter(
            Q(property_code__icontains=query) |
            Q(label__icontains=query) |
            Q(city__icontains=query) |
            Q(owner__icontains=query)
        ).values(
            "id", "property_code", "label", "city"
        )

        for e in expired:
            results.append({
                "id": e["id"],
                "property_code": e["property_code"],
                "label": e["label"],
                "city": e["city"],
                "type": "expired"
            })

        # ---------------- PREMIUM AGENTS ----------------
        premium = Premium.objects.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(speacialised__icontains=query) |
            Q(location__icontains=query) |
            Q(phone__icontains=query)
        ).values("id", "name", "city")

        for pr in premium:
            results.append({
                "id": pr["id"],
                "label": pr["name"],
                "city": pr["city"],
                "type": "premium"
            })

        # ---------------- EXPIRED PREMIUM ----------------
        expired_premium = ExpiredPremium.objects.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(city__icontains=query) |
            Q(location__icontains=query)
        ).values("id", "name", "city")

        for exp in expired_premium:
            results.append({
                "id": exp["id"],
                "label": exp["name"],
                "city": exp["city"],
                "type": "expired_premium"
            })

        # ---------------- AGENTS ----------------
        agents = Agents.objects.filter(
            Q(agentsname__icontains=query) |
            Q(agentscity__icontains=query) |
            Q(agentsphone__icontains=query) |
            Q(agentslocation__icontains=query)
        ).values("id", "agentsname", "agentscity")

        for agent in agents:
            results.append({
                "id": agent["id"],
                "label": agent["agentsname"],
                "city": agent["agentscity"],
                "type": "agents"
            })

        # ---------------- EXPIRED AGENTS ----------------
        exp_agents = ExpireAgents.objects.filter(
            Q(agentsname__icontains=query) |
            Q(agentscity__icontains=query) |
            Q(agentsphone__icontains=query) |
            Q(agentslocation__icontains=query)
        ).values("id", "agentsname", "agentscity")

        for ex_agent in exp_agents:
            results.append({
                "id": ex_agent["id"],
                "label": ex_agent["agentsname"],
                "city": ex_agent["agentscity"],
                "type": "ex_agent"
            })

    return JsonResponse({"results": results})




def blog_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if Blogadmin.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("blog_register")

        Blogadmin.objects.create(
            username=username,
            password=make_password(password)
        )

        messages.success(request, "Account created successfully")
        return redirect("blog_login")

    return render(request, "blogregister.html")


MAX_ATTEMPTS = 5
BLOCK_HOURS = 2

def blog_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        cache_key = f"login_attempts_{username}"
        block_key = f"login_block_{username}"

        # 🚫 Check if user is blocked
        if cache.get(block_key):
            messages.error(
                request,
                "Too many failed attempts. Try again after 2 hours."
            )
            return render(request, "bloglogin.html")

        try:
            user = Blogadmin.objects.get(username=username)

            if check_password(password, user.password):
                # ✅ Successful login → clear attempts
                cache.delete(cache_key)
                cache.delete(block_key)

                request.session["user_id"] = user.id
                request.session["username"] = user.username

                return redirect("blog_dashboard")

            else:
                raise Blogadmin.DoesNotExist  # Treat as failed attempt

        except Blogadmin.DoesNotExist:
            # ❌ Failed attempt
            attempts = cache.get(cache_key, 0) + 1
            cache.set(cache_key, attempts, timeout=60 * 60 * BLOCK_HOURS)

            remaining = MAX_ATTEMPTS - attempts

            if attempts >= MAX_ATTEMPTS:
                cache.set(block_key, True, timeout=60 * 60 * BLOCK_HOURS)
                messages.error(
                    request,
                    "Account locked due to 5 failed attempts. Try again in 2 hours."
                )
            else:
                messages.error(
                    request,
                    f"Invalid credentials. {remaining} attempts remaining."
                )

    return render(request, "bloglogin.html")

@never_cache
def blog_dashboard(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("blog_login")

    blogs_qs = Blog.objects.order_by("-id")  # latest first

    paginator = Paginator(blogs_qs, 10)  # 🔹 5 posts per page
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)

    return render(request, "blogdashboard.html", {
        "blogs": blogs,
        "username": request.session.get("username"),
    })


def blog_logout(request):
    request.session.flush()
    return redirect("blog_login")

# 100 KB
from PIL import Image

MAX_IMAGE_SIZE = 100 * 1024  # 100 KB

@never_cache
def blog_dashboard_create(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("blog_login")

    if request.method == "POST":
        image = request.FILES.get("image")

        if image:
            # Size check
            if image.size > MAX_IMAGE_SIZE:
                messages.error(
                    request,
                    f"Image size must be 100 KB or less. Current size: {round(image.size / 1024)} KB"
                )
                return redirect("blog_dashboard")

            # Real image validation
            try:
                img = Image.open(image)
                img.verify()
                image.seek(0)  # 🔥 CRITICAL LINE
            except Exception:
                messages.error(request, "Only valid image files are allowed.")
                return redirect("blog_dashboard")

        Blog.objects.create(
            blog_head=request.POST.get("blog_head"),
            modal_head=request.POST.get("modal_head"),
            date=request.POST.get("date"),
            card_paragraph=request.POST.get("card_paragraph"),
            modal_paragraph=request.POST.get("modal_paragraph"),
            image=image,
        )

        messages.success(request, "Blog post created successfully.")

    return redirect("blog_dashboard")



@never_cache
@require_POST
def blog_dashboard_update(request, blog_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("blog_login")

    blog = get_object_or_404(Blog, id=blog_id)

    blog.blog_head = request.POST.get("blog_head")
    blog.modal_head = request.POST.get("modal_head")
    blog.date = request.POST.get("date")
    blog.card_paragraph = request.POST.get("card_paragraph")
    blog.modal_paragraph = request.POST.get("modal_paragraph")

    image = request.FILES.get("image")
    if image:
        if image.size > MAX_IMAGE_SIZE:
            messages.error(
                request,
                f"Image size must be 100 KB or less. Current size: {round(image.size / 1024)} KB"
            )
            return redirect("blog_dashboard")

        try:
            img = Image.open(image)
            img.verify()
            image.seek(0)  # 🔥 REQUIRED
        except Exception:
            messages.error(request, "Only valid image files are allowed.")
            return redirect("blog_dashboard")

        blog.image = image

    blog.save()
    messages.success(request, "Blog post updated successfully.")
    return redirect("blog_dashboard")



@never_cache
@require_POST
def blog_dashboard_delete(request, blog_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("blog_login")

    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    return redirect("blog_dashboard")



import openpyxl

def AddUser(request):
    success = None
    error = None

    if request.method == "POST":
        action = request.POST.get("action")

        try:

            # ================= ADD USER =================
            if action == "add":
                name = request.POST.get("name")
                email = request.POST.get("email")
                mobile = request.POST.get("mobile")

                plan_ids = request.POST.getlist("plan_id")
                print("PLAN IDS:", plan_ids)

                allowed_domains = ["gmail.com", "yahoo.com", "email.com"]

                # ===== VALIDATIONS =====
                if not name or not mobile:
                    error = "Name and Mobile are required"

                elif not mobile.isdigit() or len(mobile) != 10:
                    error = "Mobile must be 10 digits"

                elif email and UserAdd.objects.filter(email=email).exists():
                    error = "Email already exists"

                elif UserAdd.objects.filter(mobile=mobile).exists():
                    error = "Mobile already exists"

                elif not plan_ids:
                    error = "Select at least one plan"

                elif len(plan_ids) > 2:
                    error = "Maximum 2 plans allowed"

                elif email:
                    domain = email.split("@")[-1]
                    if domain not in allowed_domains:
                        error = "Only Gmail, Yahoo or Email.com allowed"

                # ===== SAVE =====
                if not error:
                    user = UserAdd.objects.create(
                        name=name,
                        email=email,
                        mobile=mobile,
                        is_active=True
                    )

                    plans = Userplan.objects.filter(id__in=plan_ids)
                    user.user_plans.set(plans)

                    success = "User created successfully"

            # ================= EDIT USER =================
            elif action == "edit":
                user = UserAdd.objects.get(id=request.POST.get("user_id"))

                name = request.POST.get("name")
                email = request.POST.get("email")
                mobile = request.POST.get("mobile")
                plan_ids = request.POST.getlist("plan_id")

                # ===== VALIDATION =====
                if not name or not mobile:
                    error = "Name and Mobile are required"

                elif not mobile.isdigit() or len(mobile) != 10:
                    error = "Mobile must be 10 digits"

                elif email and UserAdd.objects.filter(email=email).exclude(id=user.id).exists():
                    error = "Email already exists"

                elif UserAdd.objects.filter(mobile=mobile).exclude(id=user.id).exists():
                    error = "Mobile already exists"

                elif len(plan_ids) > 2:
                    error = "Maximum 2 plans allowed"

                # ===== SAVE =====
                if not error:
                    user.name = name
                    user.email = email
                    user.mobile = mobile

                    plans = Userplan.objects.filter(id__in=plan_ids)
                    user.user_plans.set(plans)

                    user.save()
                    success = "User updated successfully"

            # ================= UPGRADE USER =================
            elif action == "upgrade":
                user = UserAdd.objects.get(id=request.POST.get("user_id"))
                plan_id = request.POST.get("upgrade_plan_id")

                # ✅ OPTIONAL UPGRADE (FIXED)
                if plan_id:
                    upgrade_plan = Userupgrade.objects.get(id=plan_id)
                    user.upgrade_plan = upgrade_plan
                    success = "User upgraded successfully"
                else:
                    user.upgrade_plan = None
                    success = "Upgrade removed"

                user.save()

            # ================= DELETE =================
            elif action == "delete":
                user = UserAdd.objects.get(id=request.POST.get("user_id"))
                user.delete()
                success = "User deleted"

            # ================= TOGGLE STATUS =================
            elif action == "toggle":
                user = UserAdd.objects.get(id=request.POST.get("user_id"))
                user.is_active = not user.is_active
                user.save()
                success = "User status updated"

        except Exception as e:
            error = f"Error: {e}"
            print("ERROR:", e)

    users = UserAdd.objects.all().order_by("-created")
    plans = Userplan.objects.all()
    upgrades = Userupgrade.objects.all()

    return render(request, "usercreate.html", {
        "users": users,
        "plans": plans,
        "upgrades": upgrades,
        "success": success,
        "error": error
    })



def plans(request):

    success = None
    error = None

    if request.method == "POST":

        form_type = request.POST.get("form_type")

        # ---------- USER PLAN ----------
        if form_type == "userplan":

            name = request.POST.get("name")
            validity = request.POST.get("validity")
            amount = request.POST.get("amount")

            category_ids = request.POST.getlist("category")
            purpose_ids = request.POST.getlist("purpose")

            if not name or not category_ids:
                error = "Please fill required fields."

            else:
                plan = Userplan.objects.create(
                    name=name,
                    validity=int(validity or 0),
                    amount=int(amount or 0)
                )

                plan.category.set(category_ids)
                plan.purpose.set(purpose_ids)

                success = "User Plan created successfully."


        # ---------- UPGRADE PLAN ----------
        elif form_type == "upgradeplan":

            name = request.POST.get("name")
            validity = request.POST.get("validity")

            if not name or not validity:
                error = "Name and validity required"

            else:
                Userupgrade.objects.create(
                    name=name,
                    validity=int(validity),

                    listing=request.POST.get("listing"),
                    enquiries=int(request.POST.get("enquiries") or 0),

                    edit=request.POST.get("edit"),
                    genuine=request.POST.get("genuine"),
                    meta=request.POST.get("meta"),
                    bulk=request.POST.get("bulk"),
                    poster=request.POST.get("poster"),
                    social_media=request.POST.get("social_media"),
                    lead_follow=request.POST.get("lead_follow"),
                    best=request.POST.get("best")
                )

                success = "Upgrade Plan created successfully"


        # ---------- PREMIUM PLAN ----------
        elif form_type == "premiumplan":

            name = request.POST.get("name")
            validity = request.POST.get("validity")

            if not name or not validity:
                error = "Name and validity required"

            else:
                PremiumPlan.objects.create(
                    name=name,
                    validity=int(validity),

                    total_listing=int(request.POST.get("total_listing") or 0),

                    residential_limit=int(request.POST.get("residential_limit") or 0),
                    commercial_limit=int(request.POST.get("commercial_limit") or 0),

                    edit=request.POST.get("edit"),
                    enquiries=request.POST.get("enquiries"),
                    priority_search=request.POST.get("priority_search"),
                    meta_ads=request.POST.get("meta_ads"),
                    Bulk_whatsapp=request.POST.get("bulk_whatsapp"),
                    Poster=request.POST.get("poster"),
                    social_media=request.POST.get("social_media"),
                    lead_follow=request.POST.get("lead_follow"),
                    lead_management=request.POST.get("lead_management"),

                    price=int(request.POST.get("price") or 0),
                )

                success = "Premium Plan created successfully"


        # ---------- ELITE PLAN ----------
        elif form_type == "eliteplan":

            name = request.POST.get("name")
            validity = request.POST.get("validity")

            if not name or not validity:
                error = "Name and validity required"

            else:
                ElitePlan.objects.create(
                    name=name,
                    validity=int(validity),

                    total_listing=int(request.POST.get("total_listing") or 0),
                    sale=int(request.POST.get("sale") or 0),

                    priority_search=request.POST.get("priority_search"),
                    meta_ads=request.POST.get("meta_ads"),
                    Bulk_whatsapp=request.POST.get("bulk_whatsapp"),
                    Poster=request.POST.get("poster"),
                    social_media=request.POST.get("social_media"),
                    lead_follow=request.POST.get("lead_follow"),
                    lead_management=request.POST.get("lead_management"),

                    price=int(request.POST.get("price") or 0),
                )

                success = "Elite Plan created successfully"


        # ---------- AGENT PLAN (✅ NEW) ----------
        elif form_type == "agentplan":

            name = request.POST.get("name")
            validity = request.POST.get("validity")

            if not name or not validity:
                error = "Name and validity required"

            else:
                AgentPlan.objects.create(
                    name=name,
                    validity=int(validity),

                    edit=request.POST.get("edit"),
                    enquiries=request.POST.get("enquiries"),
                    priority_search=request.POST.get("priority_search"),
                    meta_ads=request.POST.get("meta_ads"),
                    Bulk_whatsapp=request.POST.get("bulk_whatsapp"),
                    Poster=request.POST.get("poster"),
                    social_media=request.POST.get("social_media"),

                    price=int(request.POST.get("price") or 0),
                )

                success = "Agent Plan created successfully"


    # ---------- FETCH DATA ----------
    purposes = Purpose.objects.all()
    categories = Category.objects.all()

    user_plans = Userplan.objects.all().order_by("-id")
    upgrade_plans = Userupgrade.objects.all().order_by("-id")
    premium_plans = PremiumPlan.objects.all().order_by("-id")
    elite_plans = ElitePlan.objects.all().order_by("-id")
    agent_plans = AgentPlan.objects.all().order_by("-id")  # ✅ NEW

    return render(request, "plans.html", {
        "purposes": purposes,
        "categories": categories,

        "plans": user_plans,
        "upgradeuser": upgrade_plans,
        "premium_plans": premium_plans,
        "elite_plans": elite_plans,
        "agent_plans": agent_plans,  # ✅ NEW

        "success": success,
        "error": error
    })


def export_users_excel(request):

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Users"

    # Header
    sheet.append([
        "ID",
        "Name",
        "Email",
        "Mobile",
        "Plan Type",
        "Plan Name",
        "Amount",
        "Validity",
        "Created"
    ])

    users = UserAdd.objects.all().order_by("-created")

    for user in users:

        plan_type = user.active_plan or "-"

        plan_name = "-"
        amount = "-"
        validity = "-"

        # ✅ BASIC PLAN
        if user.user_plan:
            plan_name = user.user_plan.name or "-"
            amount = user.user_plan.amount or "-"
            validity = user.user_plan.validity or "-"

        # ✅ UPGRADE PLAN (override if active)
        if user.active_plan == "upgrade" and user.upgrade_plan:
            plan_name = user.upgrade_plan.name or "-"
            validity = user.upgrade_plan.validity or "-"
            amount = "Included"  # or set if you add amount field

        sheet.append([
            user.id,
            user.name,
            user.email,
            user.mobile,
            plan_type,
            plan_name,
            amount,
            validity,
            user.created.strftime("%Y-%m-%d %H:%M")
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="users.xlsx"'

    workbook.save(response)

    return response

def promotion(request):

    promotions = Promotion.objects.all().order_by("-id")
    advertisements = Advertisement.objects.all().order_by("-id")

    if request.method == "POST":

        action = request.POST.get("action")

        # ---------------------------
        # PROMOTION SECTION
        # ---------------------------

        if action in ["add", "update"]:

            name = request.POST.get("name")
            purpose = request.POST.get("purpose")
            feature = request.POST.get("feature")
            amount = request.POST.get("amount")

            extra_names = request.POST.getlist("extra_name[]")
            extra_amounts = request.POST.getlist("extra_amount[]")

            total_extra = 0

            # ADD PROMOTION
            if action == "add":

                promotion = Promotion.objects.create(
                    name=name,
                    purpose=purpose,
                    feature=feature,
                    amount=amount
                )

            # UPDATE PROMOTION
            else:

                promotion_id = request.POST.get("promotion_id")
                promotion = get_object_or_404(Promotion, id=promotion_id)

                promotion.name = name
                promotion.purpose = purpose
                promotion.feature = feature
                promotion.amount = amount
                promotion.save()

                promotion.extras.all().delete()

            # SAVE EXTRAS
            for n, a in zip(extra_names, extra_amounts):
                if n and a:
                    PromotionExtra.objects.create(
                        promotion=promotion,
                        name=n,
                        amount=a
                    )
                    total_extra += int(a)

            promotion.total_amount = int(amount) + total_extra
            promotion.save()

            return redirect("promotion")


        # DELETE PROMOTION
        elif action == "delete":

            promotion_id = request.POST.get("promotion_id")

            promotion = get_object_or_404(Promotion, id=promotion_id)
            promotion.delete()

            return redirect("promotion")


        # ---------------------------
        # ADVERTISEMENT SECTION
        # ---------------------------

        elif action == "add_ad":

            Advertisement.objects.create(
                name=request.POST.get("ad_name"),
                feature=request.POST.get("ad_feature"),
                amount=request.POST.get("ad_amount")
            )

            return redirect("promotion")


        elif action == "update_ad":

            ad_id = request.POST.get("ad_id")

            ad = get_object_or_404(Advertisement, id=ad_id)

            ad.name = request.POST.get("ad_name")
            ad.feature = request.POST.get("ad_feature")
            ad.amount = request.POST.get("ad_amount")
            ad.save()

            return redirect("promotion")


        elif action == "delete_ad":

            ad_id = request.POST.get("ad_id")

            ad = get_object_or_404(Advertisement, id=ad_id)
            ad.delete()

            return redirect("promotion")


    return render(request, "promotion.html", {
        "promotions": promotions,
        "advertisements": advertisements
    })










