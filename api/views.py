from django.shortcuts import render

from django.http import HttpResponse,JsonResponse
import requests
import json
# Create your views here.



def index(request):
    return HttpResponse("index")


def categories(request):
    categoryQuery="""{
    allCategories {
        name,
        id,
    }
    }"""
    url = "http://"+request.get_host()+"/graphql/"
    r = requests.post(url, json={'query': categoryQuery})
    json_data = json.loads(r.text)

    #return JsonResponse(json_data["data"])
    try:
        return {
            "categories":json_data["data"]
        }
    except:
        return {}    


def allPostsHomePage(request,categoryID=99999):
    newpostsQuery="""{
    allPosts(orderby:"created",first:10,ordermode:"desc") {
    postId,
    title,
    slug,
    tags,
    category{
        name,
    },
    synopsis,
    createdAgo,
    readTime,
    image,
    views,
    claps,
    absoluteUrl,
    }
    }"""

    popularpostsQuery="""{
    allPosts(orderby:"views",first:10,ordermode:"desc") {
    postId,
    title,
    slug,
    tags,
    category{
        name,
    },
    synopsis,
    createdAgo,
    readTime,
    image,
    views,
    claps,
    absoluteUrl,
    }
    }"""
    if(categoryID != 99999):
        newpostsQuery="""{
        allPosts(orderby:"created",first:10,ordermode:"desc",categoryID:"""+categoryID+""") {
        postId,
        title,
        slug,
        tags,
        category{
            name,
        },
        synopsis,
        createdAgo,
        readTime,
        image,
        views,
        claps,
        absoluteUrl,
        }
        }"""

        popularpostsQuery="""{
        allPosts(orderby:"views",first:10,ordermode:"desc",categoryID:"""+categoryID+""") {
        postId,
        title,
        slug,
        tags,
        category{
            name,
        },
        synopsis,
        createdAgo,
        readTime,
        image,
        views,
        claps,
        absoluteUrl,
        }
        }"""

    url = "http://"+request.get_host()+"/graphql/"
    r = requests.post(url, json={'query': newpostsQuery})
    try:
        newpost_json_data = json.loads(r.text)

        url = "http://"+request.get_host()+"/graphql/"
        r = requests.post(url, json={'query': popularpostsQuery})
        popularpost_json_data = json.loads(r.text)
        if(newpost_json_data["data"] and  popularpost_json_data["data"]):
            homedata={"newposts":newpost_json_data["data"],"popularposts":popularpost_json_data["data"]}
        else:
            homedata={}    
        return homedata
    except:
        return {}

def getPostById(request,postid):
    postById="""{
  postById(postId:"""+str(postid)+"""){
    title,
    postId,
    slug,
    tags,
    image,
    readTime,
    post,
    claps,
    views,
    createdAgo,
    category {
      name
    },
    
  }
}"""
    url = "http://"+request.get_host()+"/graphql/"
    r = requests.post(url, json={'query': postById})
    post_json_data = json.loads(r.text)

    return post_json_data["data"]

    ##return JsonResponse({"data":post_json_data})


def getPostBySlug(request,slug):
    postBySlug="""{
  postById(id:"""+slug+"""){
    title,
    postId,
    slug,
    tags,
    image,
    post,
    readTime,
    claps,
    views,
    createdAgo,
    category {
      name
    },
    
  }
}"""
    url = "http://"+request.get_host()+"/graphql/"
    r = requests.post(url, json={'query': postBySlug})
    post_json_data = json.loads(r.text)

    return post_json_data


def categories1(request):
    url = "http://"+request.get_host()+"/graphql/"
    r = requests.post(url, json={'query': categoryQuery})
    json_data = json.loads(r.text)

    return JsonResponse(json_data["data"])