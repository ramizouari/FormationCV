from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pickle
from . import detector
import cv2

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        file = request.FILES["image"]
        if file:
                img=cv2.imread(file.temporary_file_path())
                return HttpResponse("Faces:{} \t Masks:{}".format(*detector.detect(img)))
        else:
            return HttpResponse("Nope")