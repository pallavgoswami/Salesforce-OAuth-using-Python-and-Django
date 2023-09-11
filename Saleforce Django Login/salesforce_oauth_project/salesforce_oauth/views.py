from django.shortcuts import render

# Create your views here.

from .models import SalesforceToken
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from django.conf import settings
import requests

class SalesforceOAuth2Adapter(OAuth2Adapter):
    provider_id = 'salesforce'
    authorize_url = 'https://login.salesforce.com/services/oauth2/authorize'
    access_token_url = 'https://login.salesforce.com/services/oauth2/token'
    profile_url = 'https://login.salesforce.com/services/oauth2/userinfo'

def salesforce_oauth_login(request):
    # Redirecting to Salesforce for OAuth authentication
    adapter = SalesforceOAuth2Adapter(request)
    params = {
        'response_type': 'code',
        'client_id': settings.SALESFORCE_CLIENT_ID,
        'redirect_uri': settings.SALESFORCE_REDIRECT_URI,
        'scope': 'id profile email address phone full chatter_api openid custom_permissions content user_registration_api sfap_api',
    }
    full_authorize_url = f"{adapter.authorize_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    # Redirecting the user to the Salesforce authorization page
    return redirect(full_authorize_url)

@login_required
def salesforce_oauth_callback(request):
    # Extracting the authorization code from the callback URL
    authorization_code = request.GET.get('code')
    if not authorization_code:
        return render(request, 'error.html', {'error_message': 'Authorization code missing'})
    # Using the authorization code to obtain an access token from Salesforce
    token_url = "https://login.salesforce.com/services/oauth2/token"
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'client_id': settings.SALESFORCE_CLIENT_ID,
        'client_secret': settings.SALESFORCE_CLIENT_SECRET,
        'redirect_uri': settings.SALESFORCE_REDIRECT_URI,
    }
    response = requests.post(token_url, data=data)
    response_data = response.json()
    access_token = None
    if response.status_code == 200:
        # Storing the access token and other details in app's database
        if 'access_token' in response_data:
            access_token = response_data['access_token']
            refresh_token = response_data.get('refresh_token', '')
            instance_url = response_data['instance_url']
            # Saving these tokens to your app's database
            SalesforceToken.objects.create(
                user=request.user,
                access_token=access_token,
                refresh_token=refresh_token,
                instance_url=instance_url,
            )
            # Redirecting the user to a welcome page
            return render(request, 'salesforce_oauth/welcome.html', {'instance_url': instance_url})
        else:
            return render(request, 'error.html', {'error_message': 'Access token not found in response'})
    else:
        return render(request, 'error.html', {'error_message': 'Failed to obtain access token'})

def login(request):
    return render(request, 'salesforce_oauth/login.html')


