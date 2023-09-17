from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from recipe.models import Ingredient, Recipe, Tag
from rest_framework import mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .serializers import (
    AuthTokenSerializer,
    IngredientReadSerializer,
    RecipeReadSerializer,
    RecipeSerializer,
    SetPasswordSerializer,
    TagSerializer,
    UserSerializer,
)

User = get_user_model()


@api_view(['POST'])
def delete_token(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        raise JsonResponse(data={}, status=status.HTTP_402_PAYMENT_REQUIRED)
    return JsonResponse(data={}, status=status.HTTP_204_NO_CONTENT)


class AuthLoginUser(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
            }
        )


obtain_auth_token = AuthLoginUser.as_view()


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        serializer = SetPasswordSerializer(request.user, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data.get(
                'password'
            ) == serializer.validated_data.get('current_password'):
                request.user.set_password(
                    serializer.validated_data.get("new_password")
                )
                request.user.save()
                return JsonResponse(data={}, status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse(
                data={"field_name": ["Обязательное поле."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False)
    def me(self, request):
        self_user = request.user
        serializer = self.get_serializer(self_user)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredienViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientReadSerializer


class TagViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
