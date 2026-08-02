from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import EmployeeProfile


class LoginForm(AuthenticationForm):
    """Kế thừa AuthenticationForm để tương thích với Django 6 LoginView."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'username', 'autofocus': True,
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control', 'placeholder': '••••••••',
        })
        self.fields['username'].label = 'Tên đăng nhập'
        self.fields['password'].label = 'Mật khẩu'



class ProductForm(forms.ModelForm):
    features_raw = forms.CharField(
        label='Tính năng (mỗi dòng 1 tính năng)',
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        required=False,
    )

    class Meta:
        from home.models import Product
        model = Product
        fields = ['key', 'title', 'subtitle', 'icon', 'tag', 'category_group', 'status', 'description', 'order', 'is_active']
        widgets = {f: forms.TextInput(attrs={'class': 'form-control'}) for f in
                   ['key', 'title', 'subtitle', 'icon', 'tag', 'order']}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget, 'attrs'):
                continue
            field.widget.attrs.setdefault('class', 'form-control')
        if self.instance and self.instance.pk:
            self.fields['features_raw'].initial = '\n'.join(self.instance.features or [])

    def save(self, commit=True):
        obj = super().save(commit=False)
        raw = self.cleaned_data.get('features_raw', '')
        obj.features = [line.strip() for line in raw.splitlines() if line.strip()]
        if commit:
            obj.save()
        return obj


class NewsArticleForm(forms.ModelForm):
    class Meta:
        from home.models import NewsArticle
        model = NewsArticle
        fields = ['slug', 'title', 'date', 'author', 'image_url', 'summary', 'content', 'is_published']
        widgets = {
            'slug':      forms.TextInput(attrs={'class': 'form-control'}),
            'title':     forms.TextInput(attrs={'class': 'form-control'}),
            'date':      forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'author':    forms.TextInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'summary':   forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content':   forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        from home.models import Project
        model = Project
        fields = ['title', 'description', 'image_url', 'tags', 'order', 'is_active']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image_url':   forms.URLInput(attrs={'class': 'form-control'}),
            'tags':        forms.TextInput(attrs={'class': 'form-control'}),
            'order':       forms.NumberInput(attrs={'class': 'form-control'}),
        }


class UserCreateForm(forms.Form):
    username  = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email     = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Xác nhận mật khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    role      = forms.ChoiceField(choices=EmployeeProfile.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            raise forms.ValidationError('Mật khẩu không khớp.')
        return cleaned


class UserEditForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=EmployeeProfile.ROLE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model  = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {f: forms.TextInput(attrs={'class': 'form-control'}) for f in ['email', 'first_name', 'last_name']}

    def __init__(self, *args, profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._profile = profile
        if profile:
            self.fields['role'].initial = profile.role

    def save(self, commit=True):
        user = super().save(commit=commit)
        role = self.cleaned_data.get('role')
        if role and self._profile:
            self._profile.role = role
            if commit:
                self._profile.save()
        return user
