# myapp/views.py

from django.shortcuts import render
from django.http import JsonResponse
import joblib
import os
import json
from django.views.decorators.csrf import csrf_exempt

# Load the model when the server starts
model_path = os.path.join(os.path.dirname(__file__), 'tv_model.pkl')
model = joblib.load(model_path)

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            data = body_data.get('input_data')
            if data is None:
                return JsonResponse({'error': 'No input data provided'})
            inputs = [float(i) for i in data.split(',')]
            predictions = model.predict([inputs])
            return JsonResponse({'predictions': predictions.tolist()})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})
