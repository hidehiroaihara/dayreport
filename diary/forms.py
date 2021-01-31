from django import forms
from .models import Post, Post2, Notice, Done, File

# 投稿フォーム
class PostCreateForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = Post
    fields = (
      'title',
      'date'
    )
    

Post2Formset = forms.inlineformset_factory(
  Post, Post2, fields='__all__',
  extra=9, max_num=9, can_delete=False

)


# お知らせフォーム
class NoticeCreateForm(forms.ModelForm):

  class Meta:
    model = Notice
    fields = (
      'title',
      'date',
      'text',
      'category',
    )
    widgets ={
      'date': forms.SelectDateWidget
    }

# やったことリストフォーム
class DoneCreateForm(forms.ModelForm):
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = Done 
    fields = (
      'category_list',
      'text',
      'point',
    )

FileFormSet = forms.inlineformset_factory(
  Done, File, fields='__all__',
   extra=1, max_num=3, can_delete=False
)
