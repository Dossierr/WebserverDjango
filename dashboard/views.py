
# Create your views here.
from django.shortcuts import render
from core.settings import redis_client
import requests
import json
from django.shortcuts import render
from cases.models import Case, File
import json
from chat.views import ChatViewSet
from rest_framework.authtoken.models import Token
from cases.models import File

def dashboard_view(request):
    user = request.user
    user_token = Token.objects.get(user=user)

    # Fetch all cases for the logged-in user
    cases = Case.objects.filter(user=user)
    # Fetch all files related to the cases for the logged-in user
    files = File.objects.filter(case__user=user)
    
    active_case = cases.get(is_active=True)
    active_case_id = active_case.id
    
    #If the user posts a query we will handle the post request. 
    if request.method == 'POST':
        query = request.POST.get('default-query', '')
        url = "http://localhost:8000/chat/chat/question/"

        payload = json.dumps({
        "dossier_id": str(active_case_id),
        "query": str(query)
        })
        headers = {
        'accept': 'application/json',
        'Authorization': 'token '+str(user_token.key),
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response_data = response.json()
        result = response_data.get("result", {})
        chat_list = result.get("chat", [])
        print(chat_list)
        sources_list = result.get("sources", [])
        source_list_url = 
        

        
        print(chat_list)
        print(sources_list)  
        context = {
            'title': 'Dashboard',
            'cases': cases,
            'files': files,
            'active_case_id': active_case_id,
            'chat_history': chat_list,
            'source_List': sources_list
        }
        return render(request, 'dashboard.html', context)      
    
    #If not a post request it's a Get request and thus we want to render the chat content. 
    else:
        #We fetch the chat history from Redis
        redis_key = f'{active_case_id}-history'
        list_length = redis_client.llen(redis_key)

        # Retrieve the last 20 items from the list
        start_index = max(0, list_length - 20)  # Ensure start_index is not negative
        end_index = list_length - 1
        last_20_items = redis_client.lrange(redis_key, start_index, end_index)

        # Transform the structure of each item
        transformed_items = []
        for item in last_20_items:
            item_data = json.loads(item.decode('utf-8'))
            transformed_item = {
                "content": item_data["data"]["content"],
                "additional_kwargs": item_data["data"]["additional_kwargs"],
                "type": item_data["data"]["type"],
                "example": item_data["data"]["example"]
            }
            transformed_items.append(transformed_item)

        # Reversing the order of the chat, so the newest message is last. 
        reverse_chat_history = transformed_items[::-1]
        context = {
            'title': 'Dashboard',
            'cases': cases,
            'files': files,
            'active_case_id': active_case_id,
            'chat_history': reverse_chat_history
        }
        return render(request, 'dashboard.html', context)

def settings_view(request):
    return render(request, 'settings.html', {'title': 'Settings'})


def profile_view(request):
    return render(request, 'profile.html', {'title': 'Profile'})
