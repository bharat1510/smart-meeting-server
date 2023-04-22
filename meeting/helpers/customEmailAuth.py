# from django.contrib.auth.models import User
from meeting.models import *

class EmailAuthentication():
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            passCheck = user.check_password(password)

            if passCheck:
                return user
        except User.DoesNotExist:
            pass
        return None

    def get_user(self,id):
        try:
            return User.objects.get(id=id)
        except:
            return None