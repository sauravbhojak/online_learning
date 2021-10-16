
from django.urls import path,include
from .import views
urlpatterns = [
   path("",views.IndexPage,name="indexpage"),
   path("registerpage/",views.RegisterPage,name="registerpage"),            #Redirect register page href on click event
   path("loginpage/",views.LoginPage,name="loginpage"),                     #Tutor login page
   path("register/",views.RegisterUser,name="register"),                    #Tata insert tutor & student     
   path("sloginpage/",views.Student_Login,name="sloginpage"),               #Student login page
   path("sregisterpage/",views.Student_RegisterPage,name="sregisterpage"),  #Redirect register page href on click event
   path("loginuser/",views.LoginUser,name="loginuser"),                     #Login user with session create
   path('aboutuspage/',views.About_uspage,name='aboutuspage'),
   path('aboutuspages/',views.About_uspagestudent,name='aboutuspages'),
   path('ourservise',views.Ourservice,name='ourservise'),
  
   
   
   
   ####################################TUTORS URLS#########################################
   
   
   
   path("tutorindex/",views.TutorIndex,name="tutorindex"),                             #After tutor login page
   path("tutorprofile/<int:pk>",views.TutorProfile,name="tutorprofile"),               #Tutor profile page
   path("updatetutorprofile/<int:pk>",views.UpdateTutorProfile,name="updatetprofile"), #Tutor profile updation query
   path("tutorlogout/",views.TutorLogout,name="tutorlogout"),                          #Logout 
   path("forgotpasspage/",views.Forgotpasspage,name="forgotpasspage"),                 #forgotpassword
   path("otppage/",views.Forgotpassindex,name="otppage"),
   path("forgotpass/",views.Forgotpass,name="forgotpass"),
   path("otpmatch/",views.OTP_match,name="otpmatch"),
   path('pass_match/',views.Passmatch,name='pass_match'),
   path('studentshow/',views.student_show,name='studentshow'),

   
   ####################################STUDENT URLS#########################################
   
   path("studentindex/",views.StudentIndex,name="studentindex"),                           #After student login page
   path("studentprofile/",views.StudentProfile,name="studentprofile"),                     #Student profile page
   path("updatestudentprofile/<int:pk>",views.UpdateStudentProfile,name="updatettprofile"),#Studnet profile updation query
   path("studentlogout/",views.StudentLogout,name="studentlogout"),                        #Logout 



  ####################################ADMIN URLS############################################
  
  
  
  path("adminloginpage/",views.AdminLoginPage,name="adminloginpage"),   #AdminLoginPage
  path("adminlogin/",views.AdminLogin,name="adminlogin"),               #Admindata validaions check
  path("adminindex/",views.AdminIndexPage,name="adminindex"),           #After Adminlogin indexpage
  path("adminlogout/",views.AdminLogout,name="adminlogout"),            #Logout 

  ##################################  Categorise  ############################

  path("addcatpage/",views.AddCatPage,name="addcatpage"),               #Category page 
  path("insertcat",views.Insertcat,name="insertcat"),                   #Category Insert
  path("catlist/",views.CatList,name="catlist"),                        #Category datashow
  path("catedit/<int:pk>",views.Editcatpage,name="catedit"),            #Edit  Catpage
  path("catupdate/<int:pk>",views.Updatecatdata,name="catupdate"),      #Update Catdata
  path("catdelete/<int:pk>",views.Deletecatdata,name="catdelete"),      #delete Catedata

  ###################################################

  path("tutordata/",views.TutorAlldata,name="tutordata"),
  path("studentdata/",views.StudenAllData,name="studentdata"),
  path("adminshowcourse/",views.AdminshowCourse,name="adminshowcourse"),



  ################################  Subcaterise  ###############################

  path("subcatpage/",views.Subcatpage,name="subcatpage"),
  path('addsubcat/',views.Insertsubcat,name='addsubcat'),
  path("subcatlist/<int:pk>",views.Subcatlist,name="subcatlist"),
  path("subcatedit/<int:pk>",views.Subcatedit,name="subcatedit"),
  path("subcatupdate/<int:pk>",views.Subcatupdate,name="subcatupdate"),
  path("subcatdelelte/<int:pk>",views.Subcatdelete,name="subcatdelelte"),
   
   
   
  ####################################COURSE URLS############################################
  
  
  path("addcoursepage/",views.AddCoursePage,name="addcoursepage"),
  path("insertcourse/",views.InsertCourse,name="insertcourse"),
  path("courselist/",views.Courselist,name="courselist"),
  path("coursedit/<int:pk>",views.CourseEdit,name="coursedit"),  
  path("courseupdate/<int:pk>",views.CourseUpdate,name="courseupdate"),
  path("coursedelete/<int:pk>",views.CourseDelete,name="coursedelete"),
  path("showcoursedata/",views.ShowCourse,name="showcoursedata"),
  path("showcoursedat/",views.ShowCourses,name="showcoursedat"),
  path("singlecoursepage/<int:pk>",views.SingleCourse,name="singlecoursepage"),
  path("sendcat/",views.Send_Subcategory,name="sendcat"),
  path('allcourse/<int:pk>',views.load_all_course,name='allcourse'),
 


  ###################################  ADD to cart  ####################################


 path("Addcart/<int:pk>",views.Addtocart,name="Addcart"),
 path('cart_view/',views.View_Cart,name='cart_view'),
 path('delcart/<int:pk>',views.Cartdelete,name='delcart'),
 path('wishlist/<int:pk>',views.Add_Wish_List,name='wishlist'),
 path('viewWlist/',views.view_wlist,name='viewWlist'),
 path('wishlists/<int:pk>',views.Add_Wish_Lists,name='wishlists'),
 path('viewWlists/',views.view_wlists,name='viewWlists'),
 path('deletewlist<int:pk>/',views.Delete_Wlist,name='deletewlist'),

 #########################################  BUY NOW  ###################################

 path("checkpage/<int:pk>",views.Checkout_data,name="checkpage"),
 path("buylist/",views.student_show_buy,name="buylist"),
 path("buy<int:pk>/",views.buyer,name="buy"),

 ######################################################## Paytm URLS #########################3

 path('pay/<int:pk>',views.initiate_payment, name='pay'),
 path('callback/', views.callback, name='callback'),

]
