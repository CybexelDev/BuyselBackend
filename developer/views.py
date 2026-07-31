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
from agents.models import AgentUserProfile
from decimal import Decimal


from django.http import JsonResponse

from django.db.models import Count
from django.db.models import Q, CharField
from django.db.models.functions import Cast
from django.utils.timezone import make_aware
from datetime import datetime
from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
from users.models import * 










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

    return render(request, 'auth/login.html', {'form': form})


# ✅ Dashboard view (only for logged-in superusers)
def superuser_required(user):
    return user.is_authenticated and user.is_superuser


# @never_cache
# @user_passes_test(superuser_required, login_url='superuser_login_view')
# def Dashboard(request):
#     #  Total properties
#     total_active = Property.objects.count()
#     total_expired = ExpiredProperty.objects.count()
#     total_all = total_active + total_expired

#     #  Get list of all purposes (for dynamic table headers)
#     all_purposes = list(Property.objects.values_list("purpose__name", flat=True).distinct())

#     #  Active properties by purpose
#     active_by_purpose = (
#         Property.objects.values("purpose__name")
#         .annotate(total=Count("id"))
#         .order_by("purpose__name")
#     )

#     context = {
#         "total_active": total_active,
#         "total_expired": total_expired,
#         "total_all": total_all,
#         "all_purposes": all_purposes,      # purposes for table headers

#         "active_by_purpose": active_by_purpose,
#     }

#     return render(request, "admin_dashboard.html", context)

from django.db.models import Count

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def Dashboard(request):
    # ===========================
    # PROPERTY COUNTS
    # ===========================

    total_active = Property.objects.count()
    total_expired = ExpiredProperty.objects.count()
    total_all = total_active + total_expired

    active_by_purpose = (
        Property.objects
        .values("purpose__name")
        .annotate(total=Count("id"))
        .order_by("purpose__name")
    )

    # ===========================
    # AGENT PROPERTY REPORT
    # ===========================

    all_purposes = list(
        AgentProperty.objects
        .values_list("purpose__name", flat=True)
        .distinct()
        .order_by("purpose__name")
    )

    premium_report = []

    agents = AgentUserProfile.objects.order_by("username")

    for index, agent in enumerate(agents, start=1):

        properties = AgentProperty.objects.filter(agent=agent)

        purpose_map = {}

        total_properties = properties.count()

        for purpose in all_purposes:

            purpose_map[purpose] = properties.filter(
                purpose__name=purpose
            ).count()

        premium_report.append({

            "sl_no": index,

            "premium_name": agent.username,

            "agent_type": agent.agent_type.title(),

            "total_properties": total_properties,

            "purpose_map": purpose_map,

        })

    context = {

        "total_active": total_active,

        "total_expired": total_expired,

        "total_all": total_all,

        "active_by_purpose": active_by_purpose,

        "all_purposes": all_purposes,

        "premium_report": premium_report,

    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )



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
        # modal_head = request.POST.get("modal_head")
        date = request.POST.get("date")
        card_paragraph = request.POST.get("card_paragraph")
        # modal_paragraph = request.POST.get("modal_paragraph")
        image = request.FILES.get("image")

        Blog.objects.create(
            blog_head=blog_head,
            # modal_head=modal_head,
            date=date,
            card_paragraph=card_paragraph,
            # modal_paragraph=modal_paragraph,
            image=image,
        )
        return redirect(reverse('create_blog'))

    #  Pagination
    blog_list = Blog.objects.all().order_by("-id")   # latest first
    paginator = Paginator(blog_list, 10)  # 5 blogs per page

    page_number = request.GET.get("page")
    blog_page = paginator.get_page(page_number)

    return render(request, "content/blogs.html", {
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







from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test

from .models import Category, Subcategory, SubcategoryField, Purpose, Amenities


@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def categories(request):

    # =========================
    # FETCH DATA
    # =========================
    categories = Category.objects.all().order_by("-id")
    purposes = Purpose.objects.all().order_by("-id")
    subcategories = Subcategory.objects.select_related("category").all().order_by("-id")

    subcategory_fields = SubcategoryField.objects.select_related(
        "subcategory", "subcategory__category"
    ).all().order_by("-id")
    field_options = FieldOption.objects.select_related(
        "field",
        "field__subcategory",
        "field__subcategory__category"
    ).all().order_by("-id")

    amenities = Amenities.objects.all().order_by("-id")  # ✅ NEW

    # =========================
    # POST ACTIONS
    # =========================
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
        # elif action == "add_field":
        #     SubcategoryField.objects.create(
        #         subcategory_id=request.POST.get("subcategory_id"),
        #         field_name=request.POST.get("field_name"),
        #         field_type=request.POST.get("field_type"),
        #         required=request.POST.get("required") == "on",
        #         icon=request.FILES.get("icon")
        #     )
        elif action == "add_field":

            field = SubcategoryField.objects.create(
                subcategory_id=request.POST.get("subcategory_id"),
                field_name=request.POST.get("field_name"),
                field_type=request.POST.get("field_type"),
                field_ui=request.POST.get("field_ui") or None,
                required=request.POST.get("required") == "on",
                icon=request.FILES.get("icon")
            )

            options = request.POST.getlist("options[]")

            icons = request.FILES.getlist("option_icons[]")

            for index, option in enumerate(options):

                if option.strip():

                    FieldOption.objects.create(
                        field=field,
                        name=option.strip(),
                        icon=icons[index] if index < len(icons) else None
                    )

        # elif action == "edit_field":
        #     field = get_object_or_404(SubcategoryField, id=request.POST.get("field_id"))

        #     field.subcategory_id = request.POST.get("subcategory_id")
        #     field.field_name = request.POST.get("field_name")
        #     field.field_type = request.POST.get("field_type")
        #     field.field_ui = request.POST.get("field_ui") 
        #     field.required = request.POST.get("required") == "on"

        #     if request.FILES.get("icon"):
        #         field.icon = request.FILES.get("icon")

        #     field.save()
        # elif action == "edit_field":

        #     field = get_object_or_404(
        #         SubcategoryField,
        #         id=request.POST.get("field_id")
        #     )

        #     field.subcategory_id = request.POST.get("subcategory_id")

        #     field.field_name = request.POST.get("field_name")

        #     field.field_type = request.POST.get("field_type")

        #     field.field_ui = request.POST.get("field_ui") or None

        #     field.required = request.POST.get("required") == "on"

        #     if request.FILES.get("icon"):
        #         field.icon = request.FILES.get("icon")

        #     field.save()

        #     # Remove old options
        #     field.options.all().delete()

        #     options = request.POST.getlist("options[]")

        #     icons = request.FILES.getlist("option_icons[]")

        #     for index, option in enumerate(options):

        #         if option.strip():

        #             FieldOption.objects.create(
        #                 field=field,
        #                 name=option.strip(),
        #                 icon=icons[index] if index < len(icons) else None
        #             )
        elif action == "edit_field":

            field = get_object_or_404(
                SubcategoryField,
                id=request.POST.get("field_id")
            )

            field.subcategory_id = request.POST.get("subcategory_id")
            field.field_name = request.POST.get("field_name")
            field.field_type = request.POST.get("field_type")
            field.field_ui = request.POST.get("field_ui") or None
            field.required = request.POST.get("required") == "on"

            if request.FILES.get("icon"):
                field.icon = request.FILES.get("icon")
            print("POST:", request.POST)
            print("FILES:", request.FILES)
            print("ICON:", request.FILES.get("icon"))

            field.save()

            option_ids = request.POST.getlist("option_ids[]")
            option_names = request.POST.getlist("options[]")

            used_option_ids = []

            new_index = 0

            for index, name in enumerate(option_names):

                name = name.strip()

                if not name:
                    continue

                option_id = option_ids[index]

                # Existing option
                if option_id:

                    option = get_object_or_404(
                        FieldOption,
                        id=option_id,
                        field=field
                    )

                    option.name = name

                    uploaded_icon = request.FILES.get(
                        f"option_icon_{option.id}"
                    )

                    if uploaded_icon:
                        option.icon = uploaded_icon

                    option.save()

                    used_option_ids.append(option.id)

                # New option
                else:

                    option = FieldOption.objects.create(
                        field=field,
                        name=name
                    )

                    uploaded_icon = request.FILES.get(
                        f"new_option_icon_{new_index}"
                    )

                    if uploaded_icon:

                        option.icon = uploaded_icon

                        option.save()

                    used_option_ids.append(option.id)

                    new_index += 1


            FieldOption.objects.filter(
                field=field
            ).exclude(
                id__in=used_option_ids
            ).delete()

        elif action == "delete_field":
            SubcategoryField.objects.filter(id=request.POST.get("field_id")).delete()

        # =========================
        # AMENITIES  ✅ NEW
        # =========================
        elif action == "add_amenity":
            name = request.POST.get("name")
            icon = request.FILES.get("icon")

            if name:
                Amenities.objects.create(
                    name=name,
                    icon=icon
                )

        elif action == "edit_amenity":
            amenity = get_object_or_404(Amenities, id=request.POST.get("amenity_id"))

            amenity.name = request.POST.get("name")

            if request.FILES.get("icon"):
                amenity.icon = request.FILES.get("icon")

            amenity.save()

        elif action == "delete_amenity":
            Amenities.objects.filter(id=request.POST.get("amenity_id")).delete()

        # =========================
        # REDIRECT AFTER POST
        # =========================
        return redirect('categories')

    # =========================
    # RENDER TEMPLATE
    # =========================
    return render(request, 'categories/categories.html', {
        'categories': categories,
        'purposes': purposes,
        'subcategories': subcategories,
        'subcategory_fields': subcategory_fields,
        'field_options': field_options,
        'amenities': amenities,  # ✅ IMPORTANT
    })


from django.core.paginator import Paginator

import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.http import HttpResponse
import traceback


#  PUT THIS AT TOP OF views.py

def parse_listing(listing):
    if not listing:
        return {}

    # ✅ Already dict (JSONField)
    if isinstance(listing, dict):
        return {k.lower(): int(v) for k, v in listing.items()}

    result = {}

    try:
        # 🔥 Support BOTH formats:
        # "residential:2,commercial:3"
        # "2 Residential 3 Commercial"

        if ":" in listing:
            parts = listing.split(",")

            for part in parts:
                if ":" not in part:
                    continue

                key, value = part.split(":", 1)
                result[key.strip().lower()] = int(value.strip())

        else:
            parts = listing.split()

            for i in range(0, len(parts), 2):
                try:
                    count = int(parts[i])
                    category = parts[i + 1].lower()
                    result[category] = count
                except:
                    continue

    except Exception as e:
        print("PARSE ERROR:", e)

    return result

# def can_add_property(owner, category, purpose):

#     category_name = category.name.lower()

#     # ================= UPGRADE PLAN =================
#     if owner.upgrade_plan:

#         listing_data = parse_listing(owner.upgrade_plan.listing)

#         allowed_count = 0

#         # 🔥 Match category (supports "residential villa" → "residential")
#         for key in listing_data:
#             if key in category_name:
#                 allowed_count = listing_data.get(key, 0)
#                 break

#         current_count = Property.objects.filter(
#             owner=owner,
#             category=category
#         ).count()

#         if allowed_count == 0:
#             return False, f"No listing allowed for {category.name}"

#         if current_count >= allowed_count:
#             return False, f"{category.name} limit reached"

#         return True, None


#     # ================= NORMAL PLAN =================
#     # if owner.user_plans.exists():

#     #     plan = owner.user_plans.first()
#     #     listing_data = parse_listing(plan.listing)

#     #     allowed_count = 0

#     #     for key in listing_data:
#     #         if key in category_name:
#     #             allowed_count = listing_data.get(key, 0)
#     #             break

#     #     current_count = Property.objects.filter(
#     #         owner=owner,
#     #         category=category
#     #     ).count()

#     #     if allowed_count == 0:
#     #         return False, f"No listing allowed for {category.name}"

#     #     if current_count >= allowed_count:
#     #         return False, f"{category.name} limit reached"

#     #     return True, None

#     # ================= NORMAL PLAN =================
#     if owner.user_plans.exists():

#         plan = owner.user_plans.first()

#         # ✅ Use numeric fields instead of listing string
#         listing_data = {
#             "residential": plan.residential_limit or 0,
#             "commercial": plan.commercial_limit or 0,
#         }

#         allowed_count = 0

#         for key in listing_data:
#             if key in category_name:
#                 allowed_count = listing_data.get(key, 0)
#                 break

#         current_count = Property.objects.filter(
#             owner=owner,
#             category=category
#         ).count()

#         if allowed_count == 0:
#             return False, f"No listing allowed for {category.name}"

#         if current_count >= allowed_count:
#             return False, f"{category.name} limit reached"

#         return True, None


#     return False, "No active plan found"



# from datetime import timedelta
# from django.utils import timezone

# def can_add_property(owner, category, purpose):

#     category_name = category.name.lower()

#     # ================= PLAN LOGIC (UNCHANGED) =================
#     if owner.upgrade_plan:
#         listing_data = parse_listing(owner.upgrade_plan.listing)

#         allowed_count = 0

#         for key in listing_data:
#             if key in category_name:
#                 allowed_count = listing_data.get(key, 0)
#                 break

#         current_count = Property.objects.filter(
#             owner=owner,
#             category=category
#         ).count()

#         if allowed_count == 0:
#             return False, f"No listing allowed for {category.name}"

#         if current_count >= allowed_count:
#             return False, f"{category.name} limit reached"

#         return True, None


#     if owner.user_plans.exists():
#         plan = owner.user_plans.first()

#         listing_data = {
#             "residential": plan.residential_limit or 0,
#             "commercial": plan.commercial_limit or 0,
#         }

#         allowed_count = 0

#         for key in listing_data:
#             if key in category_name:
#                 allowed_count = listing_data.get(key, 0)
#                 break

#         current_count = Property.objects.filter(
#             owner=owner,
#             category=category
#         ).count()

#         if allowed_count == 0:
#             return False, f"No listing allowed for {category.name}"

#         if current_count >= allowed_count:
#             return False, f"{category.name} limit reached"

#         return True, None


#     # ================= 🔥 NEW SYSTEM =================

#     now = timezone.now()

#     # reset after expiry
#     if owner.last_plan_expiry and now > owner.last_plan_expiry:
#         owner.paid_property_count = 0
#         owner.last_plan_expiry = None
#         owner.save(update_fields=["paid_property_count", "last_plan_expiry"])

#     # allow 2 paid properties
#     if owner.paid_property_count < 2:
#         return True, None

#     return False, "Choose a plan"

from django.contrib.auth.models import AnonymousUser

def can_add_property(owner, category, purpose, is_admin=False):
    """
    Master Admin:
        - Always allow property creation.

    User:
        - Validate plan/free limits.
    """

    # ==========================
    # MASTER ADMIN BYPASS
    # ==========================
    if is_admin:
        return True, None

    category_name = category.name.lower()

    # ==========================
    # UPGRADE PLAN
    # ==========================
    if owner.upgrade_plan:

        listing_data = parse_listing(owner.upgrade_plan.listing)

        allowed_count = 0

        for key, value in listing_data.items():
            if key in category_name:
                allowed_count = value
                break

        current_count = Property.objects.filter(
            user=owner
        ).filter(
            category=category
        ).count()

        if allowed_count <= 0:
            return False, f"No listing allowed for {category.name}"

        if current_count >= allowed_count:
            return False, f"{category.name} limit reached"

        return True, None

    # ==========================
    # NORMAL PLAN
    # ==========================
    if owner.user_plans.exists():

        plan = owner.user_plans.first()

        if "residential" in category_name:
            allowed_count = plan.residential_limit or 0
        elif "commercial" in category_name:
            allowed_count = plan.commercial_limit or 0
        else:
            allowed_count = 0

        current_count = Property.objects.filter(
            user=owner,
            category=category
        ).count()

        if allowed_count <= 0:
            return False, f"No listing allowed for {category.name}"

        if current_count >= allowed_count:
            return False, f"{category.name} limit reached"

        return True, None

    # ==========================
    # FREE USER
    # ==========================
    now = timezone.now()

    if owner.last_plan_expiry and now > owner.last_plan_expiry:

        owner.paid_property_count = 0
        owner.last_plan_expiry = None

        owner.save(
            update_fields=[
                "paid_property_count",
                "last_plan_expiry"
            ]
        )

    if owner.paid_property_count < 2:
        return True, None

    return False, "Choose a subscription plan."


# @never_cache
# @user_passes_test(lambda u: u.is_superuser, login_url='superuser_login_view')
# def add_property(request):

#     categories = Category.objects.all()
#     purposes = Purpose.objects.all()
#     amenities_list = Amenities.objects.all()
#     users = UserCreate.objects.all()

#     properties = Property.objects.all().order_by('-created_at')

#     paginator = Paginator(properties, 15)
#     page_number = request.GET.get('page')
#     properties = paginator.get_page(page_number)

#     if request.method == "POST":
#         try:
#             print(" STARTING PROPERTY SAVE")

#             category_id = request.POST.get("category")
#             subcategory_id = request.POST.get("subcategory")
#             purpose_id = request.POST.get("purpose")
#             owner_id = request.POST.get("owner")

#             if not category_id or not purpose_id or not owner_id:
#                 messages.error(request, "Missing required fields")
#                 return redirect("add_property")

#             category = Category.objects.get(id=category_id)
#             purpose = Purpose.objects.get(id=purpose_id)
#             owner = UserCreate.objects.get(id=owner_id)

#             subcategory = None
#             if subcategory_id:
#                 subcategory = Subcategory.objects.get(id=subcategory_id)

#             can_add, error = can_add_property(owner, category, purpose)

#             if not can_add:
#                 messages.error(request, error)
#                 return redirect("add_property")

#             uploaded_images = request.FILES.getlist("images")

#             if not uploaded_images:
#                 messages.error(request, "Please upload at least one image")
#                 return redirect("add_property")

#             main_image = uploaded_images[0]

#             # =========================
#             # DYNAMIC FIELDS
#             # =========================
#             dynamic_fields = {}

#             if subcategory:
#                 fields = SubcategoryField.objects.filter(subcategory=subcategory)

#                 for field in fields:
#                     key = f"field_{field.id}"

#                     if field.field_type == "boolean":
#                         value = key in request.POST
#                     else:
#                         value = request.POST.get(key)

#                     dynamic_fields[field.field_name] = {
#                         "id": field.id,
#                         "value": value
#                     }

#             # =========================
#             # PACKAGE / PLAN
#             # =========================
#             package = None

#             if owner.user_plans.exists():
#                 package = owner.user_plans.first()

#             duration_days = 30

#             if owner.upgrade_plan:
#                 duration_days = owner.upgrade_plan.validity
#             elif package:
#                 duration_days = package.validity

#             # =========================
#             # ✅ KEY SELLING POINTS
#             # =========================
#             key_points = request.POST.getlist("key_selling_points")
#             key_points = [p.strip() for p in key_points if p.strip()]

#             if len(key_points) > 6:
#                 messages.error(request, "Maximum 6 key selling points allowed")
#                 return redirect("add_property")

#             # =========================
#             # ✅ LANDMARKS (MULTIPLE WITH DISTANCE)
#             # =========================
#             landmark_names = request.POST.getlist("landmark_name")
#             landmark_distances = request.POST.getlist("landmark_distance")

#             landmarks = []

#             for name, distance in zip(landmark_names, landmark_distances):
#                 name = name.strip()
#                 distance = distance.strip()

#                 if name and distance:
#                     landmarks.append({
#                         "name": name,
#                         "distance": distance
#                     })

#             # Limit to max 3
#             if len(landmarks) > 3:
#                 messages.error(request, "Maximum 3 landmarks allowed")
#                 return redirect("add_property")

#             # =========================
#             # CREATE PROPERTY
#             # =========================
#             property_obj = Property.objects.create(
#                 category=category,
#                 subcategory=subcategory,
#                 purpose=purpose,

#                 dynamic_fields=dynamic_fields,

#                 label=request.POST.get("label"),
#                 land_area=request.POST.get("land_area"),
#                 sq_ft=request.POST.get("sq_ft"),

#                 description=request.POST.get("description"),
#                 message=request.POST.get("message"),

#                 image=main_image,

#                 perprice=request.POST.get("perprice"),
#                 price=request.POST.get("price"),

#                 owner=owner,
#                 package=package,

#                 whatsapp=request.POST.get("whatsapp"),
#                 phone=request.POST.get("phone"),

#                 location=request.POST.get("location"),

#                 city=request.POST.get("city"),
#                 pincode=request.POST.get("pincode"),
#                 district=request.POST.get("district"),
#                 taluk=request.POST.get("taluk"),
#                 village=request.POST.get("village"),
#                 state=request.POST.get("state"),

#                 # ✅ SAVE LANDMARK JSON
#                 land_mark=landmarks,

#                 paid=request.POST.get("paid"),

#                 added_by=request.POST.get("added_by"),
#                 market_staff=request.POST.get("market_staff"),

#                 duration_days=duration_days,

#                 note=request.POST.get("note") or "",

#                 key_selling_points=key_points
#             )

#             print(" PROPERTY SAVED:", property_obj.id)
#             # =========================
#             # 🔥 PAID PROPERTY TRACKING FIX
#             # =========================
#             if not owner.user_plans.exists() and not owner.upgrade_plan:
#                 owner.paid_property_count += 1

#                 # optional rotation reset logic (safe keep)
#                 if not owner.last_plan_expiry:
#                     owner.last_plan_expiry = timezone.now() + timedelta(days=3650)

#                 owner.save(update_fields=["paid_property_count", "last_plan_expiry"])

#             # =========================
#             # AMENITIES
#             # =========================
#             # amenities = request.POST.getlist("amenities")
#             # if amenities:
#             #     property_obj.amenities.set(amenities)
            
#             # =========================
#             # AMENITIES FIX
#             # =========================
#             amenity_ids = request.POST.getlist(
#                 "amenities"
#             )

#             print(
#                 "Selected amenities:",
#                 amenity_ids
#             )

#             if amenity_ids:

#                 amenities_qs = Amenities.objects.filter(
#                     id__in=amenity_ids
#                 )

#                 property_obj.amenities.set(
#                     amenities_qs
#                 )

#                 property_obj.save()

#                 print(
#                     "Saved amenities count:",
#                     property_obj.amenities.count()
#     )
#             # =========================
#             # MULTIPLE IMAGES
#             # =========================
#             for img in uploaded_images:
#                 PropertyImage.objects.create(
#                     property=property_obj,
#                     image=img
#                 )

#             messages.success(request, "Property added successfully")

#         except Exception as e:
#             traceback.print_exc()
#             return HttpResponse(f"ERROR: {str(e)}")

#         return redirect("add_property")

#     print("POST:", request.POST)
#     print("FILES:", request.FILES)

#     return render(request, "admin_propertylistings.html", {
#         "categories": categories,
#         "purposes": purposes,
#         "amenities": amenities_list,
#         "properties": properties,
#         "users": users
#     })



# ==============================
# IMPORTS
# ==============================
import traceback
from datetime import timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone

from .models import (
    Category,
    Subcategory,
    Purpose,
    Amenities,
    Property,
    PropertyImage,
    SubcategoryField,
    UserCreate,
)

# @never_cache
# @user_passes_test(lambda u: u.is_superuser, login_url="superuser_login_view")
# def add_property(request):

#     categories = Category.objects.all()
#     purposes = Purpose.objects.all()
#     amenities_list = Amenities.objects.all()
#     users = UserCreate.objects.all()

#     property_list = Property.objects.select_related(
#         "category",
#         "subcategory",
#         "owner"
#     ).order_by("-created_at")

#     paginator = Paginator(property_list, 15)
#     page = request.GET.get("page")
#     properties = paginator.get_page(page)

#     if request.method == "POST":

#         try:

#             print("=" * 80)
#             print("MASTER ADMIN PROPERTY CREATE")
#             print("=" * 80)

#             # =====================================================
#             # REQUIRED IDS
#             # =====================================================

#             category_id = request.POST.get("category")
#             subcategory_id = request.POST.get("subcategory")
#             purpose_id = request.POST.get("purpose")
#             owner_id = request.POST.get("owner")

#             if not category_id:
#                 messages.error(request, "Category is required.")
#                 return redirect("add_property")

#             if not purpose_id:
#                 messages.error(request, "Purpose is required.")
#                 return redirect("add_property")

#             if not owner_id:
#                 messages.error(request, "Owner is required.")
#                 return redirect("add_property")

#             category = Category.objects.get(id=category_id)
#             purpose = Purpose.objects.get(id=purpose_id)
#             owner = UserCreate.objects.get(id=owner_id)

#             subcategory = None

#             if subcategory_id:
#                 subcategory = Subcategory.objects.get(id=subcategory_id)

#             # =====================================================
#             # IMAGES
#             # =====================================================

#             uploaded_images = request.FILES.getlist("images")

#             if len(uploaded_images) == 0:
#                 messages.error(request, "Upload at least one image.")
#                 return redirect("add_property")

#             main_image = uploaded_images[0]

#             # =====================================================
#             # DYNAMIC FIELDS
#             # =====================================================

#             dynamic_fields = {}

#             if subcategory:

#                 fields = SubcategoryField.objects.filter(
#                     subcategory=subcategory
#                 )

#                 for field in fields:

#                     field_key = f"field_{field.id}"

#                     if field.field_type == "boolean":

#                         value = field_key in request.POST

#                     else:

#                         value = request.POST.get(field_key)

#                     dynamic_fields[field.field_name] = {
#                         "id": field.id,
#                         "type": field.field_type,
#                         "value": value
#                     }

#             # =====================================================
#             # PACKAGE
#             # =====================================================

#             package = None

#             if owner.user_plans.exists():
#                 package = owner.user_plans.first()

#             duration_days = 30

#             if owner.upgrade_plan:

#                 duration_days = owner.upgrade_plan.validity

#             elif package:

#                 duration_days = package.validity

#             expiry_date = timezone.now() + timedelta(days=duration_days)

#             # =====================================================
#             # KEY SELLING POINTS
#             # =====================================================

#             key_points = []

#             for item in request.POST.getlist("key_selling_points"):

#                 item = item.strip()

#                 if item:

#                     key_points.append(item)

#             if len(key_points) > 6:

#                 messages.error(
#                     request,
#                     "Maximum 6 key selling points allowed."
#                 )

#                 return redirect("add_property")

#             # =====================================================
#             # LANDMARKS
#             # =====================================================

#             landmark_names = request.POST.getlist(
#                 "landmark_name"
#             )

#             landmark_distances = request.POST.getlist(
#                 "landmark_distance"
#             )

#             landmarks = []

#             for name, distance in zip(
#                 landmark_names,
#                 landmark_distances
#             ):

#                 name = name.strip()
#                 distance = distance.strip()

#                 if name and distance:

#                     landmarks.append({

#                         "name": name,

#                         "distance": distance

#                     })

#             if len(landmarks) > 3:

#                 messages.error(
#                     request,
#                     "Maximum 3 landmarks allowed."
#                 )

#                 return redirect("add_property")

#             # =====================================================
#             # CREATE PROPERTY
#             # =====================================================

#             property_obj = Property.objects.create(

#                 category=category,

#                 subcategory=subcategory,

#                 purpose=purpose,

#                 owner=owner,

#                 package=package,

#                 dynamic_fields=dynamic_fields,

#                 label=request.POST.get("label"),

#                 land_area=request.POST.get("land_area"),

#                 sq_ft=request.POST.get("sq_ft"),

#                 description=request.POST.get("description"),

#                 message=request.POST.get("message"),

#                 image=main_image,

#                 perprice=request.POST.get("perprice"),

#                 price=request.POST.get("price"),

#                 whatsapp=request.POST.get("whatsapp"),

#                 phone=request.POST.get("phone"),

#                 city=request.POST.get("city"),

#                 village=request.POST.get("village"),

#                 taluk=request.POST.get("taluk"),

#                 district=request.POST.get("district"),

#                 state=request.POST.get("state"),

#                 pincode=request.POST.get("pincode"),

#                 location=request.POST.get("location"),

#                 land_mark=landmarks,

#                 key_selling_points=key_points,

#                 added_by=request.POST.get("added_by"),

#                 market_staff=request.POST.get("market_staff"),

#                 paid=request.POST.get("paid"),

#                 note=request.POST.get("note"),

#                 duration_days=duration_days,

#                 expiry_date=expiry_date,

#             )

#             print("PROPERTY CREATED :", property_obj.id)
#              # =====================================================
#             # SAVE AMENITIES
#             # =====================================================

#             amenity_ids = (
#                 request.POST.getlist("amenities") or
#                 request.POST.getlist("amenities[]")
#             )

#             if amenity_ids:

#                 amenities = Amenities.objects.filter(
#                     id__in=amenity_ids
#                 )

#                 property_obj.amenities.set(amenities)

#                 print(
#                     f"Amenities Saved : {property_obj.amenities.count()}"
#                 )
#                         # =====================================================
#             # SAVE PROPERTY IMAGES
#             # =====================================================

#             for image in uploaded_images:

#                 PropertyImage.objects.create(
#                     property=property_obj,
#                     image=image
#                 )

#             print(
#                 f"Images Saved : {len(uploaded_images)}"
#             )

#                         # =====================================================
#             # FREE USER PROPERTY COUNT
#             # =====================================================

#             if (
#                 not owner.user_plans.exists()
#                 and not owner.upgrade_plan
#             ):

#                 owner.paid_property_count += 1

#                 if not owner.last_plan_expiry:

#                     owner.last_plan_expiry = (
#                         timezone.now() +
#                         timedelta(days=3650)
#                     )

#                 owner.save(
#                     update_fields=[
#                         "paid_property_count",
#                         "last_plan_expiry",
#                     ]
#                 )
#                             # =====================================================
#             # SUCCESS
#             # =====================================================

#             messages.success(
#                 request,
#                 "Property added successfully."
#             )

#             return redirect("add_property")
#         except Exception as e:

#             traceback.print_exc()

#             messages.error(
#                 request,
#                 str(e)
#             )

#             return redirect("add_property")
#     return render(
#         request,
#         "admin_propertylistings.html",
#         {
#             "categories": categories,
#             "purposes": purposes,
#             "amenities": amenities_list,
#             "users": users,
#             "properties": properties,
#         },
#     )

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db import transaction
import traceback


@never_cache
@user_passes_test(
    lambda u: u.is_superuser,
    login_url="superuser_login_view"
)
def add_property(request):
    categories = Category.objects.all()
    purposes = Purpose.objects.all()
    amenities_list = Amenities.objects.all()
    users = UserCreate.objects.all()
    # properties = (
    #     Property.objects
    #     .all()
    #     .order_by("-created_at")
    # )
    search = request.GET.get("search", "").strip()

    properties = Property.objects.select_related(
        "category",
        "purpose",
        "subcategory",
        "user"
    ).order_by("-created_at")

    if search:

        properties = properties.filter(
            Q(property_code__icontains=search) |
            Q(category__name__icontains=search) |
            Q(subcategory__name__icontains=search) |
            Q(purpose__name__icontains=search) |
            Q(label__icontains=search) |
            Q(sq_ft__icontains=search) |
            Q(city__icontains=search) |
            Q(taluk__icontains=search) |
            Q(village__icontains=search) |
            Q(district__icontains=search) |
            Q(state__icontains=search) |
            Q(price__icontains=search) |
            Q(owner__icontains=search) |
            Q(phone__icontains=search) |
            Q(paid__icontains=search) |
            Q(added_by__icontains=search) |
            Q(market_staff__icontains=search) |
            Q(created_at__icontains=search) |
            Q(updated_at__icontains=search)
        )
    paginator = Paginator(properties,15)
    page_number=request.GET.get("page")
    properties=paginator.get_page(page_number)
    if request.method=="POST":
        try:
            with transaction.atomic():
                # =============================
                # BASIC IDS
                # =============================
                category_id=request.POST.get("category")
                subcategory_id=request.POST.get("subcategory")
                purpose_id=request.POST.get("purpose")
                user_id=request.POST.get("user")
                if not category_id or not purpose_id:
                    messages.error(
                        request,
                        "Category and Purpose required"
                    )
                    return redirect("add_property")
                category=Category.objects.get(
                    id=category_id
                )
                purpose=Purpose.objects.get(
                    id=purpose_id
                )
                subcategory=None

                if subcategory_id:

                    subcategory=Subcategory.objects.get(
                        id=subcategory_id
                    )
                user=None

                if user_id:

                    user=UserCreate.objects.get(
                        id=user_id
                    )
                # =============================
                # IMAGES
                # =============================
                uploaded_images=request.FILES.getlist(
                    "images"
                )
                if not uploaded_images:
                    messages.error(
                        request,
                        "Upload minimum one image"
                    )
                    return redirect(
                        "add_property"
                    )
                main_image=uploaded_images[0]
                # =============================
                # DYNAMIC FEATURES
                # =============================
                dynamic_features = []
                if subcategory:
                    fields = (
                        SubcategoryField.objects
                        .filter(subcategory=subcategory)
                        .prefetch_related("options")
                    )

                    for field in fields:

                        key = f"field_{field.id}"

                        # -------------------------
                        # BOOLEAN FIELD
                        # -------------------------
                        if field.field_type == "boolean":

                            value = "Yes" if key in request.POST else "No"
                        # -------------------------
                        # MULTI SELECT
                        # -------------------------
                        elif field.field_type == "multi_select":

                            value = request.POST.get(key)

                        # -------------------------
                        # SELECT / TEXT / NUMBER / COUNTABLE
                        # -------------------------
                        else:

                            value = request.POST.get(key)

                        if value not in [None, ""]:

                            dynamic_features.append({
                                "field": field,
                                "value": value
                            })


                # =============================
                # FEATURED PROPERTY
                # =============================
                is_featured = "is_featured" in request.POST
                
                # =============================
                # SELLING POINTS
                # =============================


                selling_points=[
                    x.strip()
                    for x in request.POST.getlist(
                        "selling_points"
                    )
                    if x.strip()
                ]


                if len(selling_points)>6:

                    messages.error(
                        request,
                        "Maximum 6 selling points allowed"
                    )

                    return redirect(
                        "add_property"
                    )

                # =============================
                # LANDMARKS
                # =============================


                landmark_names=request.POST.getlist(
                    "landmark_name"
                )

                landmark_distances=request.POST.getlist(
                    "landmark_distance"
                )


                landmarks=[]


                for name,distance in zip(
                    landmark_names,
                    landmark_distances
                ):


                    if name and distance:

                        landmarks.append(
                            {
                                "name":name.strip(),
                                "distance":distance.strip()
                            }
                        )



                if len(landmarks)>3:


                    messages.error(
                        request,
                        "Maximum 3 landmarks allowed"
                    )

                    return redirect(
                        "add_property"
                    )
                # =============================
                # CREATE PROPERTY
                # =============================
                property_obj=Property.objects.create(
                    category=category,
                    subcategory=subcategory,
                    purpose=purpose,
                    user=user,
                    owner=(
                        user.name
                        if user
                        else request.POST.get("owner")
                    ),
                    label=request.POST.get(
                        "label"
                    ),
                    land_area=request.POST.get(
                        "land_area"
                    ),
                    sq_ft=request.POST.get(
                        "sq_ft"
                    ),
                    description=request.POST.get(
                        "description"
                    ),
                    image=main_image,
                    perprice=request.POST.get("perprice"),
                    price=request.POST.get(
                        "price"
                    ),
                    deposit=request.POST.get(
                        "deposit"
                    ),
                    duration_days=int(
                        request.POST.get("duration_days", 30)
                    ),
                    whatsapp=request.POST.get(
                        "whatsapp"
                    ),
                    phone=request.POST.get(
                        "phone"
                    ),
                    location=request.POST.get(
                        "location"
                    ),
                    city=request.POST.get(
                        "city"
                    ),
                    village=request.POST.get(
                        "village"
                    ),
                    taluk=request.POST.get(
                        "taluk"
                    ),
                    district=request.POST.get(
                        "district"
                    ),
                    state=request.POST.get(
                        "state"
                    ),
                    pincode=request.POST.get(
                        "pincode"
                    ),
                    land_mark=landmarks,
                    selling_points=selling_points,
                    paid=request.POST.get(
                        "paid",
                        "no"
                    ),
                    added_by=request.POST.get(
                        "added_by"
                    ),
                    market_staff=request.POST.get(
                        "market_staff"
                    ),
                    message=request.POST.get(
                        "message"
                    ),
                    note=request.POST.get(
                        "note"
                    ),
                    is_featured=is_featured,
                )
                # =============================
                # SAVE FEATURES
                # =============================
                import json

                for item in dynamic_features:

                    field = item["field"]
                    value = item["value"]

                    # -------------------------
                    # MULTI SELECT
                    # -------------------------
                    if field.field_type == "multi_select":

                        try:
                            values = json.loads(value)
                        except Exception:
                            values = []

                        for feature in values:

                            option_name = feature.get("option", "")
                            count = feature.get("value", "")

                            option = FieldOption.objects.filter(
                                field=field,
                                name=option_name
                            ).first()

                            PropertyFeature.objects.create(
                                property=property_obj,
                                field=field,
                                value=f"{option_name} ({count})",
                                icon=option.icon if option else None
                            )

                    # -------------------------
                    # SELECT
                    # -------------------------
                    elif field.field_type == "select":

                        option = FieldOption.objects.filter(
                            field=field,
                            name=value
                        ).first()

                        PropertyFeature.objects.create(
                            property=property_obj,
                            field=field,
                            value=value,
                            icon=option.icon if option else None
                        )
                    # -------------------------
                    # NORMAL FIELDS
                    # -------------------------
                    else:
                        PropertyFeature.objects.create(
                            property=property_obj,
                            field=field,
                            value=value
                        )
                # =============================
                # AMENITIES
                # =============================
                amenity_ids=request.POST.getlist(
                    "amenities"
                )
                if amenity_ids:
                    property_obj.amenities.set(
                        Amenities.objects.filter(
                            id__in=amenity_ids
                        )
                    )
                # =============================
                # MULTIPLE IMAGES
                # =============================
                for img in uploaded_images:
                    PropertyImage.objects.create(
                        property=property_obj,
                        image=img
                    )
                messages.success(
                    request,
                    "Property added successfully"
                )
        except Exception as e:
            traceback.print_exc()
            messages.error(
                request,
                str(e)
            )
        return redirect(
            "add_property"
        )
    return render(
        request,
        "properties/property_listings.html",
        {
            "categories":categories,
            "purposes":purposes,
            "amenities":amenities_list,
            "users":users,
            "properties":properties,
            "search": search,
        }
    )


from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def get_property(request, property_id):

    property_obj = get_object_or_404(
        Property.objects.select_related(
            "category",
            "subcategory",
            "purpose",
            "user"
        ).prefetch_related(
            "amenities",
            # "propertyfeature_set__field",
            "images"
        ),
        id=property_id
    )

    dynamic_fields = []

    for feature in PropertyFeature.objects.select_related("field").filter(property=property_obj):

        dynamic_fields.append({
            "field_id": feature.field.id,
            # "field_name": feature.field_name,
            "value": feature.value
        })

    return JsonResponse({

        "id": str(property_obj.id),

        "category": property_obj.category.id if property_obj.category else "",

        "subcategory": property_obj.subcategory.id if property_obj.subcategory else "",

        "purpose": property_obj.purpose.id if property_obj.purpose else "",

        "user": str(property_obj.user.id) if property_obj.user else "",

        "label": property_obj.label,

        "land_area": property_obj.land_area,

        "sq_ft": property_obj.sq_ft,

        "description": property_obj.description,

        "message": property_obj.message,

        "perprice": property_obj.perprice,

        "price": property_obj.price,

        "deposit": property_obj.deposit,

        "owner": property_obj.owner,

        "phone": property_obj.phone,

        "whatsapp": property_obj.whatsapp,

        "location": property_obj.location,

        "city": property_obj.city,

        "village": property_obj.village,

        "taluk": property_obj.taluk,

        "district": property_obj.district,

        "state": property_obj.state,

        "pincode": property_obj.pincode,

        "paid": property_obj.paid,

        "added_by": property_obj.added_by,
        "is_featured": property_obj.is_featured,
        "market_staff": property_obj.market_staff,

        "note": property_obj.note,

        "duration_days": property_obj.duration_days,

        "selling_points": property_obj.selling_points or [],

        "landmarks": property_obj.land_mark or [],

        "amenities": list(
            property_obj.amenities.values_list(
                "id",
                flat=True
            )
        ),

        "dynamic_fields": dynamic_fields,

        "images": [

            {
                "id": img.id,
                "url": img.image.url
            }

            for img in property_obj.images.all()

        ]

    })

from django.http import JsonResponse


# def get_subcategories(request, category_id):

#     subcategories = Subcategory.objects.filter(
#         category_id=category_id
#     ).order_by("name")

#     data = []

#     for sub in subcategories:

#         data.append({

#             "id": sub.id,

#             "name": sub.name

#         })

#     return JsonResponse(
#         data,
#         safe=False
#     )

def get_subcategories(request, category_id):

    print("Category ID:", category_id)

    subcategories = Subcategory.objects.filter(
        category_id=category_id
    ).order_by("name")

    print("Count:", subcategories.count())

    data = []

    for sub in subcategories:
        print(sub.name)

        data.append({
            "id": sub.id,
            "name": sub.name
        })

    return JsonResponse(data, safe=False)

# def get_subcategory_fields(request, subcategory_id):

#     fields = SubcategoryField.objects.filter(
#         subcategory_id=subcategory_id
#     ).order_by("id")

#     response = []

#     for field in fields:

#         response.append({

#             "id": field.id,

#             "name": field.field_name,

#             "type": field.field_type,

#             "icon": (
#                 field.icon.url
#                 if field.icon
#                 else ""
#             ),

#         })

#     return JsonResponse(
#         response,
#         safe=False
#     )

from django.http import JsonResponse


def get_subcategory_fields(request, subcategory_id):

    fields = (
        SubcategoryField.objects
        .filter(subcategory_id=subcategory_id)
        .prefetch_related("options")
    )

    data = []

    for field in fields:

        data.append({

            "id": field.id,

            "name": field.field_name,

            "type": field.field_type,

            "ui": field.field_ui,

            "required": field.required,

            "icon": field.icon.url if field.icon else "",

            "options": [

                {
                    "id": option.id,
                    "name": option.name,
                    "icon": option.icon.url if option.icon else ""
                }

                for option in field.options.all()

            ]

        })

    return JsonResponse(data, safe=False)
def get_user_details(request, user_id):

    try:

        user = UserCreate.objects.get(id=user_id)

        package = None

        validity = ""

        listing = ""

        expiry = ""

        if user.upgrade_plan:

            package = user.upgrade_plan

            validity = package.validity

            expiry = (
                user.last_plan_expiry.strftime("%d-%m-%Y")
                if user.last_plan_expiry
                else ""
            )

            listing = package.listing

        elif user.user_plans.exists():

            package = user.user_plans.first()

            validity = package.validity

            expiry = (
                user.last_plan_expiry.strftime("%d-%m-%Y")
                if user.last_plan_expiry
                else ""
            )

            listing = package.listing

        return JsonResponse({

            "status": True,

            "phone": user.mobile,

            "plan_name": (
                package.name
                if package
                else ""
            ),

            "validity": validity,

            "listing": listing,

            "expiry": expiry,

        })

    except UserCreate.DoesNotExist:

        return JsonResponse({

            "status": False,

            "message": "User not found."

        })

# def get_user_details(request, user_id):
#     try:
#         user = UserAdd.objects.get(id=user_id)

#         #  Phone
#         phone = user.mobile

#         #  Plan logic
#         plan = None

#         if user.upgrade_plan:
#             plan = user.upgrade_plan
#         else:
#             plan = user.user_plans.first()  # or latest()

#         if plan:
#             validity = plan.validity  # days
#             listing = getattr(plan, "listing_limit", "")

#             expiry_date = user.created + timedelta(days=validity)
#         else:
#             validity = ""
#             listing = ""
#             expiry_date = ""

#         return JsonResponse({
#             "phone": phone,
#             "plan_name": str(plan) if plan else "",
#             "validity": validity,
#             "listing": listing,
#             "expiry": expiry_date.strftime("%Y-%m-%d") if expiry_date else ""
#         })

#     except UserAdd.DoesNotExist:
#         return JsonResponse({"error": "User not found"}, status=404)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import timedelta

def get_user_details(request, user_id):
    user = get_object_or_404(UserCreate, id=user_id)

    phone = user.mobile

    plan_name = ""
    validity = ""
    listing = ""
    expiry_date = ""

    # ✅ Upgrade Plan
    if user.upgrade_plan:
        plan = user.upgrade_plan

        plan_name = plan.name
        validity = plan.validity
        listing = plan.listing  # ✅ correct

        expiry_date = user.created + timedelta(days=validity)

    # ✅ Userplan
    elif user.user_plans.exists():
        plan = user.user_plans.first()

        plan_name = plan.name
        validity = plan.validity

        # ✅ convert numeric → string format
        listing = f"{plan.residential_limit or 0} Residential / {plan.commercial_limit or 0} Commercial"

        expiry_date = user.created + timedelta(days=validity)

    return JsonResponse({
        "phone": phone,
        "plan_name": plan_name,
        "validity": validity,
        "listing": listing,
        "expiry": expiry_date.strftime("%Y-%m-%d") if expiry_date else ""
    })



# @never_cache
# @user_passes_test(superuser_required, login_url='superuser_login_view')
# @require_POST
# def edit_property(request, property_id):
#     prop = get_object_or_404(Property, id=property_id)

#     # --- Basic Fields ---
#     prop.label = request.POST.get("label")
#     prop.land_area = request.POST.get("land_area")
#     prop.sq_ft = request.POST.get("sq_ft")
#     prop.description = request.POST.get("description")
#     prop.message = request.POST.get("message")  #  ADDED
#     prop.amenities = request.POST.get("amenities")
#     prop.perprice = request.POST.get("perprice")
#     prop.price = request.POST.get("price")
#     prop.owner = request.POST.get("owner")
#     prop.whatsapp = request.POST.get("whatsapp")
#     prop.phone = request.POST.get("phone")
#     prop.location = request.POST.get("location")
#     prop.city = request.POST.get("city")
#     prop.district = request.POST.get("district")
#     prop.village = request.POST.get("village")
#     prop.taluk = request.POST.get("taluk")
#     prop.state = request.POST.get("state")
#     prop.pincode = request.POST.get("pincode")
#     prop.land_mark = request.POST.get("land_mark")
#     prop.added_by = request.POST.get("added_by")
#     prop.market_staff = request.POST.get("market_staff")

#     # --- Paid (safe boolean handling) ---
#     paid_value = request.POST.get("paid")
#     prop.paid = True if paid_value in ["True", "Yes", "1"] else False

#     # --- Category & Purpose ---
#     category_id = request.POST.get("category")
#     purpose_id = request.POST.get("purpose")

#     if category_id:
#         prop.category = get_object_or_404(Category, id=category_id)

#     if purpose_id:
#         prop.purpose = get_object_or_404(Purpose, id=purpose_id)

#     # --- Duration Days ---
#     duration_days = request.POST.get("duration_days")
#     if duration_days:
#         try:
#             prop.duration_days = int(duration_days)
#         except ValueError:
#             pass

#     # --- MANUAL SCREENSHOT UPLOAD ---
#     screenshot_file = request.FILES.get("manual_screenshot")
#     if screenshot_file:
#         prop.screenshot = screenshot_file  # overwrite old screenshot

#     # Save all updates BEFORE images
#     prop.save()

#     # --- ADD NEW IMAGES ---
#     new_images = request.FILES.getlist("images")
#     for img in new_images:
#         PropertyImage.objects.create(property=prop, image=img)

#     # --- DELETE SELECTED IMAGES ---
#     delete_images = request.POST.getlist("delete_images")
#     for img_id in delete_images:
#         PropertyImage.objects.filter(id=img_id, property=prop).delete()

#     messages.success(request, "Property updated successfully.")
#     return redirect("add_property")

# def get_subcategories(request, category_id):
#     subs = Subcategory.objects.filter(category_id=category_id)
#     return JsonResponse([{"id": s.id, "name": s.name} for s in subs], safe=False)


# def get_subcategory_fields(request, subcategory_id):
#     fields = SubcategoryField.objects.filter(subcategory_id=subcategory_id)

#     return JsonResponse([
#         {
#             "id": f.id,
#             "name": f.field_name,
#             "type": f.field_type,
#             "icon": f.icon.url if f.icon else ""
#         } for f in fields
#     ], safe=False)

@never_cache
@user_passes_test(
    lambda u: u.is_superuser,
    login_url="superuser_login_view"
)
# def edit_property(request, property_id):

#     property_obj = get_object_or_404(
#         Property,
#         id=property_id
#     )

#     if request.method != "POST":
#         return redirect("add_property")

#     try:

#         category = Category.objects.get(
#             id=request.POST.get("category")
#         )

#         purpose = Purpose.objects.get(
#             id=request.POST.get("purpose")
#         )

#         subcategory = None

#         if request.POST.get("subcategory"):

#             subcategory = Subcategory.objects.get(
#                 id=request.POST.get("subcategory")
#             )

#         user = None

#         if request.POST.get("user"):

#             user = UserCreate.objects.get(
#                 id=request.POST.get("user")
#             )

#         property_obj.category = category
#         property_obj.subcategory = subcategory
#         property_obj.purpose = purpose
#         property_obj.user = user

#         property_obj.owner = (
#             user.name
#             if user
#             else request.POST.get("owner")
#         )

#         property_obj.label = request.POST.get("label")
#         property_obj.land_area = request.POST.get("land_area")
#         property_obj.sq_ft = request.POST.get("sq_ft")
#         property_obj.description = request.POST.get("description")
#         property_obj.perprice = request.POST.get("perprice")
#         property_obj.price = request.POST.get("price")
#         property_obj.deposit = request.POST.get("deposit")
#         property_obj.phone = request.POST.get("phone")
#         property_obj.whatsapp = request.POST.get("whatsapp")
#         property_obj.location = request.POST.get("location")
#         property_obj.city = request.POST.get("city")
#         property_obj.village = request.POST.get("village")
#         property_obj.taluk = request.POST.get("taluk")
#         property_obj.district = request.POST.get("district")
#         property_obj.state = request.POST.get("state")
#         property_obj.pincode = request.POST.get("pincode")

#         property_obj.paid = request.POST.get(
#             "paid",
#             "no"
#         )

#         property_obj.added_by = request.POST.get(
#             "added_by"
#         )

#         property_obj.market_staff = request.POST.get(
#             "market_staff"
#         )

#         property_obj.message = request.POST.get(
#             "message"
#         )

#         property_obj.note = request.POST.get(
#             "note"
#         )

#         property_obj.duration_days = int(
#             request.POST.get(
#                 "duration_days",
#                 30
#             )
#         )

#         property_obj.selling_points = [
#             x.strip()
#             for x in request.POST.getlist("selling_points")
#             if x.strip()
#         ]

#         landmarks = []

#         landmark_names = request.POST.getlist(
#             "landmark_name"
#         )

#         landmark_distances = request.POST.getlist(
#             "landmark_distance"
#         )

#         for name, distance in zip(
#             landmark_names,
#             landmark_distances
#         ):

#             if name and distance:

#                 landmarks.append({
#                     "name": name.strip(),
#                     "distance": distance.strip()
#                 })

#         property_obj.land_mark = landmarks

#         uploaded_images = request.FILES.getlist(
#             "images"
#         )

#         if uploaded_images:

#             property_obj.image = uploaded_images[0]

#         property_obj.save()

#         amenity_ids = request.POST.getlist(
#             "amenities"
#         )

#         property_obj.amenities.set(
#             Amenities.objects.filter(
#                 id__in=amenity_ids
#             )
#         )

#         messages.success(
#             request,
#             "Property updated successfully."
#         )

#     except Exception as e:

#         messages.error(
#             request,
#             str(e)
#         )

#     return redirect("add_property")
@never_cache
@user_passes_test(
    lambda u: u.is_superuser,
    login_url="superuser_login_view"
)
def edit_property(request, property_id):

    property_obj = get_object_or_404(
        Property,
        id=property_id
    )

    if request.method != "POST":
        return redirect("add_property")

    try:

        # ====================================
        # CATEGORY / PURPOSE / SUBCATEGORY
        # ====================================

        category = Category.objects.get(
            id=request.POST.get("category")
        )

        purpose = Purpose.objects.get(
            id=request.POST.get("purpose")
        )

        subcategory = None

        if request.POST.get("subcategory"):

            subcategory = Subcategory.objects.get(
                id=request.POST.get("subcategory")
            )

        user = None

        if request.POST.get("user"):

            user = UserCreate.objects.get(
                id=request.POST.get("user")
            )

        # ====================================
        # BASIC DETAILS
        # ====================================

        property_obj.category = category
        property_obj.subcategory = subcategory
        property_obj.purpose = purpose
        property_obj.user = user

        property_obj.owner = (
            user.name
            if user
            else request.POST.get("owner")
        )

        property_obj.label = request.POST.get("label")
        property_obj.land_area = request.POST.get("land_area")
        property_obj.sq_ft = request.POST.get("sq_ft")
        property_obj.description = request.POST.get("description")

        property_obj.perprice = request.POST.get("perprice")
        property_obj.price = request.POST.get("price")
        property_obj.deposit = request.POST.get("deposit")

        property_obj.phone = request.POST.get("phone")
        property_obj.whatsapp = request.POST.get("whatsapp")

        property_obj.location = request.POST.get("location")
        property_obj.is_featured = (
            "is_featured" in request.POST
        )
        property_obj.city = request.POST.get("city")
        property_obj.village = request.POST.get("village")
        property_obj.taluk = request.POST.get("taluk")
        property_obj.district = request.POST.get("district")
        property_obj.state = request.POST.get("state")
        property_obj.pincode = request.POST.get("pincode")

        property_obj.paid = request.POST.get(
            "paid",
            "no"
        )

        property_obj.added_by = request.POST.get(
            "added_by"
        )

        property_obj.market_staff = request.POST.get(
            "market_staff"
        )

        property_obj.message = request.POST.get(
            "message"
        )

        property_obj.note = request.POST.get(
            "note"
        )

        property_obj.duration_days = int(
            request.POST.get(
                "duration_days",
                30
            )
        )

        # ====================================
        # SELLING POINTS
        # ====================================

        property_obj.selling_points = [

            point.strip()

            for point in request.POST.getlist(
                "selling_points"
            )

            if point.strip()

        ]

        # ====================================
        # LANDMARKS
        # ====================================

        landmarks = []

        landmark_names = request.POST.getlist(
            "landmark_name"
        )

        landmark_distances = request.POST.getlist(
            "landmark_distance"
        )

        for name, distance in zip(
            landmark_names,
            landmark_distances
        ):

            if name.strip() and distance.strip():

                landmarks.append({

                    "name": name.strip(),

                    "distance": distance.strip()

                })

        property_obj.land_mark = landmarks
        # ====================================
        # MAIN IMAGE
        # ====================================

        uploaded_images = request.FILES.getlist("images")

        if uploaded_images:

            property_obj.image = uploaded_images[0]

        property_obj.save()

        # ====================================
        # UPDATE DYNAMIC FEATURES
        # ====================================

        PropertyFeature.objects.filter(
            property=property_obj
        ).delete()

        import json

        if subcategory:

            fields = (
                SubcategoryField.objects
                .filter(subcategory=subcategory)
                .prefetch_related("options")
            )

            for field in fields:

                key = f"field_{field.id}"

                # --------------------------
                # BOOLEAN
                # --------------------------

                if field.field_type == "boolean":

                    value = "Yes" if key in request.POST else "No"

                # --------------------------
                # MULTI SELECT
                # --------------------------

                elif field.field_type == "multi_select":

                    value = request.POST.get(key)

                # --------------------------
                # NORMAL
                # --------------------------

                else:

                    value = request.POST.get(key)

                if value in [None, ""]:

                    continue

                # --------------------------
                # MULTI SELECT SAVE
                # --------------------------

                if field.field_type == "multi_select":

                    try:

                        values = json.loads(value)

                    except Exception:

                        values = []

                    for feature in values:

                        option_name = feature.get(
                            "option",
                            ""
                        )

                        count = feature.get(
                            "value",
                            ""
                        )

                        option = FieldOption.objects.filter(
                            field=field,
                            name=option_name
                        ).first()

                        PropertyFeature.objects.create(
                            property=property_obj,
                            field=field,
                            value=f"{option_name} ({count})",
                            icon=option.icon if option else None
                        )

                # --------------------------
                # SELECT
                # --------------------------

                elif field.field_type == "select":

                    option = FieldOption.objects.filter(
                        field=field,
                        name=value
                    ).first()

                    PropertyFeature.objects.create(
                        property=property_obj,
                        field=field,
                        value=value,
                        icon=option.icon if option else None
                    )

                # --------------------------
                # NORMAL FIELD
                # --------------------------

                else:

                    PropertyFeature.objects.create(
                        property=property_obj,
                        field=field,
                        value=value
                    )

        # ====================================
        # UPDATE AMENITIES
        # ====================================
        print("POST:", request.POST)
        print("Amenity IDs:", request.POST.getlist("amenities"))

        amenity_ids = request.POST.getlist(
            "amenities"
        )

        property_obj.amenities.set(

            Amenities.objects.filter(
                id__in=amenity_ids
            )

        )

        # ====================================
        # UPDATE MULTIPLE IMAGES
        # ====================================

        # if uploaded_images:

        #     PropertyImage.objects.filter(
        #         property=property_obj
        #     ).delete()

        #     for img in uploaded_images:

        #         PropertyImage.objects.create(
        #             property=property_obj,
        #             image=img
        #         )
        # ====================================
        # REMOVE SELECTED IMAGES
        # ====================================

        deleted_images = request.POST.get(
            "deleted_images",
            ""
        )

        if deleted_images:

            ids = [

                i.strip()

                for i in deleted_images.split(",")

                if i.strip()

            ]

            PropertyImage.objects.filter(

                property=property_obj,

                id__in=ids

            ).delete()


        # ====================================
        # ADD NEW IMAGES
        # ====================================

        uploaded_images = request.FILES.getlist("images")

        for image in uploaded_images:

            PropertyImage.objects.create(

                property=property_obj,

                image=image

            )

        # ====================================
        # SUCCESS
        # ====================================

        messages.success(

            request,

            "Property updated successfully."

        )

    except Exception as e:

        import traceback

        traceback.print_exc()

        messages.error(

            request,

            str(e)

        )

    return redirect(
        "add_property"
    )

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test

@never_cache
@user_passes_test(
    lambda u: u.is_superuser,
    login_url="superuser_login_view"
)
def delete_property(request, property_id):

    property_obj = get_object_or_404(
        Property,
        id=property_id
    )

    try:

        property_obj.delete()

        messages.success(
            request,
            "Property deleted successfully."
        )

    except Exception as e:

        messages.error(
            request,
            str(e)
        )

    return redirect("add_property")

# @never_cache
# @user_passes_test(
#     superuser_required,
#     login_url='superuser_login_view'
# )
# @require_POST
# def edit_property(request, property_id):

#     prop = get_object_or_404(
#         Property,
#         id=property_id
#     )

#     # BASIC FIELDS

#     prop.label = request.POST.get("label")
#     prop.land_area = request.POST.get("land_area")
#     prop.sq_ft = request.POST.get("sq_ft")

#     prop.description = request.POST.get(
#         "description"
#     )

#     prop.message = request.POST.get(
#         "message"
#     )

#     prop.perprice = request.POST.get(
#         "perprice"
#     )

#     prop.price = request.POST.get(
#         "price"
#     )

#     prop.whatsapp = request.POST.get(
#         "whatsapp"
#     )

#     prop.phone = request.POST.get(
#         "phone"
#     )

#     prop.location = request.POST.get(
#         "location"
#     )

#     prop.city = request.POST.get(
#         "city"
#     )

#     prop.district = request.POST.get(
#         "district"
#     )

#     prop.village = request.POST.get(
#         "village"
#     )

#     prop.taluk = request.POST.get(
#         "taluk"
#     )

#     prop.state = request.POST.get(
#         "state"
#     )

#     prop.pincode = request.POST.get(
#         "pincode"
#     )

#     prop.added_by = request.POST.get(
#         "added_by"
#     )

#     prop.market_staff = request.POST.get(
#         "market_staff"
#     )

#     # PAID

#     prop.paid = request.POST.get(
#         "paid",
#         "no"
#     )

#     # CATEGORY

#     category_id = request.POST.get(
#         "category"
#     )

#     if category_id:

#         prop.category = get_object_or_404(
#             Category,
#             id=category_id
#         )

#     # PURPOSE

#     purpose_id = request.POST.get(
#         "purpose"
#     )

#     if purpose_id:

#         prop.purpose = get_object_or_404(
#             Purpose,
#             id=purpose_id
#         )

#     # OWNER

#     owner_id = request.POST.get(
#         "owner"
#     )

#     if owner_id:

#         prop.owner = get_object_or_404(
#             UserCreate,
#             id=owner_id
#         )

#     # DURATION

#     duration_days = request.POST.get(
#         "duration_days"
#     )

#     if duration_days:

#         try:
#             prop.duration_days = int(
#                 duration_days
#             )

#         except ValueError:
#             pass

#     # SCREENSHOT

#     screenshot_file = request.FILES.get(
#         "manual_screenshot"
#     )

#     if screenshot_file:

#         prop.screenshot = screenshot_file

#     # SAVE

#     prop.save()

#     # AMENITIES

#     amenity_ids = request.POST.getlist(
#         "amenities"
#     )

#     if amenity_ids:

#         amenities_qs = Amenities.objects.filter(
#             id__in=amenity_ids
#         )

#         prop.amenities.set(
#             amenities_qs
#         )

#     # ADD NEW IMAGES

#     new_images = request.FILES.getlist(
#         "images"
#     )

#     for img in new_images:

#         PropertyImage.objects.create(
#             property=prop,
#             image=img
#         )

#     # DELETE IMAGES

#     delete_images = request.POST.getlist(
#         "delete_images"
#     )

#     for img_id in delete_images:

#         PropertyImage.objects.filter(
#             id=img_id,
#             property=prop
#         ).delete()

#     messages.success(
#         request,
#         "Property updated successfully."
#     )

#     return redirect("add_property")



# @never_cache
# @user_passes_test(superuser_required, login_url='superuser_login_view')
# @require_POST
# def delete_property(request, pk):
#     prop = get_object_or_404(Property, pk=pk)
#     prop.delete()
#     return redirect('add_property')

@never_cache
@user_passes_test(
    superuser_required,
    login_url="superuser_login_view"
)
@require_POST
def delete_property(request, property_id):

    property_obj = get_object_or_404(
        Property,
        id=property_id
    )

    property_obj.delete()

    messages.success(
        request,
        "Property deleted successfully."
    )

    return redirect("add_property")


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
            duration_days = request.POST.get("duration_days")  #  from POST, not FILES

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
            messages.success(request, " Premium Agent created successfully!")


        elif "agentname" in request.POST:
            agentsname = request.POST.get("agentname")
            agentsspeacialised = request.POST.get("agentspeacialised")
            agentsphone = request.POST.get("agentphone")
            agentswhatsapp = request.POST.get("agentwhatsapp")
            agentsemail = request.POST.get("agentemail")
            agentslocation = request.POST.get("agentlocation")
            agentscity = request.POST.get("agentscity")
            agentspincode = request.POST.get("agentspincode")
            agentsimage = request.FILES.get("agentsimage")
            plan_id = request.POST.get("plan_id")
            # validate plan
            try:

                plan = AgentPlan.objects.get(id=plan_id)
            except AgentPlan.DoesNotExist:
                messages.error(request, " Invalid plan selected")
                return redirect("agents_login")

            if Agents.objects.filter(agentsphone=agentsphone).exists():
                messages.error(request, "This phone number is already registered.")
                return redirect("agents_login")

            Agents.objects.create(
                agentsname=agentsname,
                agentsspeacialised=agentsspeacialised,
                agentsphone=agentsphone,
                agentswhatsapp=agentswhatsapp,
                agentsemail=agentsemail,
                agentslocation=agentslocation,
                agentscity=agentscity,
                agentspincode=agentspincode,
                agentsimage=agentsimage,
                duration_days=plan.validity
            )

            messages.success(request, f"[------------- Agent added with {plan.validity} days plan!")

            return redirect("agents_login")
    return render(request, "agents/add_agent.html")

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

    return render(request, 'agents/premium_agents.html', {
        'premium': premium,
        'search_query': search_query,
        'from_date': from_date,
        'to_date': to_date,
    })


# @never_cache
# @user_passes_test(superuser_required, login_url='superuser_login_view')
# def admin_agents(request):

#     search_query = request.GET.get("search", "").strip()
#     from_date = request.GET.get("from_date", "")
#     to_date = request.GET.get("to_date", "")

#     # Base Querysets
#     all_premium = Premium.objects.all()
#     all_agents = Agents.objects.all()

#     # ------------------------------
#     # 🔍 TEXT SEARCH (Both tables)
#     # ------------------------------
#     if search_query:

#         # Premium search
#         all_premium = all_premium.annotate(
#             created_str=Cast("created_at", output_field=CharField()),
#             duration_str=Cast("duration_days", output_field=CharField()),
#         ).filter(
#             Q(name__icontains=search_query) |
#             Q(speacialised__icontains=search_query) |
#             Q(phone__icontains=search_query) |
#             Q(whatsapp__icontains=search_query) |
#             Q(email__icontains=search_query) |
#             Q(location__icontains=search_query) |
#             Q(city__icontains=search_query) |
#             Q(pincode__icontains=search_query) |
#             Q(username__icontains=search_query) |
#             Q(created_str__icontains=search_query)
#         )

#         # Agents search
#         all_agents = all_agents.annotate(
#             created_str=Cast("created_at", output_field=CharField()),
#             duration_str=Cast("duration_days", output_field=CharField()),
#         ).filter(
#             Q(agentsname__icontains=search_query) |
#             Q(agentsspeacialised__icontains=search_query) |
#             Q(agentsphone__icontains=search_query) |
#             Q(agentswhatsapp__icontains=search_query) |
#             Q(agentsemail__icontains=search_query) |
#             Q(agentslocation__icontains=search_query) |
#             Q(agentscity__icontains=search_query) |
#             Q(agentspincode__icontains=search_query) |
#             Q(created_str__icontains=search_query)
#         )

#     # ------------------------------
#     # 📅 DATE RANGE FILTER
#     # ------------------------------
#     if from_date:
#         all_premium = all_premium.filter(created_at__date__gte=from_date)
#         all_agents = all_agents.filter(created_at__date__gte=from_date)

#     if to_date:
#         all_premium = all_premium.filter(created_at__date__lte=to_date)
#         all_agents = all_agents.filter(created_at__date__lte=to_date)

#     # Sort both by latest first
#     all_premium = all_premium.order_by("-created_at")
#     all_agents = all_agents.order_by("-created_at")

#     # ------------------------------
#     # 📄 Pagination
#     # ------------------------------
#     premium_paginator = Paginator(all_premium, 10)
#     agents_paginator = Paginator(all_agents, 20)

#     premium_page_number = request.GET.get('premium_page', 1)
#     agents_page_number = request.GET.get('agents_page', 1)

#     premium = premium_paginator.get_page(premium_page_number)
#     agents = agents_paginator.get_page(agents_page_number)

#     return render(request, 'agents/agents_list.html', {
#         'premium': premium,
#         'agents': agents,
#         'search_query': search_query,
#         'from_date': from_date,
#         'to_date': to_date,
#     })
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache

from .models import AgentUserProfile



@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_agents(request):

    search_query = request.GET.get("search", "").strip()
    from_date = request.GET.get("from_date", "")
    to_date = request.GET.get("to_date", "")


    agents = AgentUserProfile.objects.all()


    # ================================
    # SEARCH
    # ================================

    if search_query:

        agents = agents.filter(

            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(agent_type__icontains=search_query)

        )


    # ================================
    # DATE FILTER
    # ================================

    if from_date:

        agents = agents.filter(
            created_at__date__gte=from_date
        )


    if to_date:

        agents = agents.filter(
            created_at__date__lte=to_date
        )


    agents = agents.order_by(
        "-created_at"
    )


    # ================================
    # PAGINATION
    # ================================

    paginator = Paginator(
        agents,
        20
    )

    page_number = request.GET.get(
        "agents_page"
    )

    agents_page = paginator.get_page(
        page_number
    )


    return render(
        request,
        "agents/agents_list.html",
        {

            "agents": agents_page,

            "search_query": search_query,

            "from_date": from_date,

            "to_date": to_date,

        }
    )



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


# @never_cache
# @user_passes_test(superuser_required, login_url='superuser_login_view')
# def edit_agent(request, pk):
#     agent = get_object_or_404(Agents, pk=pk)
#     if request.method == "POST":
#         agent.agentsname = request.POST.get("name")
#         agent.agentsspeacialised = request.POST.get("specialised")
#         agent.agentsphone = request.POST.get("phone")
#         agent.agentswhatsapp = request.POST.get("whatsapp")
#         agent.agentsemail = request.POST.get("email")
#         agent.agentslocation = request.POST.get("location")
#         agent.agentspincode = request.POST.get("pincode")
#         agent.duration_days = request.POST.get("duration_days")


#         if request.FILES.get("image"):
#             agent.agentsimage = request.FILES.get("image")

#         agent.save()
#         messages.success(request, "✅ Agent updated successfully!")
#         return redirect("admin_agents")  # adjust to your listing page

#     return redirect("admin_agents")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def edit_agent(request, pk):

    agent = get_object_or_404(
        AgentUserProfile,
        pk=pk
    )


    if request.method == "POST":

        agent.username = request.POST.get(
            "username",
            agent.username
        )

        agent.professional_title = request.POST.get(
            "professional_title",
            agent.professional_title
        )


        agent.phone_number = request.POST.get(
            "phone_number",
            agent.phone_number
        )


        agent.whatsapp_number = request.POST.get(
            "whatsapp_number",
            agent.whatsapp_number
        )


        agent.email = request.POST.get(
            "email",
            agent.email
        )


        agent.address = request.POST.get(
            "address",
            agent.address
        )


        agent.city = request.POST.get(
            "city",
            agent.city
        )


        agent.pin_code = request.POST.get(
            "pin_code",
            agent.pin_code
        )


        agent.agent_type = request.POST.get(
            "agent_type",
            agent.agent_type
        )


        status = request.POST.get("is_active")

        if status:
            agent.is_active = (
                True if status == "true"
                else False
            )


        if request.FILES.get("image"):

            agent.profile_image = request.FILES.get(
                "image"
            )


        agent.save()


        messages.success(
            request,
            "Agent updated successfully"
        )

        return redirect(
            "admin_agents"
        )


    return redirect(
        "admin_agents"
    )

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_agent(request, pk):

    agent = get_object_or_404(
        AgentUserProfile,
        pk=pk
    )

    agent.delete()


    messages.success(
        request,
        "Agent deleted successfully"
    )


    return redirect(
        "admin_agents"
    )

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_agent(request, pk):
    agent = get_object_or_404(
        AgentUserProfile,
        pk=pk
    )
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

    return render(request, 'content/contacts.html', {'contacts': contacts})

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

    return render(request,"content/messages.html", {'page_obj': page_obj})

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

    return render(request, "agents/agent_registrations.html", {
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

    return render(request, "properties/property_registerations.html", {
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

    return render(request, 'content/request_forms.html', {'page_obj': page_obj})

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

    return render(request, 'properties/expired_properties.html', {
        'property': expired,
        'search': search,
        'start_date': start_date,
        'end_date': end_date,
        "categories": Category.objects.all(),
        "purposes": Purpose.objects.all(),
        "amenities": Amenities.objects.all(),
    })

# @never_cache
# @require_POST
# def edit_exproperty(request, property_id):
#     prop = get_object_or_404(ExpiredProperty, id=property_id)

#     category_id = request.POST.get("category")
#     purpose_id = request.POST.get("purpose")
#     prop.label = request.POST.get('label')
#     prop.land_area = request.POST.get("land_area")
#     prop.sq_ft = request.POST.get("sq_ft")
#     prop.description = request.POST.get("description")
#     # prop.amenities = request.POST.get("amenities")
#     # amenity_ids = request.POST.getlist("amenities")
#     amenity_ids = request.POST.get("amenities", "")

#     prop.save()

#     if amenity_ids:
#         prop.amenities.set(amenity_ids.split(","))
#     else:
#         prop.amenities.clear()
#     prop.perprice = request.POST.get("perprice")
#     prop.price = request.POST.get("price")
#     prop.owner = request.POST.get("owner")
#     prop.whatsapp = request.POST.get("whatsapp")
#     prop.phone = request.POST.get("phone")
#     prop.location = request.POST.get("location")
#     prop.city = request.POST.get("city")
#     prop.pincode = request.POST.get("pincode")
#     prop.land_mark = request.POST.get("land_mark")
#     prop.paid = request.POST.get("paid") == "Yes"
#     prop.added_by = request.POST.get("added_by")

#     # Duration
#     duration_days = request.POST.get("duration_days")
#     if duration_days:
#         try:
#             prop.duration_days = int(duration_days)
#         except ValueError:
#             prop.duration_days = 0

#     if category_id:
#         prop.category = get_object_or_404(Category, id=category_id)
#     if purpose_id:
#         prop.purpose = get_object_or_404(Purpose, id=purpose_id)

#     prop.save()

#     # Handle new images
#     for img in request.FILES.getlist("images"):
#         PropertyImage.objects.create(expired_property=prop, image=img)

#     # Handle image deletions
#     for img_id in request.POST.getlist("delete_images"):
#         try:
#             image_obj = PropertyImage.objects.get(id=img_id, expired_property=prop)
#             image_obj.delete()
#         except PropertyImage.DoesNotExist:
#             pass

#     messages.success(request, "Property updated successfully.")
#     return redirect('expired_property')

@never_cache
@require_POST
def edit_exproperty(request, property_id):
    prop = get_object_or_404(ExpiredProperty, id=property_id)

    prop.label = request.POST.get("label")
    prop.land_area = request.POST.get("land_area")
    prop.sq_ft = request.POST.get("sq_ft")
    prop.description = request.POST.get("description")
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

    category_id = request.POST.get("category")
    purpose_id = request.POST.get("purpose")

    if category_id:
        prop.category = Category.objects.get(id=category_id)

    if purpose_id:
        prop.purpose = Purpose.objects.get(id=purpose_id)

    duration = request.POST.get("duration_days")
    if duration:
        prop.duration_days = int(duration)

    prop.save()

    # ----------- Amenities -------------
    amenity_ids = request.POST.get("amenities")

    print("Amenity ids =", amenity_ids)

    if amenity_ids:
        ids = [int(i) for i in amenity_ids.split(",") if i]
        prop.amenities.set(ids)
    else:
        prop.amenities.clear()

    # -------- Images --------

    for img in request.FILES.getlist("images"):
        PropertyImage.objects.create(
            expired_property=prop,
            image=img
        )

    for img_id in request.POST.getlist("delete_images"):
        PropertyImage.objects.filter(
            id=img_id,
            expired_property=prop
        ).delete()

    messages.success(request, "Updated successfully.")
    return redirect("expired_property")

# @never_cache
# @user_passes_test(superuser_required, login_url='superuser_login_view')
# @require_POST
# def delete_property(request, pk):
#     prop = get_object_or_404(Property, pk=pk)
#     prop.delete()
#     return redirect('add_property')


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

    return render(request, "agents/expired_agents.html", {"premium": premium})


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

    return render(request, "agents/expired_agents.html", {
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

# def AddUser(request):
#     success = None
#     error = None

#     if request.method == "POST":
#         action = request.POST.get("action")

#         try:

#             # ================= ADD USER =================
#             if action == "add":
#                 name = request.POST.get("name")
#                 email = request.POST.get("email")
#                 mobile = request.POST.get("mobile")

#                 plan_ids = request.POST.getlist("plan_id")
#                 print("PLAN IDS:", plan_ids)

#                 allowed_domains = ["gmail.com", "yahoo.com", "email.com"]

#                 # ===== VALIDATIONS =====
#                 if not name or not mobile:
#                     error = "Name and Mobile are required"

#                 elif not mobile.isdigit() or len(mobile) != 10:
#                     error = "Mobile must be 10 digits"

#                 elif email and UserAdd.objects.filter(email=email).exists():
#                     error = "Email already exists"

#                 elif UserAdd.objects.filter(mobile=mobile).exists():
#                     error = "Mobile already exists"

#                 elif not plan_ids:
#                     error = "Select at least one plan"

#                 elif len(plan_ids) > 2:
#                     error = "Maximum 2 plans allowed"

#                 elif email:
#                     domain = email.split("@")[-1]
#                     if domain not in allowed_domains:
#                         error = "Only Gmail, Yahoo or Email.com allowed"

#                 # ===== SAVE =====
#                 if not error:
#                     user = UserAdd.objects.create(
#                         name=name,
#                         email=email,
#                         mobile=mobile,
#                         is_active=True
#                     )

#                     plans = Userplan.objects.filter(id__in=plan_ids)
#                     user.user_plans.set(plans)

#                     success = "User created successfully"

#             # ================= EDIT USER =================
#             elif action == "edit":
#                 user = UserAdd.objects.get(id=request.POST.get("user_id"))

#                 name = request.POST.get("name")
#                 email = request.POST.get("email")
#                 mobile = request.POST.get("mobile")
#                 plan_ids = request.POST.getlist("plan_id")

#                 # ===== VALIDATION =====
#                 if not name or not mobile:
#                     error = "Name and Mobile are required"

#                 elif not mobile.isdigit() or len(mobile) != 10:
#                     error = "Mobile must be 10 digits"

#                 elif email and UserAdd.objects.filter(email=email).exclude(id=user.id).exists():
#                     error = "Email already exists"

#                 elif UserAdd.objects.filter(mobile=mobile).exclude(id=user.id).exists():
#                     error = "Mobile already exists"

#                 elif len(plan_ids) > 2:
#                     error = "Maximum 2 plans allowed"

#                 # ===== SAVE =====
#                 if not error:
#                     user.name = name
#                     user.email = email
#                     user.mobile = mobile

#                     plans = Userplan.objects.filter(id__in=plan_ids)
#                     user.user_plans.set(plans)

#                     user.save()
#                     success = "User updated successfully"

#             # ================= UPGRADE USER =================
#             elif action == "upgrade":
#                 user = UserAdd.objects.get(id=request.POST.get("user_id"))
#                 plan_id = request.POST.get("upgrade_plan_id")

#                 # ✅ OPTIONAL UPGRADE (FIXED)
#                 if plan_id:
#                     upgrade_plan = Userupgrade.objects.get(id=plan_id)
#                     user.upgrade_plan = upgrade_plan
#                     success = "User upgraded successfully"
#                 else:
#                     user.upgrade_plan = None
#                     success = "Upgrade removed"

#                 user.save()

#             # ================= DELETE =================
#             elif action == "delete":
#                 user = UserAdd.objects.get(id=request.POST.get("user_id"))
#                 user.delete()
#                 success = "User deleted"

#             # ================= TOGGLE STATUS =================
#             elif action == "toggle":
#                 user = UserAdd.objects.get(id=request.POST.get("user_id"))
#                 user.is_active = not user.is_active
#                 user.save()
#                 success = "User status updated"

#         except Exception as e:
#             error = f"Error: {e}"
#             print("ERROR:", e)

#     users = UserAdd.objects.all().order_by("-created")
#     plans = Userplan.objects.all()
#     upgrades = Userupgrade.objects.all()

#     return render(request, "usercreate.html", {
#         "users": users,
#         "plans": plans,
#         "upgrades": upgrades,
#         "success": success,
#         "error": error
#     })

from django.shortcuts import render
from django.db import transaction
from django.contrib.auth.hashers import make_password

from .models import UserCreate, Userplan


def AddUser(request):

    success = None
    error = None

    if request.method == "POST":

        action = request.POST.get("action")

        try:

            # ==================================================
            # ADD USER
            # ==================================================
            if action == "add":

                name = request.POST.get("name", "").strip()
                email = request.POST.get("email", "").strip().lower()
                mobile = request.POST.get("mobile", "").strip()

                plan_ids = request.POST.getlist("plan_id")

                allowed_domains = [
                    "gmail.com",
                    "yahoo.com",
                    "email.com",
                ]

                # ---------------- VALIDATION ----------------

                if not name or not email:

                    error = "Name and Email are required."

                elif UserCreate.objects.filter(
                    email=email
                ).exists():

                    error = "Email already exists."

                elif mobile and (
                    not mobile.isdigit() or len(mobile) != 10
                ):

                    error = "Mobile number must contain exactly 10 digits."

                else:

                    domain = email.split("@")[-1]

                    if domain not in allowed_domains:

                        error = (
                            "Only Gmail, Yahoo and Email.com addresses are allowed."
                        )

                # ---------------- CREATE USER ----------------

                if not error:

                    with transaction.atomic():

                        user = UserCreate.objects.create(
                            name=name,
                            email=email,
                            mobile=mobile if mobile else None,
                            password=make_password("123456"),
                            is_verified=True,
                        )

                        if plan_ids:

                            plans = Userplan.objects.filter(
                                id__in=plan_ids
                            )

                            user.user_plans.set(plans)

                        # Save again so your model updates
                        # role/profile after assigning plans
                        user.save()

                    success = "User created successfully."

            # ==================================================
            # EDIT USER
            # ==================================================
            elif action == "edit":

                user_id = request.POST.get("user_id")

                try:

                    user = UserCreate.objects.get(
                        id=user_id
                    )

                except UserCreate.DoesNotExist:

                    user = None
                    error = "User not found."

                if user:

                    name = request.POST.get("name", "").strip()
                    email = request.POST.get("email", "").strip().lower()
                    mobile = request.POST.get("mobile", "").strip()

                    plan_ids = request.POST.getlist("plan_id")

                    # ------------ VALIDATION ------------

                    if not name or not email:

                        error = "Name and Email are required."

                    elif UserCreate.objects.filter(
                        email=email
                    ).exclude(
                        id=user.id
                    ).exists():

                        error = "Email already exists."

                    elif mobile and (
                        not mobile.isdigit()
                        or len(mobile) != 10
                    ):

                        error = (
                            "Mobile number must contain exactly 10 digits."
                        )

                    # ------------ UPDATE ------------

                    if not error:

                        with transaction.atomic():

                            user.name = name
                            user.email = email
                            user.mobile = (
                                mobile if mobile else None
                            )

                            if plan_ids:

                                plans = Userplan.objects.filter(
                                    id__in=plan_ids
                                )

                                user.user_plans.set(plans)

                            else:

                                user.user_plans.clear()

                            user.save()

                        success = (
                            "User updated successfully."
                        )

            # ==================================================
            # DELETE USER
            # ==================================================
            elif action == "delete":

                user_id = request.POST.get("user_id")

                try:

                    user = UserCreate.objects.get(
                        id=user_id
                    )

                    user.delete()

                    success = "User deleted successfully."

                except UserCreate.DoesNotExist:

                    error = "User not found."

        except Exception as e:

            print(e)

            error = str(e)

    # ==================================================
    # PAGE DATA
    # ==================================================

    users = UserCreate.objects.prefetch_related(
        "user_plans"
    ).order_by("-created_at")

    plans = Userplan.objects.all().order_by("name")

    return render(
        request,
        "users/users.html",
        {
            "users": users,
            "plans": plans,
            "success": success,
            "error": error,
        },
    )


# from django.shortcuts import render, redirect
# from django.db import transaction
# from django.contrib import messages
# import openpyxl

# from django.shortcuts import render
# from django.db import transaction
# from .models import UserCreate, Userplan


# def AddUser(request):

#     success = None
#     error = None

#     if request.method == "POST":

#         action = request.POST.get("action")

#         try:

#             # ==========================================
#             # ADD USER
#             # ==========================================
#             if action == "add":

#                 name = request.POST.get("name")
#                 email = request.POST.get("email")
#                 mobile = request.POST.get("mobile")

#                 plan_ids = request.POST.getlist("plan_id")

#                 allowed_domains = [
#                     "gmail.com",
#                     "yahoo.com",
#                     "email.com"
#                 ]

#                 # ---------------- VALIDATION ----------------

#                 if not name or not email:

#                     error = "Name and Email are required"

#                 elif UserCreate.objects.filter(
#                     email=email
#                 ).exists():

#                     error = "Email already exists"

#                 elif (
#                     mobile
#                     and (
#                         not mobile.isdigit()
#                         or len(mobile) != 10
#                     )
#                 ):

#                     error = "Mobile must be 10 digits"

#                 elif email:

#                     domain = email.split("@")[-1]

#                     if domain not in allowed_domains:

#                         error = (
#                             "Only Gmail, Yahoo or "
#                             "Email.com allowed"
#                         )

#                 # ---------------- SAVE ----------------

#                 if not error:

#                     with transaction.atomic():

#                         user = UserCreate.objects.create(
#                             name=name,
#                             email=email,
#                             mobile=mobile,
#                             password="123456"
#                         )

#                         # USER PLANS

#                         if plan_ids:

#                             plans = Userplan.objects.filter(
#                                 id__in=plan_ids
#                             )

#                             user.user_plans.set(plans)

#                         user.save()

#                         success = (
#                             "User created successfully"
#                         )

#             # ==========================================
#             # EDIT USER
#             # ==========================================
#             elif action == "edit":

#                 user = UserCreate.objects.get(
#                     id=request.POST.get("user_id")
#                 )

#                 name = request.POST.get("name")
#                 email = request.POST.get("email")
#                 mobile = request.POST.get("mobile")

#                 plan_ids = request.POST.getlist(
#                     "plan_id"
#                 )

#                 # ---------------- VALIDATION ----------------

#                 if not name or not email:

#                     error = "Name and Email are required"

#                 elif UserCreate.objects.filter(
#                     email=email
#                 ).exclude(
#                     id=user.id
#                 ).exists():

#                     error = "Email already exists"

#                 elif (
#                     mobile
#                     and (
#                         not mobile.isdigit()
#                         or len(mobile) != 10
#                     )
#                 ):

#                     error = "Mobile must be 10 digits"

#                 # ---------------- UPDATE ----------------

#                 if not error:

#                     user.name = name
#                     user.email = email
#                     user.mobile = mobile

#                     # UPDATE USER PLANS

#                     if plan_ids:

#                         plans = Userplan.objects.filter(
#                             id__in=plan_ids
#                         )

#                         user.user_plans.set(plans)

#                     else:

#                         user.user_plans.clear()

#                     user.save()

#                     success = (
#                         "User updated successfully"
#                     )

#             # ==========================================
#             # DELETE USER
#             # ==========================================
#             elif action == "delete":

#                 user = UserCreate.objects.get(
#                     id=request.POST.get("user_id")
#                 )

#                 user.delete()

#                 success = "User deleted"

#             # ==========================================
#             # TOGGLE USER
#             # ==========================================
#             elif action == "toggle":

#                 user = UserCreate.objects.get(
#                     id=request.POST.get("user_id")
#                 )

#                 if hasattr(user, "is_active"):

#                     user.is_active = (
#                         not user.is_active
#                     )

#                     user.save()

#                 success = (
#                     "User status updated"
#                 )

#         except Exception as e:

#             error = f"Error: {str(e)}"

#             print("ERROR:", e)

#     # ==========================================
#     # TEMPLATE DATA
#     # ==========================================

#     users = UserCreate.objects.all().order_by(
#         "-created_at"
#     )

#     plans = Userplan.objects.all()

#     return render(
#         request,
#         "users/users.html",
#         {
#             "users": users,
#             "plans": plans,
#             "success": success,
#             "error": error
#         }
#     )

# from .models import UserCreate, Userplan, Userupgrade


# def AddUser(request):
#     success = None
#     error = None

#     if request.method == "POST":
#         action = request.POST.get("action")

#         try:
#             # ================= ADD USER =================
#             if action == "add":
#                 name = request.POST.get("name")
#                 email = request.POST.get("email")
#                 mobile = request.POST.get("mobile")

#                 plan_ids = request.POST.getlist("plan_id")
#                 upgrade_plan_id = request.POST.get("upgrade_plan_id")

#                 allowed_domains = ["gmail.com", "yahoo.com", "email.com"]

#                 # ===== VALIDATION =====
#                 if not name or not email:
#                     error = "Name and Email are required"

#                 elif UserCreate.objects.filter(email=email).exists():
#                     error = "Email already exists"

#                 elif mobile and (not mobile.isdigit() or len(mobile) != 10):
#                     error = "Mobile must be 10 digits"

#                 elif email:
#                     domain = email.split("@")[-1]
#                     if domain not in allowed_domains:
#                         error = "Only Gmail, Yahoo or Email.com allowed"

#                 # ===== SAVE =====
#                 if not error:

#                     with transaction.atomic():

#                         user = UserCreate.objects.create(
#                             name=name,
#                             email=email,
#                             mobile=mobile,
#                             password="123456"  # default (replace with proper auth later)
#                         )

#                         # ================= PLANS =================
#                         if plan_ids:
#                             plans = Userplan.objects.filter(id__in=plan_ids)
#                             user.user_plans.set(plans)

#                         # ================= UPGRADE PLAN =================
#                         if upgrade_plan_id:
#                             try:
#                                 upgrade_plan = Userupgrade.objects.get(id=upgrade_plan_id)
#                                 user.upgrade_plan = upgrade_plan
#                                 user.save()
#                             except Userupgrade.DoesNotExist:
#                                 pass

#                         success = "User created successfully"

#             # ================= EDIT USER =================
#             elif action == "edit":

#                 user = UserCreate.objects.get(id=request.POST.get("user_id"))

#                 name = request.POST.get("name")
#                 email = request.POST.get("email")
#                 mobile = request.POST.get("mobile")

#                 plan_ids = request.POST.getlist("plan_id")
#                 upgrade_plan_id = request.POST.get("upgrade_plan_id")

#                 # ===== VALIDATION =====
#                 if not name or not email:
#                     error = "Name and Email are required"

#                 elif UserCreate.objects.filter(email=email).exclude(id=user.id).exists():
#                     error = "Email already exists"

#                 elif mobile and (not mobile.isdigit() or len(mobile) != 10):
#                     error = "Mobile must be 10 digits"

#                 # ===== SAVE =====
#                 if not error:

#                     user.name = name
#                     user.email = email
#                     user.mobile = mobile

#                     # update plans
#                     if plan_ids:
#                         plans = Userplan.objects.filter(id__in=plan_ids)
#                         user.user_plans.set(plans)
#                     else:
#                         user.user_plans.clear()

#                     # update upgrade plan
#                     if upgrade_plan_id:
#                         try:
#                             user.upgrade_plan = Userupgrade.objects.get(id=upgrade_plan_id)
#                         except Userupgrade.DoesNotExist:
#                             user.upgrade_plan = None
#                     else:
#                         user.upgrade_plan = None

#                     user.save()

#                     success = "User updated successfully"

#             # ================= UPGRADE ONLY =================
#             elif action == "upgrade":

#                 user = UserCreate.objects.get(id=request.POST.get("user_id"))
#                 plan_id = request.POST.get("upgrade_plan_id")

#                 if plan_id:
#                     user.upgrade_plan = Userupgrade.objects.get(id=plan_id)
#                     success = "User upgraded successfully"
#                 else:
#                     user.upgrade_plan = None
#                     success = "Upgrade removed"

#                 user.save()

#             # ================= DELETE =================
#             elif action == "delete":
#                 user = UserCreate.objects.get(id=request.POST.get("user_id"))
#                 user.delete()
#                 success = "User deleted"

#             # ================= TOGGLE (OPTIONAL) =================
#             elif action == "toggle":
#                 user = UserCreate.objects.get(id=request.POST.get("user_id"))

#                 if hasattr(user, "is_active"):
#                     user.is_active = not user.is_active
#                     user.save()

#                 success = "User status updated"

#         except Exception as e:
#             error = f"Error: {str(e)}"
#             print("ERROR:", e)

#     # ================= DATA FOR TEMPLATE =================
#     users = UserCreate.objects.all().order_by("-created_at")
#     plans = Userplan.objects.all()
#     upgrades = Userupgrade.objects.all()

#     return render(request, "usercreate.html", {
#         "users": users,
#         "plans": plans,
#         "upgrades": upgrades,
#         "success": success,
#         "error": error
#     })

# from django.shortcuts import render, redirect, get_object_or_404
# from decimal import Decimal

# from .models import (
#     Userplan,
#     PremiumPlan,
#     ElitePlan,
#     AgentPlan,
#     Purpose,
#     Category
# )


# def plans(request):

#     success = None
#     error = None
#     edit_plan = None

#     # =========================================
#     # DELETE
#     # =========================================

#     delete_id = request.GET.get("delete_id")
#     delete_type = request.GET.get("delete_type")

#     if delete_id and delete_type:

#         model_map = {
#             "userplan": Userplan,
#             "premiumplan": PremiumPlan,
#             "eliteplan": ElitePlan,
#             "agentplan": AgentPlan
#         }

#         model = model_map.get(delete_type)

#         if model:
#             model.objects.filter(id=delete_id).delete()

#         return redirect("userplan")

#     # =========================================
#     # EDIT FETCH
#     # =========================================

#     edit_id = request.GET.get("edit_id")
#     edit_type = request.GET.get("type")

#     if edit_id and edit_type == "userplan":

#         edit_plan = get_object_or_404(
#             Userplan,
#             id=edit_id
#         )

#     # =========================================
#     # POST
#     # =========================================

#     if request.method == "POST":

#         form_type = request.POST.get("form_type")

#         # =====================================
#         # USER PLAN
#         # =====================================

#         if form_type == "userplan":

#             plan_id = request.POST.get("plan_id")

#             plan = (
#                 get_object_or_404(
#                     Userplan,
#                     id=plan_id
#                 )
#                 if plan_id
#                 else Userplan()
#             )

#             plan.name = request.POST.get(
#                 "name",
#                 ""
#             )

#             plan.validity = int(
#                 request.POST.get("validity") or 0
#             )

#             plan.amount = Decimal(
#                 request.POST.get("amount") or 0
#             )

#             # =================================
#             # OLD UPGRADE FIELDS MOVED HERE
#             # =================================

#             plan.listing = request.POST.get(
#                 "listing"
#             )

#             plan.enquiries = int(
#                 request.POST.get("enquiries") or 0
#             )

#             plan.edit = int(
#                 request.POST.get("edit") or 0
#             )

#             plan.genuine = request.POST.get(
#                 "genuine"
#             )

#             plan.meta = int(
#                 request.POST.get("meta") or 0
#             )

#             plan.bulk = int(
#                 request.POST.get("bulk") or 0
#             )

#             plan.poster = int(
#                 request.POST.get("poster") or 0
#             )

#             plan.social_media = request.POST.get(
#                 "social_media"
#             )

#             plan.lead_follow = request.POST.get(
#                 "lead_follow"
#             )

#             plan.best = request.POST.get(
#                 "best"
#             )

#             # =================================
#             # OLD USERPLAN FIELDS
#             # =================================

#             plan.residential_limit = int(
#                 request.POST.get(
#                     "residential_limit"
#                 ) or 0
#             )

#             plan.commercial_limit = int(
#                 request.POST.get(
#                     "commercial_limit"
#                 ) or 0
#             )

#             plan.edit_option = request.POST.get(
#                 "edit_option"
#             )

#             plan.matching_clients = request.POST.get(
#                 "matching_clients"
#             )

#             plan.top_priority_search = request.POST.get(
#                 "top_priority_search"
#             )

#             plan.meta_ads_promotion = request.POST.get(
#                 "meta_ads_promotion"
#             )

#             plan.bulk_whatsapp = request.POST.get(
#                 "bulk_whatsapp"
#             )

#             plan.offline_agent_share = request.POST.get(
#                 "offline_agent_share"
#             )

#             plan.poster_creation = request.POST.get(
#                 "poster_creation"
#             )

#             plan.social_media_marketing = request.POST.get(
#                 "social_media_marketing"
#             )

#             plan.lead_followup_support = request.POST.get(
#                 "lead_followup_support"
#             )

#             plan.save()

#             return redirect("userplan")

#         # =====================================
#         # PREMIUM PLAN
#         # =====================================

#         elif form_type == "premiumplan":

#             plan_id = request.POST.get("plan_id")

#             plan = (
#                 get_object_or_404(
#                     PremiumPlan,
#                     id=plan_id
#                 )
#                 if plan_id
#                 else PremiumPlan()
#             )

#             plan.name = request.POST.get(
#                 "name",
#                 ""
#             )

#             plan.validity = int(
#                 request.POST.get("validity") or 0
#             )

#             plan.total_listing = int(
#                 request.POST.get(
#                     "total_listing"
#                 ) or 0
#             )

#             plan.residential_limit = int(
#                 request.POST.get(
#                     "residential_limit"
#                 ) or 0
#             )

#             plan.commercial_limit = int(
#                 request.POST.get(
#                     "commercial_limit"
#                 ) or 0
#             )

#             plan.edit = request.POST.get(
#                 "edit"
#             )

#             plan.enquiries = request.POST.get(
#                 "enquiries"
#             )

#             plan.priority_search = request.POST.get(
#                 "priority_search"
#             )

#             plan.meta_ads = request.POST.get(
#                 "meta_ads"
#             )

#             plan.Bulk_whatsapp = request.POST.get(
#                 "Bulk_whatsapp"
#             )

#             plan.Poster = request.POST.get(
#                 "Poster"
#             )

#             plan.social_media = request.POST.get(
#                 "social_media"
#             )

#             plan.lead_follow = request.POST.get(
#                 "lead_follow"
#             )

#             plan.lead_management = request.POST.get(
#                 "lead_management"
#             )

#             plan.price = int(
#                 request.POST.get("price") or 0
#             )

#             plan.save()

#             return redirect("userplan")

#         # =====================================
#         # ELITE PLAN
#         # =====================================

#         elif form_type == "eliteplan":

#             plan_id = request.POST.get("plan_id")

#             plan = (
#                 get_object_or_404(
#                     ElitePlan,
#                     id=plan_id
#                 )
#                 if plan_id
#                 else ElitePlan()
#             )

#             plan.name = request.POST.get(
#                 "name",
#                 ""
#             )

#             plan.plan_validity_days = int(
#                 request.POST.get("validity") or 0
#             )

#             plan.total_property_listings = int(
#                 request.POST.get(
#                     "total_listing"
#                 ) or 0
#             )

#             plan.sale_listings_limit = int(
#                 request.POST.get("sale") or 0
#             )

#             plan.priority_search = request.POST.get(
#                 "priority_search"
#             )

#             plan.meta_ads_promotion = request.POST.get(
#                 "meta_ads"
#             )

#             plan.bulk_whatsapp_messages = request.POST.get(
#                 "bulk_whatsapp"
#             )

#             plan.poster_creation = request.POST.get(
#                 "poster"
#             )

#             plan.social_media_marketing = request.POST.get(
#                 "social_media"
#             )

#             plan.lead_followup_support = request.POST.get(
#                 "lead_follow"
#             )

#             plan.lead_management = request.POST.get(
#                 "lead_management"
#             )

#             plan.price = int(
#                 request.POST.get("price") or 0
#             )

#             plan.save()

#             return redirect("userplan")

#         # =====================================
#         # AGENT PLAN
#         # =====================================

#         elif form_type == "agentplan":

#             plan_id = request.POST.get("plan_id")

#             plan = (
#                 get_object_or_404(
#                     AgentPlan,
#                     id=plan_id
#                 )
#                 if plan_id
#                 else AgentPlan()
#             )

#             plan.name = request.POST.get(
#                 "name",
#                 ""
#             )

#             plan.validity = int(
#                 request.POST.get("validity") or 0
#             )

#             plan.edit = request.POST.get(
#                 "edit"
#             )

#             plan.enquiries = request.POST.get(
#                 "enquiries"
#             )

#             plan.priority_search = request.POST.get(
#                 "priority_search"
#             )

#             plan.meta_ads = request.POST.get(
#                 "meta_ads"
#             )

#             plan.Bulk_whatsapp = request.POST.get(
#                 "Bulk_whatsapp"
#             )

#             plan.Poster = request.POST.get(
#                 "Poster"
#             )

#             plan.social_media = request.POST.get(
#                 "social_media"
#             )

#             plan.price = int(
#                 request.POST.get("price") or 0
#             )

#             plan.save()

#             return redirect("userplan")

#     # =========================================
#     # RENDER
#     # =========================================

#     return render(request, "plans.html", {

#         "plans": Userplan.objects.all().order_by(
#             "-created"
#         ),

#         "premium_plans": PremiumPlan.objects.all().order_by(
#             "-id"
#         ),

#         "elite_plans": ElitePlan.objects.all().order_by(
#             "-id"
#         ),

#         "agent_plans": AgentPlan.objects.all().order_by(
#             "-id"
#         ),

#         "edit_plan": edit_plan,

#         "success": success,
#         "error": error
#     })

from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Userplan,
    PremiumPlan,
    ElitePlan,
    AgentPlan,
    Purpose,
    Category
)


def plans(request):

    success = None
    error = None
    edit_plan = None

    # =========================================
    # DELETE
    # =========================================

    delete_id = request.GET.get("delete_id")
    delete_type = request.GET.get("delete_type")

    if delete_id and delete_type:

        model_map = {
            "userplan": Userplan,
            "premiumplan": PremiumPlan,
            "eliteplan": ElitePlan,
            "agentplan": AgentPlan
        }

        model = model_map.get(delete_type)

        if model:

            model.objects.filter(
                id=delete_id
            ).delete()

        return redirect("userplan")

    # =========================================
    # EDIT FETCH
    # =========================================

    edit_id = request.GET.get("edit_id")
    edit_type = request.GET.get("type")

    if edit_id and edit_type == "userplan":

        edit_plan = get_object_or_404(
            Userplan,
            id=edit_id
        )

    # =========================================
    # POST
    # =========================================

    if request.method == "POST":

        form_type = request.POST.get("form_type")

        # =====================================
        # USER PLAN
        # =====================================

        if form_type == "userplan":

            plan_id = request.POST.get("plan_id")

            plan = (
                get_object_or_404(
                    Userplan,
                    id=plan_id
                )
                if plan_id
                else Userplan()
            )

            # =================================
            # BASIC
            # =================================

            plan.name = request.POST.get(
                "name",
                ""
            )

            plan.validity = request.POST.get(
                "validity",
                ""
            )

            plan.price = request.POST.get(
                "price"
            ) or 0

            # =================================
            # PROPERTY LISTING
            # =================================

            plan.property_listing_limit = request.POST.get(
                "property_listing_limit",
                ""
            )

            plan.listing_type = request.POST.get(
                "listing_type",
                ""
            )

            # =================================
            # ENQUIRIES
            # =================================

            plan.enquiry_limit = request.POST.get(
                "enquiry_limit",
                ""
            )

            # =================================
            # EDIT OPTION
            # =================================

            plan.property_edit_option = request.POST.get(
                "property_edit_option",
                ""
            )

            # =================================
            # PROPERTY VISIBILITY
            # =================================

            plan.property_visibility = request.POST.get(
                "property_visibility",
                ""
            )

            # =================================
            # PRIORITY SEARCH
            # =================================

            plan.priority_search = request.POST.get(
                "priority_search",
                ""
            )

            # =================================
            # META ADS PROMOTION
            # =================================

            plan.meta_ads_promotion = request.POST.get(
                "meta_ads_promotion",
                ""
            )

            # =================================
            # BULK WHATSAPP MESSAGE
            # =================================

            plan.bulk_whatsapp_message = request.POST.get(
                "bulk_whatsapp_message",
                ""
            )

            # =================================
            # POSTER CREATION
            # =================================

            plan.poster_creation = request.POST.get(
                "poster_creation",
                ""
            )

            # =================================
            # SOCIAL MEDIA MARKETING
            # =================================

            plan.social_media_marketing = request.POST.get(
                "social_media_marketing",
                ""
            )

            # =================================
            # LEAD FOLLOW SUPPORT
            # =================================

            plan.lead_follow_support = request.POST.get(
                "lead_follow_support",
                ""
            )

            # =================================
            # BEST SUITED FOR
            # =================================

            plan.best_suited_for = request.POST.get(
                "best_suited_for",
                ""
            )

            # =================================
            # SAVE
            # =================================

            plan.save()

            return redirect("userplan")

        # =====================================
        # ELITE PLAN
        # =====================================

        elif form_type == "eliteplan":

            plan_id = request.POST.get("plan_id")

            plan = (
                get_object_or_404(
                    ElitePlan,
                    id=plan_id
                )
                if plan_id
                else ElitePlan()
            )

            plan.name = request.POST.get(
                "name",
                ""
            )

            plan.plan_validity_days = int(
                request.POST.get("validity") or 0
            )

            plan.total_property_listings = int(
                request.POST.get(
                    "total_listing"
                ) or 0
            )

            # plan.sale_listings_limit = int(
            #     request.POST.get("sale") or 0
            # )
            plan.featured_listings_limit = int(
                request.POST.get("sale") or 0
            )

            plan.priority_search = request.POST.get(
                "priority_search"
            )

            plan.meta_ads_promotion = request.POST.get(
                "meta_ads"
            )

            plan.bulk_whatsapp_messages = request.POST.get(
                "bulk_whatsapp"
            )

            plan.poster_creation = request.POST.get(
                "poster"
            )

            plan.social_media_marketing = request.POST.get(
                "social_media"
            )

            plan.lead_followup_support = request.POST.get(
                "lead_follow"
            )

            plan.lead_management = request.POST.get(
                "lead_management"
            )

            plan.price = int(
                request.POST.get("price") or 0
            )

            plan.save()

            return redirect("userplan")
        
        # =====================================
        # PREMIUM PLAN
        # =====================================

        elif form_type == "premiumplan":

            plan_id = request.POST.get("plan_id")

            plan = (
                get_object_or_404(
                    PremiumPlan,
                    id=plan_id
                )
                if plan_id
                else PremiumPlan()
            )

            plan.name = request.POST.get(
                "name",
                ""
            )

            plan.validity = int(
                request.POST.get("validity") or 0
            )

            plan.total_listing = int(
                request.POST.get("total_listing") or 0
            )

            plan.residential_limit = int(
                request.POST.get("residential_limit") or 0
            )

            plan.commercial_limit = int(
                request.POST.get("commercial_limit") or 0
            )

            plan.edit = request.POST.get(
                "edit",
                ""
            )

            plan.enquiries = request.POST.get(
                "enquiries",
                ""
            )

            plan.priority_search = request.POST.get(
                "priority_search",
                ""
            )

            plan.meta_ads = request.POST.get(
                "meta_ads",
                ""
            )

            plan.bulk_whatsapp = request.POST.get(
                "bulk_whatsapp",
                ""
            )

            plan.poster = request.POST.get(
                "poster",
                ""
            )

            plan.social_media = request.POST.get(
                "social_media",
                ""
            )

            plan.lead_follow = request.POST.get(
                "lead_follow",
                ""
            )

            plan.lead_management = request.POST.get(
                "lead_management",
                ""
            )

            plan.price = int(
                request.POST.get("price") or 0
            )

            plan.save()

            return redirect("userplan")

        # =====================================
        # AGENT PLAN
        # =====================================

        elif form_type == "agentplan":

            plan_id = request.POST.get("plan_id")

            plan = (
                get_object_or_404(
                    AgentPlan,
                    id=plan_id
                )
                if plan_id
                else AgentPlan()
            )

            plan.name = request.POST.get(
                "name",
                ""
            )

            plan.validity = int(
                request.POST.get("validity") or 0
            )

            plan.agent_badge = request.POST.get(
                "agent_badge"
            )

            plan.priority_search = request.POST.get(
                "priority_search"
            )

            plan.meta_ads = request.POST.get(
                "meta_ads"
            )

            plan.bulk_whatsapp = request.POST.get(
                "bulk_whatsapp"
            )

            plan.poster = request.POST.get(
                "poster"
            )

            plan.social_media = request.POST.get(
                "social_media"
            )

            plan.price = int(
                request.POST.get("price") or 0
            )

            plan.save()

            return redirect("userplan")

    # =========================================
    # RENDER
    # =========================================

    return render(request, "plans/plans.html", {

        "plans": Userplan.objects.all().order_by(
            "-created"
        ),

        "premium_plans": PremiumPlan.objects.all().order_by(
            "-id"
        ),

        "elite_plans": ElitePlan.objects.all().order_by(
            "-id"
        ),

        "agent_plans": AgentPlan.objects.all().order_by(
            "-id"
        ),

        "edit_plan": edit_plan,

        "success": success,
        "error": error
    })

# from django.shortcuts import render, redirect, get_object_or_404
# from .models import (
#     Userplan, Userupgrade, PremiumPlan,
#     ElitePlan, AgentPlan, Purpose, Category
# )


# from django.shortcuts import render, redirect, get_object_or_404

# from django.shortcuts import render, redirect, get_object_or_404
# from decimal import Decimal

# def plans(request):

#     success = None
#     error = None
#     edit_plan = None

#     # ================= DELETE =================
#     delete_id = request.GET.get("delete_id")
#     delete_type = request.GET.get("delete_type")

#     if delete_id and delete_type:

#         model_map = {
#             "userplan": Userplan,
#             "upgradeplan": Userupgrade,
#             "premiumplan": PremiumPlan,
#             "eliteplan": ElitePlan,
#             "agentplan": AgentPlan
#         }

#         model = model_map.get(delete_type)
#         if model:
#             model.objects.filter(id=delete_id).delete()

#         return redirect("userplan")

#     # ================= EDIT FETCH =================
#     edit_id = request.GET.get("edit_id")
#     edit_type = request.GET.get("type")

#     if edit_id and edit_type == "userplan":
#         edit_plan = get_object_or_404(Userplan, id=edit_id)

#     # ================= POST =================
#     if request.method == "POST":

#         form_type = request.POST.get("form_type")

#         # ---------- USER PLAN ----------
#         if form_type == "userplan":

#             plan_id = request.POST.get("plan_id")
#             plan = get_object_or_404(Userplan, id=plan_id) if plan_id else Userplan()

#             plan.name = request.POST.get("name", "")
#             plan.validity = int(request.POST.get("validity") or 0)
#             plan.amount = Decimal(request.POST.get("amount") or 0)

#             plan.residential_limit = int(request.POST.get("residential_limit") or 0)
#             plan.commercial_limit = int(request.POST.get("commercial_limit") or 0)

#             plan.edit_option = request.POST.get("edit_option")
#             plan.matching_clients = request.POST.get("matching_clients")
#             plan.top_priority_search = request.POST.get("top_priority_search")
#             plan.meta_ads_promotion = request.POST.get("meta_ads_promotion")
#             plan.bulk_whatsapp = request.POST.get("bulk_whatsapp")
#             plan.offline_agent_share = request.POST.get("offline_agent_share")
#             plan.poster_creation = request.POST.get("poster_creation")
#             plan.social_media_marketing = request.POST.get("social_media_marketing")
#             plan.lead_followup_support = request.POST.get("lead_followup_support")

#             plan.save()
#             return redirect("userplan")

#         # ---------- UPGRADE ----------
#         elif form_type == "upgradeplan":

#             plan_id = request.POST.get("plan_id")
#             plan = get_object_or_404(Userupgrade, id=plan_id) if plan_id else Userupgrade()

#             plan.name = request.POST.get("name", "")
#             plan.validity = int(request.POST.get("validity") or 0)

#             plan.listing = request.POST.get("listing")
#             plan.enquiries = int(request.POST.get("enquiries") or 0)

#             plan.edit = request.POST.get("edit")
#             plan.genuine = request.POST.get("genuine")
#             plan.meta = request.POST.get("meta")
#             plan.bulk = request.POST.get("bulk")
#             plan.poster = request.POST.get("poster")
#             plan.social_media = request.POST.get("social_media")
#             plan.lead_follow = request.POST.get("lead_follow")
#             plan.best = request.POST.get("best")

#             plan.save()
#             return redirect("userplan")

#         # ---------- PREMIUM ----------
#         elif form_type == "premiumplan":

#             plan_id = request.POST.get("plan_id")
#             plan = get_object_or_404(PremiumPlan, id=plan_id) if plan_id else PremiumPlan()

#             plan.name = request.POST.get("name", "")
#             plan.validity = int(request.POST.get("validity") or 0)

#             plan.total_listing = int(request.POST.get("total_listing") or 0)
#             plan.residential_limit = int(request.POST.get("residential_limit") or 0)
#             plan.commercial_limit = int(request.POST.get("commercial_limit") or 0)

#             plan.edit = request.POST.get("edit")
#             plan.enquiries = request.POST.get("enquiries")
#             plan.priority_search = request.POST.get("priority_search")
#             plan.meta_ads = request.POST.get("meta_ads")

#             # ✅ IMPORTANT FIX (matching HTML names)
#             plan.Bulk_whatsapp = request.POST.get("Bulk_whatsapp")
#             plan.Poster = request.POST.get("Poster")

#             plan.social_media = request.POST.get("social_media")
#             plan.lead_follow = request.POST.get("lead_follow")
#             plan.lead_management = request.POST.get("lead_management")

#             plan.price = int(request.POST.get("price") or 0)

#             plan.save()
#             return redirect("userplan")

#         # ---------- ELITE ----------
#         elif form_type == "eliteplan":

#             plan_id = request.POST.get("plan_id")
#             plan = get_object_or_404(ElitePlan, id=plan_id) if plan_id else ElitePlan()

#             plan.name = request.POST.get("name", "")
#             plan.plan_validity_days = int(request.POST.get("validity") or 0)

#             plan.total_property_listings = int(request.POST.get("total_listing") or 0)
#             plan.sale_listings_limit = int(request.POST.get("sale") or 0)

#             plan.priority_search = request.POST.get("priority_search")
#             plan.meta_ads_promotion = request.POST.get("meta_ads")
#             plan.bulk_whatsapp_messages = request.POST.get("bulk_whatsapp")
#             plan.poster_creation = request.POST.get("poster")
#             plan.social_media_marketing = request.POST.get("social_media")
#             plan.lead_followup_support = request.POST.get("lead_follow")
#             plan.lead_management = request.POST.get("lead_management")

#             plan.price = int(request.POST.get("price") or 0)

#             plan.save()
#             return redirect("userplan")

#         # ---------- AGENT ----------
#         elif form_type == "agentplan":

#             plan_id = request.POST.get("plan_id")
#             plan = get_object_or_404(AgentPlan, id=plan_id) if plan_id else AgentPlan()

#             plan.name = request.POST.get("name", "")
#             plan.validity = int(request.POST.get("validity") or 0)

#             plan.edit = request.POST.get("edit")
#             plan.enquiries = request.POST.get("enquiries")
#             plan.priority_search = request.POST.get("priority_search")
#             plan.meta_ads = request.POST.get("meta_ads")

#             # ✅ FIX HERE ALSO
#             plan.Bulk_whatsapp = request.POST.get("Bulk_whatsapp")
#             plan.Poster = request.POST.get("Poster")

#             plan.social_media = request.POST.get("social_media")

#             plan.price = int(request.POST.get("price") or 0)

#             plan.save()
#             return redirect("userplan")

#     # ================= RENDER =================
#     return render(request, "plans.html", {
#         "plans": Userplan.objects.all().order_by("-id"),
#         "upgradeuser": Userupgrade.objects.all().order_by("-id"),
#         "premium_plans": PremiumPlan.objects.all().order_by("-id"),
#         "elite_plans": ElitePlan.objects.all().order_by("-id"),
#         "agent_plans": AgentPlan.objects.all().order_by("-id"),
#         "edit_plan": edit_plan,
#         "success": success,
#         "error": error
#     })

# def export_users_excel(request):

#     workbook = openpyxl.Workbook()
#     sheet = workbook.active
#     sheet.title = "Users"

#     # Header
#     sheet.append([
#         "ID",
#         "Name",
#         "Email",
#         "Mobile",
#         "Plan Type",
#         "Plan Name",
#         "Amount",
#         "Validity",
#         "Created"
#     ])

#     users = UserCreate.objects.all().order_by("-created")

#     for user in users:

#         plan_type = user.active_plan or "-"

#         plan_name = "-"
#         amount = "-"
#         validity = "-"

#         # ✅ BASIC PLAN
#         if user.user_plan:
#             plan_name = user.user_plan.name or "-"
#             amount = user.user_plan.amount or "-"
#             validity = user.user_plan.validity or "-"

#         # ✅ UPGRADE PLAN (override if active)
#         if user.active_plan == "upgrade" and user.upgrade_plan:
#             plan_name = user.upgrade_plan.name or "-"
#             validity = user.upgrade_plan.validity or "-"
#             amount = "Included"  # or set if you add amount field

#         sheet.append([
#             user.id,
#             user.name,
#             user.email,
#             user.mobile,
#             plan_type,
#             plan_name,
#             amount,
#             validity,
#             user.created.strftime("%Y-%m-%d %H:%M")
#         ])

#     response = HttpResponse(
#         content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )

#     response["Content-Disposition"] = 'attachment; filename="users.xlsx"'

#     workbook.save(response)

#     return response

from django.http import HttpResponse
import openpyxl

from .models import UserCreate


def export_users_excel(request):

    workbook = openpyxl.Workbook()

    sheet = workbook.active

    sheet.title = "Users"


    # ==========================
    # HEADER
    # ==========================

    sheet.append([
        "ID",
        "Name",
        "Email",
        "Mobile",
        "Role",
        "Plan Name",
        "Plan Amount",
        "Plan Validity",
        "Property Used",
        "Created"
    ])



    # ==========================
    # USERS
    # ==========================

    users = UserCreate.objects.prefetch_related(
        "user_plans"
    ).order_by("-created_at")



    for user in users:


        plans = user.user_plans.all()



        if plans.exists():

            plan_names = []

            plan_amounts = []

            plan_validities = []


            for plan in plans:

                plan_names.append(
                    plan.name
                )


                if hasattr(plan, "amount"):

                    plan_amounts.append(
                        str(plan.amount)
                    )

                else:

                    plan_amounts.append("-")



                if hasattr(plan, "validity"):

                    plan_validities.append(
                        str(plan.validity)
                    )

                else:

                    plan_validities.append("-")



            plan_name = ", ".join(
                plan_names
            )


            amount = ", ".join(
                plan_amounts
            )


            validity = ", ".join(
                plan_validities
            )



        else:


            plan_name = "Free 2 Listings"

            amount = "-"

            validity = "-"



        sheet.append([

            str(user.id),

            user.name,

            user.email,

            user.mobile or "-",

            user.role,

            plan_name,

            amount,

            validity,

            f"{user.paid_property_count}/2",

            user.created_at.strftime(
                "%Y-%m-%d %H:%M"
            )

        ])




    # ==========================
    # RESPONSE
    # ==========================

    response = HttpResponse(
        content_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


    response["Content-Disposition"] = (
        'attachment; filename="users.xlsx"'
    )


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


    return render(request, "plans/promotion.html", {
        "promotions": promotions,
        "advertisements": advertisements
    })
from django.views.decorators.http import require_http_methods
@require_http_methods(["POST"])
def pending_agent_register_api(request):
    full_name = request.POST.get("full_name")
    email = request.POST.get("email")
    phone = request.POST.get("phone_number")
    password = request.POST.get("password")
    city = request.POST.get("city")
    pin_code = request.POST.get("pin_code")
    agent_type = request.POST.get("agent_type")
    plan_name = request.POST.get("plan_name")
    address = request.POST.get("address")

    if PendingAgentRegistration.objects.filter(email=email, status='pending').exists():
        return JsonResponse({
            "status": False,
            "message": "You have already submitted a registration request."
        }, status=400)

    PendingAgentRegistration.objects.create(
        full_name=full_name,
        email=email,
        phone_number=phone,
        password=password,
        city=city,
        pin_code=pin_code,
        agent_type=agent_type,
        plan_name=plan_name,
        address=address,
        status='pending'
    )

    return JsonResponse({
        "status": True,
        "message": "Registration request submitted. Waiting for approval."
    })


def pending_agents_list_view(request):
    pending_agents = PendingAgentRegistration.objects.filter(status='pending')
    return render(request, "agents/pending_agents.html", {"pending_agents": pending_agents})


@require_POST
def approve_agent(request, agent_id):
    pending = get_object_or_404(PendingAgentRegistration, id=agent_id)

    # Generate username
    base_username = pending.email.split("@")[0]
    username = base_username
    counter = 1

    while AgentUserProfile.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    # Create agent
    agent = AgentUserProfile.objects.create(
        username=username,
        email=pending.email,
        phone_number=pending.phone_number,
        whatsapp_number=pending.phone_number,
        city=pending.city,
        pin_code=int(pending.pin_code) if pending.pin_code else 0,
        address=pending.address,
        agent_type=pending.agent_type,
        is_agent=True,
        password=pending.password
    )

    # ✅ FIXED PLAN LOGIC
    if pending.agent_type == "premium" and pending.premium_plan:
        agent.activate_premium_plan(pending.premium_plan)

    elif pending.agent_type == "elite" and pending.elite_plan:
        agent.activate_elite_plan(pending.elite_plan)

    # Delete pending
    pending.delete()

    messages.success(request, f"{agent.username} approved successfully.")
    return redirect("pending_agents_list")

@require_http_methods(["POST"])
def reject_agent(request, agent_id):
    agent_request = get_object_or_404(PendingAgentRegistration, id=agent_id)
    agent_request.status = 'rejected'
    agent_request.save()

    messages.info(request, f"{agent_request.full_name} has been rejected.")
    return redirect('pending_agents_list')





# from django.shortcuts import render, redirect
# from .models import SliderBannerAd

# def banner_management(request):

#     if request.method == "POST":
#         action = request.POST.get("action")

#         # ADD
#         if action == "add":
#             image = request.FILES.get("image")
#             is_active = request.POST.get("is_active") == "on"

#             if image:
#                 SliderBannerAd.objects.create(
#                     image=image,
#                     is_active=is_active
#                 )

#         # DELETE
#         elif action == "delete":
#             banner_id = request.POST.get("banner_id")
#             SliderBannerAd.objects.filter(id=banner_id).delete()

#         # TOGGLE
#         elif action == "toggle":
#             banner_id = request.POST.get("banner_id")
#             try:
#                 banner = SliderBannerAd.objects.get(id=banner_id)
#                 banner.is_active = not banner.is_active
#                 banner.save()
#             except SliderBannerAd.DoesNotExist:
#                 pass

#         return redirect("banner_management")

#     banners = SliderBannerAd.objects.all().order_by("-created_at")

#     return render(request, "banner_management.html", {
#         "banners": banners
#     })


# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from .models import SliderBannerAd


# @login_required(login_url="superuser_login")
# def slider_banner_view(request):

#     # super admin only
#     # if not request.user.is_superuser:
#     #     messages.error(
#     #         request,
#     #         "Unauthorized"
#     #     )
#     #     return redirect("superuser_login")


#     if request.method == "POST":

#         action = request.POST.get("action")


#         # ---------------- ADD ----------------
#         if action == "add_banner":

#             image = request.FILES.get("image")

#             if image:
#                 SliderBannerAd.objects.create(
#                     image=image
#                 )
#                 messages.success(
#                     request,
#                     "Banner uploaded successfully"
#                 )

#             else:
#                 messages.error(
#                     request,
#                     "Please select image"
#                 )

#             return redirect("slider_banner")


#         # ---------------- DELETE ----------------
#         if action == "delete_banner":

#             banner_id = request.POST.get(
#                 "banner_id"
#             )

#             banner = get_object_or_404(
#                 SliderBannerAd,
#                 id=banner_id
#             )

#             banner.delete()

#             messages.success(
#                 request,
#                 "Banner deleted"
#             )

#             return redirect("slider_banner")


#         # ---------------- TOGGLE ----------------
#         if action == "toggle_banner":

#             banner_id = request.POST.get(
#                 "banner_id"
#             )

#             banner = get_object_or_404(
#                 SliderBannerAd,
#                 id=banner_id
#             )

#             banner.is_active = not banner.is_active
#             banner.save()

#             messages.success(
#                 request,
#                 "Banner status updated"
#             )

#             return redirect("slider_banner")


#     banners = SliderBannerAd.objects.all().order_by("-id")

#     return render(
#         request,
#         "banner_management.html",
#         {
#             "banners": banners
#         }
#     )



# def hero_management(request):

#     if request.method == "POST":
#         action = request.POST.get("action")

#         # ADD
#         if action == "add":
#             image = request.FILES.get("image")
#             is_active = request.POST.get("is_active") == "on"

#             if image:
#                 HeroImage.objects.create(
#                     image=image,
#                     is_active=is_active
#                 )

#         # DELETE
#         elif action == "delete":
#             HeroImage.objects.filter(id=request.POST.get("hero_id")).delete()

#         # TOGGLE
#         elif action == "toggle":
#             hero = HeroImage.objects.get(id=request.POST.get("hero_id"))
#             hero.is_active = not hero.is_active
#             hero.save()

#         return redirect("hero_management")

#     heroes = HeroImage.objects.all().order_by("-created_at")

#     return render(request, "hero_management.html", {
#         "heroes": heroes
#     })


def testimonial_admin_view(request):

    if request.method == "POST":
        Testimonial.objects.create(
            user_id=request.POST.get("user"),
            rating=request.POST.get("rating"),
            image=request.FILES.get("image"),
            opinion=request.POST.get("opinion"),
            description=request.POST.get("description"),
            designation=request.POST.get("designation"),
        )
        return redirect("testimonial")

    testimonials = Testimonial.objects.select_related("user", "user__profile").order_by("-id")
    users = UserCreate.objects.all()

    return render(request, "content/testimonials.html", {
        "testimonials": testimonials,
        "users": users
    })
def delete_testimonial(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)
    testimonial.delete()
    return redirect("testimonial")


def edit_testimonial(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)
    users = UserCreate.objects.all()

    if request.method == "POST":
        testimonial.user_id = request.POST.get("user")
        testimonial.rating = request.POST.get("rating")
        # testimonial.image=request.FILES.get("image")
        testimonial.opinion = request.POST.get("opinion")
        testimonial.description = request.POST.get("description")
        testimonial.designation = request.POST.get("designation")

        # if request.FILES.get("image"):
        #     testimonial.image = request.FILES.get("image")
        if request.FILES.get("image"):
            testimonial.image = request.FILES["image"]


        testimonial.save()
        return redirect("testimonial")

    return render(request, "edit_testimonial.html", {
        "t": testimonial,
        "users": users
    })

def userprofile_list_view(request):

    # =========================================================
    # EDIT USER PROFILE
    # Handles profile update submitted from the edit modal
    # =========================================================
    if request.method == "POST" and request.POST.get("profile_id"):

        try:
            profile = get_object_or_404(
                UserProfile,
                id=request.POST.get("profile_id")
            )

            # =====================================================
            # UPDATE EDITABLE PROFILE DETAILS
            # =====================================================
            profile.full_name = request.POST.get("full_name", "").strip()
            profile.username = request.POST.get("username", "").strip()
            profile.mobile = request.POST.get("mobile", "").strip()
            profile.alternate_mobile = request.POST.get(
                "alternate_mobile",
                ""
            ).strip()
            profile.city = request.POST.get("city", "").strip()
            profile.auth_provider = request.POST.get(
                "auth_provider",
                "mobile"
            )

            profile.is_active = (
                request.POST.get("is_active") == "True"
            )

            # =====================================================
            # OPTIONAL PROFILE IMAGE UPDATE
            # Updates image only when a new image is selected
            # =====================================================
            if request.FILES.get("image"):
                profile.image = request.FILES.get("image")

            profile.save()

            # =====================================================
            # TOAST NOTIFICATION — EDIT SUCCESS
            # This message appears as a green toast after redirect
            # =====================================================
            messages.success(
                request,
                "User profile updated successfully."
            )

        except Exception as error:
            print("USER PROFILE UPDATE ERROR:", error)

            # =====================================================
            # TOAST NOTIFICATION — EDIT ERROR
            # This message appears as a red toast when update fails
            # =====================================================
            messages.error(
                request,
                "Unable to update the user profile. Please try again."
            )

        return redirect("userprofiles")

    # =========================================================
    # LOAD USER PROFILES
    # select_related avoids additional queries for user details
    # =========================================================
    profiles = (
        UserProfile.objects
        .select_related("user")
        .all()
        .order_by("-id")
    )

    return render(
        request,
        "users/user_profiles.html",
        {
            "profiles": profiles
        }
    )




def delete_userprofile(request, id):

    try:
        # =========================================================
        # FIND AND DELETE USER PROFILE
        # Returns a 404 page when the profile does not exist
        # =========================================================
        profile = get_object_or_404(UserProfile, id=id)

        # Store the name before deleting for the toast message
        profile_name = (
            profile.full_name
            or profile.username
            or "User profile"
        )

        profile.delete()

        # =========================================================
        # TOAST NOTIFICATION — DELETE SUCCESS
        # This message appears as a green toast after deletion
        # =========================================================
        messages.success(
            request,
            f'{profile_name} deleted successfully.'
        )

    except Exception as error:
        print("USER PROFILE DELETE ERROR:", error)

        # =========================================================
        # TOAST NOTIFICATION — DELETE ERROR
        # This message appears as a red toast when deletion fails
        # =========================================================
        messages.error(
            request,
            "Unable to delete the user profile. Please try again."
        )

    return redirect("userprofiles")


def edit_userprofile(request, id):

    profile = get_object_or_404(UserProfile, id=id)

    if request.method == "POST":

        try:
            # =====================================================
            # UPDATE USER PROFILE FROM SEPARATE EDIT PAGE
            # =====================================================
            profile.full_name = request.POST.get(
                "full_name",
                ""
            ).strip()

            profile.username = request.POST.get(
                "username",
                profile.username
            ).strip()

            profile.mobile = request.POST.get(
                "mobile",
                ""
            ).strip()

            profile.alternate_mobile = request.POST.get(
                "alternate_mobile",
                ""
            ).strip()

            profile.city = request.POST.get(
                "city",
                ""
            ).strip()

            profile.auth_provider = request.POST.get(
                "auth_provider",
                profile.auth_provider
            )

            profile.is_active = (
                request.POST.get("is_active") == "True"
            )

            # =====================================================
            # OPTIONAL IMAGE UPDATE
            # =====================================================
            if request.FILES.get("image"):
                profile.image = request.FILES.get("image")

            profile.save()

            # =====================================================
            # TOAST NOTIFICATION — EDIT SUCCESS
            # =====================================================
            messages.success(
                request,
                "User profile updated successfully."
            )

        except Exception as error:
            print("USER PROFILE EDIT ERROR:", error)

            # =====================================================
            # TOAST NOTIFICATION — EDIT ERROR
            # =====================================================
            messages.error(
                request,
                "Unable to update the user profile. Please try again."
            )

        return redirect("userprofiles")

    return render(
        request,
        "edit_userprofile.html",
        {
            "profile": profile
        }
    )

# def userprofile_list_view(request):

#     if request.method == "POST" and request.POST.get("profile_id"):
#         profile = get_object_or_404(UserProfile, id=request.POST.get("profile_id"))

#         # ✅ Update all editable fields
#         profile.full_name = request.POST.get("full_name")
#         profile.username = request.POST.get("username")
#         profile.mobile = request.POST.get("mobile")
#         profile.alternate_mobile = request.POST.get("alternate_mobile")
#         profile.city = request.POST.get("city")
#         profile.auth_provider = request.POST.get("auth_provider")
#         profile.is_active = request.POST.get("is_active") == "True"

#         # ✅ Image update (Cloudinary)
#         if request.FILES.get("image"):
#             profile.image = request.FILES.get("image")

#         profile.save()

#         return redirect("userprofiles")

#     # ✅ Optimized query
#     profiles = UserProfile.objects.select_related("user").all().order_by("-id")

#     return render(request, "users/user_profiles.html", {
#         "profiles": profiles
#     })

# # ✅ DELETE
# def delete_userprofile(request, id):
#     profile = get_object_or_404(UserProfile, id=id)
#     profile.delete()
#     return redirect("userprofiles")


# # ✅ EDIT
# def edit_userprofile(request, id):
#     profile = get_object_or_404(UserProfile, id=id)

#     if request.method == "POST":
#         profile.full_name = request.POST.get("full_name")
#         profile.mobile = request.POST.get("mobile")
#         profile.city = request.POST.get("city")

#         # ✅ Optional image update
#         if request.FILES.get("image"):
#             profile.image = request.FILES.get("image")

#         profile.save()
#         return redirect("userprofiles")

#     return render(request, "edit_userprofile.html", {"profile": profile})

# def package_dashboard(request):

#     if request.method == "POST":
#         pkg_type = request.POST.get("main_type")
#         pkg_id = request.POST.get("id")

#         # ================= AD PACKAGE =================
#         if pkg_type == "ad":

#             pkg = AdvertisementPackage.objects.get(id=pkg_id) if pkg_id else AdvertisementPackage()

#             pkg.name = request.POST.get("name")
#             pkg.ad_format = request.POST.get("ad_format")
#             pkg.package_type = request.POST.get("package_type")

#             pkg.price_per_day = request.POST.get("price") or 0
#             pkg.ads_per_day = request.POST.get("ads_per_day") or 1
#             pkg.display_seconds = request.POST.get("display_seconds") or 5

#             # features list
#             features = request.POST.get("features", "")
#             pkg.features = [f.strip() for f in features.split(",") if f.strip()]

#             pkg.save()

#         # ================= REEL PACKAGE (UPDATED MODEL) =================
#         elif pkg_type == "reel":

#             pkg = ReelPackage.objects.get(id=pkg_id) if pkg_id else ReelPackage()

#             pkg.name = request.POST.get("name")
#             pkg.reel_type = request.POST.get("reel_type")

#             pkg.price_per_day = request.POST.get("price") or 0
#             pkg.duration = request.POST.get("duration")

#             # ✅ NEW FIELD (replaces includes_editing)

#             # optional new field
#             pkg.reel_format = request.POST.get("reel_format")

#             # optional description
#             pkg.description = request.POST.get("description")

#             pkg.save()

#         return redirect("package_dashboard")

#     # ================= FETCH =================
#     ads = AdvertisementPackage.objects.all()
#     reels = ReelPackage.objects.all()

#     return render(request, "admin_packages.html", {
#         "ads": ads,
#         "reels": reels
#     })
# def delete_package(request, type, id):
#     if type == "ad":
#         AdvertisementPackage.objects.filter(id=id).delete()
#     else:
#         ReelPackage.objects.filter(id=id).delete()

#     return redirect("package_dashboard")


from django.shortcuts import render, redirect, get_object_or_404
from .models import AdvertisementPackage, ReelPackage


def package_dashboard(request):

    if request.method == "POST":

        pkg_type = request.POST.get("main_type")
        pkg_id = request.POST.get("id")

        # =====================================================
        # ADVERTISEMENT PACKAGE
        # =====================================================

        if pkg_type == "ad":

            if pkg_id:
                pkg = get_object_or_404(
                    AdvertisementPackage,
                    id=pkg_id
                )
            else:
                pkg = AdvertisementPackage()

            pkg.name = request.POST.get("name")
            pkg.ad_format = request.POST.get("ad_format")
            pkg.package_type = request.POST.get("package_type")

            pkg.price_per_day = (
                request.POST.get("price") or 0
            )

            pkg.ads_per_day = (
                request.POST.get("ads_per_day") or 1
            )

            pkg.display_seconds = (
                request.POST.get("display_seconds") or 5
            )

            # FEATURES
            features = request.POST.get(
                "features",
                ""
            )

            pkg.features = [

                f.strip()

                for f in features.split(",")

                if f.strip()
            ]

            pkg.description = request.POST.get(
                "description"
            )

            pkg.save()

        # =====================================================
        # REEL PACKAGE
        # =====================================================

        elif pkg_type == "reel":

            if pkg_id:
                pkg = get_object_or_404(
                    ReelPackage,
                    id=pkg_id
                )
            else:
                pkg = ReelPackage()

            pkg.name = request.POST.get("name")

            pkg.reel_type = request.POST.get(
                "reel_type"
            )

            pkg.price_per_day = (
                request.POST.get("price") or 0
            )

            pkg.duration = request.POST.get(
                "duration"
            )

            pkg.reel_format = request.POST.get(
                "reel_format"
            )

            pkg.description = request.POST.get(
                "description"
            )

            pkg.save()

        return redirect("package_dashboard")

    # =====================================================
    # FETCH DATA
    # =====================================================

    ads = AdvertisementPackage.objects.all().order_by("-id")

    reels = ReelPackage.objects.all().order_by("-id")

    return render(request, "plans/packages.html", {
        "ads": ads,
        "reels": reels
    })


# =====================================================
# DELETE PACKAGE
# =====================================================

def delete_package(request, type, id):

    if type == "ad":

        package = get_object_or_404(
            AdvertisementPackage,
            id=id
        )

    elif type == "reel":

        package = get_object_or_404(
            ReelPackage,
            id=id
        )

    else:
        return redirect("package_dashboard")

    package.delete()

    return redirect("package_dashboard")



# from django.shortcuts import render, redirect
# from django.contrib import messages

# from .forms import PendingAgentRegistrationForm


# def agent_registration(request):

#     if request.method == "POST":

#         form = PendingAgentRegistrationForm(request.POST)

#         if form.is_valid():

#             obj = form.save(commit=False)

#             if request.user.is_authenticated:
#                 obj.submitted_by = request.user

#             obj.save()

#             messages.success(
#                 request,
#                 "Registration submitted successfully."
#             )

#             return redirect("agent_registration")

#     else:

#         form = PendingAgentRegistrationForm()

#     return render(
#         request,
#         "agents/admin_agentregistrations.html",
#         {
#             "form": form
#         }
#     )

from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import PendingAgentRegistrationForm
from .models import PendingAgentRegistration


def agent_registration(request):

    if request.method == "POST":

        form = PendingAgentRegistrationForm(request.POST)

        if form.is_valid():

            registration = form.save(commit=False)

            # if request.user.is_authenticated:
            #     registration.submitted_by = request.user
            registration.submitted_by = None

            registration.save()

            if registration.status == "approved":
                messages.success(
                    request,
                    "Agent approved successfully. Agent profile has been created."
                )

            elif registration.status == "pending":
                messages.success(
                    request,
                    "Agent registration saved as Pending."
                )

            elif registration.status == "rejected":
                messages.success(
                    request,
                    "Agent registration has been Rejected."
                )

            return redirect("agent_registration")

    else:

        form = PendingAgentRegistrationForm()

    registrations = PendingAgentRegistration.objects.order_by("-created_at")

    context = {
        "form": form,
        "registrations": registrations,
    }

    return render(
        request,
        "agents/admin_agentregistrations.html",
        context,
    )


def blog_dashboard(request):

    blogs = Blog.objects.select_related(
        "category"
    ).order_by("-date")


    categories = Category.objects.all()


    form = BlogForm()


    edit_form = BlogForm()



    if request.method == "POST":


        form = BlogForm(
            request.POST,
            request.FILES
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "Blog added successfully."
            )


            return redirect(
                "blog_dashboard"
            )


        else:

            print(form.errors)



    context = {

        "blogs": blogs,

        "categories": categories,

        "form": form,

        "edit_form": edit_form,

    }


    return render(
        request,
        "blogs/admin_blog.html",
        context
    )



from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Blog
from .forms import BlogForm


def edit_blog(request, id):

    blog = get_object_or_404(
        Blog,
        id=id
    )

    if request.method == "POST":

        form = BlogForm(
            request.POST,
            request.FILES,
            instance=blog
        )

        if form.is_valid():

            # Keep old image if no new image uploaded
            if not request.FILES.get("image"):

                form.instance.image = blog.image

            form.save()

            messages.success(
                request,
                "Blog updated successfully."
            )

            return redirect(
                "blog_dashboard"
            )

        else:

            print(form.errors)

            messages.error(
                request,
                "Please correct the errors below."
            )

            return redirect(
                "blog_dashboard"
            )

    messages.error(
        request,
        "Invalid request."
    )

    return render(
        "blog_dashboard"
    )

def delete_blog(request, id):

    blog = get_object_or_404(
        Blog,
        id=id
    )

    if request.method == "POST":

        blog.delete()

        messages.success(
            request,
            "Blog deleted successfully."
        )

    return redirect("blog_dashboard")


from django.shortcuts import render
from .models import BannerAd, SliderAd
from .forms import BannerAdForm, SliderAdForm


def ads_dashboard(request):

    context = {

        "banners": BannerAd.objects.order_by("-created_at"),

        "sliders": SliderAd.objects.order_by("-created_at"),

        "banner_form": BannerAdForm(),

        "slider_form": SliderAdForm(),

    }

    return render(
        request,
        "ads/ads_dashboard.html",
        context
    )

from django.shortcuts import redirect
from django.contrib import messages


def add_banner(request):

    if request.method == "POST":

        form = BannerAdForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Banner added successfully."
            )

        else:

            messages.error(
                request,
                form.errors
            )

    return redirect("ads_dashboard")

from django.shortcuts import get_object_or_404


def edit_banner(request, id):

    banner = get_object_or_404(
        BannerAd,
        id=id
    )

    if request.method == "POST":

        form = BannerAdForm(
            request.POST,
            request.FILES,
            instance=banner
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Banner updated."
            )

        else:

            messages.error(
                request,
                form.errors
            )

    return redirect("ads_dashboard")

def delete_banner(request, id):

    banner = get_object_or_404(
        BannerAd,
        id=id
    )

    banner.delete()

    messages.success(
        request,
        "Banner deleted."
    )

    return redirect("ads_dashboard")

def add_slider(request):

    if request.method == "POST":

        form = SliderAdForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Slider image added."
            )

        else:

            messages.error(
                request,
                form.errors
            )

    return redirect("ads_dashboard")

def edit_slider(request, id):

    slider = get_object_or_404(
        SliderAd,
        id=id
    )

    if request.method == "POST":

        form = SliderAdForm(
            request.POST,
            request.FILES,
            instance=slider
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Slider updated."
            )

        else:

            messages.error(
                request,
                form.errors
            )

    return redirect("ads_dashboard")

def delete_slider(request, id):

    slider = get_object_or_404(
        SliderAd,
        id=id
    )

    slider.delete()

    messages.success(
        request,
        "Slider deleted."
    )

    return redirect("ads_dashboard")

from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import (
    AdvertisementRequestNotification,
    ReelPurchaseNotification,
)


# ============================================================
# Advertisement & Reel Dashboard
# ============================================================

# @login_required
def advertisement_notifications(request):

    advertisement_requests = (
        AdvertisementRequestNotification.objects
        .select_related(
            "agent",
            "advertisement_package"
        )
        .order_by("-created_at")
    )

    reel_requests = (
        ReelPurchaseNotification.objects
        .select_related(
            "agent",
            "payment",
            "payment__reel_package"
        )
        .order_by("-created_at")
    )

    # -----------------------------------
    # Search
    # -----------------------------------

    search = request.GET.get("search", "").strip()

    if search:

        advertisement_requests = advertisement_requests.filter(

            Q(agent__username__icontains=search) |
            Q(agent__phone_number__icontains=search) |
            Q(title__icontains=search)

        )

        reel_requests = reel_requests.filter(

            Q(agent__username__icontains=search) |
            Q(agent__phone_number__icontains=search) |
            Q(title__icontains=search)

        )

    # -----------------------------------
    # Type Filter
    # -----------------------------------

    request_type = request.GET.get("type", "")

    if request_type == "advertisement":

        reel_requests = ReelPurchaseNotification.objects.none()

    elif request_type == "reel":

        advertisement_requests = AdvertisementRequestNotification.objects.none()

    # -----------------------------------
    # Status Filter
    # -----------------------------------

    status = request.GET.get("status", "")

    if status:

        advertisement_requests = advertisement_requests.filter(
            status=status
        )

        reel_requests = reel_requests.filter(
            status=status
        )

    # -----------------------------------
    # Create One Common List
    # -----------------------------------

    notifications = []

    for ad in advertisement_requests:

        notifications.append({

            "id": ad.id,

            "request_type": "advertisement",

            "title": ad.title,

            "message": ad.message,

            "agent": ad.agent,

            "package_name": (
                ad.advertisement_package.name
                if ad.advertisement_package
                else "-"
            ),

            "status": ad.status,

            "is_read": ad.is_read,

            "created_at": ad.created_at,

            "object": ad,

        })

    for reel in reel_requests:

        package_name = "-"

        if reel.payment and reel.payment.reel_package:

            package_name = reel.payment.reel_package.name

        notifications.append({

            "id": reel.id,

            "request_type": "reel",

            "title": reel.title,

            "message": reel.message,

            "agent": reel.agent,

            "package_name": package_name,

            "status": reel.status,

            "is_read": reel.is_read,

            "created_at": reel.created_at,

            "object": reel,

        })

    notifications = sorted(

        notifications,

        key=lambda x: x["created_at"],

        reverse=True

    )

    # -----------------------------------
    # Dashboard Counts
    # -----------------------------------

    advertisement_count = AdvertisementRequestNotification.objects.count()

    reel_count = ReelPurchaseNotification.objects.count()

    total_requests = advertisement_count + reel_count

    requested_count = AdvertisementRequestNotification.objects.filter(
        status="requested"
    ).count()

    in_progress_count = (
        AdvertisementRequestNotification.objects.filter(
            status="in_progress"
        ).count()
        +
        ReelPurchaseNotification.objects.filter(
            status="in_progress"
        ).count()
    )

    completed_count = (
        AdvertisementRequestNotification.objects.filter(
            status="completed"
        ).count()
        +
        ReelPurchaseNotification.objects.filter(
            status="completed"
        ).count()
    )

    contacted_count = ReelPurchaseNotification.objects.filter(
        status="contacted"
    ).count()

    unread_count = (
        AdvertisementRequestNotification.objects.filter(
            is_read=False
        ).count()
        +
        ReelPurchaseNotification.objects.filter(
            is_read=False
        ).count()
    )

    context = {

        "notifications": notifications,

        "advertisement_count": advertisement_count,

        "reel_count": reel_count,

        "total_requests": total_requests,

        "requested_count": requested_count,

        "in_progress_count": in_progress_count,

        "completed_count": completed_count,

        "contacted_count": contacted_count,

        "unread_count": unread_count,

        "search": search,

        "current_type": request_type,

        "current_status": status,

    }

    return render(

        request,

        "ads_reels_package/advertisement_notifications.html",

        context,

    )


# ============================================================
# MARK AS READ
# ============================================================

# @login_required
# @require_POST
def mark_notification_read(request, request_type, id):

    if request_type == "advertisement":

        notification = get_object_or_404(
            AdvertisementRequestNotification,
            id=id
        )

    elif request_type == "reel":

        notification = get_object_or_404(
            ReelPurchaseNotification,
            id=id
        )

    else:

        messages.error(
            request,
            "Invalid notification type."
        )

        return redirect("advertisement_notifications")

    notification.is_read = True

    notification.save(update_fields=["is_read"])

    messages.success(
        request,
        "Notification marked as read."
    )

    return redirect("advertisement_notifications")


# ============================================================
# UPDATE STATUS
# ============================================================

# @login_required
# @require_POST
def update_status(request, request_type, id):

    status = request.POST.get("status")

    # -----------------------------
    # Advertisement Request
    # -----------------------------

    if request_type == "advertisement":

        notification = get_object_or_404(
            AdvertisementRequestNotification,
            id=id
        )

        allowed_status = [

            "requested",
            "in_progress",
            "completed",

        ]

    # -----------------------------
    # Reel Request
    # -----------------------------

    elif request_type == "reel":

        notification = get_object_or_404(
            ReelPurchaseNotification,
            id=id
        )

        allowed_status = [

            "in_progress",
            "contacted",
            "completed",

        ]

    else:

        messages.error(
            request,
            "Invalid request type."
        )

        return redirect(
            "advertisement_notifications"
        )

    # -----------------------------
    # Validate Status
    # -----------------------------

    if status not in allowed_status:

        messages.error(
            request,
            "Invalid status selected."
        )

        return redirect(
            "advertisement_notifications"
        )

    notification.status = status

    notification.is_read = True

    notification.save(
        update_fields=[
            "status",
            "is_read"
        ]
    )

    messages.success(
        request,
        "Status updated successfully."
    )

    return redirect(
        "advertisement_notifications"
    )


# ============================================================
# VIEW DETAILS
# ============================================================

# @login_required
def notification_detail(request, request_type, id):

    if request_type == "advertisement":

        notification = get_object_or_404(

            AdvertisementRequestNotification,

            id=id

        )

    elif request_type == "reel":

        notification = get_object_or_404(

            ReelPurchaseNotification,

            id=id

        )

    else:

        messages.error(
            request,
            "Invalid request."
        )

        return redirect(
            "advertisement_notifications"
        )

    if not notification.is_read:

        notification.is_read = True

        notification.save(
            update_fields=["is_read"]
        )

    return render(

        request,

        "ads_reels_package/notification_detail.html",

        {

            "notification": notification,

            "request_type": request_type,

        }

    )


def subscription_dashboard(request):

    payments = (
        Payment.objects.select_related(
            "user_plan",
            "premium_plan",
            "elite_plan",
            "agent_plan",
        )
        .filter(payment_status="success")
        .order_by("-created_at")
    )

    user_subscriptions = (
        UserPlanSubscription.objects.select_related(
            "user",
            "plan"
        )
        .filter(
            is_active=True
        )
        .distinct()
        .order_by("-purchased_at")
    )
    # for sub in user_subscriptions:
    #     print(
    #         "USER:",
    #         sub.user.name,
    #         "PLAN:",
    #         sub.plan.name
    #     )

    agent_subscriptions = (
        Subscription.objects.select_related(
            "agent",
            "payment"
        )
        .filter(
            is_active=True
        )
        .order_by("-start_date")
    )

    context = {
        "payments": payments,
        "user_subscriptions": user_subscriptions,
        "agent_subscriptions": agent_subscriptions,
    }

    return render(
        request,
        "subscription_management/subscription_dashboard.html",
        context,
    )




def expired_agents_dashboard(request):

    expired_agents = (
        ExpireAgents.objects
        .select_related("agent")
        .order_by("-expired_on")
    )

    search = request.GET.get("search", "").strip()

    if search:
        expired_agents = expired_agents.filter(
            Q(agent__username__icontains=search) |
            Q(agent__email__icontains=search) |
            Q(agent__phone_number__icontains=search) |
            Q(agent__city__icontains=search) |
            Q(agent__agent_code__icontains=search)
        )

    agent_type = request.GET.get("agent_type", "")

    if agent_type:
        expired_agents = expired_agents.filter(
            agent__agent_type=agent_type
        )

    date_filter = request.GET.get("date", "")

    today = timezone.now()

    if date_filter == "today":

        expired_agents = expired_agents.filter(
            expired_on__date=today.date()
        )

    elif date_filter == "month":

        expired_agents = expired_agents.filter(
            expired_on__month=today.month,
            expired_on__year=today.year
        )


    total_expired = ExpireAgents.objects.count()

    expired_today = ExpireAgents.objects.filter(
        expired_on__date=today.date()
    ).count()

    expired_month = ExpireAgents.objects.filter(
        expired_on__month=today.month,
        expired_on__year=today.year
    ).count()

    premium_count = ExpireAgents.objects.filter(
        agent__agent_type="premium"
    ).count()

    elite_count = ExpireAgents.objects.filter(
        agent__agent_type="elite"
    ).count()

    basic_count = ExpireAgents.objects.filter(
        agent__agent_type="basic"
    ).count()

    paginator = Paginator(expired_agents, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {

        "page_obj": page_obj,

        "expired_agents": page_obj,

        "search": search,

        "agent_type": agent_type,

        "date_filter": date_filter,

        "total_expired": total_expired,

        "expired_today": expired_today,

        "expired_month": expired_month,

        "premium_count": premium_count,

        "elite_count": elite_count,

        "basic_count": basic_count,

    }

    return render(
        request,
        "agents/expired_agents.html",
        context
    )