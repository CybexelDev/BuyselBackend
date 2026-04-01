# agents/utils.py

from .models import AgentProperty



def check_agent_property_limit(agent, category_name):

    # Plan expired
    if agent.plan and not agent.is_plan_active():
        return False, "Your plan expired. Renew to add properties."

    # Free agent
    if agent.agent_type == "basic":
        if AgentProperty.objects.filter(agent=agent).count() >= 5:
            return False, "Basic plan allows only 5 properties."

    # Premium / Elite based on plan limit
    if agent.plan:
        limit = agent.plan.property_limit
        if AgentProperty.objects.filter(agent=agent).count() >= limit:
            return False, f"Your plan allows only {limit} properties."

    return True, "Allowed"