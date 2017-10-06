from django.contrib import admin
from .models import Project, Review, UserProfile


admin.site.register(Project)
admin.site.register(Review)
admin.site.register(UserProfile)