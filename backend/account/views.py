from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .serializer import SignUpSerializer, UserSerializer
from .validators import validate_files_extension

# Create your views here.


@api_view(["POST"])
def register(request):
    data = request.data

    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data["email"]).exists():
            user = User.objects.create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                username=data["email"],
                email=data["email"],
                password=make_password(data["password"]),
            )
            return Response(
                {"message": "User Registered", "status": status.HTTP_200_OK}
            )
        else:
            return Response(
                {
                    "error": "user already registered",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
    else:
        return Response(user.errors)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def currentUser(request):
    user = UserSerializer(request.user)
    return Response(user.data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUser(request):
    user = request.user
    data = request.data
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.username = data['email']

    if data["password"] != '':
        user.password = make_password(data['password'])

    user.save()
    
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def uploadResume(request):
    user = request.user
    resume = request.FILES['resume']

    if resume == '':
        return Response({'error': 'Please upload your resume.'})

    isValidFile= validate_files_extension(resume.name)
    if not isValidFile:
        return Response({'error': 'Please upload only pdf.'})
        
    user.userprofile.resume = resume
    user.userprofile.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)