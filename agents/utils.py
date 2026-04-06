from agents.models import AgentProperty


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
            category_name_iexact="Residential"
        ).count()

        if residential_limit and residential_used >= residential_limit:
            return False, f"Residential limit reached ({residential_limit})."

    # Commercial limit
    if category_name == "commercial":
        commercial_used = AgentProperty.objects.filter(
            agent=agent,
            category_name_iexact="Commercial"
        ).count()

        if commercial_limit and commercial_used >= commercial_limit:
            return False, f"Commercial limit reached ({commercial_limit})."

    return True, "Allowed"