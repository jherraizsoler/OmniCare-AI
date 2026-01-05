from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import HexColor  # Importación específica para colores Hex
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


from .models import Patient, AiAuditLog, ConsultaIA
from .serializers import PatientSerializer, AiAuditLogSerializer

# --- VISTAS EXISTENTES (MODEL VIEWSETS) ---

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'patient_id'
    permission_classes = [IsAuthenticated]

class AiAuditLogViewSet(viewsets.ModelViewSet):
    queryset = AiAuditLog.objects.all()
    serializer_class = AiAuditLogSerializer
    permission_classes = [IsAuthenticated]

# --- AUTENTICACIÓN ---

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    try:
        if User.objects.filter(username=data['username']).exists():
            return Response({"error": "El usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data.get('email', ''),
        )
        
        if data.get('is_staff'):
            user.is_staff = True
            user.save()
            
        return Response({"message": "Usuario creado con éxito"}, status=status.HTTP_201_CREATED)
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
        refresh = RefreshToken.for_user(user)
        if user.is_superuser:
            user_role = 'supervisor'
        elif user.is_staff:
            user_role = 'medico'
        else:
            user_role = 'paciente'
            
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
            'role': user_role
        })
    return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

# --- GESTIÓN DE MÉDICOS (SUPERVISOR) ---

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_medicos(request):
    if not request.user.is_superuser:
        return Response({"error": "Acceso denegado."}, status=403)
        
    medicos = User.objects.filter(is_staff=True, is_superuser=False).values(
        'id', 'username', 'email', 'date_joined'
    )
    return Response(list(medicos))

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):
    if not request.user.is_superuser:
        return Response({"error": "Permiso denegado"}, status=403)
    try:
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=204)
    except User.DoesNotExist:
        return Response(status=404)

# --- GESTIÓN DE PACIENTES (MÉDICO) ---

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_patients(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return Response({"error": "No tiene permisos médicos"}, status=403)

    if request.method == 'GET':
        if request.user.is_superuser:
            pacientes = Patient.objects.all()
        else:
            pacientes = Patient.objects.filter(doctor=request.user)
        
        data = pacientes.values('id', 'patient_id', 'name', 'clinical_history', 'created_at')
        return Response(list(data))

    elif request.method == 'POST':
        data = request.data
        try:
            nuevo_paciente = Patient.objects.create(
                doctor=request.user,
                patient_id=data['patient_id'],
                name=data['name'],
                clinical_history=data.get('clinical_history', '')
            )
            return Response({"message": "Paciente creado y asignado"}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

# --- NUEVAS FUNCIONES DE PERSISTENCIA IA ---

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def guardar_consulta(request):
    """Guarda la conversación y métricas generadas por el agente de LangGraph."""
    data = request.data
    try:
        ConsultaIA.objects.create(
            paciente=request.user,
            mensaje_usuario=data.get('mensaje'),
            respuesta_ia=data.get('respuesta'),
            dolor=data.get('dolor', 0),
            urgencia=data.get('urgencia', 0),
            riesgo=data.get('riesgo', 0)
        )
        return Response({"status": "Consulta guardada correctamente"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def historial_paciente(request, patient_id=None):
    """Retorna el historial de consultas. Soporta vista de paciente y vista de médico."""
    if patient_id:
        # Lógica para médico: ver historial de un paciente específico
        if not request.user.is_staff:
            return Response({"error": "No autorizado"}, status=403)
        consultas = ConsultaIA.objects.filter(paciente__username=patient_id).order_by('-fecha')
    else:
        # Lógica para paciente: ver su propio historial
        consultas = ConsultaIA.objects.filter(paciente=request.user).order_by('-fecha')

    data = [{
        "mensaje_usuario": c.mensaje_usuario,
        "respuesta_ia": c.respuesta_ia,
        "dolor": c.dolor,
        "urgencia": c.urgencia,
        "riesgo": c.riesgo,
        "fecha": c.fecha.strftime('%Y-%m-%d %H:%M')
    } for c in consultas]
    
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    new_password = request.data.get('new_password')
    if not new_password or len(new_password) < 4:
        return Response({"error": "Contraseña demasiado corta"}, status=400)
    user.set_password(new_password)
    user.save()
    return Response({"message": "Contraseña actualizada"}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_paciente_pdf(request, patient_id):
    consultas = ConsultaIA.objects.filter(paciente__username=patient_id).order_by('-fecha')
    
    if not consultas.exists():
        return HttpResponse("No hay consultas para este paciente", status=404)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Historial_Clinico_{patient_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # --- CORRECCIÓN AQUÍ: HexColor con H mayúscula ---
    primary_color = HexColor("#1C83E1")
    
    title_style = ParagraphStyle(
        'TitleStyle', 
        parent=styles['Heading1'], 
        textColor=primary_color, 
        spaceAfter=12
    )
    header_style = ParagraphStyle(
        'HeaderStyle', 
        parent=styles['Normal'], 
        fontSize=10, 
        textColor=colors.grey
    )
    body_style = ParagraphStyle(
    'BodyStyle',
    parent=styles['Normal'],
    fontSize=9,
    leading=12,
    alignment=0 # Justificado a la izquierda
)

    # ... Resto del encabezado igual ...
    elements.append(Paragraph("🏥 OMNICARE AI - SISTEMA DE GESTIÓN CLÍNICA", title_style))
    elements.append(Paragraph(f"<b>Reporte de Evolución del Paciente</b>", styles['Heading2']))
    elements.append(Paragraph(f"Identificador del Paciente: {patient_id}", header_style))
    elements.append(Spacer(1, 20))

    # --- TABLA CON CORRECCIÓN DE COLORES ---
    data = [["FECHA", "TRIAJE (Dolor / Urgente / Riesgo)", "RESUMEN DE CONSULTA"]]
    for c in consultas:
        metrics = f"Dolor: {c.dolor} | Urgencia: {c.urgencia} | Riesgo: {c.riesgo}"
        msg_summary = (c.mensaje_usuario[:100] + '..') if len(c.mensaje_usuario) > 100 else c.mensaje_usuario
        data.append([c.fecha.strftime('%d/%m/%Y %H:%M'), metrics, Paragraph(msg_summary, body_style)])

    t = Table(data, colWidths=[90, 170, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color), # Usamos la variable primary_color corregida
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
    ]))
    
    elements.append(t)
    doc.build(elements)
    return response