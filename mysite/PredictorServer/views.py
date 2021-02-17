from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pickle
from . import detector
import cv2

@csrf_exempt
def predict_min(request):
    if request.method == 'POST':
        file = request.FILES["image"]
        print(file)
        if file:
                img=cv2.imread(file.temporary_file_path())
                return HttpResponse("{}:{}".format(*detector.detect(img)))
        else:
            return HttpResponse("Nope")

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        file = request.FILES["image"]
        if file:
                img=cv2.imread(file.temporary_file_path())
                return HttpResponse("Faces:{} \t Masks:{}".format(*detector.detect(img)))
        else:
            return HttpResponse("Nope")


@csrf_exempt
def predict_detailed(request):
    if request.method == 'POST':
        file = request.FILES["image"]
        if file:
                img=cv2.imread(file.temporary_file_path())
                detections=detector.detect(img,retCrops=True)
                S=""
                for crop in detections:
                    S=S+"{}:{}:{}:{}:{}\n".format(*crop)
                return HttpResponse(S[:-1])
        else:
            return HttpResponse("Nope")