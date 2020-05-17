from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, NewaccountForm
from home.models import Setting, ContactFormMessages, ContactFormu
from duyuru.models import Duyuru, Category, Images , Comment
import json

def index(request):
    setting = Setting.objects.get(pk=2)
    sliderData = Duyuru.objects.all()[:4]
    category = Category.objects.filter(status=True)
    anahaber= Duyuru.objects.filter(type__contains='haber')[:4]
    anaduyuru = Duyuru.objects.filter(type__contains='duyuru')[:4]
    anaetkinlik = Duyuru.objects.filter(type__contains='etkinlik')[:4]
    anaulusal = Duyuru.objects.filter(type__contains='inogrenci')[:4]

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderData': sliderData,
               'anahaber': anahaber,
               'anaduyuru': anaduyuru,
               'anaetkinlik': anaetkinlik,
               'anaulusal':anaulusal
               }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=2)
    category = Category.objects.filter(status=True)
    context = {'setting': setting,
              'category': category,
              'page' : 'hakkimizda'}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=2)
    context = {'setting': setting}
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):

    if request.method == 'POST' : #form pst edildi ise
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessages() #model ile bağlantı kur
            data.name = form.cleaned_data['name'] #form dan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request,"Mesajınız başarı ile gönderilmiştir.Teşekkür Ederiz")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=2)
    category = Category.objects.filter(status=True)
    form = ContactFormu()
    context = {'setting': setting,
               'form': form,
               'category': category,
               'page': 'iletisim'
               }
    return render(request, 'iletisim.html', context)

def category_duyurus(request, id, slug):
    duyurus = Duyuru.objects.filter(category_id=id)
    category = Category.objects.filter(status=True)
    categorydata=Category.objects.get(pk=id)

    context={'duyurus': duyurus,
             'category': category,
             'categorydata':categorydata

             }
    return render(request,'icerik.html', context)

def duyuru_detail(request,id,slug):
    setting = Setting.objects.get(pk=2)
    category = Category.objects.filter(status=True)
    duyuru = Duyuru.objects.get(pk=id)
    images= Images.objects.filter(duyuru_id=id)[:3]
    comments = Comment.objects.filter(duyuru_id=id,status=True)
    context = {'duyuru': duyuru,
               'category': category,
               'images': images,
               'comments': comments,
               'setting': setting


               }
    return render(request,'icerik_detail.html',context)

def duyuru_search(request):
    if request.method == 'POST': #Eğer form POST edildi ise
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.filter(status=True)
            query = form.cleaned_data['query'] #formdan bilgiyi al
            duyurus = Duyuru.objects.filter(title__icontains=query) #Select * from duyuru where title like %query%
            #return HttpResponse(duyurus)
            context = {'duyurus': duyurus,
                       'category': category,
                       }
            return render(request, 'icerik_search.html',context)

    return HttpResponseRedirect('/')



def duyuru_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        duyuru = Duyuru.objects.filter(title__icontains=q)
        results = []
        for rs in duyuru:
            duyuru_json = {}
            duyuru_json = rs.title
            results.append(duyuru_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)



def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':  # Eğer form POST edildi ise
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # İşlem Başarılı ise
            return HttpResponseRedirect('/')
        else:
            # İşlem Başarısız ise
            messages.warning(request, "Login İşlemi Hatası! Kullanıcı Adı veya parola Hatalı")
            return HttpResponseRedirect('/login')


    category = Category.objects.filter(status=True)
    context = {
               'category': category,
               }
    return render(request, 'login.html', context)

def new_account_view(request):
    if request.method == 'POST':  # Eğer form POST edildi ise
        form = NewaccountForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')


    form = NewaccountForm()
    category = Category.objects.filter(status=True)
    context = {
                'category': category,
                'form': form,
              }
    return render(request, 'New_account.html', context)