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
    name = forms.CharField(max_length=50)
    comment = forms.CharField(
        widget = forms.Textarea(),
        error_messages = {
            'require':'亲～这是必填项哟',
        },
        validators=[keyword,lessword]
        )
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.CharField()