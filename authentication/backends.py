# # from django.contrib.auth.backends import ModelBackend
# # from django.contrib.auth.hashers import check_password
# # from .models import CustomUser


#  class EmailBackend(ModelBackend):
#      def authenticate(self, request, email=None, password=None, **kwargs):
#          try:
#              user = CustomUser.objects.get(email=email)
#          except CustomUser.DoesNotExist:
#             return None