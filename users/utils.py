from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import User
import uuid

def send_verification_email(user):
    """
    Send verification email to user
    """
    # Generate new token
    user.email_verification_token = uuid.uuid4()
    user.email_verification_sent_at = timezone.now()
    user.save()
    
    # Create verification URL
    verification_url = f"{settings.EMAIL_VERIFICATION['MAIL_PAGE_DOMAIN']}verify-email-page/{user.email_verification_token}/"
    
    # Email context
    context = {
        'user': user,
        'verification_url': verification_url,
        'expires_in': '۱ ساعت'
    }
    
    # Render email templates
    html_message = render_to_string('users/email_verification.html', context)
    plain_message = strip_tags(html_message)
    
    # Send email
    try:
        send_mail(
            subject=settings.EMAIL_VERIFICATION['MAIL_SUBJECT'],
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def is_verification_token_expired(user):
    """
    Check if verification token is expired (1 hour)
    """
    if not user.email_verification_sent_at:
        return True
    
    expiration_time = user.email_verification_sent_at + timedelta(hours=1)
    return timezone.now() > expiration_time

def verify_email_token(token):
    """
    Verify email token and activate user
    """
    try:
        user = User.objects.get(email_verification_token=token)
        
        # Check if token is expired
        if is_verification_token_expired(user):
            return False, "کد تایید منقضی شده است. لطفاً دوباره درخواست کنید."
        
        # Activate user and mark email as verified
        user.is_active = True
        user.is_email_verified = True
        user.email_verification_token = uuid.uuid4()  # Generate new token for security
        user.save()
        
        return True, "ایمیل شما با موفقیت تایید شد."
        
    except User.DoesNotExist:
        return False, "کد تایید نامعتبر است."
    except Exception as e:
        return False, "خطا در تایید ایمیل. لطفاً دوباره تلاش کنید."

def resend_verification_email(email):
    """
    Resend verification email
    """
    try:
        user = User.objects.get(email=email)
        
        # Check if user is already verified
        if user.is_email_verified:
            return False, "ایمیل شما قبلاً تایید شده است."
        
        # Check if last email was sent recently (prevent spam)
        if user.email_verification_sent_at:
            time_since_last = timezone.now() - user.email_verification_sent_at
            if time_since_last < timedelta(minutes=5):
                return False, "لطفاً ۵ دقیقه صبر کنید و دوباره تلاش کنید."
        
        # Send new verification email
        if send_verification_email(user):
            return True, "ایمیل تایید دوباره ارسال شد."
        else:
            return False, "خطا در ارسال ایمیل. لطفاً دوباره تلاش کنید."
            
    except User.DoesNotExist:
        return False, "کاربری با این ایمیل یافت نشد." 