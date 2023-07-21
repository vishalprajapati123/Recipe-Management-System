from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Recipe,Rating
from .serializers import UserSerializer, RecipeSerializer, RatingSerializer
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
    
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if user.check_password(password):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({'access_token': access_token}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET', 'POST'])
def recipe_list_create(request):
    if request.method == 'GET':
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Check if the user is authenticated before processing the POST request
        if not IsAuthenticated().has_permission(request, None):
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        data = request.data.copy()
        data['user'] = request.user.id
        serializer = RecipeSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def recipe_detail(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return Response({'error': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not IsAuthenticated().has_permission(request, None):
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        serializer = RecipeSerializer(recipe, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not IsAuthenticated().has_permission(request, None):
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def rating_create(request):
    data = request.data.copy()
    data['user'] = request.user.id
    
    # Check if the rating already exists
    recipe_id = data.get('recipe')
    existing_rating = Rating.objects.filter(user=request.user, recipe_id=recipe_id).first()

    if existing_rating:
        return Response({'error': 'You have already rated this recipe'}, status=status.HTTP_400_BAD_REQUEST)
    
    # If not, create a new rating
    serializer = RatingSerializer(data=data, context={'request': request})
    
    try:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
        return Response({'error': 'You have already rated this recipe'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def recipe_search(request):
    query = request.query_params.get('q', '')
    recipes = Recipe.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(ingredients__name__icontains=query) |
        Q(instructions__description__icontains=query)
    ).distinct()
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)



