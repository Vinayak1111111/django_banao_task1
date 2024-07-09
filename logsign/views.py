from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import mysql.connector
from datetime import datetime, timedelta

def backtodashboard(request):
    user_data = request.session.get('user_data')
    return render(request, "dashboard.html",{"user_data":user_data})


def login(request):
    return render(request, "login.html")

def view_events(request):
    
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinay@2000",
            database="task2"
        )

        mycursor = mydb.cursor(dictionary=True)
        
        mycursor.execute("SELECT * FROM appointments")
        events = mycursor.fetchall()

        # print(user_type)
        # Close cursor and database connection
        mycursor.close()
        mydb.close()

        return render(request, 'view_events.html', {'events': events})
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return HttpResponse(f"Database error: {err}")
    # return render(request, "view_events.html")


def appointment_form(request):
    if request.method == "POST":
        doctors_name = request.POST.get('doctor_id')
        print(doctors_name)
        
        # request.session['doctors_name'] = doctors_name
    return render(request, "appointment_form.html", {"doctors_name" : doctors_name })


def creating_appointment(request):
    # doctors_name = request.session.get('doctors_name')
    if request.method == "POST":
        doctors_name = request.POST.get('doctors_name')
        Required_speciality = request.POST.get('Required_speciality')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        
        end_time = (datetime.strptime(appointment_time, '%H:%M') + timedelta(minutes=45)).time()
        print(doctors_name)
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Vinay@2000",
                database="task2"
            )

            mycursor = mydb.cursor()
            
            
            
            # Check if the record already exists
            sql_check = "SELECT * FROM appointments WHERE doctors_name = %s AND required_speciality = %s AND appointment_date = %s AND appointment_time = %s  AND end_time = %s"
            val_check = (doctors_name, Required_speciality, appointment_date, appointment_time, end_time)
            mycursor.execute(sql_check, val_check)
            existing_record = mycursor.fetchone()

            if existing_record:
                # Record already exists, do not insert again
                return HttpResponse("Event is already Schedueled")

            
            # Prepare SQL query to insert data into the database
            sql = "INSERT INTO appointments (doctors_name, required_speciality, appointment_date, appointment_time, end_time) VALUES (%s, %s,%s, %s, %s)"
            val = (doctors_name, Required_speciality, appointment_date, appointment_time, end_time)
            
            # Execute the SQL query
            mycursor.execute(sql, val)
            
            # Commit the transaction
            mydb.commit()
            
            # Close the cursor and database connection
            mycursor.close()
            mydb.close()
            
            

            appointment_details ={
                'doctors_name':doctors_name,'appointment_date':appointment_date, 'appointment_time':appointment_time, "end_time":end_time
            }
            return render(request, 'creating_appointment.html', {'appointment_details':appointment_details})
        
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return HttpResponse(f"Database error: {err}")
    
    return render(request, 'appointment_form.html')





def list_of_doctors(request):
    
    user_data = request.session.get('user_data')
    
    # if user_data:
    #     user_type = user_data.get('user_type')

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vinay@2000",
            database="task2"
        )

        mycursor = mydb.cursor(dictionary=True)
        
        mycursor.execute("SELECT * FROM doctor_profile")
        doctors = mycursor.fetchall()

        # print(user_type)
        # Close cursor and database connection
        mycursor.close()
        mydb.close()

        return render(request, 'list_of_doctors.html', {'doctors': doctors, 'user_data': user_data})
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return HttpResponse(f"Database error: {err}")

    # return redirect('login')
    
    
    # return render(request, "list_of_doctors.html")


def add_doctors_details(request):
    return render(request, "add_doctors_details.html")


def doctor_details(request):
    user_data = request.session.get('user_data')
    if request.method == "POST":
        name = request.POST.get('doctor_name')
    
        Image_url = None
        if request.FILES.get('Profile_Picture'):
            doctor_image = request.FILES['Profile_Picture']
            fs = FileSystemStorage()
            filename = fs.save(doctor_image.name, doctor_image)
            doctor_Image_url = fs.url(filename)

        if not name:
            return HttpResponse("Name cannot be null")

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Vinay@2000",
                database="task2"
            )

            mycursor = mydb.cursor()
            
            # Prepare SQL query to insert data into the database
            sql = "INSERT INTO doctor_profile (name, doctor_Image_url) VALUES (%s, %s)"
            val = (name, doctor_Image_url)
            
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
    
    return render(request, 'add_doctors_details.html')


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
                password="Vinay@2000",
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
                password="Vinay@2000",
                database="task2"
            )

            mycursor = mydb.cursor(dictionary=True)

            if user_type == "Doctor":
                # Fetch all blog posts for doctors
                mycursor.execute("SELECT * FROM blogdetails")
                blog_posts = mycursor.fetchall()
            elif user_type == "Patient":
                # Fetch only published blog posts for patients
                mycursor.execute("SELECT * FROM blogdetails WHERE is_draft == 0")
                blog_posts = mycursor.fetchall()
            print(user_type)
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
            password="Vinay@2000",
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
                password="Vinay@2000",
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
                password="Vinay@2000",
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
