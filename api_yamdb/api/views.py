from rest_framework import status, viewsets, filters

from .serializers import UserSerializer
from .permissions import IsAdmin, IsAdminOrModeratorOrAuthor, ReadOnlyPermission
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)