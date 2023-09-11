from django.contrib import admin

# Register your models here.


from .models import SalesforceToken

admin.site.register(SalesforceToken)
