from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from .forms import LoginForm, ProductForm, NewsArticleForm, ProjectForm, UserCreateForm, UserEditForm
from .models import EmployeeProfile
from home.models import Product, NewsArticle, Project
from contact.models import ContactSubmission


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'career/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        profile = EmployeeProfile.objects.filter(user=self.request.user).first()
        role_display = profile.get_role_display() if profile else 'User'
        messages.success(self.request, f'Chào mừng {self.request.user.username}! ({role_display})')
        return response


def _get_profile(user):
    return EmployeeProfile.objects.filter(user=user).first()


def role_required(min_role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('career-login')
            profile = _get_profile(request.user)
            if not profile or not profile.has_role_at_least(min_role):
                messages.error(request, 'Bạn không có quyền truy cập trang này.')
                return redirect('career-dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


@login_required
def dashboard(request):
    profile = _get_profile(request.user)
    context = {
        'profile': profile,
        'product_count': Product.objects.count(),
        'news_count': NewsArticle.objects.count(),
        'project_count': Project.objects.count(),
        'contact_count': ContactSubmission.objects.count(),
        'user_count': User.objects.count(),
        'role_label': profile.get_role_display() if profile else 'User',
    }
    return render(request, 'career/dashboard.html', context)


# ==================== PRODUCTS ====================

@login_required
@role_required('author')
def product_list(request):
    profile = _get_profile(request.user)
    if profile.is_author() and not profile.is_editor():
        products = Product.objects.filter(created_by=request.user)
    else:
        products = Product.objects.all()
    return render(request, 'career/cms/product_list.html', {
        'products': products,
        'profile': profile,
    })


@login_required
@role_required('author')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if not _get_profile(request.user).is_editor():
                obj.is_active = False
            obj.save()
            form.save_m2m()
            messages.success(request, 'Đã thêm sản phẩm thành công.')
            return redirect('cms-product-list')
    else:
        form = ProductForm()
    return render(request, 'career/cms/product_form.html', {
        'form': form,
        'title': 'Thêm sản phẩm',
        'profile': _get_profile(request.user),
    })


@login_required
@role_required('author')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    profile = _get_profile(request.user)
    if profile.is_author() and not profile.is_editor() and product.created_by != request.user:
        messages.error(request, 'Bạn chỉ có thể sửa sản phẩm do mình tạo.')
        return redirect('cms-product-list')
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật sản phẩm.')
            return redirect('cms-product-list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'career/cms/product_form.html', {
        'form': form,
        'title': 'Sửa sản phẩm',
        'profile': profile,
    })


@login_required
@role_required('admin')
def product_delete(request, pk):
    get_object_or_404(Product, pk=pk).delete()
    messages.success(request, 'Đã xóa sản phẩm.')
    return redirect('cms-product-list')


@login_required
@role_required('reviewer')
def product_toggle_active(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_active = not product.is_active
    product.save()
    status = 'kích hoạt' if product.is_active else 'ẩn'
    messages.success(request, f'Đã {status} sản phẩm "{product.title}".')
    return redirect('cms-product-list')


# ==================== NEWS ====================

@login_required
@role_required('author')
def news_list(request):
    profile = _get_profile(request.user)
    if profile.is_author() and not profile.is_editor():
        articles = NewsArticle.objects.filter(created_by=request.user)
    else:
        articles = NewsArticle.objects.all()
    return render(request, 'career/cms/news_list.html', {
        'articles': articles,
        'profile': profile,
    })


@login_required
@role_required('author')
def news_create(request):
    if request.method == 'POST':
        form = NewsArticleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            if not _get_profile(request.user).is_editor():
                obj.is_published = False
            obj.save()
            messages.success(request, 'Đã thêm bài viết thành công.')
            return redirect('cms-news-list')
    else:
        form = NewsArticleForm()
    return render(request, 'career/cms/news_form.html', {
        'form': form,
        'title': 'Thêm bài viết',
        'profile': _get_profile(request.user),
    })


@login_required
@role_required('author')
def news_edit(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    profile = _get_profile(request.user)
    if profile.is_author() and not profile.is_editor() and article.created_by != request.user:
        messages.error(request, 'Bạn chỉ có thể sửa bài viết do mình tạo.')
        return redirect('cms-news-list')
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật bài viết.')
            return redirect('cms-news-list')
    else:
        form = NewsArticleForm(instance=article)
    return render(request, 'career/cms/news_form.html', {
        'form': form,
        'title': 'Sửa bài viết',
        'profile': profile,
    })


@login_required
@role_required('admin')
def news_delete(request, pk):
    get_object_or_404(NewsArticle, pk=pk).delete()
    messages.success(request, 'Đã xóa bài viết.')
    return redirect('cms-news-list')


@login_required
@role_required('reviewer')
def news_toggle_publish(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    article.is_published = not article.is_published
    article.save()
    status = 'xuất bản' if article.is_published else 'ẩn'
    messages.success(request, f'Đã {status} bài viết "{article.title}".')
    return redirect('cms-news-list')


# ==================== PROJECTS ====================

@login_required
@role_required('author')
def project_list(request):
    profile = _get_profile(request.user)
    if profile.is_author() and not profile.is_editor():
        projects = Project.objects.filter(created_by=request.user)
    else:
        projects = Project.objects.all()
    return render(request, 'career/cms/project_list.html', {
        'projects': projects,
        'profile': profile,
    })


@login_required
@role_required('author')
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            if not _get_profile(request.user).is_editor():
                obj.is_active = False
            obj.save()
            messages.success(request, 'Đã thêm dự án thành công.')
            return redirect('cms-project-list')
    else:
        form = ProjectForm()
    return render(request, 'career/cms/project_form.html', {
        'form': form,
        'title': 'Thêm dự án',
        'profile': _get_profile(request.user),
    })


@login_required
@role_required('author')
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    profile = _get_profile(request.user)
    if profile.is_author() and not profile.is_editor() and project.created_by != request.user:
        messages.error(request, 'Bạn chỉ có thể sửa dự án do mình tạo.')
        return redirect('cms-project-list')
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật dự án.')
            return redirect('cms-project-list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'career/cms/project_form.html', {
        'form': form,
        'title': 'Sửa dự án',
        'profile': profile,
    })


@login_required
@role_required('admin')
def project_delete(request, pk):
    get_object_or_404(Project, pk=pk).delete()
    messages.success(request, 'Đã xóa dự án.')
    return redirect('cms-project-list')


@login_required
@role_required('reviewer')
def project_toggle_active(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.is_active = not project.is_active
    project.save()
    status = 'kích hoạt' if project.is_active else 'ẩn'
    messages.success(request, f'Đã {status} dự án "{project.title}".')
    return redirect('cms-project-list')


# ==================== CONTACTS ====================

@login_required
@role_required('admin')
def contact_list(request):
    contacts = ContactSubmission.objects.all()
    return render(request, 'career/cms/contact_list.html', {'contacts': contacts})


@login_required
@role_required('admin')
def contact_delete(request, pk):
    get_object_or_404(ContactSubmission, pk=pk).delete()
    messages.success(request, 'Đã xóa liên hệ.')
    return redirect('cms-contact-list')


# ==================== USER MANAGEMENT ====================

@login_required
@role_required('admin')
def user_list(request):
    profile = _get_profile(request.user)
    users = User.objects.select_related('employeeprofile').all()
    if profile.is_admin() and not profile.is_root():
        users = users.exclude(employeeprofile__role='root')
    return render(request, 'career/user_list.html', {
        'users': users,
        'profile': profile,
    })


@login_required
@role_required('root')
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data.get('email', ''),
            )
            EmployeeProfile.objects.update_or_create(
                user=user,
                defaults={'role': form.cleaned_data.get('role', 'viewer')},
            )
            messages.success(request, f'Đã tạo user "{user.username}".')
            return redirect('user-list')
    else:
        form = UserCreateForm()
    return render(request, 'career/user_form.html', {
        'form': form,
        'title': 'Thêm nhân viên',
        'profile': _get_profile(request.user),
    })


@login_required
@role_required('admin')
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = _get_profile(user)
    my_profile = _get_profile(request.user)

    if profile and profile.is_root() and not my_profile.is_root():
        messages.error(request, 'Chỉ Root mới có thể chỉnh sửa thông tin Root.')
        return redirect('user-list')

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user, profile=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật user "{user.username}".')
            return redirect('user-list')
    else:
        form = UserEditForm(instance=user, profile=profile)
    return render(request, 'career/user_form.html', {
        'form': form,
        'title': 'Sửa nhân viên',
        'profile': my_profile,
    })


@login_required
@role_required('root')
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    target_profile = _get_profile(user)
    if target_profile and target_profile.is_root():
        messages.error(request, 'Không thể xóa tài khoản Root.')
        return redirect('user-list')
    username = user.username
    user.delete()
    messages.success(request, f'Đã xóa user "{username}".')
    return redirect('user-list')
