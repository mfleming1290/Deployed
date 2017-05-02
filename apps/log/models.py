from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):
      def register(self, postData):
          errors = []
          exists = User.objects.filter(email=postData['email'])
          if exists:
              errors.append('Email already in database')
              print "in database"
              return (False, errors)
          else:

              if len(postData['first_name']) < 1:
                  errors.append('First name cannot be empty')

              if len(postData['last_name']) < 1:
                 errors.append('Last name cannot be empty')

              if not postData['first_name'].isalpha():
                  errors.append('First Name must only contain letters')

              if not postData['last_name'].isalpha():
                  errors.append('Last Name must only contain letters')

              if not EMAIL_REGEX.match(postData['email']):
                 errors.append('Email must be a valid email')

              if len(postData['password']) < 1:
                  errors.append('Password must not be empty')

              if len(postData['password']) < 8:
                  errors.append('Password to short')

              if len(postData['confirm_password']) < 1:
                  errors.append('Confirm password must not be empty')

              if postData['password'] != postData['confirm_password']:
                  errors.append('Password and Confirm password must match')
              if errors:
                  return (False, errors)
              else:
                  pw = postData['password']
                  hashed_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
                  newobj = User.objects.create(
                    first_name=postData['first_name'],
                    last_name=postData['last_name'],
                    email=postData['email'],
                    password=hashed_pw,
                  )
                  return (True, newobj)



      def login(self, postData):
        errors = []
        exists = User.objects.filter(email=postData['email'])
        if not exists:
            errors.append('Must be a valid user')
            print "not in database"

        if errors:
                return (False, errors)
        else:
            try:
                if exists:
                    user = User.objects.get(email=postData['email'])
                    password = postData['password']
                if bcrypt.hashpw(password.encode(), user.password.encode()) == user.password.encode():
                    print "success"
                    return (True, user)

            except:
                    print 'something failed', user

        errors.append('incorrect password')
        return (False, errors)

      def delete_user(self, postData):
          user = User.objects.get(id=postData)
          user.delete()
          return True
      def update_user(self, ids, postData):
          errors = []
          exists = User.objects.filter(email=postData['email'])
          if exists:
              errors.append('Email already in database')
              print "in database"
              return (False, errors)
          else:
              user = User.objects.get(id=ids)
              user.first_name = postData['first_name']
              user.last_name = postData['last_name']
              user.email = postData['email']
              user.save()
              return (True, user)
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
