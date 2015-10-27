from django.db import models
from django.core.mail import send_mail
from django.core.mail.message import EmailMultiAlternatives

    
class Email(models.Model):
    name = models.CharField(max_length=255, help_text='Please provide your full name')
    sender = models.EmailField(default='email@example.com',
        help_text='Please provide your valid email address')
    subject = models.CharField(blank=True, null=True,
        max_length=255, help_text='Please provide an email subject')
    email = models.EmailField(help_text='Please provide the email address to send to')
    body = models.TextField()
    
    def __unicode__(self):
        return "%s <%s>" % (self.name, self.email)

    def send(self, request=None, email=None, force=False, file_path=None, \
            file_name=None, file_type=None, context=None, **kwargs):

        # Save a version
        #import pdb;pdb.set_trace()

        msg = EmailMultiAlternatives(
            self.subject, self.body, self.sender, [self.email])
        msg.attach_alternative(self.body, 'text/html')

        try:
            file_path = context['file']['file_path']
        except:
            pass

        if file_path:
            msg.attach_file(file_path)
        try:
            return msg.send()
        except SMTPAuthenticationError as (code, resp):
            print '\n!! SMTP authenication issue \'%s\': "%s"\n' % (code, resp)
            raise SMTPAuthenticationError(code)
        except Exception, e:
            if is_test:
                print "\nSend error: ", e
                raise Exception(e)