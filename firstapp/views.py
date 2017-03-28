from django.shortcuts import render, redirect,HttpResponse
from firstapp.models import Article,Tickets, Comment_New
from firstapp.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth import login as auth_login , authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def index(request,cate=None):
    context = {}
    if cate == None:
        result_list = Article.objects.all()
    if cate == 'hot':
        result_list = Article.objects.filter(cate_choice='hot')
    if cate == 'best':
        result_list = Article.objects.filter(cate_choice='best')


    page_robot = Paginator(result_list, 9)
    page_num = request.GET.get('page')

    try:
        article_list = page_robot.page(page_num)
    except EmptyPage:
        article_list = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger :
        article_list = page_robot.page(1)

    print (article_list.number)


    # 传递页码
    if article_list.number <= 3:
        index_list = [1,2,3,'...',page_robot.num_pages]

    elif article_list.number < page_robot.num_pages -2 :
        index_list = [article_list.number-2, article_list.number-1, article_list.number, '...',page_robot.num_pages]

    elif article_list.number == page_robot.num_pages -2 :
        index_list = [article_list.number-2, article_list.number-1, article_list.number, page_robot.num_pages-1, page_robot.num_pages]

    elif article_list.number == page_robot.num_pages - 1:
        index_list = [article_list.number-3,article_list.number-2,article_list.number-1,article_list.number,page_robot.num_pages]

    elif article_list.number == page_robot.num_pages:
        index_list = [page_robot.num_pages-x for x in range(4,-1,-1)]



    context = {}
    context['index_list'] = index_list
    context["article_list"] = article_list
    return render(request, 'index.html', context)


def detail(request, page_num, error_form=None):

    context = {}

    if error_form == None:
        form = CommentForm()

    if error_form :
        form = error_form

    article = Article.objects.get(id=page_num)
    # 获取关联这篇文章的所有评论
    comments = Comment_New.objects.filter(belong_to_id=article.id)

    # 处理投票业务的数据渲染
    all_ticket_count = article.tickers.count()
    ticket_like_count = article.tickers.filter(vote='like').count()
    ticket_dislike_count = article.tickers.filter(vote='dislike').count()
    context['all_ticket_count'] = all_ticket_count
    context['ticket_like_count'] = ticket_like_count
    context['ticket_dislike_count'] = ticket_dislike_count

    if request.user.is_authenticated:
        user_vote_ticket_like = article.tickers.filter(voter_id=request.user.id,vote='like').count()
        print ('like_count:',user_vote_ticket_like)
        user_vote_ticket_dislike = article.tickers.filter(voter_id=request.user.id,vote='dislike').count()
        print ('dislike_count:',user_vote_ticket_dislike)
        context['user_vote_ticket_like'] = user_vote_ticket_like
        context['user_vote_ticket_dislike'] = user_vote_ticket_dislike


    context['article'] = article
    context['form'] = form
    context['comments'] = comments
    return render(request, 'detail.html', context)


def detail_vote(request, id):
    if request.user.is_authenticated:
        vote = request.POST['vote']
        article = Article.objects.get(id=id)
        user = User.objects.get(username=request.user.username)
        ticket = Tickets(voter=user,article=article,vote=vote)
        ticket.save()
        return redirect('detail',id)
    else:
        return redirect('register')

# 新的评论功能 用户可以对一篇文章点评多次
def detail_comment(request, page_num):
    # 判断是否登录
    if request.user.is_authenticated:
        # 表单绑定
        form = CommentForm(request.POST)
        # 验证表单
        if form.is_valid():
            content = form.cleaned_data['comment']
            publisher = request.user
            belong_to = Article.objects.get(id=page_num)

            comment =  Comment_New(publisher=publisher, content=content, belong_to=belong_to)
            comment.save()
            return redirect('detail',page_num)
        else:
            return detail(request, page_num=page_num, error_form=form)


# 注册业务
def register(request):
    context = {}
    if request.method == 'GET':
        form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            auth_login(request, user)
            return redirect('index')
    context['form']= form
    return render(request, 'register.html', context)

# 登录业务
def login(request):
    context = {}
    if request.method == 'GET':
        form = AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            print ('已经登录')
            return redirect('index')
    context['form']= form
    return render(request, 'register.html', context)
