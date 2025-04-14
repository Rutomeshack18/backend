import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
import logging
logger = logging.getLogger(__name__) 
from openai import AzureOpenAI
import logging
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from openai import AzureOpenAI
from docx import Document
from io import BytesIO


logger = logging.getLogger(__name__)

# Initialize the AzureOpenAI client
client = AzureOpenAI(
    azure_endpoint=settings.AZURE_ENDPOINT,
    api_key=settings.AZURE_API_KEY,
    api_version=settings.API_VERSION
)

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


SUPPORTED_DOCUMENTS = {
    "contract extension": "Contract Extension",
    "affidavit": "Affidavit",
    "power of attorney": "Power of Attorney",
    "tenancy agreement": "Tenancy Agreement",
    "employment contract": "Employment Contract"
}

# Store user sessions in memory (for a production system, use a proper session store)
user_sessions = {}

@csrf_exempt
def legal_doc_generator_view(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        user_message = data.get("message", "").strip().lower()

        if not user_id or not user_message:
            return JsonResponse({"error": "User ID and message are required"}, status=400)

        session = user_sessions.get(user_id, {"step": "greet"})

        # Step 1: Greeting
        if session["step"] == "greet":
            user_sessions[user_id] = {"step": "select_doc"}
            return JsonResponse({
                "reply": (
                    "Hello! I can help you generate the following legal documents in the Kenyan context:\n"
                    "- Contract Extension\n"
                    "- Affidavit\n"
                    "- Power of Attorney\n"
                    "- Tenancy Agreement\n"
                    "- Employment Contract\n"
                    "Please type the name of the document you would like to create."
                )
            })

        # Step 2: Document selection
        elif session["step"] == "select_doc":
            selected_doc = SUPPORTED_DOCUMENTS.get(user_message)
            if not selected_doc:
                return JsonResponse({"error": "Sorry, that document type is not supported."}, status=400)
            user_sessions[user_id] = {
                "step": "collect_info",
                "doc_type": selected_doc,
                "details": {}
            }
            return JsonResponse({
                "reply": f"You selected '{selected_doc}'. Please provide the required details for this document."
            })

        # Step 3: Collecting details and generating the document
        elif session["step"] == "collect_info":
            doc_type = session["doc_type"]
            user_input = user_message

            conversation = [
                {
                    "role": "system",
                    "content": (
                        "You are a legal assistant trained on Kenyan law. Use only Kenyan legal standards and formats. "
                        f"Create a complete {doc_type} based on this information: {user_input}"
                    )
                },
                {"role": "user", "content": user_input}
            ]

            response = client.chat.completions.create(
                model=settings.DEPLOYMENT_NAME,
                messages=conversation,
                max_tokens=1000,
                temperature=0.5,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0
            )

            if not response.choices:
                return JsonResponse({"error": "Failed to generate the document."}, status=500)

            doc_text = response.choices[0].message.content.strip()

            doc = Document()
            for paragraph in doc_text.split("\n"):
                doc.add_paragraph(paragraph)

            file_stream = BytesIO()
            doc.save(file_stream)
            file_stream.seek(0)

            # Clear session
            user_sessions.pop(user_id, None)

            # Return document as downloadable file
            response = HttpResponse(file_stream, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{doc_type.replace(" ", "_")}.docx"'
            return response

    except Exception as e:
        logger.error(f"Error: {e}")
        return JsonResponse({"error": f"Internal error: {str(e)}"}, status=500)