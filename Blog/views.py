from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from Blog.models import *
from accounts.views import *
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def handler404(request,exception):
    return render(request,'404.html')

def home(request):

    try:
        cate=category.objects.all()
        posts=post.objects.all()[:2]
        pop_post=post.objects.order_by('views').reverse()[:5]


        context={
            'cat':cate,
            'posts':posts,
            'pop_post':pop_post
        }
        return render(request,'index.html',context)

    except:
        return render(request,'404.html')

def categories(request,name):
    
    try:
        cat=category.objects.filter(name=name).first()
        recent_post=post.objects.filter(category=cat.id)[:5]
        all_category=category.objects.all()

        posts=get_page(request,post.objects.filter(category=cat.id))

        context={
            'cate':cat,
            'posts':posts,
            'recent_post':recent_post,
            'all_category':all_category
        }
        
        return render(request,'category.html',context)

    except:
        return render(request,'404.html')

def blog(request):

    try:
        cat=category.objects.all()
        pop_post=post.objects.all()[:5]
        posts=get_page(request,post.objects.order_by("date").reverse())
        print(posts)
        context={
            'cat':cat,
            'posts':posts,
            'pop_post':pop_post,
        }
        return render(request,'blog.html',context)

    except:
        return render(request,'404.html')

def add_post(request):
    try:
        fatch_cat=category.objects.all()

        if(request.method=='POST'):
            path=request.get_full_path()
            print (path) 
            verify=googlecaptcha(request)
            if(verify):        
                title=request.POST['title']
                desc=request.POST['description']
                cate=request.POST['category']
                img=request.FILES.get('image')

                if img==None:
                    messages.info(request,"Please Select Image ...")
                    return render(request,'add_post.html')

                title=post.objects.filter(title=title).first()

                if title!=None:
                    messages.info(request,"Title Is Already Exist")
                    return render(request,'add_post.html')

                cat_obj=category.objects.filter(name=cate).first()
                
                obj=post.objects.create(title=title,desc=desc,img=img,post_by=request.user,category=cat_obj)
                obj.save()

                messages.info(request,"Post Added Successfully")

                

        return render(request,'add_post.html',{'cat':fatch_cat})

    except:
            return render(request,'404.html')

def about(request):
    try:
        return render(request,'about.html')

    except:
        return render(request,'404.html')

def post_detail(request,title):

    try:
        cat=category.objects.all()
        post_obj=post.objects.filter(title=title).first()
        comments=comment.objects.filter(comment_to=post_obj.id).all()
        no_comment=comment.objects.filter(comment_to=post_obj.id).count()
        pop_post=post.objects.all()[:5]
        liked=False

        if request.user.is_authenticated:
            likes=like.objects.filter(like_by=request.user,like_to=post_obj.id).first()
            liked=True
            if not likes:   
                liked=False

        no_likes=like.objects.filter(like_to=post_obj.id).all().count()

        if(request.method=='GET' and request.user.is_authenticated):
            post_obj.views=post_obj.views+1
            post_obj.save()

        context={
            'cats':cat,
            'post':post_obj,
            'pop_posts':pop_post,
            'comments':comments,
            'no_comment':no_comment,
            'no_likes':no_likes,
            'liked':liked
        }
        return render(request,'post_details.html',context)

    except:
        return render(request,'404.html')

def likes(request,title):

    try:
        if request.user.is_authenticated==False:
            messages.info(request,"you must logged in for this service")
            return redirect(request.META['HTTP_REFERER'])

        like_by=request.user
        like_to=post.objects.filter(title=title).first()

        likes=like.objects.filter(like_by=request.user,like_to=like_to.id)

        if not likes:
            like_obj=like.objects.create(like_by=like_by,like_to=like_to)
            like_obj.save()
        else:
            likes.delete()
                
        return redirect(request.META['HTTP_REFERER'])

    except:
        return render(request,'404.html')

def add_comment(request,title):
    
    try:
        comm=request.POST['comment']
        comment_to=post.objects.filter(title=title).first()
        comment_obj=comment.objects.create(comment=comm,comment_to=comment_to,comment_by=request.user)
        comment_obj.save()

        return redirect(request.META['HTTP_REFERER'])
        
    except:
        return render(request,'404.html')

def get_page(request,post_obj):
        all_post=Paginator(post_obj.all(),5)
        page=request.GET.get('page')

        try:
            posts=all_post.page(page)
        except EmptyPage:
            posts=all_post.page(all_post.num_pages)
        except PageNotAnInteger:
            posts=all_post.page(1)

        return posts

def search(request):
    query=request.GET['search']

    if len(query)>30:
        posts=[]

    else:
        posts_title=post.objects.filter(title__icontains=query)
        posts_desc=post.objects.filter(desc__icontains=query)

        posts=posts_title.union(posts_desc)

    content={
        'posts':posts,
        'query':query
    }
    return render(request,'search.html',content)
