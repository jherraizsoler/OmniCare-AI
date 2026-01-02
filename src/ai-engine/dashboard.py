import streamlit as st
import httpx
import matplotlib.pyplot as plt
import asyncio
from langchain_core.messages import HumanMessage
from graph_engine import medical_graph

# --- CONFIGURACIÓN ---
DJANGO_URL = "http://localhost:8001/api"
st.set_page_config(page_title="OmniCare Pro", layout="wide", page_icon="🏥")

# --- FUNCIONES DE APOYO ---
def extraer_metricas(texto):
    """Analiza el texto de la IA para actualizar el gráfico de barras"""
    texto = texto.lower()
    dolor = 8 if any(w in texto for w in ["fuerte", "intenso", "agudo", "10/10"]) else 4
    urgencia = 9 if any(w in texto for w in ["urgente", "emergencia", "inmediata"]) else 3
    riesgo = 7 if any(w in texto for w in ["grave", "crítico", "complicado"]) else 2
    return [dolor, urgencia, riesgo]

# --- INICIALIZACIÓN DE ESTADOS ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "token" not in st.session_state:
    st.session_state.token = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "metricas" not in st.session_state:
    st.session_state.metricas = [0, 0, 0]

# --- VISTA DE LOGIN ACTUALIZADA Y CENTRADA ---
def login_view():
    # Usamos columnas laterales más anchas para que el login sea más estrecho y elegante
    empty_l, col_center, empty_r = st.columns([1.2, 1, 1.2])
    
    with col_center:
        # Espaciado superior generoso
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        # Título limpio sin el emoji si quieres algo más sobrio, o con él pero centrado
        st.markdown("<h2 style='text-align: center;'>OmniCare AI</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Acceso al Portal Médico</p>", unsafe_allow_html=True)
        
        # Eliminamos el st.container(border=True) para que los tabs floten sobre el fondo
        tab_login, tab_register = st.tabs(["Entrar", "Nueva Cuenta"])
        
        with tab_login:
            # Quitamos el borde del formulario también usando el parámetro border=False (disponible en versiones recientes)
            # o simplemente confiando en la estructura de los tabs.
            with st.form("login_form", border=False):
                u = st.text_input("Usuario", placeholder="nombre_usuario")
                p = st.text_input("Contraseña", type="password")
                    
                st.markdown("<br>", unsafe_allow_html=True)
                # Botón centrado dentro del formulario
                submit_login = st.form_submit_button("Iniciar Sesión", use_container_width=True)

                if submit_login:
                    try:
                        resp = httpx.post(f"{DJANGO_URL}/login/", json={"username": u, "password": p})
                        if resp.status_code == 200:
                            st.session_state.token = resp.json()['access']
                            st.session_state.authenticated = True
                            st.success("¡Acceso concedido!")
                            st.rerun()
                        else: 
                            st.error("Usuario o contraseña incorrectos")
                    except Exception: 
                        st.error("Error de conexión: Revisa el servidor Django (Puerto 8001)")

            with tab_register:
                with st.form("reg_form", border=False):
                    nu = st.text_input("Nuevo Usuario")
                    np = st.text_input("Nueva Contraseña", type="password")
                    em = st.text_input("Email")
                    submit_reg = st.form_submit_button("Crear Cuenta", use_container_width=True)
                    
                    if submit_reg:
                        try:
                            resp = httpx.post(f"{DJANGO_URL}/register/", json={"username": nu, "password": np, "email": em})
                            if resp.status_code == 201: 
                                st.success("Cuenta creada exitosamente. Ya puedes iniciar sesión.")
                            else: 
                                st.error("El nombre de usuario ya está en uso.")
                        except Exception: 
                            st.error("Error de comunicación con la base de datos.")

# --- INTERFAZ PRINCIPAL (DESPUÉS DEL LOGIN) ---
if not st.session_state.authenticated:
    login_view()
else:
    # Barra lateral
    st.sidebar.title("🏥 OmniCare Pro")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.rerun()

    # Pestañas de Navegación
    tab_consulta, tab_historial = st.tabs(["💬 Nueva Consulta", "📁 Portal del Paciente"])

    with tab_consulta:
        col_chat, col_stats = st.columns([2, 1])

        with col_chat:
            st.subheader("Consulta Inteligente")
            # Contenedor con scroll para los mensajes
            chat_container = st.container(height=450)
            
            with chat_container:
                for msg in st.session_state.messages:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

            if prompt := st.chat_input("Describa sus síntomas..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with chat_container:
                    with st.chat_message("user"): st.markdown(prompt)
                    with st.chat_message("assistant"):
                        placeholder = st.empty()
                        res_container = {"text": ""}
                        
                        async def run_ai():
                            init_state = {
                                "messages": [HumanMessage(content=prompt)],
                                "patient_data": {"patient_id": "PAC-001"}, # ID ejemplo
                                "resource_focus": "Diagnóstico General"
                            }
                            async for event in medical_graph.astream_events(init_state, version="v2"):
                                if event["event"] == "on_chat_model_stream":
                                    chunk = event["data"]["chunk"].content
                                    if chunk:
                                        res_container["text"] += chunk
                                        placeholder.markdown(res_container["text"] + "▌")
                            return res_container["text"]

                        final_text = asyncio.run(run_ai())
                        st.session_state.messages.append({"role": "assistant", "content": final_text})
                        st.session_state.metricas = extraer_metricas(final_text)
                        
                        # --- GUARDAR AUDITORÍA EN DJANGO ---
                        try:
                            headers = {"Authorization": f"Bearer {st.session_state.token}"}
                            httpx.post(f"{DJANGO_URL}/audit-logs/", headers=headers, json={
                                "patient": 1, 
                                "input_query": prompt,
                                "ai_response": final_text,
                                "model_used": "LangGraph-Agent"
                            })
                        except: pass
                        
                        st.rerun()

        with col_stats:
            st.subheader("📊 Estado Actual")
            
            # 1. Ajustamos el tamaño a uno más pequeño (ej: 4x4 o 5x4)
            # Al ser barras verticales, un formato más cuadrado queda mejor
            fig, ax = plt.subplots(figsize=(4, 3.5)) 
            
            labels = ['Dolor', 'Urgencia', 'Riesgo']
            colors = ['#FF4B4B', '#FFAA00', '#1C83E1']
            
            # Dibujamos las barras
            ax.bar(labels, st.session_state.metricas, color=colors, width=0.6)
            
            # 2. Limpieza estética para que no se vea "amontonado"
            ax.set_ylim(0, 10)
            ax.set_ylabel("Escala", fontsize=9)
            ax.tick_params(axis='both', which='major', labelsize=8) # Letra más pequeña en ejes
            
            # Mostramos el gráfico
            # use_container_width=True hará que se ajuste al ancho de la columna pequeña
            st.pyplot(fig, use_container_width=True)
            
            # Alertas visuales debajo del gráfico compacto
            if st.session_state.metricas[1] > 7:
                st.error("🚨 PRIORIDAD ALTA")
            elif st.session_state.metricas[1] > 0:
                st.success("✅ Análisis estable")

    with tab_historial:
        st.subheader("📋 Tu Historial Médico")
        try:
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            logs = httpx.get(f"{DJANGO_URL}/audit-logs/", headers=headers).json()
            
            for log in logs:
                with st.expander(f"Consulta: {log['created_at'][:10]} - {log['input_query'][:40]}..."):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.caption("Resumen Médico:")
                        st.write(log['ai_response'])
                    with c2:
                        st.caption("Interpretación Paciente:")
                        st.success("Esta consulta indica que debes mantener reposo y seguir tu tratamiento habitual.")
            
            if logs:
                st.divider()
                
                # 1. Definimos una altura fija en pulgadas. 
                # En mobile, al apilarse, es mejor que no sean excesivamente altos.
                ALTURA_FIG = 3.0 
                
                # En Streamlit, las columnas [1.5, 1] se apilarán automáticamente en móvil.
                col_evolucion, col_estado = st.columns([1.5, 1])

                with col_evolucion:
                    st.markdown("### 📈 Evolución")
                    # Usamos un ancho ligeramente mayor para la evolución (aspect ratio)
                    fig_evol, ax_evol = plt.subplots(figsize=(6, ALTURA_FIG)) 
                    
                    fechas = [log['created_at'][:10] for log in logs[-5:]]
                    riesgos = [5, 7, 4, 8, 3] 
                    
                    ax_evol.plot(fechas, riesgos[:len(fechas)], marker='o', color='#1C83E1', linewidth=2)
                    ax_evol.set_ylim(0, 10)
                    ax_evol.tick_params(labelsize=8)
                    
                    # Limpieza para diseño minimalista
                    ax_evol.spines['top'].set_visible(False)
                    ax_evol.spines['right'].set_visible(False)
                    fig_evol.patch.set_facecolor('white')
                    ax_evol.patch.set_facecolor('white')
                    
                    plt.tight_layout()
                    # use_container_width=True es la CLAVE para el modo responsive
                    st.pyplot(fig_evol, use_container_width=True)

                with col_estado:
                    st.markdown("### 📊 Estado Actual")
                    # Usamos la MISMA ALTURA_FIG para que en Tablet/PC midan lo mismo
                    fig_est, ax_est = plt.subplots(figsize=(4, ALTURA_FIG)) 
                    
                    labels = ['Dolor', 'Urgencia', 'Riesgo']
                    colors = ['#FF4B4B', '#FFAA00', '#1C83E1']
                    
                    ax_est.bar(labels, st.session_state.metricas, color=colors, width=0.6)
                    ax_est.set_ylim(0, 10)
                    ax_est.tick_params(labelsize=8)
                    
                    # Misma limpieza visual
                    ax_est.spines['top'].set_visible(False)
                    ax_est.spines['right'].set_visible(False)
                    fig_evol.patch.set_facecolor('white')
                    ax_evol.patch.set_facecolor('white')
                    
                    plt.tight_layout()
                    # En móvil, esto hará que la barra ocupe el ancho completo de la pantalla
                    st.pyplot(fig_est, use_container_width=True)

        except Exception as e:
            st.info("No hay consultas previas registradas para este paciente.")