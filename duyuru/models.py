from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.contrib.auth.models import User
from django.forms import ModelForm


class Category(MPTTModel):
    STATUS = (
        ('True','Evet'),
        ('False','Hayır'),
    )
    title = models.CharField(max_length=200)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=500)
    image = models.ImageField(blank=True,upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    parent = TreeForeignKey('self',blank=True ,null=True ,related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']



    def __str__(self):                         #__str  method elborated later in
        full_path = [self.title]                #post. use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' /'.join(full_path[::-1])


    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Duyuru(models.Model):
    STATUS = (
        ('True','Evet'),
        ('False','Hayır'),

    )
    TYPE = (
        ('haber','haber'),
        ('duyuru','duyuru'),
        ('etkinlik', 'etkinlik'),
        ('inogrenci','inogrenci'),
        ('menu', 'menu'),

    )
    category = models.ForeignKey(Category,on_delete=models.CASCADE) #Relation with Category Table
    title = models.CharField(max_length=200)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=500)
    image = models.ImageField(blank=True, upload_to='images/')
    detail = RichTextUploadingField()

    slug = models.SlugField(blank=True, max_length=200)
    status = models.CharField(max_length=10, choices=STATUS)
    type = models.CharField(max_length=10, choices=TYPE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Images(models.Model):
    duyuru=models.ForeignKey(Duyuru,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class Comment(models.Model):
    STATUS = (
        ('New','Yeni'),
        ('True','Evet'),
        ('False','Hayır'),
    )

    duyuru = models.ForeignKey(Duyuru,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50,blank=True)
    comment = models.TextField(max_length=200, blank=True)
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(max_length=20,blank=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject','comment']