from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from recipe.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    SubscriptAuthor,
    Tag,
)
from rest_framework import mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .serializers import (
    AuthTokenSerializer,
    CreateUserSerializer,
    IngredientReadSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
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
        raise Response(data={}, status=status.HTTP_402_PAYMENT_REQUIRED)
    return Response(data={}, status=status.HTTP_204_NO_CONTENT)


class AuthLoginUser(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'auth_token': token.key})


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
        user = request.user
        serializer = SetPasswordSerializer(user, data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get("current_password")
            if user.check_password(password):
                user.set_password(
                    serializer.validated_data.get("new_password")
                )
                user.save()
                return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data={"field_name": ["Обязательное поле."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return UserSerializer

    @action(detail=False)
    def me(self, request):
        self_user = request.user
        serializer = self.get_serializer(self_user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredienViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientReadSerializer
    permission_classes = (AllowAny,)


class TagViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


@api_view(['POST', 'DELETE'])
def favorite(request):
    if request.method == 'POST':
        FavoriteRecipe.objects.create(
            user=request.user, recipe=Recipe.objects.get(request.get('recipe'))
        )
        return Response('', status=status.HTTP_201_CREATED)
    else:
        FavoriteRecipe.objects.delete(
            user=request.user, recipe=Recipe.objects.get(request.get('recipe'))
        )
        return Response('', status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'DELETE'])
def subscribe(request, author_id):
    try:
        author = User.objects.get(id=author_id)
    except ValueError:
        raise ValueError()
    if request.method == 'POST':
        SubscriptAuthor.objects.create(user=request.user, author=author)
        context = {'request': request}
        serializer = UserSerializer(author, context=context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        object = SubscriptAuthor.objects.filter(
            user=request.user, author=author
        )
        if object.exists():
            object.delete()
            return Response('', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('', status=status.HTTP_400_BAD_REQUEST)
