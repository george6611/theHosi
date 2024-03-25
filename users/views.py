from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib import auth
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator

from .models import AdminUser, Hospital , Departments,Staff, Patient, PatientData, History, FamilyHistory, SocialHistory, HealthHistory
from .serializers import UserProfileSerializer

class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user
        try:    
            isAuthenticated = user.is_authenticated

            if isAuthenticated:
                return Response({'isAuthenticated':'success'})
            else:
                return Response({'isAuthenticated':'error'})
        except:
            return Response({'error':'Something wrong when checking authentication status'})    


@method_decorator(csrf_protect, name='dispatch')
class AdminUserCreate(APIView):
    permission_classes =(permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        first_name = data['first_name']
        last_name = data['last_name']
        sur_name = data['sur_name']
        email = data['email']
        password = data['password']
        phone_number = data['phone_number']
        hospital_name = data['hospital_name']
        admin_type =  data['admin_type']

        
        if AdminUser.objects.filter(email=email).exists():
            return Response({'error':'Admin or Email already Exists'})
        elif Hospital.objects.filter(hospital_name=hospital_name).exists():
            # if Hospital.objects.get(hospital_name.admin_user):
                return Response({'error': hospital_name +' exists and has an admin'})
        else:
            user = AdminUser.objects.create_user(first_name=first_name, last_name=last_name,sur_name=sur_name,email=email,password=password,
                                                phone_number=phone_number, hospital_name=hospital_name,admin_type=admin_type)    
            return Response({'success':'Admin User Created succefully'})

class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        email = data['email']
        password = data['password']

        if not email or not password:
            return Response({'error':'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = AdminUser.objects.get(email=email)

            if not user.password:
                user.set_password(password)
                user.save()
            authenticated_user = auth.authenticate(email=email, password=password)

            if user is not None:
                auth.login(request, user)
                return Response({'success':'User Logged in'})
            else:
                return Response({'error':'Error when Authenticating'}) 
        except:
            return Response({'error':'Sorry  Login you in'})    

class LogoutView(APIView):
    def post(self, request, format=None):
        try:
           auth.logout(request)
           return Response({'success':'Logged Out'})
        except:
            return Response({'error':'SSomething went wrong when logging out'})  


@method_decorator(csrf_protect, name='dispatch')
class HospitalCreate(APIView):
    permission_classes =(permissions.AllowAny, )

    def post(self, request, format=None):
        data = request.data

        required_fields = ['hospital_name', 'hospital_reg', 'hospital_email', 'hospital_phone_number', 'physical_address']
        for field in required_fields:
            if field not in data:
                return Response({'error': f"Missing required field: {field}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            admin_user_id = data.get('admin_user_id')  # Assuming you provide admin_user_id in your request data
            if not admin_user_id:
                return Response({'error': 'Admin user ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            admin_user = AdminUser.objects.get(pk=admin_user_id)
            
            hospital = Hospital.objects.create(
                admin_user=admin_user,
                hospital_name=data['hospital_name'],
                hospital_reg=data['hospital_reg'],
                hospital_email=data['hospital_email'],
                hospital_phone_number=data['hospital_phone_number'],
                hospital_phone_number_2=data.get('hospital_phone_number_2', ''),  # Optional field
                hospital_phone_number_3=data.get('hospital_phone_number_3', ''),  # Optional field
                physical_address=data['physical_address']
            )
            return Response({'success': 'Hospital created successfully'}, status=status.HTTP_201_CREATED)
        except AdminUser.DoesNotExist:
            return Response({'error': 'Admin user not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_protect, name='dispatch')
class DepartmentsCreate(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        data = self.request.data
        
        admin_user = request.user

        hospital_name = admin_user.hospital_name
        # print(hospital_name)
        hosi = Hospital.objects.get(hospital_name=hospital_name)
        
        hospital_id  = hosi.id
        print(hospital_id)
        department_name = data['department_name']
        description = data['description']
        in_charge = data['in_charge']

        if Departments.objects.filter(hospital=hospital_id, department_name=department_name).exists():
                return Response({'error':'Department already exists'})
        else :
            deptartment = Departments.objects.create(hospital=hosi,department_name=department_name,description=description,in_charge=in_charge)
            return Response({'success':department_name + ' Department created successfully'})    


@method_decorator(csrf_protect, name='dispatch')
class CreateStaff(APIView):
     permission_classes = (permissions.IsAuthenticated, )

     def post(self, request, format=None):
        data = self.request.data

        first_name = data['first_name']
        last_name = data['last_name']
        sur_name = data['sur_name']
        email = data['email']
        password = data['password']
        phone_number = data['phone_number']
        profession = data['profession']
        position = data['position']
        date_ended = data['date_ended']
        department = data['department'] 
        
        if Staff.objects.filter(email=email).exists():
            return Response({'error':'Staff or Email already Exists'})
        else:
            user = Staff.objects.create_user(first_name=first_name, last_name=last_name,sur_name=sur_name,email=email,
                                             password=password,phone_number=phone_number, profession=profession,position=position,
                                                date_ended=date_ended,department=department)    
            return Response({'success':'Admin User Created succefully'})


@method_decorator(csrf_protect, name='dispatch')
class CreatePatient(APIView):
     permission_classes = (permissions.IsAuthenticated, )

     def post(self, request, format=None):
        data = self.request.data

        admin_user = request.user

        hospital_name = admin_user.hospital_name
        # print(hospital_name)
        hosi = Hospital.objects.get(hospital_name=hospital_name)
        

        first_name = data['first_name']
        last_name = data['last_name']
        sur_name = data['sur_name']
        email = data['email']
        password = data['password']
        phone_number = data['phone_number']
        physical_address= data['physical_address']
        
        
        if Patient.objects.filter(email=email).exists():
            return Response({'error':'Patient or Email already Exists'})
        else:
            user = Patient.objects.create_user(first_name=first_name, last_name=last_name,sur_name=sur_name,email=email,
                                             password=password,phone_number=phone_number,physical_address=physical_address,hospital_registered=hosi )    
            return Response({'success':'Patient User Created succefully'})

@method_decorator(csrf_protect, name='dispatch')
class PatientDataCreate(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = request.data

        required_fields = ['patient_id', 'data', 'data_type', 'hospital_id', 'medic_author', 'record_officer']
        for field in required_fields:
            if field not in data:
                return Response({'error': f"Missing required field: {field}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient_id = data.get('patient_id')
            if not patient_id:
                return Response({'error': 'Patient ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            patient = Patient.objects.get(pk=patient_id)

            hospital_id = data.get('hospital_id')
            if not hospital_id:
                return Response({'error': 'Hospital ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            hospital = Hospital.objects.get(pk=hospital_id)

            patient_data = PatientData.objects.create(
                patient=patient,
                data=data['data'],
                data_type=data['data_type'],
                hospital=hospital,
                medic_author=data['medic_author'],
                record_officer=data['record_officer']
            )
            return Response({'success': 'Patient data created successfully'}, status=status.HTTP_201_CREATED)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Hospital.DoesNotExist:
            return Response({'error': 'Hospital not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username


            user_profile = AdminUser.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)

            return Response({'profile':user_profile.data, 'username':str(user.username)})
        except:
            return Response({'error':'something went wrong when retrieving profile'})
   

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({'success':'CSRF cookie set'})




























# @csrf_exempt
# def admin_register(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         custom_user_data = data.get('custom_user_data')
#         admin_user_data = data.get('admin_user_data')

#         # Process and save custom user data
#         custom_user = CustomUser(
#             first_name=custom_user_data.get('first_name'),
#             last_name=custom_user_data.get('last_name'),
#             sur_name=custom_user_data.get('sur_name'),
#             email=custom_user_data.get('email'),
#             password=make_password(custom_user_data.get('password')),  # Hash the password
#             user_type=custom_user_data.get('user_type'),
#             phone_number=admin_user_data.get('phone_number')
#         )
#         custom_user.save()

#         # Process and save admin user data
#         admin_user = AdminUser(
#             user=custom_user,
            
#             hospital_name=admin_user_data.get('hospitalName'),
#             admin_type=admin_user_data.get('adminType')
#         )
#         admin_user.save()

#         return JsonResponse({'success': 'User registered successfully'})

#     return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

