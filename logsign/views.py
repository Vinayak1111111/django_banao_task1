from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

def login(request):
    return render(request, "login.html")

def dashboard(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user_name = request.POST.get('user_name')
        user_type = request.POST.get('user_type')
        address_line1 = request.POST.get('address_line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        profile_picture_url = None
        if request.FILES.get('profilePicture'):
            profile_picture = request.FILES['profilePicture']
            fs = FileSystemStorage()
            filename = fs.save(profile_picture.name, profile_picture)
            profile_picture_url = fs.url(filename)

        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'user_name': user_name,
            'user_type': user_type,
            'address_line1': address_line1,
            'city': city,
            'state': state,
            'pincode': pincode,
            'profile_picture': profile_picture_url if profile_picture_url else None
        }
        return render(request, 'dashboard.html', {'user_data': user_data})
    return redirect('login')
