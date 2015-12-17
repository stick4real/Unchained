from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.contrib.auth.models import User
from .models import Article, Comment
# # # # # # # # # # 
# Authentification #
# # # # # # # # # #  
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    # Django function to log user
    user = authenticate(username=username, password=password)
    if user is not None:
        # Check if user is active or not
        if user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('myblog:index'))
        else:
            messages.add_message(request, messages.ERROR, """Your account isn't active.""")
            return HttpResponseRedirect("/accounts/login/?next=/myblog/")
    else:
        messages.add_message(request, messages.ERROR, """Wrong user informations""")
        return HttpResponseRedirect("/accounts/login/?next=/myblog/")

def register(request):
    # If request is get just show the template
    if request.method == 'GET':
       return render(request, 'registration/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')


        # check if user fills every inputs
        if not (username and password and email):
            messages.add_message(request, messages.ERROR, """You must fill every inputs""")
            return HttpResponseRedirect("/myblog/register/")
        else:
            # Create user in db and then log him
            user = User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return HttpResponseRedirect(reverse('myblog:index'))  

def logout(request):
    # If user is connected then logout
    if request.user.is_authenticated():
        auth_logout(request)
    else:
        messages.add_message(request, messages.ERROR, """You must be connected to logout""")
    
    return HttpResponseRedirect("/accounts/login/?next=/myblog/")  

# # # # # # # # # # 
#      Home       #
# # # # # # # # # #
@login_required(login_url='/accounts/login/')
def index(request):
    # Get the five last articles created 
    latest_article_list = Article.objects.order_by('-date')[:5]
    context = {'latest_article_list': latest_article_list}
    return render(request, 'myblog/index.html', context)

# # # # # # # # # # 
#     Article     #
# # # # # # # # # #
@login_required(login_url='/accounts/login/')
def article(request, article_id):
    # Get unique article or launch 404 error
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'myblog/article.html', {'article': article})

@login_required(login_url='/accounts/login/')
def newArticle(request):
    title = request.POST['title']
    content = request.POST['content']
    user = request.user

    # Check if user set content and title for article
    if not (content and title):
        messages.add_message(request, messages.ERROR, """You didn't fill every input.""")
    else:
        Article.objects.create(user=user, title=title, content=content, date=timezone.now())
    
    return HttpResponseRedirect(reverse('myblog:index'))

@login_required(login_url='/accounts/login/')
def deleteArticle(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if article.user.id == request.user.id:
        article.delete()
        messages.add_message(request, messages.SUCCESS, """Article deleted""")
    else:
        messages.add_message(request, messages.ERROR, """No right for deleting this article""")

    return HttpResponseRedirect(reverse('myblog:index'))

# # # # # # # # # # 
#     Comment     #
# # # # # # # # # #
@login_required(login_url='/accounts/login/')
def newComment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    content = request.POST['content']
    user = request.user

    # Check if user set content for comment
    if not content:
        messages.add_message(request, messages.ERROR, """You didn't write a content.""")
        return HttpResponseRedirect(reverse('myblog:article', args=(article_id,)))
    else:
        article.comment_set.create(user=user, content=content, date=timezone.now())
        return HttpResponseRedirect(reverse('myblog:article', args=(article_id,)))

@login_required(login_url='/accounts/login/')
def deleteComment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    article_id = comment.article.id
    if comment.user.id == request.user.id:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, """Comment deleted""")
    else:
        messages.add_message(request, messages.ERROR, """No right for deleting this comment""")
    
    return HttpResponseRedirect(reverse('myblog:article', args=(article_id,)))


