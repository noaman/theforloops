from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from api.models import Post
import api
# Create your views here.

def index(request):
    allposts=api.views.allPostsHomePage(request)
    context={"postdata":allposts}
    return render(request, "index.html",context)


def post_detail(request, id,slug):
    post=api.views.getPostById(request,id)
    context={"post":post["postById"][0]}
    return render(request, "post_details.html",context)

def update_claps(request,pid):
    posts = Post.objects.filter(id=pid).first()
    posts.claps+=1
    posts.save()
    
    return JsonResponse({"claps":posts.claps})

def category_list(request,category,category_id):
    allposts=api.views.allPostsHomePage(request,category_id)
    context={"postdata":allposts,"categoryname":category}

    return render(request, "categorylist.html",context)