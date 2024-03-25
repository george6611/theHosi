@csrf_exempt
def user_login(request):
    user_data = json.loads(request.body)
    print(user_data)
    # user = CustomUser.objects.filter()
    response = JsonResponse(user_data)
    return response



@csrf_exempt
def logout_view(request):
    logout(request)
    
    return JsonResponse({'message': 'User logged out successfully'})

@csrf_exempt
def admin_panel(request):
    try:
        print("Hello")
        user_email = request.session.get('email')
        user_id = request.session.get('user_id')
        user_type = request.session.get('user_type')
        print(request.session.get('email'), 'the email')
        if user_email is None or user_id is None or user_type is None:
            return JsonResponse({'error': 'User data not found in session'}, status=401)

        admin_data = {'email': user_email, 'user_id': user_id, 'user_type': user_type}
        return JsonResponse({'admin_data': admin_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@login_required
@csrf_exempt
def hospital_details(request):
    if request.method == 'POST':
        admin_user = request.user.adminuser  # Assuming 'adminuser' is the OneToOneField related name
        if admin_user is None:
            return JsonResponse({'error': 'No associated admin user found'}, status=400)
        
        data = request.POST  # Assuming form data is sent via POST request

        hospital_name = data.get('hospital_name')
        hospital_reg = data.get('hospital_reg')
        hospital_email = data.get('hospital_email')
        hospital_phone_number = data.get('hospital_phone_number')
        hospital_phone_number_2 = data.get('hospital_phone_number_2')
        hospital_phone_number_3 = data.get('hospital_phone_number_3')
        physical_address = data.get('physical_address')

        hospital = Hospital.objects.create(
            admin_user=admin_user,
            hospital_name=hospital_name,
            hospital_reg=hospital_reg,
            hospital_email=hospital_email,
            hospital_phone_number=hospital_phone_number,
            hospital_phone_number_2=hospital_phone_number_2,
            hospital_phone_number_3=hospital_phone_number_3,
            physical_address=physical_address
        )

        return JsonResponse({'success': 'Hospital created successfully'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)     