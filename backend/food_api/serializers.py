import base64

from django.contrib.auth import authenticate, get_user_model
from django.core.files.base import ContentFile
from recipe.models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    Tag,
)
from rest_framework import serializers

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')
        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=150, write_only=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(
        max_length=254,
        required=True,
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
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'colour',
            'slug',
        )
        read_only_fields = ('slug',)


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
    tags = TagSerializer(many=True, source='recipe_tag_used', required=True)
    ingredients = IngredientSerializer(
        many=True, source='recipe_ingredient_used', required=True
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)

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
            'is_favorited',
        )

    def get_is_favorited(self, obj):
        favorite, status = FavoriteRecipe.objects.get_or_create(
            user=self.context.get('request').user, recipe=obj
        )
        return favorite.is_favorited


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True,
    )
    ingredients = IngredientSerializer(
        many=True, source='recipe_ingredient_used', required=True
    )

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

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data
