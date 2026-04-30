# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import AgentPropertyEnquiry, Notification


# @receiver(post_save, sender=AgentPropertyEnquiry)
# def create_enquiry_notification(sender, instance, created, **kwargs):
#     if created:
#         agent = instance.property.agent   #instance.agent_property.agent

#         Notification.objects.create(
#             agent=agent,
#             title="New Enquiry",
#             message=f"You received a new enquiry for {instance.agent_property.label}",
#             type="property"
#         )


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AgentPropertyEnquiry, Notification


@receiver(post_save, sender=AgentPropertyEnquiry)
def create_enquiry_notification(sender, instance, created, **kwargs):

    if not created:
        return

    # ✅ FIX: correct field name is "property"
    agent = instance.property.agent  # AgentProperty -> agent

    Notification.objects.create(
        agent=agent,
        title="New Enquiry",
        message=f"You received a new enquiry for {instance.property.label}",
        type="property"
    )