from agents.models import *


def check_agent_property_limit(agent, category_name):
    """
    Validate agent property listing limits based on plan.
    Returns (True, message) or (False, error_message)
    """

    # Check plan active
    if not agent.is_plan_active():
        return False, "Your plan is not active or expired."

    # Get limits from model method
    total_limit, residential_limit, commercial_limit = agent.get_plan_limits()

    # Current usage
    total_used = AgentProperty.objects.filter(agent=agent).count()

    if total_limit and total_used >= total_limit:
        return False, f"You reached total property limit ({total_limit})."

    category_name = category_name.lower()

    # Residential limit
    if category_name == "residential":
        residential_used = AgentProperty.objects.filter(
            agent=agent,
            category__name__iexact="Residential"
        ).count()

        if residential_limit and residential_used >= residential_limit:
            return False, f"Residential limit reached ({residential_limit})."

    # Commercial limit
    if category_name == "commercial":
        commercial_used = AgentProperty.objects.filter(
            agent=agent,
            category__name__iexact="Commercial"
        ).count()

        if commercial_limit and commercial_used >= commercial_limit:
            return False, f"Commercial limit reached ({commercial_limit})."

    return True, "Allowed"




# ================= CREATE NOTIFICATION =================
def create_notification(agent, title, message, type):
    # جلوگیری duplicate notifications
    exists = Notification.objects.filter(
        agent=agent,
        title=title,
        message=message
    ).exists()

    if not exists:
        Notification.objects.create(
            agent=agent,
            title=title,
            message=message,
            type=type
        )


def check_plan_notifications(agent):
    if not agent.plan_expiry_date:
        return

    days_left = (agent.plan_expiry_date - timezone.now()).days

    # 🔔 Expiring soon
    if 0 < days_left <= 3:
        create_notification(
            agent,
            "Plan Expiring Soon",
            f"Your plan will expire in {days_left} day(s).",
            "expiry"
        )

    # ❌ Expired
    if days_left < 0:
        create_notification(
            agent,
            "Plan Expired",
            "Your plan has expired. Please upgrade.",
            "expiry"
        )
# ================= PLAN EXPIRY =================
def check_plan_expiry(agent):
    notifications = []

    if not agent.plan_expiry_date:
        return notifications

    days_left = (agent.plan_expiry_date - timezone.now()).days

    if days_left == 7:
        notifications.append(("expiry", "Plan expiring soon", "Your plan will expire in 7 days"))

    elif days_left == 3:
        notifications.append(("expiry", "Plan expiring soon", "Your plan will expire in 3 days"))

    elif days_left == 1:
        notifications.append(("expiry", "Plan expiring tomorrow", "Renew your plan now"))

    elif days_left < 0:
        notifications.append(("expiry", "Plan expired", "Your plan has expired"))

    return notifications



def check_listing_usage(agent):
    notifications = []

    properties = agent.properties.all()

    total_used = properties.count()

    # 🔥 Use your built-in method (VERY GOOD DESIGN)
    total_limit, residential_limit, commercial_limit = agent.get_plan_limits()

    if total_limit == 0:
        return notifications

    # ================= TOTAL USAGE =================
    usage_percent = (total_used / total_limit) * 100

    if usage_percent >= 90:
        notifications.append(("usage", "Listing limit almost reached", "You have used 90% of your listings"))

    elif usage_percent >= 80:
        notifications.append(("usage", "Listing usage high", "You have used 80% of your listings"))

    # ================= CATEGORY BASED =================
    residential_used = properties.filter(category__name__iexact="residential").count()
    commercial_used = properties.filter(category__name__iexact="commercial").count()

    # Residential check
    if residential_limit and residential_used >= residential_limit:
        notifications.append((
            "usage",
            "Residential limit reached",
            f"You used {residential_used}/{residential_limit} residential listings"
        ))

    # Commercial check
    if commercial_limit and commercial_used >= commercial_limit:
        notifications.append((
            "usage",
            "Commercial limit reached",
            f"You used {commercial_used}/{commercial_limit} commercial listings"
        ))

    # ================= REMAINING WARNING =================
    remaining = total_limit - total_used

    if remaining <= 2 and remaining > 0:
        notifications.append((
            "usage",
            "Listings almost finished",
            f"Only {remaining} listings remaining"
        ))

    return notifications

def generate_agent_notifications(agent):
    expiry_notes = check_plan_expiry(agent)
    usage_notes = check_listing_usage(agent)

    all_notes = expiry_notes + usage_notes

    for n_type, title, message in all_notes:
        create_notification(agent, title, message, n_type)