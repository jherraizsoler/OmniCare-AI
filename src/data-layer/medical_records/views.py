from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Patient, AiAuditLog
from .serializers import PatientSerializer, AiAuditLogSerializer

# --- VISTAS EXISTENTES (MODEL VIEWSETS) ---

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'patient_id'

class AiAuditLogViewSet(viewsets.ModelViewSet):
    queryset = AiAuditLog.objects.all()
    serializer_class = AiAuditLogSerializer

# --- NUEVAS VISTAS PARA AUTENTICACIÓN (LOGIN Y REGISTRO) ---

@api_view(['POST'])
@permission_classes([AllowAny]) # Permite que cualquier persona se registre
def register_user(request):
    data = request.data
    try:
        # Verificamos si el usuario ya existe para dar un error claro
        if User.objects.filter(username=data['username']).exists():
            return Response({"error": "El nombre de usuario ya está en uso"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data.get('email', '')
        )
        return Response({"message": "Usuario médico creado con éxito"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Generamos el par de tokens (Access y Refresh)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Usuario o contraseña incorrectos"}, status=status.HTTP_401_UNAUTHORIZED)