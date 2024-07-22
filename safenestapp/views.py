from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import face_recognition
import os
import imghdr

known_folder = "knownfolder"

def is_image(filename):
    if not os.path.isfile(filename):
        return False
    _, ext = os.path.splitext(filename)
    if ext.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
        return True
    return False

def upload_image(request):
    matched_images = []
    if request.method == 'POST' and request.FILES['image']:
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(filename)
        
        # Perform face recognition
        if is_image(fs.path(filename)):
            image = face_recognition.load_image_file(fs.path(filename))
            unknown_encoding = face_recognition.face_encodings(image)[0]
            
            # Check all images in the dummy folder
            for img in os.listdir(known_folder):
                img_path = os.path.join(known_folder, img)
                if is_image(img_path):
                    known_image = face_recognition.load_image_file(img_path)
                    known_face_encodings = face_recognition.face_encodings(known_image)
                    if known_face_encodings:
                        known_face_encoding = known_face_encodings[0]
                        results = face_recognition.compare_faces([known_face_encoding], unknown_encoding)
                        if results[0]:
                            matched_images.append(img_path)
        
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'matched_images': matched_images,
        })
    return render(request, 'upload.html')

