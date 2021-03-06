from django.db import models

import re
import uuid
from dateutil.relativedelta import relativedelta

from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django import forms



def two_days_from_now():
  return timezone.now() + relativedelta(days=2)


def get_uuid_str():
  return uuid.uuid4().__str__()
      

class UserManager(BaseUserManager):

  def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
    now = timezone.now()
    if not username:
      raise ValueError(_('The given username must be set'))
    email = self.normalize_email(email)
    user = self.model(username=username, email=email,
             is_staff=is_staff, is_active=False,
             is_superuser=is_superuser, last_login=now,
             date_joined=now, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, username, email=None, password=None, **extra_fields):
    return self._create_user(username, email, password, False, False,
                 **extra_fields)

  def create_superuser(self, username, email, password, **extra_fields):
    user=self._create_user(username, email, password, True, True,
                 **extra_fields)
    user.is_active=True
    user.save(using=self._db)
    return user

class Interest(models.Model):
    name = models.CharField(_('Name'), max_length=30, blank=True, null=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    def __unicode__(self):
        return self.name
    def __iter__(self):
        return [ self.name ] 
    class Meta:
        verbose_name_plural = 'Interests'

class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['name']


class User(AbstractBaseUser, PermissionsMixin):
  GENDER_CHOICES = (
    ('unspecified', 'Unsepcified'),
    ('male', 'Male'),
    ('female', 'Female'),
  )
  first_name = models.CharField(_('First name'), max_length=255, blank=False, null=False,default='')
  last_name = models.CharField(_('Last name'), max_length=255, blank=False, null=False,default='')
  username = models.CharField(_('Username'), max_length=30, unique=True,
    help_text=_('Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
    validators=[
      validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), _('invalid'))
    ])
  email = models.EmailField(_('Email address'), max_length=255, unique=True,default='')
  telephone = models.CharField(_('Telephone'), max_length=255, blank=True, null=True,default='')
  affiliation = models.CharField(_('Affiliation'), max_length=255, blank=True, null=True,default='')
  department = models.CharField(_('Department'), max_length=255, blank=True, null=True,default='')
  address = models.TextField(_('Address'), max_length=255, blank=True, null=True,default='')
  bill_address = models.TextField(_('Billing/reimbursement address (if different from affiliation address)'), max_length=255, blank=True, null=True,default='')

  avatar = models.ImageField("Picture", upload_to="images/profile/", blank=True, null=True,default='')
  research_status = models.CharField(_('Status (Student, faculty, staff, ...)'), max_length=255, blank=True, null=True,default='')
  gender = models.CharField(_('Gender'), max_length=16, blank=True, null=True, choices = GENDER_CHOICES, default='unspecified')
  research_field = models.CharField(_('Research field/keywords (comma separated)'), max_length=255, blank=True, null=True,default='')
  supervisor = models.CharField(_('Scientific advisor/mentor'), max_length=255, blank=True, null=True,default='')
  short_bio = models.TextField(_('Short bio/bragging rights'), blank=True, null=True,default='')
  
  twitter = models.CharField(_('Twitter'), max_length=255, blank=True, null=True,default='')
  google_plus = models.CharField(_('Google+'), max_length=255, blank=True, null=True,default='')
  facebook = models.CharField(_('Facebook'), max_length=255, blank=True, null=True,default='')
  personal_email = models.EmailField(_('Email (personal)'), max_length=255, null=True,blank=True,default='')
  news_feed = models.CharField(_('news feed (RSS/Atom)'), max_length=255, blank=True, null=True,default='')
  google_scholar = models.CharField(_('Google scholar url'), max_length=255, blank=True, null=True,default='')
  orcid_id = models.CharField(_('ORCID id'), max_length=255, blank=True, null=True,default='')
  interests = models.ManyToManyField(Interest, blank=True, null=True, related_name='users')

  is_staff = models.BooleanField(_('staff status'), default=False,
    help_text=_('Designates whether the user can log into this admin site.'))
  is_active = models.BooleanField(_('active'), default=False,
    help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
  date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
  receive_newsletter = models.BooleanField(_('receive newsletter'), default=False)
  accept_terms = models.BooleanField(_('Accept the <a href="/impressum/" target="_blank">terms and conditions</a> and our <a href="/data-protection/" target="_blank">data protection</a> policies'), default=False)

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email','first_name','last_name']


  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')

  def get_full_name(self):
    return self.last_name+', '+self.first_name
 
  def get_short_name(self):
    return self.username

  def email_user(self, subject, message, from_email=None):
    send_mail(subject, message, from_email, [self.email])

  objects = UserManager()


class Registration(models.Model):
  uuid = models.CharField(max_length=36, default=get_uuid_str)
  user = models.ForeignKey(User, related_name='registration')
  expires = models.DateTimeField(default=two_days_from_now)
  type = models.CharField(max_length=10, choices=(
    ('register', 'register'),
    ('lostpass', 'lostpass'),
  ), default = 'register')
