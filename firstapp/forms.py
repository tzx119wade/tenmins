from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re

def keyword(comment):
    pattern1 = re.compile(r'发票')
    pattern2 = re.compile(r'钱')

    if re.findall(pattern1,comment) or re.findall(pattern2,comment):
        raise ValidationError('请不要输入敏感词，如钱或发票')

def lessword(comment):
    if len(comment) < 4 :
        raise ValidationError('评论内容需超过4个字～～')

class CommentForm(forms.Form):

    # name = forms.CharField(max_length=50)
    comment = forms.CharField(
        widget = forms.Textarea(attrs={'placeholder':'添加一条评论吧～'}),
        error_messages = {
            'require':'亲～这是必填项哟',
        },
        validators=[keyword,lessword]
        )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.CharField()


class ArticleForm(forms.Form):

    title = forms.CharField(
        label='文章标题',
        max_length=100,
        error_messages = {'required':'亲～一定要有标题哟'},
        validators = [keyword,lessword]
        )


    content = forms.CharField(
        label='内容',
        error_messages = {'required':'亲～一定要有标题哟'},
        validators = [lessword],
        widget = forms.Textarea(),
    )

    imgURL = forms.CharField(label='封面图地址')

    MY_CHOICES = (
    ('hot', 'HOT'),
    ('best', 'BEST'),
                    )

    category = forms.ChoiceField(choices=MY_CHOICES,
                            label = '选择文章分类',
                            widget=forms.RadioSelect,
                                )
