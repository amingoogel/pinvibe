from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pin, Comment, Like, Category
from users.models import Follow
from .serializers import PinSerializer, CommentSerializer, LikeSerializer, CategorySerializer
from rest_framework import viewsets, permissions, filters
from users.models import User
from boards.models import Board
from django.core.exceptions import PermissionDenied

class PinViewSet(viewsets.ModelViewSet):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

def pin_list(request):
    pins = Pin.objects.all()
    if request.user.is_authenticated and 'following' in request.GET:
        following_users = request.user.following.values_list('following__id', flat=True)
        pins = pins.filter(user__id__in=following_users)
    categories = Category.objects.all()
    return render(request, 'pins/pin_list.html', {'pins': pins, 'categories': categories})

def pin_detail(request, pk):
    pin = Pin.objects.get(pk=pk)
    comments = pin.comments.all()
    return render(request, 'pins/pin_detail.html', {'pin': pin, 'comments': comments})

@login_required
def add_comment(request, pk):
    pin = Pin.objects.get(pk=pk)
    if request.method == 'POST':
        text = request.POST['text']
        Comment.objects.create(pin=pin, user=request.user, text=text)
    return redirect('pin_detail', pk=pk)

@login_required
def add_like(request, pk):
    pin = Pin.objects.get(pk=pk)
    Like.objects.get_or_create(pin=pin, user=request.user)
    return redirect('pin_detail', pk=pk)

@login_required
def save_pin(request, pk):
    pin = Pin.objects.get(pk=pk)
    if request.method == 'POST':
        board_id = request.POST.get('board')
        if board_id:
            board = Board.objects.get(id=board_id, user=request.user)
            pin.board = board
            pin.save()
        pin.saved_by.add(request.user)
    return redirect('pin_detail', pk=pk)

@login_required
def create_pin(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES['image']
        board_id = request.POST.get('board')
        category_id = request.POST.get('category')
        board = Board.objects.get(id=board_id) if board_id else None
        category = Category.objects.get(id=category_id) if category_id else None
        Pin.objects.create(title=title, description=description, image=image, user=request.user, board=board, category=category)
        return redirect('pin_list')
    boards = Board.objects.filter(user=request.user)
    categories = Category.objects.all()
    return render(request, 'pins/create_pin.html', {'boards': boards, 'categories': categories})

@login_required
def edit_pin(request, pk):
    pin = get_object_or_404(Pin, pk=pk, user=request.user)
    if request.method == 'POST':
        pin.title = request.POST['title']
        pin.description = request.POST['description']
        if 'image' in request.FILES:
            pin.image = request.FILES['image']
        board_id = request.POST.get('board')
        category_id = request.POST.get('category')
        pin.board = Board.objects.get(id=board_id) if board_id else None
        pin.category = Category.objects.get(id=category_id) if category_id else None
        pin.save()
        messages.success(request, 'Pin updated successfully!')
        return redirect('user_pins_boards')
    boards = Board.objects.filter(user=request.user)
    categories = Category.objects.all()
    return render(request, 'pins/edit_pin.html', {'pin': pin, 'boards': boards, 'categories': categories})

@login_required
def delete_pin(request, pk):
    pin = get_object_or_404(Pin, pk=pk, user=request.user)
    if request.method == 'POST':
        pin.delete()
        messages.success(request, 'Pin deleted successfully!')
        return redirect('user_pins_boards')
    return render(request, 'pins/delete_pin.html', {'pin': pin})

@login_required
def edit_board(request, pk):
    board = get_object_or_404(Board, pk=pk, user=request.user)
    if request.method == 'POST':
        board.name = request.POST['name']
        board.save()
        messages.success(request, 'Board updated successfully!')
        return redirect('user_pins_boards')
    return render(request, 'pins/edit_board.html', {'board': board})

@login_required
def delete_board(request, pk):
    board = get_object_or_404(Board, pk=pk, user=request.user)
    if request.method == 'POST':
        board.delete()
        messages.success(request, 'Board deleted successfully!')
        return redirect('user_pins_boards')
    return render(request, 'pins/delete_board.html', {'board': board})

def login_view(request):
    # اگر کاربر قبلاً login کرده، به صفحه اصلی redirect کن
    if request.user.is_authenticated:
        return redirect('pin_list')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            return render(request, 'pins/login.html', {
                'error': 'نام کاربری و رمز عبور الزامی است.',
                'form_data': {'username': username}
            })
        
        user = authenticate(request, username=username, password=password)
        
        if user:
            # بررسی تایید ایمیل
            if not user.is_active:
                return render(request, 'pins/login.html', {
                    'error': 'حساب کاربری شما فعال نیست. لطفاً ایمیل خود را تایید کنید.',
                    'form_data': {'username': username},
                    'needs_verification': True,
                    'email': user.email
                })
            
            if not user.is_email_verified:
                return render(request, 'pins/login.html', {
                    'error': 'ایمیل شما تایید نشده است. لطفاً ایمیل خود را تایید کنید.',
                    'form_data': {'username': username},
                    'needs_verification': True,
                    'email': user.email
                })
            
            login(request, user)
            # اگر next parameter وجود دارد، به آن صفحه برو
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('pin_list')
        else:
            return render(request, 'pins/login.html', {
                'error': 'نام کاربری یا رمز عبور اشتباه است.',
                'form_data': {'username': username}
            })
    
    return render(request, 'pins/login.html')

def register_view(request):
    # اگر کاربر قبلاً login کرده، به صفحه اصلی redirect کن
    if request.user.is_authenticated:
        return redirect('pin_list')
    
    if request.method == 'POST':
        from users.models import User
        from users.validators import PersianPasswordValidator
        from django.core.exceptions import ValidationError
        
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        errors = {}
        
        # اعتبارسنجی نام کاربری
        if not username:
            errors['username'] = 'نام کاربری الزامی است.'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'این نام کاربری قبلاً استفاده شده است.'
        elif not username.replace('_', '').isalnum():
            errors['username'] = 'نام کاربری فقط می‌تواند شامل حروف، اعداد و خط زیر باشد.'
        
        # اعتبارسنجی ایمیل
        if not email:
            errors['email'] = 'ایمیل الزامی است.'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'این ایمیل قبلاً استفاده شده است.'
        
        # اعتبارسنجی رمز عبور
        if not password:
            errors['password'] = 'رمز عبور الزامی است.'
        elif password != password_confirm:
            errors['password'] = 'رمزهای عبور مطابقت ندارند.'
        else:
            try:
                validator = PersianPasswordValidator()
                validator.validate(password)
            except ValidationError as e:
                errors['password'] = e.messages[0] if e.messages else 'رمز عبور نامعتبر است.'
        
        if errors:
            return render(request, 'pins/register.html', {
                'errors': errors,
                'form_data': {
                    'username': username,
                    'email': email
                }
            })
        
        # ایجاد کاربر
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=False  # کاربر باید ایمیل را تایید کند
            )
            
            # ارسال ایمیل تایید
            from users.utils import send_verification_email
            if send_verification_email(user):
                messages.success(request, 'ثبت نام با موفقیت انجام شد. لطفاً ایمیل خود را برای تایید بررسی کنید.')
            else:
                messages.warning(request, 'ثبت نام انجام شد اما ارسال ایمیل تایید با مشکل مواجه شد.')
            
            return redirect('login')
            
        except Exception as e:
            errors['general'] = f'خطا در ثبت نام: {str(e)}'
            return render(request, 'pins/register.html', {
                'errors': errors,
                'form_data': {
                    'username': username,
                    'email': email
                }
            })
    
    return render(request, 'pins/register.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('pin_list')

@login_required
def create_board(request):
    if request.method == 'POST':
        from boards.models import Board
        name = request.POST['name']
        Board.objects.create(name=name, user=request.user)
        return redirect('pin_list')
    return render(request, 'pins/create_board.html')

def search_pins(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    pins = Pin.objects.all()
    if query:
        pins = pins.filter(title__icontains=query) | pins.filter(description__icontains=query)
    if category_id:
        pins = pins.filter(category_id=category_id)
    categories = Category.objects.all()
    return render(request, 'pins/search.html', {'pins': pins, 'categories': categories, 'query': query})

@login_required
def user_profile(request):
    if request.method == 'POST':
        user = request.user
        user.bio = request.POST.get('bio', '')
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')
    
    # Get followers and following counts
    followers = request.user.followers.count()
    following = request.user.following.count()
    
    return render(request, 'pins/user_profile.html', {
        'followers': followers,
        'following': following
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        user = authenticate(username=request.user.username, password=current_password)
        if user:
            user.set_password(new_password)
            user.save()
            login(request, user)
            messages.success(request, 'Password changed successfully!')
        else:
            messages.error(request, 'Current password is incorrect.')
        return redirect('change_password')
    return render(request, 'pins/change_password.html')

@login_required
def user_pins_boards(request):
    pins = Pin.objects.filter(user=request.user)
    boards = Board.objects.filter(user=request.user)
    return render(request, 'pins/user_pins_boards.html', {'pins': pins, 'boards': boards})

@login_required
def user_likes_saves(request):
    liked_pins = Pin.objects.filter(likes__user=request.user)
    saved_pins = Pin.objects.filter(saved_by=request.user)
    return render(request, 'pins/user_likes_saves.html', {'liked_pins': liked_pins, 'saved_pins': saved_pins})

@login_required
def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk, user=request.user)
    return render(request, 'pins/board_detail.html', {'board': board})

@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    pins = Pin.objects.filter(user=user_profile)
    boards = Board.objects.filter(user=user_profile)
    followers = user_profile.followers.count()
    following = user_profile.following.count()
    is_following = request.user.is_authenticated and Follow.objects.filter(follower=request.user, following=user_profile).exists()
    return render(request, 'pins/profile.html', {
        'profile_user': user_profile,
        'pins': pins,
        'boards': boards,
        'followers': followers,
        'following': following,
        'is_following': is_following
    })

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)
    return redirect('profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', username=username)

@login_required
def remove_follower(request, username):
    follower = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=follower, following=request.user).delete()
    return redirect('followers_list', request.user.username)

@login_required
def followers_list(request, username):
    user_profile = get_object_or_404(User, username=username)
    followers = user_profile.followers.all()
    return render(request, 'pins/followers_list.html', {'profile_user': user_profile, 'followers': followers})

@login_required
def following_list(request, username):
    user_profile = get_object_or_404(User, username=username)
    following = user_profile.following.all()
    return render(request, 'pins/following_list.html', {'profile_user': user_profile, 'following': following})