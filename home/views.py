from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormMessages, ContactFormu
from duyuru.models import Duyuru,Category

def index(request):
    setting = Setting.objects.get(pk=2)
    sliderData = Duyuru.objects.all()[:4]
    category = Category.objects.filter(status=True)

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderData': sliderData}
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