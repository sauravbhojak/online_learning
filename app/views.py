from django.http import request
from django.shortcuts import render, redirect
from django.utils.html import simple_url_2_re
from .models import *
from random import randint
from .utils import *
import socket
socket.getaddrinfo('127.0.0.1',8080)


from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum

from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def IndexPage(request):
    data = load_all_category()
    course = Course.objects.all()
    print('===============================',course)
    return render(request, "app/index.html",{'cat':data,'cor':course})


def TutorIndex(request):
    master = User.objects.get(id= request.session['id'])
    data= Tutor.objects.get(user_id=master) 
    return render(request, "app/tutor/index.html",{'key1':data  })


def StudentIndex(request):
    master = User.objects.get(id= request.session['id'])
    data = Student.objects.get(user_id=master)
    course = Course.objects.all()
    return render(request, "app/student/index-2.html",{'key1':data,'c':course})


def RegisterPage(request):
    return render(request, "app/register.html")


def LoginPage(request):
    return render(request, "app/login.html")


def Student_RegisterPage(request):
    return render(request, "app/Student_Register.html")


def Student_Login(request):
    return render(request, "app/Student_login.html")

def student_show(request):
    return render(request, "app/tutor/studentshow.html")

# def Stu_Profile(request):
#     if "Email" in request.session and "Password" in request.session:
#         return render(request, "app/student/sprofile.html")
#     else:
#         return redirect("sloginpage")

def Ourservice(request):
    return render(request,"app/service.html")   

def About_uspage(request):
    tutor = Tutor.objects.all()
    course = Course.objects.all()
    return render(request,'app/about-us.html',{'t':tutor,'c':course})


def About_uspagestudent(request):
    tutor = Tutor.objects.all()
    course = Course.objects.all()
    return render(request,'app/student/about-us.html',{'t':tutor,'c':course})


def RegisterUser(request):
    if request.POST['role'] == 'tutor':
        role = request.POST['role']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['psw']
        cpassword = request.POST['cpsw']

        # for check in database email are register or not using filter.
        user = User.objects.filter(Email=email)
        if user:
            message = "User Already Register!"
            return render(request, "app/login.html",{'msg':message})
        else:
            if password == cpassword:
                otp = randint(100000, 999999)
                newuser = User.objects.create(
                    Email=email, Password=password, OTP=otp, Role=role)
                newtutor = Tutor.objects.create(
                    user_id=newuser, Firstname=fname, Lastname=lname)
                email_subject = "Tutor Finder : Account Verification"
                sendmail(email_subject,'mail_template',email,{"name":fname,'otp':otp,'link':'http://localhost:8000/enterprise/user_verify/'})
                    
                return redirect("loginpage")
            else:
                message = "Password & Confirm Password do not match"
                return render(request, "app/register.html", {'msg': message})
    else:
        if request.POST['role'] == 'student':
            role = request.POST['role']
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['psw']
            cpassword = request.POST['cpsw']

            user = User.objects.filter(Email=email)
            if user:
                message = "User Already Exist"
                return render(request, "app/login.html",{'msg':message})
            else:
                if password == cpassword:
                    otp = randint(100000, 999999)
                    newuser = User.objects.create(
                        Email=email, Password=password, OTP=otp, Role=role)
                    newstudent = Student.objects.create(
                        user_id=newuser, Firstname=fname, Lastname=lname)
                    email_subject = "Student Finder : Account Verification"
                    sendmail(email_subject,'mail_template',email,{"name":fname,'otp':otp,'link':'http://localhost:8000/enterprise/user_verify/'})
                    
                    return redirect("loginpage")
                else:
                    message = "Password & Confirm Password do not match"
                    return render(request, "app/Student_Register.html", {'msg': message})


def LoginUser(request):
    email = request.POST['email']
    password = request.POST['password']

    try:
        user = User.objects.get(Email=email) #master table data get
        print('------------------------------',user.Email, user.Role)

        if user.Password == password:
            print('-------------------------------------Pssword is match')

            request.session['id']=user.id
            request.session['Email'] = user.Email
            request.session['Password'] = user.Password
            
            
            if user.Role=='tutor':
                kpp=request.session['role'] = user.Role
                tdata = Tutor.objects.get(user_id=user)

                request.session['FirstName'] = tdata.Firstname
                request.session['LastName'] = tdata.Lastname
                print('-------------------------------my role',kpp)
                return redirect(TutorIndex)

            else:
                user.Role=='student'
                print('==================================elseeeeeeeeeeeee')
                sdata  = Student.objects.get(user_id=user)
                request.session['role'] = 'student'
                request.session['FirstName'] = sdata.Firstname
                request.session['LastName'] = sdata.Lastname
                return redirect(StudentIndex)

        else:
            message = "password does not match"
            return render(request,"app/login.html",{'msg':message})
    except Exception as e:
        print('------------------------------ exception handling ')
        return render(request,"app/register.html")

def Forgotpasspage(request):
    return render(request,"app/Forgotpass.html")

def Forgotpass(request):
    email = request.POST['email']
    user = User.objects.filter(Email=email)
    
    if user:
        master= User.objects.get(Email=email)

        email_subject = "Your OTP is : "
        master.OTP=randint(100000, 999999)
        print('--------------------------------',master.OTP)
        master.save()
        request.session['email']=email
        sendmail(email_subject,'mail_template',email,{'otp':master.OTP,'link':'http://localhost:8000/enterprise/user_verify/'})
        return render(request,'app/otp.html')
    else:
        m = 'Email is not valid'
        return render(request,'app/Forgotpass.html',{'M':m})
        
def Forgotpassindex(request):
    return render(request,'app/otp.html')       
        
def OTP_match(request):
    master = User.objects.get(Email=request.session['email'])

    otp=int(request.POST['otp'])
    if master.OTP==otp:
        return render(request,'app/changepass.html')
    else:
        msg = 'OTP not match'
        return render(request,'app/otp.html',{'key1':msg})

def Passmatch(request):
    master = User.objects.get(Email=request.session['email'])
    psd= request.POST['psd']
    cpsd= request.POST['cpsd']

    if psd==cpsd:
        master.Password=psd
        master.save()
        request.session.clear()
        return redirect(LoginPage)




def TutorProfile(request, pk):
    if "Email" in request.session and "Password" in request.session:
        udata = User.objects.get(id=pk)
        print('--------------------------------',udata.Role)
        if udata.Role == "tutor":
            tdata = Tutor.objects.get(user_id=udata)
            return render(request, "app/tutor/profile.html", {'key1': tdata})
    else:
        return redirect("loginpage")


def StudentProfile(request):
    if "Email" in request.session and "Password" in request.session:
        print('888888888888888888')
        udata = User.objects.get(id=request.session['id'])
        print('888888888888888888')
        print(udata.id)
        print(request.session['role'])
        if  request.session['role'] == "student":
            print('44444444444444444') 
            sdata = Student.objects.get(user_id=udata.id)
            print('888888888888888888') 
            return render(request, "app/student/sprofile.html", {'key1': sdata})
    else:
        return redirect("sloginpage")



def UpdateTutorProfile(request, pk):
    if "Email" in request.session and "Password" in request.session:
        udata = User.objects.get(id=pk)
        if udata.Role == "tutor":
            tdata = Tutor.objects.get(user_id=udata)
            tdata.Firstname = request.POST['fname']
            tdata.Lastname = request.POST['lname']
            tdata.gender = request.POST['gender']
            tdata.Contact = request.POST['contact']
            tdata.Address = request.POST['address']
            tdata.Qualification = request.POST['Qualification']
            tdata.Skills = request.POST['skills']
            tdata.DOB = request.POST['dob']
            tdata.profile_pic = request.FILES['profilepic']
            tdata.save()
            url = f"/tutorprofile/{pk}"
            return redirect(url)
            
    else:
        return redirect("loginpage")


def UpdateStudentProfile(request, pk):
    if "Email" in request.session and "Password" in request.session:
        udata = User.objects.get(id=pk)
        if udata.Role == "student":
            sdata = Student.objects.get(user_id=udata)
            sdata.Firstname = request.POST['fname']
            sdata.Lastname = request.POST['lname']
            sdata.gender = request.POST['gender']
            sdata.Contact = request.POST['contact']
            sdata.Address = request.POST['address']
            sdata.profile_pic = request.FILES['profilepic']
            sdata.save()
            #url = f"/studentprofile/{pk}"
            #return redirect(url)
            return render(request, "app/student/sprofile.html", {'key1': sdata})
    else:
        return redirect("sloginpage ")
        
        
    
def TutorLogout(request):
    del request.session['Email']
    del request.session['Password']
    return redirect("loginpage")

def StudentLogout(request):
    del request.session['Email']
    del request.session['Password']
    return redirect(LoginPage)


def TutorAlldata(request):
    if 'username' in request.session and 'password' in request.session:
        tutor_data = Tutor.objects.all()
        return render(request,"app/admin/tutordata.html",{'tutordata':tutor_data})
    else:
        return redirect("loginpage")

def StudenAllData(request):
    if 'username' in request.session and 'password' in request.session:
        tutor_data = Student.objects.all()
        return render(request,"app/admin/studentdata.html",{'studentdata':tutor_data})
    else:
        return redirect("sloginpage")


####################################ADMIN PART#########################################

def AdminLoginPage(request):
    return render(request,"app/admin/login.html")

def AddCatPage(request):
    if "username" in request.session and "password" in request.session:
        return render(request,"app/admin/addCat.html")
    else:
        return redirect("adminloginpage")

def AdminIndexPage(request):
    if 'username' in request.session and 'password' in request.session:
        return render(request,"app/admin/index.html")
    else:
        return redirect("adminloginpage")

def AdminLogin(request):
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            
            if username == "admin" and password == "admin":
                request.session['username']  = username
                request.session['password']  = password
                return redirect("adminindex")
            else:
                message = "Username & Password Doesnot Match"
                return render(request,"app/admin/login.html",{'msg':message})
     
def AdminLogout(request):
    del request.session['username']
    del request.session['password']
    return redirect("adminloginpage")

def AdminshowCourse(request):
    if 'username' in request.session and 'password' in request.session:
        course_data = Course.objects.all() 
        return render(request,"app/admin/showcourse.html",{'course':course_data})
    else:
        return redirect('adminloginpage')


####################################CATEGORY PART#########################################
        
def Insertcat(request):
    if 'username' in request.session and 'password' in request.session:
        catname    = request.POST['catname']
        existcat   = Category.objects.filter(Cat_Name=catname) 
        if existcat:
            msg = "Category Allready Exist"
            return render(request,"app/admin/addCat.html",{'msg':msg})
        else:                                
            newcat   = Category.objects.create(Cat_Name=catname)
            return redirect('catlist')
    else:
        return redirect("adminloginpage")
    
def CatList(request):
    if 'username' in request.session and 'password' in request.session:
        cat_data = Category.objects.all()
        return render(request,"app/admin/catlist.html",{'key1':cat_data})
    else:
        return redirect("adminloginpage")

def Editcatpage(request,pk):
    if 'username' in request.session and 'password' in request.session:
        edata = Category.objects.get(id=pk)
        return render(request,"app/admin/cat_edit.html",{'key2':edata})
    else:
        return redirect("adminloginpage")

def Updatecatdata(request,pk):
    if 'username' in request.session and 'password' in request.session:
        udata = Category.objects.get(id=pk)
        udata.Cat_Name = request.POST['catname']
        udata.save()
        return redirect('catlist')
    else:
        return redirect("adminloginpage")
    
def Deletecatdata(request,pk):
    if 'username' in request.session and 'password' in request.session:
        ddata = Category.objects.get(id=pk)
        ddata.delete()
        return redirect('catlist')
    else:
        return redirect("adminloginpage")


########################################### SUB CATEGORY ##########################################

def Subcatpage(request):
    if 'username' in request.session and 'password' in request.session:
        cat_data = Category.objects.all()
        return render(request,"app/admin/subcategories.html",{'cdata':cat_data})

def Insertsubcat(request):
    if 'username' in request.session and 'password' in request.session:
        subcatname = request.POST['subcatname']
        cdata = Category.objects.get(id=request.POST['catid'])
        
        if  Subcategory.objects.filter(Sub_cat_name=subcatname):
            msg= 'Sub category is already exist'
            cdataa= Category.objects.all()
            return render(request,"app/admin/subcategories.html",{'msg':msg,'cdata':cdataa})
            
        else:
            subcat= Subcategory.objects.create(Sub_cat_name=subcatname, category_id=cdata)
            return redirect(AdminIndexPage)
    else:
        return redirect("adminloginpage")

def Subcatlist(request,pk):
    if 'username' in request.session and 'password' in request.session:
        cdata= Category.objects.get(id=pk)
        print('-----------------------------------pk',pk)
        print('-----------------------------------cdata',cdata)
        sdata= Subcategory.objects.all().filter(category_id=cdata)
        print('-----------------------------------cdata',cdata)
        return render(request,"app/admin/subcatlist.html",{'sdata':sdata})
    else:
        return redirect('loginpage')

def Subcatedit(request,pk):
    if 'username' in request.session and 'password' in request.session:
        esubcatdata = Subcategory.objects.get(id=pk)
        return render(request,"app/admin/edit_subcat.html",{'key1':esubcatdata})
    else:
        return redirect("adminloginpage")

def Subcatupdate(request,pk):
    if 'username' in request.session and 'password' in request.session:
        udata = Subcategory.objects.get(id=pk)
        udata.Sub_cat_name = request.POST['subcatname']
        udata.save()
        pkk=udata.category_id.id
        print('----------------------------------------',pkk)
        url= f'/subcatlist/{pkk}'
        return redirect(url)
    else:
        return redirect("adminloginpage")

def Subcatdelete(request,pk):
    if 'username' in request.session and 'password' in request.session:
        ddata = Subcategory.objects.get(id=pk)
        ddata.delete()
        return redirect('subcatlist')
    else:
        return redirect("adminloginpage")

def load_all_category():
    cat_data   = Category.objects.all()
    cat_list = []

    for cd in cat_data:
        sub_cat = Subcategory.objects.filter(category_id=cd)[::-1]
        for i in sub_cat:
            course = Course.objects.filter(subcategory_id=i)
            print('------------------------------>>>>>>>>>>>>>>..>>>')
            print(course)
            cat_list.append({'category':cd,'sub_cat':sub_cat,'c':course})
    print('********************************8')
    print(cat_list) 
    return cat_list

def load_all_course(request,pk):
    #c_data = Category.objects.all()
    print('888888888888888888888888888')
    print(pk)
    sub = Subcategory.objects.filter(category_id=pk)   
    for i in sub:
        course = Course.objects.filter(subcategory_id=i)
    #courses = Course.objects.all().filter(subcategory_id=sub)

        return render(request,'app/filtercourse.html',{'k':course})

####################################   Course Part  #########################################

def AddCoursePage(request):
    if "Email" in request.session and "Password" in request.session:
        all_data = Category.objects.all()
        return render(request,"app/tutor/addcourse.html",{'category':all_data})
    else:
        return redirect("loginpage")

def Send_Subcategory(request):
    cid= request.POST['cid']
    request.session['cid'] = cid
    print('-----------------------------------ciddd  gateddd',cid)
    cdata= Subcategory.objects.all().filter(category_id = cid)
    return render(request,"app/tutor/addcourse.html",{'subcat':cdata})

def Tutorcatlist(request):
    if "Email" in request.session and "Password" in request.session:
        all_data = Category.objects.all()
        return render(request,"app/tutor/addcourse.html",{'category':all_data})
    else:
        return redirect("loginpage")
    
    
def InsertCourse(request):
    if "Email" in request.session and "Password" in request.session:

        ddata             = Subcategory.objects.get(id=request.POST['sid'])
        c_data            = Category.objects.get(id=request.session['cid'])
        

        uid               = request.session['id']
        TTid              = Tutor.objects.get(user_id=uid)
        coursename        = request.POST['coursename']
        Code              = request.POST['code']
        Description       = request.POST['description']
        Duration          = request.POST['duration']
        Price             = request.POST['price']
        Pre_Requirement   = request.POST['pre_requirement']
        Course_Pic        = request.FILES['course_pic']
    
        print('=======================================================')
        
        course_exist      = Course.objects.filter(Course_Name=coursename) 
        
        if course_exist:
            msg = "Category Allready Exist"
            return render(request,"app/tutor/addcourse.html",{'msg':msg})
        else:                                
            new_course   = Course.objects.create(
                tutor_id=TTid,
                category_id=c_data,
                subcategory_id=ddata,
                Course_Name=coursename,
                Code=Code,
                Description=Description,
                Price=Price,
                Duration=Duration,
                Pre_Requirement=Pre_Requirement,
                Course_Pic=Course_Pic)
            return redirect('courselist')
    else:
        return redirect("loginpage")
    
def Courselist(request):
    if 'Email' in request.session and 'Password' in request.session:
        master = User.objects.get(id = request.session['id'])
        user= Tutor.objects.get(user_id=master)
        
        course_data = Course.objects.all().filter(tutor_id=user) 
        return render(request,"app/tutor/Courselist.html",{'catdata':course_data})
    else:
        return redirect('loginpage')
    

def CourseEdit(request,pk):
    if 'Email' in request.session and 'Password' in request.session:
        edata = Course.objects.get(id=pk)
        return render(request,"app/tutor/Course_edit.html",{'key2':edata})
    else:
        return redirect("loginpage")
    
def CourseUpdate(request,pk):
    if 'Email' in request.session and 'Password' in request.session:
        udata = Course.objects.get(id=pk)
        udata.Course_Name       = request.POST['coursename']
        udata.Code              = request.POST['code']
        udata.Description       = request.POST['description']
        udata.Duration          = request.POST['duration']
        udata.Price             = request.POST['price']
        udata.Pre_Requirement   = request.POST['pre_requirement']
        
        if 'course_pic' in request.FILES:
          udata.Course_Pic        = request.FILES['course_pic']
          
        udata.save()
        return redirect('courselist')
    else:
        return redirect("loginpage")
    
    
def CourseDelete(request,pk):
    if 'Email' in request.session and 'Password' in request.session:
        ddata = Course.objects.get(id=pk)
        ddata.delete()
        return redirect('courselist')
    else: 
        return redirect("loginpage")

# def buyer(request):
#     if 'Email' in request.session and 'Password' in request.session:
#         user  = User.objects.get(id=request.session['id'])
#         tdata = Tutor.objects.get(user_id=user)

#         chk = Check_out.objects.all().filter(id=course)

#         newbuy = Buyer.objects.create(
#             check_out_id=chk,
#             Student_name=chk.Student_name,
#             Course_name=chk.course_id.Course_name,

#         )
#         print('----------------------------------',newbuy)
#         return render(request,"app/tutor/studentshow.html",{'buy':newbuy})

def buyer(request):
    if 'Email' in request.session and 'Password' in request.session:
        user  = User.objects.get(id=request.session['id'])
        tdata = Tutor.objects.get(user_id=user)

        cdata = Course.objects.filter(tutor_id = tdata).all()

        print(cdata)
        return render(request,'app/tutor/index.html')




   

####################################   Student Show Course  #########################################

def ShowCourse(request):
    course_data = Course.objects.all() 
    return render(request,"app/shop-grid.html",{'course':course_data})

def ShowCourses(request):
    course_data = Course.objects.all() 
    return render(request,"app/student/courses.html",{'course':course_data})

def SingleCourse(request,pk):
    s_course = Course.objects.get(id=pk) 
    return render(request,"app/shop-single.html",{'single':s_course})

####################################  Add to cart  #####################################

def Addtocart(request,pk):
    if 'Email' in request.session and 'Password' in request.session:

        master = User.objects.get(id = request.session['id'])
        user= Student.objects.get(user_id=master)
        
        c_data = Course.objects.get(id=pk)
        total = int(c_data.Price*1)
        if Add_Cart.objects.filter(Course_name=c_data.Course_Name):
            return redirect('studentindex')
        else:
            addtocart = Add_Cart.objects.create(
            student_id=user,
            course_id=c_data,
            Course_name=c_data.Course_Name,
            Course_price=c_data.Price,
            Total=total,    
            Subtotal=total,
            Grandtotal=total+200
            )
            return redirect(View_Cart)
    else:
        return redirect(IndexPage)

def View_Cart(request):
    if 'Email' in request.session and 'Password' in request.session:

        master = User.objects.get(id = request.session['id'])
        user= Student.objects.get(user_id=master)
        cdata= Add_Cart.objects.all().filter(student_id=user)
        print('------------------------------cdata',)
        return render(request,'app/cart.html',{'cdata':cdata})

    else:
        return redirect('loginpage')

def Cartdelete(request,pk):
    if 'Email' in request.session and 'Password' in request.session:

        ddata = Add_Cart.objects.get(id=pk)
        ddata.delete()

        return redirect(View_Cart)

    else:
        return redirect('loginpage')

def Add_Wish_List(request,pk):
    if 'Email' in request.session and 'Password' in request.session:
        master = User.objects.get(id = request.session['id'])
        user= Student.objects.get(user_id=master)

        c_data = Course.objects.get(id=pk)
        Wish_list.objects.create(course_id = c_data,student_id=user)
        return redirect(ShowCourse)

    else:
        return redirect('loginpage')

def Add_Wish_Lists(request,pk):
    if 'Email' in request.session and 'Password' in request.session:
        master = User.objects.get(id = request.session['id'])
        user= Student.objects.get(user_id=master)

        c_data = Course.objects.get(id=pk)
        Wish_list.objects.create(course_id = c_data,student_id=user)
        return render(request,'app/student/courses.html')

    else:
        return redirect('loginpage')

def view_wlist(request):
    if 'Email' in request.session and 'Password' in request.session:

        master = User.objects.get(id = request.session['id'])
        user= Student.objects.get(user_id=master)
        wdata= Wish_list.objects.all().filter(student_id=user)
        return render(request,'app/wishlist.html',{'Wdata':wdata})

    else:
        return redirect('loginpage')

def view_wlists(request):
    if 'Email' in request.session and 'Password' in request.session:

        master = User.objects.get(id = request.session['id'])
        user= Student.objects.get(user_id=master)
        wdata= Wish_list.objects.all().filter(student_id=user)
        return render(request,'app/student/wishlists.html',{'Wdata':wdata})

    else:
        return redirect('loginpage')

def Delete_Wlist(request,pk):
    if 'Email' in request.session and 'Password' in request.session:

        wdata = Wish_list.objects.get(id=pk)
        wdata.delete()

        return redirect(view_wlist)
    else:
        return redirect('loginpage') 

######################################  BUY NOW  ###########################################

def Checkout_data(request,pk):
    if "Email" in request.session and "Password" in request.session:
        master = User.objects.get(id=request.session['id'])
        user   = Student.objects.get(user_id=master)
        codata = Course.objects.get(id=pk)

        return render(request,'app/checkout.html',{'course':codata})
    else:
        return redirect('loginpage')


############################################# Paytm Block #################################################

def initiate_payment(request,pk):
    if 'Email' in request.session and 'Password' in request.session:
        try:
            udata = User.objects.get(Email=request.session['Email'])
            
            #user = authenticate(request, username=username, password=password)
            
            master = User.objects.get(id=request.session['id'])
            user   = Student.objects.get(user_id=master)
            buycourse = Course.objects.get(id=pk)
            amount= int(buycourse.Price)
            print('-----------------------------data Gated',amount)
            state = request.POST['state']
            name = request.POST['name']
            city = request.POST['city']
            add = request.POST['add']
            pincode = request.POST['pincode']
            phone = request.POST['phone']
            print('-----------------------------Input implated')
            bdata = Check_out.objects.create(
                student_id=user,
                course_id=buycourse,
                Student_name=name,
                State=state,
                City=city,
                Address=add,
                Pincode=pincode,
                Course_name=buycourse.Course_Name,
                Total=amount,
                Subtotal=amount,
                Course_price=amount,
                Phone=phone)
        except Exception as err:
            print('-----------------------------------------error',err)
            return render(request, 'app/checkout.html', context={'error': 'Wrong Accound Details or amount'})

        transaction = Transaction.objects.create(made_by=udata, amount=amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.Email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'app/redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'app/callback.html', context=received_data)
        return render(request, 'app/callback.html', context=received_data)

def student_show_buy(request):

    if 'Email' in request.session and 'Password' in request.session:

        admin  = User.objects.get(id=request.session['id'])
        t_id   = Tutor.objects.get(user_id=admin)
        course = Course.objects.filter(tutor_id=t_id)
        data = []
        val = []
        for i in course:
            #data.append(i.Course_Name)
            v = Check_out.objects.filter(course_id=i)
            for j in v:
                data.append(i.Course_Name)
                print(val.append(j))

        print('*******************')
        print(data)
        print(val)
        return render(request,'app/tutor/studentshow.html',{'course':data,'value':val})
     
    else:
        return redirect('loginpage')

    # if 'Email' in request.session and 'Password' in request.session:
    #     user  = User.objects.get(id=request.session['id'])
    #     print('************************')
    #     print(user)
    #     tdata = Tutor.objects.get(user_id=user.id)
        
    #     cdata = Course.objects.filter(tutor_id = tdata).all()
    #     print('----------------------------------')
    #     print(cdata)
    #     cda=[]
    #     student = []
    #     for i in cdata:
    #         cda.append(Check_out.objects.filter(course_id = i).all())
    #         mm = Check_out.objects.filter(course_id = i).all()
    #         print(mm)
    #         for j in mm:
    #             st = Student.objects.filter(id=j.student_id_id) 
    #             print('£££££££££££££££££££££££££££££££££££££££')
    #             print(st)
    #             print(mm)
    #             try:
    #                 for i in st:    
    #                     student.append(i)
    #             except:
    #                 pass

    #     print('****************')
    #     print(cda)
    #     print(student)
    #     return render(request,'app/tutor/studentshow.html',{'key':cda ,'s':student})



         








