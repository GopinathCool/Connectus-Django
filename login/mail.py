from django.core.mail import send_mail

def registration_mail(host, activation_key, to):
    print 'REGISTRATION MAIL ###'
    mail_body = 'Click the below link\n\nhttp://localhost:8000/connectus/account/activation/{0}'.format(activation_key)
    send_mail('ConnectUs App Django', mail_body, 'gopinathcool1993@gmail.com', to,
              fail_silently=False)
    print 'end of reg mail ...'