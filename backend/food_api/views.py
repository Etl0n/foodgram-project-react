from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipe.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeInShoppingCart,
    SubscriptAuthor,
    Tag,
)
from rest_framework import filters, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import MySearchFilter, RecipeFilter
from .permisions import OwnerOrReadOnly
from .serializers import (
    AuthTokenSerializer,
    CreateUserSerializer,
    IngredientReadSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
    SetPasswordSerializer,
    ShortInfoRecipeSerializer,
    SubsciptionsSerializer,
    TagSerializer,
    UserSerializer,
)
from .utils import create_txt_with_ingredients

User = get_user_model()


def view_for_shopp_and_favorite(models_obj, request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except ValueError:
        raise ValueError()
    if request.method == 'POST':
        models_obj.objects.create(user=request.user, recipe=recipe)
        serializer = ShortInfoRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        try:
            obj = models_obj.objects.get(user=request.user, recipe=recipe)
        except ValueError:
            return Response('', status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        return Response('', status=status.HTTP_204_NO_CONTENT)


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

    def get_queryset(self):
        if self.action == 'list':
            limit = self.request.GET.get('limit')
            if limit is None:
                return super().get_queryset()
            self.paginator.page_size = int(self.request.GET.get('limit'))
        return super().get_queryset()

    @action(detail=False)
    def me(self, request):
        self_user = request.user
        serializer = self.get_serializer(self_user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = RecipeFilter
    ordering = ('-pub_day',)

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
    pagination_class = None
    filter_backends = (MySearchFilter,)
    search_fields = ('^name',)
    permission_classes = (AllowAny,)


class TagViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class Subscriptions(mixins.ListModelMixin, GenericViewSet):
    serializer_class = SubsciptionsSerializer

    def get_queryset(self):
        authors = SubscriptAuthor.objects.filter(user=self.request.user)
        lst = [author.author.username for author in authors]
        queryset = User.objects.filter(username__in=lst)
        limit = self.request.GET.get('limit')
        if limit is None:
            return queryset
        self.paginator.page_size = int(self.request.GET.get('limit'))
        return queryset


@api_view(['POST', 'DELETE'])
def favorite(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except ValueError:
        raise ValueError()
    if request.method == 'POST':
        FavoriteRecipe.objects.create(user=request.user, recipe=recipe)
        serializer = ShortInfoRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        try:
            favorite = FavoriteRecipe.objects.get(
                user=request.user, recipe=recipe
            )
        except ValueError:
            return Response('', status=status.HTTP_400_BAD_REQUEST)
        favorite.delete()
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
        serializer = SubsciptionsSerializer(author, context=context)
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


@api_view(['POST', 'DELETE'])
def is_in_shopping_cart(request, recipe_id):
    return view_for_shopp_and_favorite(
        RecipeInShoppingCart, request, int(recipe_id)
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_shopping_cart(request):
    create_txt_with_ingredients(request)
    shopp_file = open(
        f'{settings.MEDIA_URL}backend.txt',
        "rb",
    )
    return FileResponse(shopp_file, content_type='text/plain')
