from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from history_chatbot import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token

# Create your views here.
def home(request):
    return render(request, "users/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.success(request, "Tên đăng nhập đã tồn tại! Vui lòng chọn tên khác.")
            return redirect('/users/signup')
        
        if User.objects.filter(email=email).exists():
            messages.success(request, "Email Đã tồn tại!!")
            return redirect('/users/signup')
        
        if len(username)>20:
            messages.success(request, "Tên đăng nhập phải nhỏ hơn 20 ký tự!!")
            return redirect('/users/signup')
        
        if pass1 != pass2:
            messages.success(request, "Mật khẩu không khớp!!")
            return redirect('/users/signup')
        
        if not username.isalnum():
            messages.success(request, "Tên đăng nhập phải là chữ!!")
            return redirect('/users/signup')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Tài khoản của bạn đã được tạo thành công!! Vui lòng kiểm tra email của bạn để xác nhận địa chỉ email của bạn để kích hoạt tài khoản của bạn.")
        
        # Welcome Email
        subject = "Welcome to GFG- Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('/users/signin')
        
        
    return render(request, "users/signup.html")


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        # messages.success(request, "Your Account has been activated!!")
        return redirect('/users/signin')
    else:
        return render(request,'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            if "next" in request.POST:
                print(request.POST.get('next'))
                return redirect(request.POST.get('next'))
            else:
                return redirect("/")
        else:
            if User.objects.filter(username=username):
                messages.success(request, "Mật khẩu không chính xác")
            else:
                messages.success(request, "Thông tin đăng nhập không chính xác")
            return redirect('/users/signin')
    
    return render(request, "users/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Bạn đã đăng xuất thành công!!")
    return redirect('/')