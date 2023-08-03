def navbar_context(request):
    user_info = request.session.get('user_info')
    navbar_context = {}
    if user_info:
        navbar_context['profile_pic'] = user_info.get('profile_pic')
        navbar_context['username'] = user_info.get('name')
    return navbar_context