from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SalesforceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    instance_url = models.URLField()
    

    def __str__(self):
        return self.user.username  # Display the username as the string representation


# This code defines a Django model called "SalesforceToken". It has the following fields: 
# - "user": a foreign key to the User model provided by Django's authentication system. It represents the user associated with this Salesforce token. 
# - "access_token": a character field with a maximum length of 255 characters. It stores the access token for the Salesforce API. 
# - "refresh_token": a character field with a maximum length of 255 characters. It stores the refresh token for the Salesforce API. 
# - "instance_url": a URL field. It stores the Salesforce instance URL. 
# The class also defines a "__str__" method that returns the username of the associated user as the string representation of the object. 
# Overall, this model is used to store Salesforce tokens for users in a Django application.