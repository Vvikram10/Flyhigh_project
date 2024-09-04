from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages,auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes 
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
# from reservation.views import *
from django.db.models import Q
from accounts.models import Account, UserProfile
from reservation.models import CustomerDetails
from django.contrib.auth import authenticate, login,logout 


def dashboard(request):
    # Retrieve orders that are reserved by the logged-in user and order them by the booking date
    orders = CustomerDetails.objects.order_by('-booking_date').filter(user_id=request.user.id, is_reserved=True)
    
    # Count the number of orders
    orders_count = orders.count()

    # Retrieve the user profile associated with the logged-in user
    userprofile = get_object_or_404(UserProfile, user_id=request.user.id)

    # Context to pass to the template
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    
    # Render the dashboard template with the provided context
    return render(request, 'accounts/dashboard.html', context)

def my_orders(request):
    orders = CustomerDetails.objects.filter(user=request.user, is_reserved=True).order_by('-booking_date')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)

def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        # Manually process the form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        profile_picture = request.FILES.get('profile_picture')

        # Update the user model
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.phone_number = phone_number
        request.user.save()

        # Update the user profile model
        user_profile.address_line_1 = address_line_1
        user_profile.address_line_2 = address_line_2
        user_profile.city = city
        user_profile.state = state
        user_profile.country = country
        if profile_picture:
            user_profile.profile_picture = profile_picture
        user_profile.save()

        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('edit_profile')
    
    # Render the form with the existing user and profile data
    context = {
        'userprofile': user_profile,
    }
    return render(request, 'accounts/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic validation
        if not all([first_name, last_name, phone_number, email, password, confirm_password]):
            messages.error(request, 'Please fill in all fields.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif Account.objects.filter(email=email).exists():
            messages.error(request, 'Email address already in use.')
        else:
            # Create the user account
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email.split("@")[0],
                password=password
            )
            user.phone_number = phone_number
            user.save()

            # Create a user profile
            profile = UserProfile(user=user)
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            # Account activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it.',extra_tags='success')
            return redirect('/accounts/login/?command=verification&email=' + email)
    
    return render(request, 'accounts/register.html')

# def user_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Authenticate the Account
#         Account = authenticate(request, email=email, password=password)

#         if Account is not None:
#             if Account.is_active:
#                 login(request, Account)
#                 messages.success(request, f'Welcome {Account.full_name()}!',extra_tags='success')
#                 return redirect('home')  # Redirect to a dashboard or homepage
#             else:
#                 messages.error(request, 'Your account is inactive. Please contact support.',extra_tags='danger')
#         else:
#             messages.error(request, 'Invalid email or password.',extra_tags='danger')

#     context = {}
#     return render(request, 'accounts/login.html', context)

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the Account
        Account = authenticate(request, email=email, password=password)

        if Account is not None:
            if Account.is_active:
                login(request, Account)
                
                # Check if the user is a superuser or staff (admin)
                if Account.is_superuser:
                    # Redirect to admin dashboard
                    messages.success(request, f'Welcome {Account.full_name()}!', extra_tags='success')
                    return redirect('admin_dashboard')  # Replace 'admin_dashboard' with your admin dashboard URL name
                elif Account.is_staff:
                    # Redirect to admin dashboard or staff dashboard
                    return redirect('admin_dashboard')  # Replace 'admin_dashboard' with your admin dashboard URL name
                else:
                    # Redirect to the home page or user-specific dashboard
                    messages.success(request, f'Welcome {Account.full_name()}!', extra_tags='success')
                    return redirect('home')  # Redirect to a dashboard or homepage
            else:
                messages.error(request, 'Your account is inactive. Please contact support.', extra_tags='danger')
        else:
            messages.error(request, 'Invalid email or password.', extra_tags='danger')

    context = {}
    return render(request, 'accounts/login.html', context)

def user_logout(request):
    logout(request)  # Log out the Account
    return redirect('login')

def admin_dashboard(request):
    User = get_user_model()

    # Initialize search query
    search_query = request.GET.get('search', '')

    # Count total users, admins, and regular users
    total_users = User.objects.count()
    total_admins = User.objects.filter(is_admin=True).count()
    total_regular_users = total_users - total_admins

    # Filter users based on search query
    if search_query:
        users = User.objects.filter(first_name__icontains=search_query)
    else:
        users = User.objects.all()

    context = {
        'total_users': total_users,
        'total_admins': total_admins,
        'total_regular_users': total_regular_users,
        'users': users,
        'search_query': search_query,
    }
    return render(request, 'admin/admin_dashboard.html', context)


def delete_user_view(request, user_id):
    user = get_object_or_404(Account, id=user_id)
    user.delete()  # Call the delete_user method to delete the user
    return redirect('admin_dashboard') 

def user_dashboard(request):
    return render(request, 'user_dashboard.html')

def activate(request, uidb64, token):
    try:
        # Decode the uidb64 value
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # Check if the user exists and the token is valid
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)

            current_site = get_current_site(request)
            mail_subject = 'Please Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account with this email does not exist.')
            return redirect('forget_password')
    else:
        return render(request, 'accounts/forget_password.html')
    
def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password.')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has expired or is invalid.')
        return redirect('login')

        
def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'accounts/reset_password.html', {'error': 'Passwords do not match'})
        
        uid = request.session.get('uid')
        if uid:
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid reset request.')
            return redirect('forget_password')

    return render(request, 'accounts/reset_password.html')

