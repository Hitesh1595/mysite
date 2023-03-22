from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator,EmptyPage,\
                                            PageNotAnInteger

from django.views.generic import ListView

# Create your views here.

from blog.models import Post

from blog.forms import EmailPostForm
from django.core.mail import send_mail

def post_share(request,post_id):
    post = get_object_or_404(Post,id = post_id,status = Post.Status.PUBLISHED)
    sent = False
    # form was sunmitted
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            # ......send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read \
                        {post.title}"
            message = f"Read {post.title} at {post_url} \n\n \
                        {cd['name']} \'s comments: {cd['comments']}"
            
            send_mail(subject,message,'hiteshpratapk92@gmail.com',[cd['to']])

            sent = True
    else:
        form = EmailPostForm()

    context = {
        'post':post,
        'form':form,
        'sent':sent
    }
    return render(request,'blog/post/share.xhtml',context = context)



# as of now it will not cover if we pass page greater than limit it show error
class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = 'blog/post/list.xhtml'


def post_list(request):
    post_list = Post.published.all()

    # Pagination with 3 post per page
    paginator = Paginator(post_list,3)
    # if not page default 1
    page_number = request.GET.get('page',1)

    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    context = {
        "posts":posts
    }

    return render(request,'blog/post/list.xhtml',context = context)

def post_detail(request,year,month,day,post):
    
    post = get_object_or_404(Post,status = Post.Status.PUBLISHED,
                             publish__year = year,
                             publish__month = month,
                             publish__day = day,
                             slug = post)
    
    
    return render(request,'blog/post/detail.xhtml', {"post":post})

