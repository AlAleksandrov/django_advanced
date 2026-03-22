from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from accounts.serializers import RegisterSerializer

UserModel = get_user_model()

# Create your views here.
class RegisterUserView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterSerializer

