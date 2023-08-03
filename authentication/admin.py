from django.contrib import admin
from .models import Custom_User, Blog, Contact
# Register your models here.
admin.site.register(Custom_User)
admin.site.register(Blog)
admin.site.register(Contact)