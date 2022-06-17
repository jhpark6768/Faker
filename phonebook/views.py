from django.shortcuts import render, redirect
import phonebook
from phonebook.models import PhoneBook
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
def index(request, page):
    alluser = PhoneBook.objects.all().order_by('-id')
    
    # print('길이 : ', len(alluser))
    # print('alluser : ', alluser)

    # Paginator(전체데이터, 분할할 갯수)
    paging = Paginator(alluser, 5)

    # page 문자열이기 때문에 int 형으로 변경
    # / 연산 결과는 파이썬에서 실수이기 때문에 int 형
    nowpage = int(int(page)/10)
    if(int(page)%10 == 0):
        nowpage = nowpage -1
    
    # 페이지의 범위는 list 형으로 만들어야 한다.
    pagerange = []

    for x in range(int(nowpage*10+1), int((nowpage+1) * 10) +1):
        pagerange.append(int(x))

    try:
        context = {
            'alluser' : paging.page(page),
            'pagerange' : pagerange,
        }
    except EmptyPage:
        context = {
            'alluser' : paging.page(paging.num_pages),
        }

    # print(PhoneBook.objects.all())
  
    return render(request, 'phonebook/pindex.html', context)

def add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        telnum = request.POST.get('telnum')
        email = request.POST.get('email')
        address = request.POST.get('address')
        birth = request.POST.get('birth')

        # 저장에 필요한 객체 생성
        phonebook_save = PhoneBook()
        phonebook_save.name = name
        phonebook_save.telnum = telnum
        phonebook_save.email = email
        phonebook_save.address = address
        phonebook_save.birth = birth

        # 객체를 DB에 저장하는 방법
        phonebook_save.save()
        # return render(request, 'phonebook/index.html')
        # return redirect("/phonebook/index")
        return redirect("/phonebook/index/1")

    elif request.method == 'GET':
        return render(request, 'phonebook/add.html')
        
def delete(request, userid):
    PhoneBook.objects.get(id=userid).delete()
    context = {
        'userid' : userid,
    }
    return render(request, 'phonebook/delete.html', context)

def detail(request, userid):
    user = PhoneBook.objects.values('id','name','telnum','address','email','birth').get(id=userid)
    context = {
        'user' : user,
    }
    return render(request, 'phonebook/detail.html', context)

def update(request, userid):
    if request.method == 'GET':
        user = PhoneBook.objects.values('id','name','telnum','address','email','birth').get(id=userid)
        context = {
            'user' : user,
        }
        return render(request, 'phonebook/update.html', context)
    elif request.method == 'POST':
        name = request.POST.get('name')
        telnum = request.POST.get('telnum')
        email = request.POST.get('email')
        address = request.POST.get('address')
        birth = request.POST.get('birth')

        # 첫번째 방법
        # 새로운 객체를 생성하고 아이디값을 중복해서 처리
        # 아이디값을 이용해 기존에 있던 데이터를 없애도 새로 저장하는 방법 
        # phonebook_save = PhoneBook()
        # phonebook_save.id = userid
        # phonebook_save.name = name
        # phonebook_save.telnum = telnum
        # phonebook_save.email = email
        # phonebook_save.address = address
        # phonebook_save.birth = birth

        # phonebook_save.save()
        # return redirect("PB:D", userid)

        # 두번째 방법
        # 기존 데이터를 불러와서 수정
        phonebook_save = PhoneBook.objects.get(id=userid)
        phonebook_save.name = name
        phonebook_save.telnum = telnum
        phonebook_save.email = email
        phonebook_save.address = address
        phonebook_save.birth = birth

        phonebook_save.save()
        return redirect("PB:D", userid)