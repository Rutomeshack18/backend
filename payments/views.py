from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import requests

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure only logged-in users can call the API
def initialize_payment(request):
    """
    Accepts email and amount from the frontend, initializes Paystack payment, and returns the payment link.
    """
    data = request.data
    email = data.get('email')
    amount = data.get('amount')  # Amount should be in Naira

    if not email or not amount:
        return Response({'error': 'Email and amount are required.'}, status=400)

    try:
        paystack_url = settings.PAYSTACK_INITIALIZE_PAYMENT_URL
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        payload = {
            "email": email,
            "amount": int(amount) * 100  # Convert to kobo
        }

        response = requests.post(paystack_url, headers=headers, json=payload)
        response_data = response.json()

        if response_data.get("status"):
            return Response({"payment_url": response_data["data"]["authorization_url"]}, status=200)
        else:
            return Response({"error": "Failed to initialize payment with Paystack."}, status=500)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)