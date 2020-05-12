from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from duyuru.models import CommentForm , Comment


def index(request):
    return HttpResponse("Duyuru Sayfası")


@login_required(login_url='/login') # Check login
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST': #form post edildi ise
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user # Access User Session information
            data = Comment() #Model ile bağlantı kur
            data.user_id = current_user.id
            data.duyuru_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR') # Client Computer ip adress
            data.save() # veritabanına kaydet
            messages.success(request,"Yorumunuz başarı ile gönderilmiştir.Teşekkür ederiz")
            return HttpResponseRedirect(url)


        messages.warning(request, "Yorumunuz kaydedilmedi. Lütfen Kontrol Ediniz")
        return HttpResponseRedirect(url)
