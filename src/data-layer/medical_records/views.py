from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from django.db.models import Count
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import HexColor  # Importación específica para colores Hex
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

from .models import Patient, ConsultaIA
from .serializers import PatientSerializer, AiAuditLogSerializer

# --- VISTAS EXISTENTES (MODEL VIEWSETS) ---

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'patient_id'
    permission_classes = [IsAuthenticated]

class AiAuditLogViewSet(viewsets.ModelViewSet):
    # Cambia '-created_at' por '-fecha'
    queryset = ConsultaIA.objects.all().order_by('-fecha') 
    serializer_class = AiAuditLogSerializer
    permission_classes = [IsAuthenticated]

# --- AUTENTICACIÓN ---

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    try:
        # Aquí 'dni' es lo que el usuario envía y lo guardamos en 'username'
        dni_nuevo = data.get('dni')
        
        if User.objects.filter(username=dni_nuevo).exists():
            return Response({"error": "El usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            username=dni_nuevo,
            password=data['password'],
            email=data.get('email', ''),
            first_name=data.get('nombre', '')
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
    credential_input = data.get('credential') # Puede ser el credential o Email
    password = data.get('password')
    user = authenticate(username=credential_input, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        # Determinamos el rol
        if user.is_superuser: user_role = 'supervisor'
        elif user.is_staff: user_role = 'medico'
        else: user_role = 'paciente'
            
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'dni': user.username,   
            'first_name': user.first_name, 
            'role': user_role
        })
    return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

# --- GESTIÓN DE MÉDICOS (SUPERVISOR) ---

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_medicos(request):
    if not request.user.is_superuser:
        return Response({"error": "Acceso denegado."}, status=403)
        
    # Anotamos cada médico con el número de pacientes que tiene asignados
    # Corrección: Usa 'username' en lugar de 'credential'
    medicos = User.objects.filter(is_staff=True).exclude(is_superuser=True).annotate(
        num_pacientes=Count('doctor_patients')
    ).values('id', 'first_name', 'last_name', 'email', 'username', 'num_pacientes')
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
    """
    Guarda la conversación en la tabla maestra ConsultaIA.
    """
    data = request.data
    try:
        # Guardamos TODO en ConsultaIA. No necesitamos la otra tabla.
        consulta = ConsultaIA.objects.create(
            paciente=request.user,
            mensaje_usuario=data.get('mensaje'),
            respuesta_ia=data.get('respuesta'),
            dolor=data.get('dolor', 0),
            urgencia=data.get('urgencia', 0), # Ahora es numérico 0-10
            riesgo=data.get('riesgo', 0)     # Ahora es numérico 0-10
        )

        return Response({
            "status": "Consulta guardada correctamente",
            "consulta_id": consulta.id
        }, status=201)

    except Exception as e:
        return Response({"error": f"Error al procesar el guardado: {str(e)}"}, status=400)

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
    # CAMBIO: paciente__username en lugar de paciente__credential
    consultas = ConsultaIA.objects.filter(paciente__username=patient_id).order_by('-fecha')
    
    if not consultas.exists():
        return HttpResponse("No hay consultas para este paciente", status=404)
    
    try:
        # CAMBIO: username=patient_id en lugar de credential=patient_id
        paciente_obj = User.objects.get(username=patient_id)
        nombre_completo = f"{paciente_obj.first_name} {paciente_obj.last_name}"
        email_paciente = paciente_obj.email
    except User.DoesNotExist:
        nombre_completo = "No registrado"
        email_paciente = "N/A"

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Historial_Clinico_{patient_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    primary_color = HexColor("#1C83E1")
    
    # Estilos personalizados
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], textColor=primary_color, spaceAfter=12)
    header_style = ParagraphStyle('HeaderStyle', parent=styles['Normal'], fontSize=10, textColor=colors.grey)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=9, leading=12)

    # --- ENCABEZADO PROFESIONAL ---
    elements.append(Paragraph("🏥 OMNICARE AI - INFORME CLÍNICO DIGITAL", title_style))
    elements.append(Paragraph(f"<b>Paciente:</b> {nombre_completo}", styles['Normal']))
    elements.append(Paragraph(f"<b>credential/ID:</b> {patient_id} | <b>Email:</b> {email_paciente}", header_style))
    elements.append(Paragraph(f"<b>Fecha de Generación:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", header_style))
    elements.append(Spacer(1, 20))

    # --- TABLA DE CONSULTAS ---
    data = [["FECHA", "MÉTRICAS TRIAJE", "RESUMEN DE CONSULTA"]]
    
    for c in consultas:
        # Formateamos las métricas de forma más visual
        metrics = f"Dolor: {c.dolor}/10\nUrgencia: {c.urgencia}\nRiesgo: {c.riesgo}"
        # Resumen limpio del mensaje
        msg_summary = (c.mensaje_usuario[:150] + '...') if len(c.mensaje_usuario) > 150 else c.mensaje_usuario
        
        data.append([
            c.fecha.strftime('%d/%m/%Y\n%H:%M'), 
            metrics, 
            Paragraph(msg_summary, body_style)
        ])

    # Ajuste de anchos: Fecha(80), Métricas(140), Resumen(300)
    t = Table(data, colWidths=[80, 140, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(t)
    
    # --- PIE DE PÁGINA / NOTA LEGAL ---
    elements.append(Spacer(1, 30))
    nota_legal = """
    <i fontSize="8">Este documento ha sido generado automáticamente por el sistema de IA OmniCare. 
    Los datos de triaje son orientativos y deben ser validados por un facultativo colegiado. 
    Cumple con la normativa RGPD de protección de datos de salud.</i>
    """
    elements.append(Paragraph(nota_legal, header_style))

    doc.build(elements)
    return response

