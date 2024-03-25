from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class AdminUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50,default='')
    sur_name = models.CharField(max_length=50,default='')
    email = models.EmailField(unique =True,default='')
    password = models.CharField(max_length=255, default='')
    phone_number = models.CharField(max_length=12,default='')
    date_joined = models.DateTimeField(auto_now_add=True)
    hospital_name = models.CharField(max_length=50,default='')
    admin_type =  models.CharField(max_length=50,default='')
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name} {self.sur_name}  {self.user_type} {self.phone_number}"
 
class Hospital(models.Model):
    admin_user = models.OneToOneField(AdminUser,on_delete=models.DO_NOTHING)
    hospital_name = models.CharField(max_length=50)
    hospital_reg = models.CharField(max_length=50)
    hospital_email = models.EmailField(unique=True)
    hospital_phone_number = models.CharField(max_length=12)
    hospital_phone_number_2 = models.CharField(max_length=12)
    hospital_phone_number_3 = models.CharField(max_length=12)
    physical_address = models.CharField(max_length=12)

class Departments(models.Model):
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE)
    department_name = models.CharField(max_length=50)
    description = models.TextField()
    in_charge = models.CharField(max_length=50)

class Staff(AbstractBaseUser):
    first_name = models.CharField(max_length=50,default='') 
    last_name =  models.CharField(max_length=50,default='')
    sur_name = models.CharField(max_length=50,default='')
    email = models.EmailField(unique=True)  
    phone_number = models.CharField(max_length=50,default='')
    profession = models.CharField(max_length=50,default='')
    position = models.CharField(max_length=50,default='')
    date_of_start = models.DateTimeField(auto_now_add=True)
    date_ended = models.CharField(max_length=50, default='')
    is_staff_active = models.BooleanField(default=False)
    department = models.CharField(max_length=50, default='')
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
  
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the object is being created for the first time
            self.is_staff_active = True  # Set is_staff_active to True when staff is created
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name} {self.sur_name}  {self.user_type} {self.phone_number}"

    
class Patient(AbstractBaseUser):
    first_name = models.CharField(max_length=50, default='') 
    last_name = models.CharField(max_length=50, default='') 
    sur_name = models.CharField(max_length=50, default='') 
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50, default='') 
    physical_address = models.CharField(max_length=50, default='') 
    hospital_registered = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name} {self.sur_name}  {self.user_type} {self.phone_number}"


class PatientData(models.Model):
    DATA_TYPES = [
        ('History', 'History'),
        ('Diagnosis', 'Diagnosis'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE) 
    data = models.TextField(max_length=50, default='') 
    data_type = models.CharField(max_length=50, choices=DATA_TYPES)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    medic_author = models.CharField(max_length=50)
    record_officer = models.CharField(max_length=50)
    date_of_entry = models.DateTimeField(auto_now_add=True) 

class History(models.Model):
    patient_data = models.ForeignKey(PatientData, on_delete=models.CASCADE)

class FamilyHistory(models.Model):
    history = models.ForeignKey(History, on_delete=models.CASCADE)
    relative = models.CharField(max_length=50)
    disease = models.CharField(max_length=50)
    disease_status = models.BooleanField(True)
    relative_status = models.BooleanField(True)
    time_of_diagnosis = models.DateField()
    kind_of_treatment = models.TextField()

class SocialHistory(models.Model):
    history = models.ForeignKey(History, on_delete=models.CASCADE)    
    drinking_habit = models.CharField(max_length=50)
    smoking_habit = models.CharField(max_length=50)
    other_drugs = models.CharField(max_length=50)
    eating_habits = models.TextField()
    others = models.TextField()

class HealthHistory(models.Model):
    history = models.ForeignKey(History, on_delete=models.CASCADE)
    surgery = models.CharField(max_length=50)  
    surgery_status = models.CharField(max_length=50) 
    disease = models.CharField(max_length=50)  
    disease_status = models.CharField(max_length=50) 
    chronic_illness = models.CharField(max_length=50) 
    terminal_illness = models.CharField(max_length=50) 
    period = models.CharField(max_length=50) 
