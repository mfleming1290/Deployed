from __future__ import unicode_literals

from django.db import models
from ..log.models import User


# Create your models here.
class SecretManager(models.Manager):
    def post(self, postData, id):
            errors = []
            if len(postData['message']) < 1:
                errors.append('Message cannot be empty')

            if errors:
                return (False, errors)

            else:
                print postData['message']
                user = User.objects.get(id=id)
                newobj = Secret.objects.create(
                  message=postData['message'],
                  user_message=user,

                )
                return (True, newobj)
    def like(self, request, id):
            errors = []
            try:
                curr_user = User.objects.get(id=request.session['id'])
                like = Secret.objects.get(id=id)
                like.liked_by.add(curr_user)
                like.save()
                print "liked"
                return (True, newobj)
            except:
                if errors:
                    return (False, errors)

    def delete(self, request, id):
        errors = []
        try:
            message = Secret.objects.get(id=id)
            print message
            message.delete()
            return True
        except:

            return False

class Secret(models.Model):
    message = models.TextField(max_length=1000)
    user_message = models.ForeignKey(User, on_delete=models.CASCADE, related_name="secrets")
    liked_by = models.ManyToManyField(User, related_name="liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SecretManager()
