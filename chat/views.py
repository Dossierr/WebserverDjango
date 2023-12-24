import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from core.settings import redis_client
import requests
from django.views.decorators.csrf import csrf_exempt


@require_GET
def chat_history_view(request, case_id):
    redis_key = f'{case_id}-history'
    list_length = redis_client.llen(redis_key)

    # Retrieve the last 20 items from the list
    start_index = max(0, list_length - 20)  # Ensure start_index is not negative
    end_index = list_length - 1
    last_20_items = redis_client.lrange(redis_key, start_index, end_index)
    print(last_20_items)
    
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

    # Return a JSON response with the transformed items
    return JsonResponse({'chat': transformed_items})

@csrf_exempt
@require_POST
def query_endpoint(request):
    # Creating a request for our GPTengine service
    url = "http://127.0.0.1:5000/q/query"
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=request.body)
    # Check the response from the external endpoint
    if response.status_code == 200:
        result = response.json()
        return JsonResponse({'result': result})
    else:
        error_message = f"Error from external endpoint: {response.status_code}"
        return JsonResponse({'error': error_message}, status=response.status_code)