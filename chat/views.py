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
    last_20_items_json = [json.loads(item.decode('utf-8')) for item in last_20_items]

    # Return a JSON response with the last 20 items as a JSON object
    return JsonResponse({'chat-history': last_20_items_json})

@csrf_exempt
@require_POST
def query_endpoint(request):
    # Assuming the data is coming as JSON in the POST request
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