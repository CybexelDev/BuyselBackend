from django.contrib import admin
from . models import *
# Register your models here.


admin.site.register(UserProfile)

admin.site.register(Inbox)

# admin.site.register(AgentProperty)
admin.site.register(PendingAgentRegistration)

admin.site.register(AgentPropertyFieldValue)
admin.site.register(AgentPropertyImage)
admin.site.register(AgentPropertyLandmark)
admin.site.register(AgentPropertySellingPoint)