from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    domain = get_current_site(request).domain
    link = reverse('accounts:email-verify', kwargs={'uidb64': uid, 'token': token})
    activate_url = f"http://{domain}{link}"

    send_mail(
        subject='Verify your email',
        message=f'Click the link to verify: {activate_url}',
        from_email='noreply@example.com',
        recipient_list=[user.email],
    )

def password_reset_confirm(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    domain = get_current_site(request).domain
    link = reverse('accounts:password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
    activate_url = f"http://{domain}{link}"
    
    send_mail(
        subject='Reset your password',
        message=f'Click the link to reset password: {activate_url}',
        from_email='noreply@example.com',
        recipient_list=[user.email],
    )