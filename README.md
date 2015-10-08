# forumdev-user

user app for the forumdev django framework

#### install

add `fduser` at the top of the `INSTALLED_APPS` list in settings.py

add `AUTH_USER_MODEL = 'myauth.User'` after `INSTALLED_APPS`

run `./manage.py syncdb`
