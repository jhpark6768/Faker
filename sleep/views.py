from django.shortcuts import render, HttpResponse
from project import settings
import os
from sleep import eyeDect

def index(request):
    if request.method == 'GET':
        for f in os.scandir(settings.MEDIA_ROOT):
            os.remove(f.path)
        for g in os.scandir(settings.BASE_DIR/ 'static/detect'):
            os.remove(g.path)
        return render(request, 'sleep/sindex.html')
    elif request.method == 'POST':
        # request.FILES.getlist("파라미터이름") : 여러개의 파일을 list 저장
        # request.FILES.get("파라미터이름") : 한개의 파일을 가져오기
       
        filename = request.FILES.get("files")
       
        try:

            uploadfile = open(settings.MEDIA_ROOT.joinpath(str(filename)), 'wb') ## media 파일 생성
        
            for chunk in filename.chunks():  

                uploadfile.write(chunk) 

            result = eyeDect.drowsy(str(filename))
            
            if result == True:
                return render(request, 'sleep/drowsy.html')
            else:
                return render(request, 'sleep/nunddeo.html')
        except:

            msg = {
                    "msg" : "파일 손상 또는 촬영이 잘못되었습니다.",
                }
            return render(request, 'sleep/sindex.html', msg)

