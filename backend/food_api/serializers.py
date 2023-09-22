import base64

from django.contrib.auth import authenticate, get_user_model
from django.core.files.base import ContentFile
from recipe.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    SubscriptAuthor,
    Tag,
)
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')
        return super().to_internal_value(data)


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=150, write_only=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='A user with that email already exists.',
            )
        ],
    )
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='A user with that username already exists.',
            )
        ],
    )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
        )


class UserSerializer(CreateUserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            'is_subscribed',
            "email",
        )

    def get_is_subscribed(self, obj):
        try:
            if SubscriptAuthor.objects.filter(
                user=self.context.get('request').user,
                author=obj,
            ).exists():
                return True
            return False
        except TypeError:
            return False


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'}
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                authenticate(
                    request=self.context.get('request'),
                    email=email,
                    password=password,
                )
                user_obj = User.objects.get(email=email)
                if not user_obj.check_password(password):
                    raise serializers.ValidationError("Incorrect credentials")
                data['user'] = user_obj
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    "This email is not registered"
                )
        else:
            raise serializers.ValidationError("Missing credentials")
        return data


class SetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(source='password', write_only=True)
    current_password = serializers.CharField()

    class Meta:
        model = User
        fields = ('new_password', 'current_password')

    def create(self, validated_data):
        validated_data.pop('current_password')
        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all())

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'colour',
            'slug',
        )
        read_only_fields = (
            'name',
            'slug',
            'colour',
        )


class IngredientReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient'
    )
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount', 'name', 'measurement_unit')


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(
        many=True, source='recipe_ingredient_used', read_only=True
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    author = UserSerializer(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_in_shopping_cart',
            'is_favorited',
        )

    def get_is_favorited(self, obj):
        if FavoriteRecipe.objects.filter(
            user=self.context.get('request').user, recipe=obj
        ).exists():
            return True
        if self.context.get('request').method == 'POST':
            FavoriteRecipe.objects.create(
                user=self.context.get('request').user, recipe=obj
            )
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        return True


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=True, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True,
    )
    ingredients = IngredientSerializer(
        many=True, source='recipe_ingredient_used', required=True
    )
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'is_favorited',
            'cooking_time',
        )

    def create(self, validate_date):
        tags = validate_date.pop('tags')
        ingredients = validate_date.pop('recipe_ingredient_used')
        recipe = Recipe.objects.create(**validate_date)
        for ingredient in ingredients:
            current_ingredient = ingredient.get('ingredient')
            recipe.ingredients.add(
                current_ingredient,
                through_defaults={'amount': ingredient.get('amount')},
            )
        for tag in tags:
            recipe.tags.add(tag)
        return recipe

    def update(self, instance, validate_date):
        instance.image = validate_date.get('image', instance.image)
        instance.name = validate_date.get('name', instance.name)
        instance.text = validate_date.get('text', instance.text)
        instance.cooking_time = validate_date.get(
            'cooking_time', instance.cooking_time
        )
        if 'recipe_ingredient_used' in validate_date:
            ingredients = validate_date.pop('recipe_ingredient_used')
            del_recipe = RecipeIngredient.objects.filter(recipe=instance)
            del_recipe.delete()
            lst = []
            for ingredient in ingredients:
                (
                    current_ingredient,
                    status,
                ) = RecipeIngredient.objects.get_or_create(
                    recipe=instance,
                    ingredient=ingredient.get('ingredient'),
                    amount=ingredient.get('amount'),
                )
                lst.append(current_ingredient)
            instance.recipe_ingredient_used.set(lst)
        lst = []
        if 'tags' in validate_date:
            tags = validate_date.pop('tags')
            for tag in tags:
                (
                    current_tag,
                    status,
                ) = Tag.objects.get_or_create(
                    recipe=instance,
                    id=tag.id,
                )
                lst.append(current_tag)
            instance.tags.set(lst)
        instance.save()
        return instance

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipeReadSerializer(instance, context=context).data

    def get_is_favorited(self, obj):
        FavoriteRecipe.objects.create(
            user=self.context.get('request').user, recipe=obj
        )
        return 'true'


class ShortInfoRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubsciptionsSerializer(UserSerializer):
    recipes = ShortInfoRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            'is_subscribed',
            "email",
            "recipes",
            "recipes_count",
        )

    def get_recipes_count(self, obj):
        return self.instance.recipes.all().count()
