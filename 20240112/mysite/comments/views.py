from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import CommentForm
from .models import Comment


def comment(request):
    comments = Comment.objects.order_by("datetime")
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/comment/")
    else:
        form = CommentForm()

    context = {
        'form': form,
        "comments": comments,
    }
    return render(request, "comments/comment.html", context)