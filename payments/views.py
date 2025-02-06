from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import requests

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure only logged-in users can call the API
def initialize_payment(request):
    """
    Accepts email, amount, fullname, phone, and plan details from the frontend, initializes Paystack payment, 
    and returns the payment link.
    """
    data = request.data
    fullname = data.get('fullname')
    email = data.get('email')
    phone = data.get('phone')
    plan = data.get('plan')
    amount = data.get('amount')  # Amount should be in Naira

    # Validate required fields
    if not email or not amount:
        return Response({'error': 'Email and amount are required.'}, status=400)

    # Optionally validate other fields
    if not fullname or not phone:
        return Response({'error': 'Fullname and phone are required.'}, status=400)

    try:
        # Paystack URL for initializing payment
        paystack_url = settings.PAYSTACK_INITIALIZE_PAYMENT_URL
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        
        # Create payload with all the necessary data
        payload = {
            "email": email,
            "amount": int(amount) * 100,  # Convert to kobo
            "metadata": {
                "fullname": fullname,
                "phone": phone,
                "plan": plan  # Including the plan in metadata if needed
            }
        }

        # Send the request to Paystack's API to initialize the payment
        response = requests.post(paystack_url, headers=headers, json=payload)
        response_data = response.json()

        # Log the response for debugging (Optional: useful for troubleshooting)
        print(response_data)

        # Check if Paystack returned a successful status
        if response_data.get("status"):
            return Response({"payment_url": response_data["data"]["authorization_url"]}, status=200)
        else:
            return Response({
                "error": "Failed to initialize payment with Paystack.",
                "details": response_data
            }, status=500)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)