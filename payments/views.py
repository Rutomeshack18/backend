from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import PaymentInitForm
import json
import requests
from django.conf import settings
from payments.models import Payment
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

api_key = settings.PAYSTACK_SECRET_KEY
url = settings.PAYSTACK_INITIALIZE_PAYMENT_URL

@csrf_exempt
def payment_init(request):
    if request.method == 'POST':
        # Get form data if POST request
        form = PaymentInitForm(request.POST)

        # Validate form before saving
        if form.is_valid():
            payment = form.save(commit=False)
            payment.save()

            # Set the payment in the current session
            request.session['payment_id'] = payment.id

            # Prepare Paystack checkout session
            payment_id = request.session.get('payment_id', None)
            payment = get_object_or_404(Payment, id=payment_id)
            amount = payment.get_amount()

            # Paystack session data (no success or cancel URLs here)
            session_data = {
                'email': payment.email,
                'amount': int(amount * 100)
            }

            headers = {"authorization": f"Bearer {api_key}"}
            # API request to Paystack server
            r = requests.post(url, headers=headers, data=session_data)
            response = r.json()

            if response.get("status"):
                try:
                    redirect_url = response["data"]["authorization_url"]
                    return redirect(redirect_url, code=303)  # Redirect directly to Paystack
                except KeyError:
                    messages.error(request, "Failed to fetch Paystack URL.")
            else:
                messages.error(request, "Failed to initialize payment.")
        else:
            messages.error(request, "Form submission failed.")
    else:
        form = PaymentInitForm()

    return render(request, 'payments/create.html', {'form': form})