import base64
import json
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .match import find_best_match
from django.shortcuts import render
from django.http import HttpResponse  
from .models import StoredImage 
from .match import find_best_match

def match_object(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image')

            if not image_data or ";base64," not in image_data:
                return JsonResponse({'success': False, 'error': 'Invalid image format'})

            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_name = f'captured_object.{ext}'

            image_path = default_storage.save(image_name, ContentFile(base64.b64decode(imgstr)))

            match = find_best_match(default_storage.path(image_path))

            if match:
                return JsonResponse({'success': True, 'image_url': match.image.url})
            else:
                return JsonResponse({'success': False, 'error': '❌ No similar image found in database.'})


        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

 

def upload_image(request):  
    if request.method == "POST":  
        image = request.FILES.get("image")  
        tags = request.POST.get("tags", "")  


        if image:  
            stored_image = StoredImage(image=image, tags=tags)  
            stored_image.save()  
            return HttpResponse("✅ Image uploaded successfully!")  

    return render(request, "upload.html")  

def main(req):
    return render(req,"upload-check.html")
 


