from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.db.models.signals import pre_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
from django.urls import reverse
import re
from django.utils.html import mark_safe
from tinymce.models import HTMLField
from django.utils.text import slugify
from django.contrib.humanize.templatetags import humanize
from django.core.paginator import Paginator


WPM = 200
WORD_LENGTH = 5


def _count_words_in_text(text: str) -> int:
    return len(text) // WORD_LENGTH


def _filter_visible_text(text: str) -> str:
    clear_html_tags = re.compile("<.*?>")
    text = re.sub(clear_html_tags, "", text)
    return "".join(text.split())

def _filter_visible_text2(text: str) -> str:
    clear_html_tags = re.compile("<.*?>")
    text = re.sub(clear_html_tags, "", text)
    return text



def estimate_reading_time(text: str) -> int:
    filtered_text = _filter_visible_text(text)
    total_words = _count_words_in_text(filtered_text)
    return total_words // WPM


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    name = models.CharField(max_length=255, verbose_name="name")
    # slug = models.SlugField(max_length=255, null=True)
    slug = models.SlugField(unique=True, max_length=255, default='')

    class Meta:
        verbose_name = "Blog - Category"
        verbose_name_plural = "Blog - Categories"
        ordering = ['name']
    def __str__(self):
        return '%s' % (self.name)   
    def __unicode__(self):
        return '%s' % (self.name)   
   

  

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')


# post model
class Post(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('unpublished', 'UnPublished'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=255, default='')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    #body = RichTextUploadingField() 
    post=HTMLField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    claps = models.FloatField(default=1)
    views = models.FloatField(default=1)
    tags = TaggableManager() 
    status = models.CharField(max_length=15,choices=STATUS_CHOICES,default='published')
    read_time = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    image = models.ImageField(upload_to='featured_image/%Y/%m/%d/',null=True) 


        
    class Meta:
        verbose_name = "Blog - Post"
        verbose_name_plural = "Blog - Posts"
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title
    

    @property
    def get_id(self):
        return self.pk

    @property
    def synopsis(self):
        return _filter_visible_text2(self.post)[:250]
    @property
    def get_tags(self):
        return self.tags.all()
    @property
    def created_ago(self):
        return humanize.naturaltime(self.created)  

    objects = models.Manager() # The default manager.
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.slug])

    def incrementViewCount(self):
        self.views += 1
        self.save()

    def __unicode__(self):
        return '%s %s' % (self.title, self.body)   
    

@receiver(pre_save, sender=Post)
def post_pre_save(sender, instance, *args, **kwargs):
    
    instance.read_time=estimate_reading_time(instance.post)



# Create your models here.
