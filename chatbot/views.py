import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
import logging
logger = logging.getLogger(__name__) 
from openai import AzureOpenAI

# Initialize the AzureOpenAI client using the settings from your configuration
client = AzureOpenAI(
  azure_endpoint = settings.AZURE_ENDPOINT,
  api_key=settings.AZURE_API_KEY,  
  api_version=settings.API_VERSION
)

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        try:
            # Parse the incoming request body
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # If the user message is empty, return an error
            if not user_message:
                return JsonResponse({"error": "Message is required"}, status=400)

            # Construct the chat prompt with instructions specific to Kenyan law
            conversation = [
                {
                    "role": "system",
                    "content": (
                        "You are an expert on Kenyan law. Only use the Constitution of Kenya, "
                        "legal acts, and case precedents from Kenyan courts in your answers. "
                        "If a query is outside the scope of Kenyan law, respond with "
                        "'I can only provide information on Kenyan law and legal precedents.'"
                    )
                },
                {"role": "user", "content": user_message}
            ]

            # Use the Azure OpenAI client to generate the response
            response = client.chat.completions.create(
                model=settings.DEPLOYMENT_NAME,  # Use the model (deployment name) from settings
                messages=conversation,
                max_tokens=500,
                temperature=0.5,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Check if the response contains valid data
            if response.choices:
                # Extract the content of the assistant's reply
                reply = response.choices[0].message.content
                return JsonResponse({"reply": reply})
            else:
                # If no choices are returned, handle that scenario
                return JsonResponse({"error": "No response from AI model."}, status=500)

        except Exception as e:
            # Log the error and return a generic internal server error message
            logger.error(f"Error occurred: {str(e)}")
            return JsonResponse({"error": f"Internal error: {str(e)}"}, status=500)

    # Return an error for non-POST requests
    return JsonResponse({"error": "Invalid request method"}, status=400)