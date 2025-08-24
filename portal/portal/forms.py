from django import forms
from .models import Post
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'categoryes',
            'title',
            'text'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title is not None and len(title) < 10:
            raise ValidationError({
                "title": "Заголовок не может быть менее 10 символов."
            })
        text = cleaned_data.get("text")
        if text is not None and len(text) < 100:
            raise ValidationError({
                "text": "Текст не может быть менее 100 символов."
            })

        # user = self.instance.user
        # if not user:
        #     return cleaned_data
        # twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        # post_count = Post.objects.filter(
        #     author__user=user,
        #     time_in__gte=twenty_four_hours_ago
        # ).count()
        #
        # if post_count >= 3:
        #     raise forms.ValidationError(
        #         "Вы не можете публиковать более 3 записей в сутки. "
        #         f"Вы уже опубликовали {post_count} постов за последние 24 часа."
        #     )

        return cleaned_data