from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Child, Therapist, Session, TherapyProgress

# Register the custom User model
admin.site.register(User, UserAdmin)

# Register other models
admin.site.register(Child)
admin.site.register(Therapist)
admin.site.register(Session)
admin.site.register(TherapyProgress)
