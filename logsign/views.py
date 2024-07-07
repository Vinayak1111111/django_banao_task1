from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import mysql.connector

def login(request):
    return render(request, "login.html")

def create_post(request):
    user_data = request.session.get('user_data')
    if request.method == "POST":
        Title = request.POST.get('Title')
        Category = request.POST.get('Category')
        Summary = request.POST.get('Summary')
        Content = request.POST.get('Content')
        action = request.POST.get('action')  # Check which button was clicked

        # Check for null Category
        if not Category:
            return HttpResponse("Category cannot be null")

        Image_url = None
        if request.FILES.get('Image'):
            image = request.FILES['Image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            Image_url = fs.url(filename)
        
        is_draft = 1 if action == 'draft' else 0  # Set is_draft based on the action

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="your_password",
                database="task2"
            )

            mycursor = mydb.cursor()
            
            # Prepare SQL query to insert data into the database
            sql = "INSERT INTO blogdetails (Title, Category, Summary, Content, Image_url, is_draft) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (Title, Category, Summary, Content, Image_url, is_draft)
            
            # Execute the SQL query
            mycursor.execute(sql, val)
            
            # Commit the transaction
            mydb.commit()
            
            # Close the cursor and database connection
            mycursor.close()
            mydb.close()
            
            # return redirect('dashboard')
            return render(request, 'dashboard.html', {'user_data': user_data})
        
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return HttpResponse(f"Database error: {err}")
    
    return render(request, 'create_post.html')

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
        request.session['user_data'] = user_data
        return render(request, 'dashboard.html', {'user_data': user_data})
    
    return redirect('login')

def blogs_list(request):
    user_data = request.session.get('user_data')
    
    if user_data:
        user_type = user_data.get('user_type')

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="your_password",
                database="task2"
            )

            mycursor = mydb.cursor(dictionary=True)

            if user_type == "Doctor":
                # Fetch all blog posts for doctors
                mycursor.execute("SELECT * FROM blogdetails")
                blog_posts = mycursor.fetchall()
            elif user_type == "Patient":
                # Fetch only published blog posts for patients
                mycursor.execute("SELECT * FROM blogdetails WHERE is_draft = 0")
                blog_posts = mycursor.fetchall()

            # Close cursor and database connection
            mycursor.close()
            mydb.close()

            return render(request, 'blogs_list.html', {'blog_posts': blog_posts, 'user_data': user_data})
        
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return HttpResponse(f"Database error: {err}")

    return redirect('login')

def blogs_details(request):
    user_data = request.session.get('user_data')
    
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",
            database="task2"
        )

        mycursor = mydb.cursor(dictionary=True)

        # Fetch all blog posts from the database
        mycursor.execute("SELECT * FROM blogdetails")
        blog_posts = mycursor.fetchall()

        # Close cursor and database connection
        mycursor.close()
        mydb.close()

        return render(request, 'blogs_list.html', {'blog_posts': blog_posts, 'user_data': user_data})
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return HttpResponse(f"Database error: {err}")

def draft_post(request, post_id):
    user_data = request.session.get('user_data')

    if user_data and user_data.get('user_type') == "Doctor":
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="your_password",
                database="task2"
            )
            mycursor = mydb.cursor()

            # Update the blog post's is_draft status to True (draft)
            sql = "UPDATE blogdetails SET is_draft = %s WHERE id = %s"
            val = (True, post_id)
            
            mycursor.execute(sql, val)
            mydb.commit()

            mycursor.close()
            mydb.close()

            return redirect('blogs_list')

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return HttpResponse(f"Database error: {err}")
    
    return HttpResponse("Unauthorized")  # Handle unauthorized access

def post_draft(request, post_id):
    user_data = request.session.get('user_data')

    if user_data and user_data.get('user_type') == "Doctor":
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="your_password",
                database="task2"
            )
            mycursor = mydb.cursor()

            # Update the blog post's is_draft status to False (posted)
            sql = "UPDATE blogdetails SET is_draft = %s WHERE id = %s"
            val = (False, post_id)
            
            mycursor.execute(sql, val)
            mydb.commit()

            mycursor.close()
            mydb.close()

            return redirect('blogs_list')

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return HttpResponse(f"Database error: {err}")
    
    return HttpResponse("Unauthorized")  # Handle unauthorized access
