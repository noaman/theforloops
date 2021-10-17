from django.shortcuts import render

from django.http import HttpResponse,JsonResponse
import requests
import json
# Create your views here.

def getHttp_https(request):
    if(".com" in request.get_host()):
        return "https://"
    else:
        return "http://"

def index(request):
    url = getHttp_https(request)+request.get_host()+"/graphql/"

    categoryQuery="""{
    allCategories {
        name,
        id,
    }
    }"""

    r = requests.post(url, json={'query': categoryQuery})
    homedata=allPostsHomePage(request)

    return JsonResponse({"url":url,"resp":r.text,"home":homedata})
    #return JsonResponse(categories(request))


def categories(request):
    categoryQuery="""{
    allCategories {
        name,
        id,
    }
    }"""

    url = getHttp_https(request)+request.get_host()+"/graphql/"
    r = requests.post(url, json={'query': categoryQuery})
    json_data = json.loads(r.text)

    #return JsonResponse(json_data["data"])

    try:
        return {
            "categories":json_data["data"]
        }
    except:
        return {}    





def allPostsHomePage(request,categoryID=99999,tag="na"):
    newpostsQuery="""{
    allPosts(orderby:"created",first:10,ordermode:"desc") {
    postId,
    title,
    slug,
    tags,
    category{
        name,
        id,
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
        id,
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
            id,
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
            id,
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
    elif(tag != "na"):
        newpostsQuery="""{
        allPosts(orderby:"created",first:10,ordermode:"desc",tag:\""""+tag+"""\") {
        postId,
        title,
        slug,
        tags,
        category{
            name,
            id,
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
        allPosts(orderby:"views",first:10,ordermode:"desc",tag:\""""+tag+"""\") {
        postId,
        title,
        slug,
        tags,
        category{
            name,
            id,
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


    # return {"query":popularpostsQuery.replace("\n","")}
    url = getHttp_https(request)+request.get_host()+"/graphql/"
    r = requests.post(url, json={'query': newpostsQuery})

    # return {"query":r.text}
    try:
        newpost_json_data = json.loads(r.text)

        url = getHttp_https(request)+request.get_host()+"/graphql/"
        r = requests.post(url, json={'query': popularpostsQuery})
        popularpost_json_data = json.loads(r.text)
        if(newpost_json_data["data"] and  popularpost_json_data["data"]):
            homedata={"newposts":newpost_json_data["data"],"popularposts":popularpost_json_data["data"]}
        else:
            homedata={}    
        return homedata
    except Exception as e:
        return {"errr":str(e)}

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
      name,
      id,
    },
    
  }
}"""
    url = getHttp_https(request)+request.get_host()+"/graphql/"
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
      name,
      id,
    },
    
  }
}"""
    url = getHttp_https(request)+request.get_host()+"/graphql/"
    r = requests.post(url, json={'query': postBySlug})
    post_json_data = json.loads(r.text)

    return post_json_data

