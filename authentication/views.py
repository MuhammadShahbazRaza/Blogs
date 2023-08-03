from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import default_storage
from .models import Custom_User
from .models import Blog, Contact
import os
from django.http import JsonResponse
# from .decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from django.shortcuts import render, HttpResponseRedirect, reverse
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import JsonResponse
import openai
from .api import post
import requests
from json.decoder import JSONDecodeError
from openai import Completion
import logging

@csrf_exempt
def signup_view(request):
    error = None
    path = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        profile_pic = request.FILES.get('profile_pic')

        if username == email:
            error = 'Username and email cannot be the same'
        elif Custom_User.objects.filter(username=username).exists() or Custom_User.objects.filter(email=email).exists():
            error = 'Username or email already exists.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif not any(char.isupper() for char in password):
            error = "The password must contain at least one uppercase letter."
        elif not any(char in '!@#$%^&*()-_+=[{]}|\/<>,.?;:' for char in password):
            error = "The password must contain at least one special character."
        elif len(password) < 8:
            error = 'Password must be at least 8 characters.'
        else:       
            # Save the profile picture to the media folder
            if profile_pic:
                path = default_storage.save(os.path.join('media', profile_pic.name), profile_pic)
            else:
                path = None

            # Create the user with hashed password
            
        user = Custom_User.objects.create(username=username, email=email, profile_pic=path, password=password)
        print(profile_pic)
        return redirect('login')

    return render(request, 'authentication/signup_1.html', {'error': error})
def profile_user(request):
    error = None
    user_info = request.session.get('user_info')
    if user_info:
        profile_pic = user_info.get('profile_pic')
        username = user_info.get('name')
        context = {
            'username': username
        }
        if profile_pic:
            context['profile_pic'] = profile_pic
        
        return render(request, 'blog/navbar.html', context)
    
    return redirect(reverse('login'))
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        try:
            user = Custom_User.objects.get(email=email, password=password)
        except Custom_User.DoesNotExist:
            error_message = "Invalid credentials. Please make sure you are signed up to this site."
            messages.error(request, error_message)
            return render(request, 'authentication/login.html', {'error': error_message})

        # Store user information in the session
        user_info = {
            'id': user.id,
            'name': user.username,
            'profile_pic': user.profile_pic.url if user.profile_pic else None,
            'is_premium':user.is_premium
        }
        request.session['user_info'] = user_info

        return redirect(reverse('blog_list'))

    return render(request, 'authentication/login.html')
def logout_view(request):
    # Remove user email from the session
    if 'user_email' in request.session:
        del request.session['user_email']
    return redirect('login')


def home(request):
    return render(request, 'authentication/home.html')

def blog_list(request):
    if request.method == 'POST':
        selected_category = request.POST.get('category')
        request.session['selected_category'] = selected_category
    else:
        selected_category = request.session.get('selected_category', None)

    if selected_category == 'all':
        blogs = Blog.objects.all()
        
    else:
        blogs = Blog.objects.filter(category__iexact=selected_category)

    categories = Blog.objects.values_list('category', flat=True).distinct()

    context = {
        'selected_category': selected_category,
        'blogs': blogs,
        'categories': categories,
    }

    return render(request, 'blog/blog_list.html', context)



def like_blog(request, blog_id):
    if request.method == 'POST':
        user_id = request.session.get('user_info').get('id')
        if user_id:
            # user_id = user.get('id')
            user1 = Custom_User.objects.get(id=user_id)
            try:
                blog = Blog.objects.get(id=blog_id)
                if blog.user == user_id:
                    # User cannot like their own post
                    return redirect('blog_list')
                else:
                    if user1 in blog.likes.all():
                        # User has already liked the post, so remove the like
                        blog.likes.remove(user_id)
                    else:
                        # User has not liked the post yet, so add the like
                        blog.likes.add(user_id)
                    # Redirect back to the blog detail page
                    return redirect('blog_detail', blog_id=blog_id)
            except Blog.DoesNotExist:
                return redirect('blog_list')
    return redirect('blog_list')
def blog_detail(request, blog_id):
    try:
        blog = get_object_or_404(Blog, id=blog_id)
        return render(request, 'blog/blog_detail.html', {'blog': blog, 'blog': blog,'code': blog.code, 'image': blog.image})

    except Blog.DoesNotExist:    
        print("Blog not found")

def create_blog(request):
    if request.method == 'POST':
        # Process the form data here
        category = request.POST.get('category')
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        code = request.POST.get('code')
        print(category, title, content, code)
        if category and title and content != '':
            user_info = request.session.get('user_info')
            user_id = user_info.get('id')
            if user_id:
                try:
                    user = Custom_User.objects.get(id=user_id)
                    print(user.username)
                    existing_blog = Blog.objects.filter(user=user, title=title).first()
                    if existing_blog:
                        return HttpResponse("You have already added a blog with the same title.")
                    else:
                        if image:
                            # Save the image to media/blog directory
                            image_path = default_storage.save(os.path.join('blog/', image.name), image)
                        else:
                            image_path = None

                        blog = Blog.objects.create(user=user, category=category, title=title, content=content, image=image_path, code=code)
                        context = {
                            'blog': blog,
                            'user': user,
                            'profile_pic': user.profile_pic.url if user.profile_pic else None,
                            'username': user.username,
                        }
                        return redirect('blog_list')
                except Custom_User.DoesNotExist:
                    return HttpResponse("User does not exist.")
            else:
                return HttpResponse("User ID not found in session.")
        else:
            return redirect(reverse('profile'))
    else:    
        return render(request, 'blog/create_blog.html')

def edit_user(request):
    user_info = request.session.get('user_info')
    id = user_info.get('id')
    try:
        user = Custom_User.objects.get(id=id)
        print(user)
        if request.method == 'POST':
            # Check each field and update the corresponding attribute if it is not empty
            if request.POST.get('username'):
                user.username = request.POST.get('username')
                user_info['name'] = user.username
                request.session['user_info'] = user_info

            if request.POST.get('email'):
                user.email = request.POST.get('email')
            if request.POST.get('password'):
                user.password = request.POST.get('password')

            # Handle the profile picture separately
            if 'profile_pic' in request.FILES:
                profile_pic = request.FILES['profile_pic']

                # Delete the old profile picture if it exists
                if user.profile_pic:
                    old_profile_pic_path = os.path.join(settings.MEDIA_ROOT, str(user.profile_pic))
                    if os.path.isfile(old_profile_pic_path):
                        os.remove(old_profile_pic_path)

                # Save the new profile picture in the media folder
                filename = profile_pic.name.strip()  # Remove leading/trailing spaces from the file name
                storage = FileSystemStorage(location=settings.MEDIA_ROOT)
                updated_profile_pic = storage.save(filename, profile_pic)
                user.profile_pic = updated_profile_pic

            # Save the updated user object
            user.save()

            # Update the profile picture in the session data
            user_info['profile_pic'] = user.profile_pic.url if user.profile_pic else None
            request.session['user_info'] = user_info

            return redirect('blog_list')

        return render(request, 'authentication/edit_user.html', {'user': user, 'user_info': user_info})
    except Custom_User.DoesNotExist:
        # Handle the case when the user does not exist
        messages.error(request, 'User not found in the database.')
        return redirect('blog_list')

        
def contactus(request):    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if name and email and message != '':
            contact =Contact.objects.create(name=name, email=email, message=message)
            contact.save()
            return redirect('contactsuccess')
        else:
            user_id= request.session.get('user_id')
            us= Custom_User.objects.get(id=user_id)
            return render(request, 'authentication/home.html', {'user':us})
    return render(request, 'blog/contactus.html')
def contact_success(request):
    return render(request, 'blog/contactsuccess.html')
def aboutus(request):
    pass 

def premium_user_view(request):
    user_info = request.session.get('user_info')
    id = user_info.get('id')
    user = Custom_User.objects.get(id=id)

    if user:
        if request.method == 'POST':
            category = request.POST.get('category')
            title = request.POST.get('title')

             # Call the generate_content function to generate content based on title and category
            content = post(title, category)
            code = ''

            if content:
                code_start_index = content.find('Code:')
                if code_start_index != -1:
                    code = content[code_start_index + len('Code:'):].strip()
                    content = content[:code_start_index].strip()

            # Set the user_id before creating the Blog instance
        blog_post = Blog(title=title, content=content, category=category, code=code, user_id=id)
        blog_post.save()

        return JsonResponse({'content': content, 'code': code})

        return render(request, 'blog/create_blog.html')

    else:
       return redirect('create')
def get_recently_updated_status():
    user = Custom_User.objects.latest('is_premium')    
    status = user.is_premium
    return status