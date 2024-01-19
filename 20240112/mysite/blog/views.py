# from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from .models import Post


def index(request):
    latest_post_list = Post.objects.order_by("-datetime")
    # output = ", ".join([q.title for q in latest_post_list])
    # return HttpResponse(output)

    template = loader.get_template("blog/index.html")
    context = {
        "latest_post_list": latest_post_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    output = post.text
    return HttpResponse(output)