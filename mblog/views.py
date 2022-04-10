from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import models,forms
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = models.Post
    paginate_by = 4

    def get_queryset(self):
        return models.Post.objects.order_by('-published_date')

class PostDetailView(DetailView):
    model = models.Post

class PostCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    form_class = forms.Post_form
    model = models.Post
    redirect_field_name = 'mlog/post_detail.html'


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'mlog/post_detail.html'
    form_class = forms.Post_form

    model = models.Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'mblog/post_list.html'
    model = models.Post

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull=True).order_by('create_date')
    
####################################
@login_required
def post_publish(request, pk):
    post = get_object_or_404(models.Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)


#@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(models.Post,pk=pk)
    if request.method == 'POST':
        form = forms.Comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = forms.Comment_form()
    return render(request,'mblog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(models.Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)