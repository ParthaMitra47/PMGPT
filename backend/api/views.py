from django.shortcuts import render

# Create your views here.
# api/views.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Load environment variables from .env file
load_dotenv()

class ChatView(APIView):
    """
    An API View to interact with the Gemini API.
    """
    def post(self, request, *args, **kwargs):
        # 1. Get the prompt from the frontend request
        prompt = request.data.get('prompt')
        model_name = request.data.get('model', 'gemini-2.5-flash')
        if not prompt:
            return Response({"error": "Prompt is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 2. Configure the Gemini API key
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                return Response({"error": "GEMINI_API_KEY not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            genai.configure(api_key=api_key)

            # 3. Initialize the model and generate content
            # model = genai.GenerativeModel('gemini-pro')
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            return Response({"response": response.text})


        except Exception as e:
            # Handle potential errors from the API call
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
