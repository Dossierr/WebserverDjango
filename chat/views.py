import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from core.settings import redis_client
import requests
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from billing.models import UserPayment

decorators = [never_cache]

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@method_decorator(decorators, name='dispatch')
class ChatViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='history/(?P<case_id>[^/.]+)')
    def chat_history(self, request, case_id):
        """Retrieves the chat history on a specific case

        Args:
            request (_type_): _description_
            case_id (uuid): Parse in the Case ID to retrieve the chat history of a case

        Returns:
            list: list of chat messages
        """
        redis_key = f'{case_id}-history'
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

        # Return a JSON response with the transformed items
        return JsonResponse({'chat': transformed_items})

    @action(detail=False, methods=['post'])
    def question(self, request):
        user_billing_profile = get_object_or_404(UserPayment, app_user=request.user )
        usage_billing_token = user_billing_profile.stripe_usage_billing_id
        # Creating a request for our GPTengine service
        url = "http://127.0.0.1:5000/q/query"
        headers = {
            'Content-Type': 'application/json',

        }
        request_body_json = json.loads(request.body)
        request_body_json['billing-token'] = usage_billing_token
        modified_request_body = json.dumps(request_body_json)



        response = requests.post(url, headers=headers, data=modified_request_body)

        # Check the response from the external endpoint
        if response.status_code == 200:
            result = response.json()
            return JsonResponse({'result': result})
        else:
            error_message = f"Error from external endpoint: {response.status_code}"
            return JsonResponse({'error': error_message}, status=response.status_code)