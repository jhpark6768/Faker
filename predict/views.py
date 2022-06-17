from django.shortcuts import render, HttpResponse
from project import settings
import os,time
from predict.model import pred
from predict import detect

# Create your views here.
def index(request):
   
    if request.method == 'GET':
        for f in os.scandir(settings.MEDIA_ROOT):
            os.remove(f.path)
        for g in os.scandir(settings.BASE_DIR/ 'static/detect'):
            os.remove(g.path)
        return render(request, 'predict/index.html')      

    elif request.method == 'POST':
        for f in os.scandir(settings.MEDIA_ROOT):
            os.remove(f.path)
        for g in os.scandir(settings.BASE_DIR/ 'static/detect'):
            os.remove(g.path)
        # request.FILES.getlist("파라미터이름") : 여러개의 파일을 list 저장
        # request.FILES.get("파라미터이름") : 한개의 파일을 가져오기
        

        filename = request.FILES.get("files") # 이게.?? 2진? 음?허?    
        
        try:

            uploadfile = open(settings.MEDIA_ROOT.joinpath(str(filename)), 'wb') ## media 파일 생성
            for chunk in filename.chunks(): ## 이게 머하는 부분이지?  
                uploadfile.write(chunk) ## 실제 파일 작성

            
            try:
                result = detect.run(str(filename))
                clsscnt = result['cnt']
                clsscnt2 = result['cnt2']
                clsslist = result['clss']
                imgpath = result['imgpath']
                imgFileName = result['fileName']
                
                context = {
                    "result" : clsslist[0],
                    "fileName" : imgFileName,
                }

                print('clss count', clsscnt)
                print('clsslist', len(clsslist), '타입은? clsslist', type(clsslist))
                print('imgFileName', imgFileName)

                if clsscnt <= 1 and clsscnt2 <= 1 and len(clsslist) == 1 and clsslist[0]=='safe':
                    return render(request, 'predict/safe.html', context) 
                else :
                    return render(request, 'predict/notsafe.html', context)
            
            except:
                print('clss count', clsscnt)
                print('clsslist', len(clsslist), '타입은? clsslist', type(clsslist))
                print('imgFileName', imgFileName)
                
            
                msg = {
                    "msg" : "파일 손상 또는 촬영이 잘못되었습니다.",
                }

                return render(request, 'predict/index.html', msg)

        except:
            msg = {
                    "msg" : "파일 손상 또는 촬영이 잘못되었습니다.",
                }
            return render(request, 'predict/index.html', msg)


def download(request, filename):
    
    filepath = settings.MEDIA_ROOT.joinpath(filename)

    readfile = open(filepath, 'rb')
   
    response = HttpResponse(readfile.read())

    response['Content-Disposition']='attachment;filename='+os.path.basename(filepath)
    response['Content-type']='image/png'

    return (response)

def downlist(request):
    dirlist = os.listdir(settings.MEDIA_ROOT)
    context = {
        'dirlist' : dirlist,
    }
    return render(request, 'predict/downlist.html', context)