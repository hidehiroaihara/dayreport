from django.urls import path
from . import views
# 画像を扱い際に必要
from django.conf import settings
from django.conf.urls.static import static

app_name = 'diary'

urlpatterns = [
  path('',views.index,name='index'),
  path('add/', views.add_post, name='add_post'),
  path('update/<int:pk>/', views.update_post, name='update_post'),
  path('detail/<int:pk>/',views.PostDetail.as_view(),name='detail'),
  # path('delete/<int:pk>/', views.post_delete, name='post_delete'),
  #お知らせ
  path('notice/add/', views.add_notice, name='add_notice'),
  path('notice/deatil/<int:pk>/', views.notice_detail, name='notice_detail'),
  path('notice/update/<int:pk>/', views.notice_update, name='notice_update'),
  # path('notice/delete/<int:pk>/', views.notice_delete, name='notice_delete'),
  # やったことリスト管理者
  path('done/', views.done_list, name='done_list'),
  path('done/add/to/<int:pk>/', views.done_add_to, name='done_add_to'),
  # やったことリストユーザー
  path('done/add/', views.done_add, name='done_add'),
  path('done/update/<int:pk>/', views.done_update, name='done_update'),
  path('done/detail/<int:pk>/', views.done_detail, name='done_detail')
]

#画像を扱う前に必要
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)