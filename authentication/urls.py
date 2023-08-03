from django.urls import path
from .views import signup_view, login_view, home, logout_view
from django.conf import settings
from .views import (
    blog_list, blog_detail, like_blog, create_blog, edit_user,
    contactus, contact_success, profile_user, premium_user_view
)
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', signup_view, name='Signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('navbar/', profile_user, name='profile'),
    path('profile/detail/create/', create_blog, name='create'),
    path('blog_list/', blog_list, name='blog_list'),
    path('category/', blog_list, name='category_list'),
    path('blog/detail/<int:blog_id>/', blog_detail, name='blog_detail'),
    path('', home, name='home'),
    path('profile/edituser/', edit_user, name='edituser'),
    path('blog/like/<int:blog_id>/', like_blog, name='like_blog'),
    path('contact/', contactus, name='contactus'),
    path('success/', contact_success, name='contactsuccess'),
    path('profile/detail/create/premium', premium_user_view, name='premium'),

    # path('category/', search_by_category, name='category'),
    # path('profile/', profile_user, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)