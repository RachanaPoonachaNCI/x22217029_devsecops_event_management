from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models
from authentication import models as userModel
from datetime import datetime


# Create your views here.
@login_required(login_url="/auth/")
def posts(request):
    try:
        user = userModel.user.objects.get(email=request.user)
        colors = ["blue", "red", "orange", "green", "yellow", "brown", "grey"]
        postsObjects = models.post.objects.all().order_by("-updated")
        post = list()

        for i in range(len(postsObjects)):
            url = None
            try:
                url = postsObjects[i].image.url
            except Exception as e:
                print("No image for", postsObjects[i].title)
            content = ""
            try:
                content = postsObjects[i].content[:500]
                content += "..."
            except Exception as e:
                print("No content")
            post.append(
                {
                    "id": postsObjects[i].id,
                    "color": colors[i % len(colors)],
                    "image": url,
                    "title": postsObjects[i].title,
                    "subheading": postsObjects[i].subheading,
                    "content": content,
                    "tag": postsObjects[i].tag,
                }
            )
        return render(
            request, "post_list.html", context={"user_name": user.name, "posts": post}
        )
    except Exception as e:
        print("error:", e)
        return redirect("/auth/")


@login_required(login_url="/auth/")
def myPosts(request):
    user = userModel.user.objects.get(email=request.user)
    colors = ["blue", "red", "orange", "green", "yellow", "brown", "grey"]
    postsObjects = models.post.objects.filter(user__email=request.user).order_by(
        "-updated"
    )
    post = list()
    for i in range(len(postsObjects)):
        url = None
        try:
            url = postsObjects[i].image.url
        except Exception as e:
            print("No image for", postsObjects[i].title)
        post.append(
            {
                "id": postsObjects[i].id,
                "color": colors[i % len(colors)],
                "image": url,
                "title": postsObjects[i].title,
                "subheading": postsObjects[i].subheading,
                "tag": postsObjects[i].tag,
            }
        )
    return render(
        request, "myposts.html", context={"user_name": user.name, "posts": post}
    )


@login_required(login_url="/auth/")
def postDetails(request, id):
    postObject = models.post.objects.get(id=id)
    suggetionObjects = models.post.objects.filter(user__email=postObject.user.email)
    suggestions = list()
    for suggestion in suggetionObjects:
        url = None
        try:
            url = suggestion.image.url
        except Exception as e:
            print("No image for", suggestion.title)
        suggestions.append(
            {
                "image": url,
                "title": suggestion.title,
                "subheading": suggestion.subheading,
                "id": suggestion.id,
            }
        )
    data = {
        "image": postObject.image.url,
        "title": postObject.title,
        "subheading": postObject.subheading,
        "author": postObject.user.name,
        "suggestions": suggestions,
        "content": postObject.content,
    }
    return render(request, "details.html", context=data)


@login_required(login_url="/auth/")
def createpost(request, id=None):
    title = ""
    subheading = ""
    content = ""
    tag = ""
    image = None
    updated = None
    user = userModel.user.objects.get(email=request.user)
    post_url = "/post/new/"
    if request.method == "GET":
        if id != None:
            post = models.post.objects.get(id=id)
            if post.user.email != str(request.user):
                return redirect("/post/personal/")
            title = post.title
            subheading = post.subheading
            content = post.content
            tag = post.tag
            post_url = f"/post/edit/{id}/"
        return render(
            request,
            "create.html",
            context={
                "title": title,
                "subheading": subheading,
                "content": content,
                "tag": tag,
                "post_url": post_url,
            },
        )
    elif request.method == "POST":
        if id == None:
            # New post
            try:
                image = request.FILES.get("img")
            except Exception as e:
                print("No image data")
            title = request.POST.get("title")
            subheading = request.POST.get("subheading")
            content = request.POST.get("content")
            tag = request.POST.get("tag")
            updated = datetime.now()

            new = models.post(
                title=title,
                subheading=subheading,
                content=content,
                tag=tag,
                image=image,
                updated=updated,
                user=user,
            )
            new.save()
        else:
            # Update post
            post = models.post.objects.get(id=id)
            try:
                image = request.FILES.get("img")
                if image != None:
                    post.image = image
            except Exception as e:
                print("No image data")
            title = request.POST.get("title")
            subheading = request.POST.get("subheading")
            content = request.POST.get("content")
            updated = datetime.now()
            tag = request.POST.get("tag")

            post.title = title
            post.subheading = subheading
            post.content = content
            post.tag = tag
            post.updated = updated
            post.save()
        return redirect("/post/personal/")


@login_required(login_url="/auth/")
def deletePost(request, id):
    post = models.post.objects.get(id=id)
    if post.user.email == str(request.user):
        post.delete()
    return redirect("/post/personal/")
