from django.db import models
from django.db.models.fields import CharField

# Create your models here.

class User(models.Model): #master Table
    Email       = models.EmailField(max_length=100)
    Password    = models.CharField(max_length=100)
    OTP         = models.IntegerField()
    Role        = models.CharField(max_length=100)
    is_created  = models.DateTimeField(auto_now_add=True)
    is_updated  = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    
class Tutor(models.Model): #Child Table
    user_id       = models.ForeignKey(User,on_delete=models.CASCADE)
    Firstname     = models.CharField(max_length=100)
    Lastname      = models.CharField(max_length=100)
    gender        = models.CharField(max_length=100)
    Contact       = models.CharField(max_length=100)
    Address       = models.CharField(max_length=100)      
    Qualification = models.CharField(max_length=100)
    Skills        = models.CharField(max_length=100)
    DOB           = models.CharField(max_length=100)
    profile_pic   = models.ImageField(upload_to="img/",default="abc.jpg")
   
    
class Student(models.Model): #Child Table
    user_id       = models.ForeignKey(User,on_delete=models.CASCADE)
    Firstname     = models.CharField(max_length=100)
    Lastname      = models.CharField(max_length=100)
    gender        = models.CharField(max_length=100)
    Contact       = models.CharField(max_length=100)
    Address       = models.CharField(max_length=100)
    profile_pic   = models.ImageField(upload_to="img/",default="abc.jpg")
    
    
class Category(models.Model):
    Cat_Name  = models.CharField(max_length=50)
    is_created  = models.DateTimeField(auto_now_add=True)
    is_updated  = models.DateTimeField(auto_now_add=True)

class Subcategory(models.Model):
    category_id     = models.ForeignKey(Category,on_delete=models.CASCADE)
    Sub_cat_name    = models.CharField(max_length=100)
    is_created  = models.DateTimeField(auto_now_add=True)
    is_updated  = models.DateTimeField(auto_now_add=True)

class Course(models.Model):
    tutor_id        = models.ForeignKey(Tutor,on_delete=models.CASCADE)
    category_id     = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory_id  = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    Course_Name     = models.CharField(max_length=100)
    Code            = models.IntegerField()
    Description     = models.CharField(max_length=250)
    Duration        = models.CharField(max_length=100)
    Price           = models.IntegerField()
    Pre_Requirement = models.CharField(max_length=100)
    Course_Pic      = models.ImageField(upload_to="img/",default="abc.jpg")
    is_created      = models.DateTimeField(auto_now_add=True)
    is_updated      = models.DateTimeField(auto_now_add=True)

class Add_Cart(models.Model):
    student_id      = models.ForeignKey(Student,on_delete=models.CASCADE)
    course_id       = models.ForeignKey(Course,on_delete=models.CASCADE)
    Course_name     = models.CharField(max_length=100)
    Course_price    = models.IntegerField()
    Total           = models.IntegerField()
    Subtotal        = models.IntegerField()
    Grandtotal      = models.IntegerField()
    is_created      = models.DateTimeField(auto_now_add=True)
    is_updated      = models.DateTimeField(auto_now_add=True)


class Wish_list(models.Model):
    student_id      = models.ForeignKey(Student,on_delete=models.CASCADE)
    course_id       = models.ForeignKey(Course,on_delete=models.CASCADE)
    is_created      = models.DateTimeField(auto_now_add=True)
    is_updated      = models.DateTimeField(auto_now_add=True)

class Check_out(models.Model):
    student_id         = models.ForeignKey(Student,on_delete=models.CASCADE)
    course_id          = models.ForeignKey(Course,on_delete=models.CASCADE)
    Student_name       = models.CharField(max_length=100)
    State              = models.CharField(max_length=100)
    City               = models.CharField(max_length=100)
    Address            = models.CharField(max_length=100)
    Pincode            = models.IntegerField()
    Phone              = models.IntegerField() 
    Course_name        = models.CharField(max_length=100)
    Course_price       = models.IntegerField()
    Total              = models.IntegerField()
    Subtotal           = models.IntegerField()
    is_created         = models.DateTimeField(auto_now_add=True)
    is_updated         = models.DateTimeField(auto_now_add=True)

class Buyer(models.Model):
    check_out_id       = models.ForeignKey(Check_out,on_delete=models.CASCADE)
    Student_name       = models.CharField(max_length=100)
    Course_name        = models.CharField(max_length=100)
    is_created         = models.DateTimeField(auto_now_add=True)
    is_updated         = models.DateTimeField(auto_now_add=True)
    
    
class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)


