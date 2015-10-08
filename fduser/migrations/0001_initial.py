# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import fduser.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(default=b'', max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(default=b'', max_length=255, verbose_name='Last name')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters', unique=True, max_length=30, verbose_name='Username', validators=[django.core.validators.RegexValidator(re.compile(b'^[\\w.@+-]+$'), 'Enter a valid username.', 'invalid')])),
                ('email', models.EmailField(default=b'', unique=True, max_length=255, verbose_name='Email address')),
                ('telephone', models.CharField(default=b'', max_length=255, null=True, verbose_name='Telephone', blank=True)),
                ('affiliation', models.CharField(default=b'', max_length=255, null=True, verbose_name='Affiliation', blank=True)),
                ('department', models.CharField(default=b'', max_length=255, null=True, verbose_name='Department', blank=True)),
                ('address', models.TextField(default=b'', max_length=255, null=True, verbose_name='Address', blank=True)),
                ('bill_address', models.TextField(default=b'', max_length=255, null=True, verbose_name='Billing/reimbursement address (if different from affiliation address)', blank=True)),
                ('avatar', models.ImageField(default=b'', upload_to=b'images/profile/', null=True, verbose_name=b'Picture', blank=True)),
                ('research_status', models.CharField(default=b'', max_length=255, null=True, verbose_name='Status (Student, faculty, staff, ...)', blank=True)),
                ('gender', models.CharField(default=b'unspecified', choices=[(b'unspecified', b'Unsepcified'), (b'male', b'Male'), (b'female', b'Female')], max_length=16, blank=True, null=True, verbose_name='Gender')),
                ('research_field', models.CharField(default=b'', max_length=255, null=True, verbose_name='Research field/keywords (comma separated)', blank=True)),
                ('supervisor', models.CharField(default=b'', max_length=255, null=True, verbose_name='Scientific advisor/mentor', blank=True)),
                ('short_bio', models.TextField(default=b'', null=True, verbose_name='Short bio/bragging rights', blank=True)),
                ('twitter', models.CharField(default=b'', max_length=255, null=True, verbose_name='Twitter', blank=True)),
                ('google_plus', models.CharField(default=b'', max_length=255, null=True, verbose_name='Google+', blank=True)),
                ('facebook', models.CharField(default=b'', max_length=255, null=True, verbose_name='Facebook', blank=True)),
                ('personal_email', models.EmailField(default=b'', max_length=255, null=True, verbose_name='Email (personal)', blank=True)),
                ('news_feed', models.CharField(default=b'', max_length=255, null=True, verbose_name='news feed (RSS/Atom)', blank=True)),
                ('google_scholar', models.CharField(default=b'', max_length=255, null=True, verbose_name='Google scholar url', blank=True)),
                ('orcid_id', models.CharField(default=b'', max_length=255, null=True, verbose_name='ORCID id', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('receive_newsletter', models.BooleanField(default=False, verbose_name='receive newsletter')),
                ('accept_terms', models.BooleanField(default=False, verbose_name='Accept the <a href="/impressum/" target="_blank">terms and conditions</a> and our <a href="/data-protection/" target="_blank">data protection</a> policies')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, null=True, verbose_name='Name', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Interests',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(default=fduser.models.get_uuid_str, max_length=36)),
                ('expires', models.DateTimeField(default=fduser.models.two_days_from_now)),
                ('type', models.CharField(default=b'register', max_length=10, choices=[(b'register', b'register'), (b'lostpass', b'lostpass')])),
                ('user', models.ForeignKey(related_name='registration', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='interests',
            field=models.ManyToManyField(related_name='users', null=True, to='fduser.Interest', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
