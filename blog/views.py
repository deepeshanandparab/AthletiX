from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from blog.filters import PostFilter
from blog.forms import CommentForm, CommentUpdateForm
from .models import Post, PostLikes, PostDislikes, PostComment


def blogHome(request):
    blog_posts = Post.objects.all().order_by('-posted_on')
    filter = PostFilter(request.GET, queryset=blog_posts)
    product_filter = PostFilter(request.GET, queryset=blog_posts).qs

    paginator = Paginator(product_filter, 3)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    first_item_number = 3 * (response.number - 1) + 1

    context = {
        'title': 'Blog',
        'search_filter': filter,
        'posts': response,
        'page_size': 3,
        'first_item_number': first_item_number
    }

    return render(request, 'blog/blog.html', context)

def blogDetails(request, id):
    post = Post.objects.get(pk=id)
    comment_form = CommentForm(request.POST or None)
    comments_list = PostComment.objects.filter(post_id=post.id).order_by('-created_at')
    # comment = PostComment.objects.get(id=comments_list.id)
    # comment_update_form = CommentUpdateForm(request.POST or None, instance=comment)

    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
        is_disliked = False
    elif post.dislikes.filter(id=request.user.id).exists():
        is_disliked = True
        is_liked = False
    else:
        is_liked = False
        is_disliked = False


    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.post.comments += 1
                comment.save()
                post.save()
                messages.success(request, 'Comment posted successfully.')
                return redirect('blog-detail-page', id=post.id)
            else:
                messages.error(request, 'Error occurred while posting comment.')
                return redirect('blog-detail-page', id=post.id)
        else:
            return redirect('login-page')
    else:
        form = CommentForm()

    # if comment_update_form.is_valid():
    #     comment_update_form.save()
    #     messages.success(request, 'Comment updated successfully')
    #     return redirect('blog_detail_page', id=comment.post.id)
    # else:
    #     messages.error(request, 'Error occurred while updating comment')
    context = {'title': 'Blog Details',
               'post': post,
               'form': form,
               'comments_list': comments_list,
               'comment_form': comment_form,
               # 'comment_update_form': comment_update_form,
               'is_liked':is_liked,
               'is_disliked':is_disliked}
    return render(request, 'blog/blog_detail.html', context)


def authorBlogs(request, author_id):
    blog_posts = Post.objects.filter(author=author_id).order_by('-posted_on')
    author_username = blog_posts[0].author
    paginator = Paginator(blog_posts, 3)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    first_item_number = 3 * (response.number - 1) + 1

    context = {
        'title': f'{author_username}\'s Blog',
        'posts': response,
        'page_size': 3,
        'first_item_number': first_item_number
    }
    return render(request, 'blog/author_blogs.html', context)

'''--------------------------------------- Likes and dislikes for the product post -----------------------------------------'''

@login_required
def likePost(request, id):
    post = Post.objects.get(id=id)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        PostLikes.objects.filter(post_id=post, user_id=request.user).delete()
        is_liked = False
    elif post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        PostDislikes.objects.filter(post_id=post, user_id=request.user).delete()
        post.likes.add(request.user)
        PostLikes.objects.create(post_id=post, user_id=request.user)
        is_disliked = False
        is_liked = True
    else:
        post.likes.add(request.user)
        PostLikes.objects.create(post_id = post, user_id = request.user)
        post.dislikes.remove(request.user)
        PostDislikes.objects.filter(post_id=post, user_id=request.user).delete()
        is_liked = True
        is_disliked = False
    return redirect('blog-detail-page', id= post.id)

@login_required
def dislikePost(request, id):
    post = Post.objects.get(id=id)
    is_disliked = False
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        PostDislikes.objects.filter(post_id=post, user_id=request.user).delete()
        is_disliked = False
    elif post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        PostLikes.objects.filter(post_id=post, user_id=request.user).delete()
        post.dislikes.add(request.user)
        PostDislikes.objects.create(post_id=post, user_id=request.user)
        is_liked = False
        is_disliked = True
    else:
        post.dislikes.add(request.user)
        PostDislikes.objects.create(post_id = post, user_id = request.user)
        post.likes.remove(request.user)
        PostLikes.objects.filter(post_id=post, user_id=request.user).delete()
        is_disliked = True
        is_liked = False
    return redirect('blog-detail-page', id= post.id)



'''-------------------------------------- Update and Delete Comments for Product ---------------------------------------'''

@login_required
def updateComment(request, comment_id):
    comment = PostComment.objects.get(pk=comment_id)
    comment_update_form = CommentUpdateForm(request.POST or None, instance=comment)

    if comment_update_form.is_valid():
        comment_update_form.save()
        messages.success(request, 'Comment updated successfully')
        return redirect('blog_detail_page', id=comment.post.id)
    else:
        messages.error(request, 'Error occurred while updating comment')
        return redirect('blog_detail_page', id=comment.post.id)
    return render(request, 'blog/blog_detail.html', {'comment_update_form': comment_update_form, 'title': 'Blog Details'})


@login_required
def deleteComment(request, comment_id):
    comment = PostComment.objects.get(pk=comment_id)
    comment.delete()
    comment.post.comments -= 1
    comment.post.save()
    messages.success(request, 'Comment has been deleted successfully.')
    return redirect('blog-detail-page', id=comment.post.id)




