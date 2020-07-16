from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment


class AboutView(TemplateView):
    template_name= 'blog/about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')



class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        context['most_recent'] = Post.objects.filter(
            published_date__lte=timezone.now()).exclude(pk=post.pk).order_by('-published_date')[:3]
        return context
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')


@login_required
def post_approve(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_list')


@login_required
def publish_now(request):
    # creating a form using request
    post = PostForm(request.POST)

    if post.is_valid():
        post_save = post.save(commit=False)
        # setting the published date
        post_save.publish()
        return redirect('post_detail', pk=post_save.pk)


def add_comment_to_post(request, pk):
    # getting the post
    post = get_object_or_404(Post, pk=pk)
    # if it is a post object
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # setting the relavent post for the comment using COmments models foriegn key
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # if it is a get request
        form = CommentForm()
    #rendering objets got by GET or POST requests
    return render(request, template_name='blog/comment_form.html', context={'form':form})


@login_required
def approve_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def remove_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    comment.delete()
    return redirect('post_detail', pk=post.pk)
