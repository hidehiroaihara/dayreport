from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

# ポイントリスト
NUM_CHOICES = (
  ('1', 1),
  ('2', 2),
  ('3', 3),
  ('4', 4),
  ('5', 5),
  ('6', 6),
  ('7', 7),
  ('8', 8),
  ('9', 9),
  ('10', 10)
)

# お知らせカテゴリー
class Category(models.Model):
  name = models.CharField('カテゴリ名', max_length=255)

  def __str__(self):
    return self.name

# お知らせモデル
class Notice(models.Model):
  title = models.CharField('タイトル', max_length=200)
  date = models.DateTimeField('日付', default=timezone.now)
  text = models.TextField('本文', max_length=200)
  category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.PROTECT)
  author = models.ForeignKey(get_user_model(),  on_delete=models.CASCADE)
  created_at = models.DateField('作成日', auto_now_add=True)

  def __str__(self):
    return self.title

# 日報投稿モデル
class Post(models.Model):
  title = models.CharField('タイトル', max_length=200)
  date = models.DateTimeField('日付', default=timezone.now)
  author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  created_at = models.DateField('作成日', auto_now_add=True)

  def __str___(self):
    return self.title 
  

# 日報に紐づいた投稿モデル
class Post2(models.Model):
  time = models.TimeField('時間')
  text = models.TextField('予定', max_length=200)
  text2 = models.TextField('実際', max_length=200, blank=True)
  target = models.ForeignKey(
    Post, related_name="se_post", verbose_name='日報',
    blank=True, null=True,
    on_delete=models.SET_NULL
  )




# 投稿にコメントできるモデル
class Comment(models.Model):
  text = models.CharField('コメント内容', max_length=255)
  author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.PROTECT, verbose_name='記事')
  created_at = models.DateTimeField('日付', default=timezone.now)


  def __str__(self):
    return self.text[:100]
 
 # やったリストに(done)紐づいたモデル
class CategoryList(models.Model):
  name = models.CharField('カテゴリ', max_length=30)

  def __str__(self):
    return self.name

# やったリスト投稿モデル
class Done(models.Model):
  category_list = models.ForeignKey(
    CategoryList, verbose_name="カテゴリリスト", on_delete=models.CASCADE)
  text = models.CharField('やったこと', max_length=100, blank=False)
  point = models.CharField('ポイント', choices=NUM_CHOICES, max_length=3)
  confirmation = models.BooleanField(default=False)
  author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  created_at = models.DateTimeField('日付', default=timezone.now)

  def __str__(self):
    return self.text

# やったことリストに紐づいたfileモデル
class File(models.Model):
  src = models.FileField('添付ファイル')
  target = models.ForeignKey(
    Done, related_name="se_done", verbose_name='紐つぐ記事',
    blank=True, null=True,
    on_delete=models.SET_NULL
  )
