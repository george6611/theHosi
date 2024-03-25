from django.urls import path
from .views import CheckAuthenticatedView,AdminUserCreate,HospitalCreate,LoginView,LogoutView,DepartmentsCreate,CreateStaff,CreatePatient,PatientDataCreate,GetUserProfileView,GetCSRFToken

urlpatterns = [
    path('authenticated', CheckAuthenticatedView.as_view()),
    path('admin_register', AdminUserCreate.as_view()),
    path('hospital_register', HospitalCreate.as_view()),
    path('login',LoginView.as_view()),
    path('logout',LogoutView.as_view()),
    path('department', DepartmentsCreate.as_view()),
    path('create_staff',CreateStaff.as_view()),
    path('create_patient', CreatePatient.as_view()),
    path('patient_data', PatientDataCreate.as_view()),
    path('admin_profile',GetUserProfileView.as_view()),
    path('csrf_cookie',GetCSRFToken.as_view()),
]