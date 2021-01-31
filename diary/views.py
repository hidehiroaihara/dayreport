from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import PostCreateForm, Post2Formset, NoticeCreateForm, DoneCreateForm, FileFormSet
from .models import Notice, Post2, Comment, Post, Category, Done
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from functools import reduce
from operator import and_
from django.views.generic.list import ListView
import logging
from django.utils import timezone
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy

def paginate_queryset(request, queryset, count):
  """ Pageオブジェクトを返す。

  ページングしたい場合に利用してください。

  countは、1ページに表示する件数です。
  返却するPgaeオブジェクトは、以下のような感じで使えます。::

      {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
      {% endif %}

  また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

  """
  paginator = Paginator(queryset, count)
  page = request.GET.get('page')
  try:
      page_obj = paginator.page(page)
  except PageNotAnInteger:
      page_obj = paginator.page(1)
  except EmptyPage:
      page_obj = paginator.page(paginator.num_pages)
  return page_obj

def index(request):
  post = Post.objects.order_by('-date')
  page_obj = paginate_queryset(request, post, 7)
  done = Done.objects.order_by('-created_at')
  # done_page_obj = paginate_queryset(request, done, 1)
  keyword = request.GET.get('keyword')

  if keyword:
    """除外リストを作成"""
    exclusion_list = set([' ',' '])
    q_list = ''

    for i in keyword:
      """全角半角の空文字が含まれいたら無視"""
      if i in exclusion_list:
        pass
      else:
        q_list += i
    query = reduce(
      and_, [ Q(title__icontains=q) | Q(date__icontains=q) for q in q_list]
    )
    post = post.filter(query)
    messages.success(request, '『{}』の検索結果'.format(keyword))
  today = datetime.datetime.now()
  delta_1 = datetime.timedelta(days=1)  
  yestday = today - delta_1
  context = {}
  context['post'] = post
  context["post_list"] = Post.objects.order_by('-date')
  context['today'] = today
  context['notice'] = Notice.objects.all()[:3]
  context['yestday'] = yestday
  context['page_obj'] = page_obj
  context['done'] = done
  # context['done_page_obj'] = done_page_obj
  

  return render(request, 'diary/post_list.html', context)

# 投稿View

@login_required
def add_post(request):
  form = PostCreateForm(request.POST or None)
  context = {'form': form}
  if request.method == 'POST' and form.is_valid():
    post = form.save(commit=False)
    post.author = request.user
    formset = Post2Formset(request.POST, instance=post)
    if formset.is_valid():
      post.save()
      formset.save()
      return redirect('diary:index')
      # エラーメッセージつきのformsetをテンプレートへ渡すため、contextに格納                                   
    else:                               
      context['formset'] = formset
           # getの時
  else:
    # 空のformsetをテンプレートへ渡す
    context['formset'] = Post2Formset()
  
  return render(request, 'diary/post_form.html', context)

@login_required
def update_post(request, pk):
  post = get_object_or_404(Post, pk=pk)
  form = PostCreateForm(request.POST or None, instance=post)
  formset = Post2Formset(request.POST or None, instance=post)
  if request.method == 'POST' and form.is_valid() and formset.is_valid():
    form.save()
    formset.save()
    # 編集ページを再度表示
    return redirect('diary:index')

  context = {
    'form': form,
    'formset': formset
  }

  return render(request, 'diary/post_form.html', context)

 # 投稿削除 
# @login_required
# def post_delete(request,pk):
#   post = get_object_or_404(Post, pk=pk)
#   post2 = get_object_or_404(Post2, pk=pk)
  
#   if request.method == 'POST':
#     post.delete()
#     post2.delete()
#     return ('diary:index')

#     context = {
#     'post': post,
#     'post2': post2
#   }
#   return render(request,'diary/post_detail.html',context)


class PostDetail(LoginRequiredMixin, generic.CreateView):
  template_name = 'diary/post_detail.html'
  model = Comment
  fields = ('text',)
 
  # コメント投稿
  def get_context_data(self, **kwargs):
    #記事のモデルインスタンスを渡す様にする
    context = super().get_context_data(**kwargs)
    post = get_object_or_404(Post, pk=self.kwargs['pk'])
    context['post'] = post
    return context

  def form_valid(self, form):
    #　コメントに、記事を紐づける
    comment = form.save(commit=False)
    comment.author = self.request.user
    comment.post = get_object_or_404(Post, pk=self.kwargs['pk'])
    comment.save()
    return redirect('diary:detail', pk=self.kwargs['pk'])


# お知らせ
@login_required
def add_notice(request):
  form = NoticeCreateForm(request.POST or None)
  context = {'form': form}
  if request.method == 'POST' and form.is_valid():
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('diary:index')
      # エラーメッセージつきのformsetをテンプレートへ渡すため、contextに格納                                                                  
  context = {
    'form': form
  } 
  
  return render(request, 'diary/notice_form.html', context)

# お知らせ詳細

@login_required
def notice_detail(request, pk):
  notice = get_object_or_404(Notice, pk=pk)
  context = {
    'notice': notice
  }

  return render(request, 'diary/notice_detail.html', context)

@login_required
def notice_update(request, pk):
  notice = get_object_or_404(Notice, pk=pk)

  form = NoticeCreateForm(request.POST or None, instance=notice)
  if request.method == 'POST' and form.is_valid():
    form.save()
    return redirect('diary:index')

  context = {
    'form': form
  }
  
  return render(request, 'diary/notice_form.html', context)

# @login_required
# def notice_delete(request, pk):
#   notice = get_object_or_404(Notice, pk=pk)
#   if request.methond == 'POST':
#     notice.delete()
#     return redirect('diary:index')
  
#   context = {
#     'notice': notice
#   }

#   return render(request, 'diary/notice_detail.html', context)


# やったリスト投稿
@login_required
def done_add(request):
  form = DoneCreateForm(request.POST or None)
  context = {'form': form}
  if request.method == 'POST' and form.is_valid():
    post = form.save(commit=False)
    post.author = request.user
    post.confirmation = False
    formset = FileFormSet(request.POST, files=request.FILES, instance=post) # 今回はファイルなのでrequest.FILESが必要
    if formset.is_valid():
      post.save()
      formset.save()
      return redirect('diary:index')

    else:
      context = {
        'formset': formset
      }
  else:
    context['formset'] = FileFormSet()

  return render(request, 'diary/done_form.html', context)

# 更新
@login_required
def done_update(request, pk):
  post = get_object_or_404(Done, pk=pk)
  post.confirmation = False
  form = DoneCreateForm(request.POST or None, instance=post)
  formset = FileFormSet(request.POST or None, files=request.FILES or None, instance=post)
  if request.method == 'POST' and form.is_valid() and formset.is_valid():
      form.save()
      formset.save()
      
      return redirect('diary:index')

  context = {
      'form': form,
      'formset': formset
  }

  return render(request, 'diary/done_form.html', context)

# 詳細は共有条件式にて送信先を分ける
@login_required
def done_detail(request, pk):
  done = get_object_or_404(Done,pk=pk)
  context = {
    'done': done
  }

  return render(request, 'diary/done_detail.html', context)


 #やったことリストトップ管理者
@login_required
def done_list(request):
  done = Done.objects.order_by('-created_at')
  # page_obj = paginate_queryset(request, done, 1)
  context = {}
  context['done'] = done
  # context['page_obj'] = page_obj

  return render(request, 'diary/confirmation.html', context)

@login_required
def done_add_to(request, pk):
  post = get_object_or_404(Done, pk=pk)
  post.confirmation = True
  form = DoneCreateForm(request.POST or None, instance=post)
  formset = FileFormSet(request.POST or None, files=request.FILES or None ,instance=post)
  if request.method == 'POST' and form.is_valid() and formset.is_valid():
    form.save()
    formset.save()

    return redirect('diary:done_list')

  context = {
    'form': form,
    'formset': formset
  }

  return render(request, 'diary/done_form.html', context)
