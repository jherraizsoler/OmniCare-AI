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
    riesgos = 7 if any(w in texto for w in ["grave", "crítico", "complicado"]) else 2
    return [dolor, urgencia, riesgos]

def render_header():
    """Renderiza el banner superior con el logo y el nombre del usuario"""
    col_brand, col_spacer, col_user = st.columns([2, 1, 1.5])
    
    with col_brand:
        st.markdown(
            """
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 2rem; margin-right: 10px;'>🏥</span>
                <h1 style='margin: 0; font-size: 1.8rem;'>OmniCare AI</h1>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with col_user:
        username = st.session_state.get('username', 'Usuario')
        st.markdown(
            f"""
            <div style='text-align: right; padding-top: 10px;'>
                <span style='color: gray;'>Bienvenido,</span><br>
                <strong>{username}</strong>
            </div>
            """, 
            unsafe_allow_html=True
        )
    st.divider()

# --- INICIALIZACIÓN DE ESTADOS ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "metricas" not in st.session_state:
    st.session_state.metricas = [0, 0, 0]

# --- VISTA DE LOGIN ---
def login_view():
    empty_l, col_center, empty_r = st.columns([1.2, 1, 1.2])
    
    with col_center:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>OmniCare AI</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Acceso al Portal Médico</p>", unsafe_allow_html=True)
        
        tab_login, tab_register = st.tabs(["Entrar", "Nueva Cuenta"])
        
        with tab_login:
            with st.form("login_form", border=False):
                u = st.text_input("Usuario", placeholder="nombre_usuario")
                p = st.text_input("Contraseña", type="password")
                st.markdown("<br>", unsafe_allow_html=True)
                submit_login = st.form_submit_button("Iniciar Sesión", use_container_width=True)

                if submit_login:
                    try:
                        resp = httpx.post(f"{DJANGO_URL}/login/", json={"username": u, "password": p})
                        if resp.status_code == 200:
                            st.session_state.token = resp.json()['access']
                            st.session_state.username = u
                            st.session_state.authenticated = True
                            st.rerun()
                        else: 
                            st.error("Usuario o contraseña incorrectos")
                    except Exception: 
                        st.error("Error de conexión con el servidor")

        with tab_register:
            with st.form("reg_form", border=False):
                nu = st.text_input("Nuevo Usuario")
                np = st.text_input("Nueva Contraseña", type="password")
                em = st.text_input("Email")
                submit_reg = st.form_submit_button("Crear Cuenta", use_container_width=True)
                if submit_reg:
                    try:
                        resp = httpx.post(f"{DJANGO_URL}/register/", json={"username": nu, "password": np, "email": em})
                        if resp.status_code == 201: st.success("¡Cuenta creada!")
                        else: st.error("Error en el registro")
                    except Exception: st.error("Error de servidor")

# --- INTERFAZ PRINCIPAL ---
if not st.session_state.authenticated:
    login_view()
else:
    render_header()
    
    # Barra lateral minimalista
    if st.sidebar.button("Cerrar Sesión", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    tab_consulta, tab_historial = st.tabs(["💬 Nueva Consulta", "📁 Portal del Paciente"])

    with tab_consulta:
        col_chat, col_stats = st.columns([2, 1])

        with col_chat:
            st.subheader("Consulta Inteligente")
            chat_container = st.container(height=450)
            
            with chat_container:
                for msg in st.session_state.messages:
                    with st.chat_message(msg["role"]): st.markdown(msg["content"])

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
                                "patient_data": {"patient_id": "PAC-001"},
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
                        
                        try:
                            headers = {"Authorization": f"Bearer {st.session_state.token}"}
                            httpx.post(f"{DJANGO_URL}/audit-logs/", headers=headers, json={
                                "patient": 1, "input_query": prompt, "ai_response": final_text, "model_used": "LangGraph-Agent"
                            })
                        except: pass
                        st.rerun()

        with col_stats:
            st.subheader("📊 Estado Actual")
            fig, ax = plt.subplots(figsize=(4, 3.5)) 
            labels = ['Dolor', 'Urgencia', 'Riesgo']
            colors = ['#FF4B4B', '#FFAA00', '#1C83E1']
            
            ax.bar(labels, st.session_state.metricas, color=colors, width=0.6)
            ax.set_ylim(0, 10)
            ax.set_ylabel("Escala")
            ax.tick_params(labelsize=8)
            
            st.pyplot(fig, use_container_width=True)
            
            if st.session_state.metricas[1] > 7: st.error("🚨 PRIORIDAD ALTA")
            elif st.session_state.metricas[1] > 0: st.success("✅ Análisis estable")

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
                        st.caption("Interpretación:")
                        st.success("Consulta analizada correctamente por OmniCare AI.")
            
            if logs:
                st.divider()
                ALTURA_FIG = 3.5 
                col_evolucion, col_estado_hist = st.columns([1.5, 1])

                with col_evolucion:
                    st.markdown("### 📈 Evolución")
                    fig_evol, ax_evol = plt.subplots(figsize=(6, ALTURA_FIG)) 
                    fig_evol.patch.set_facecolor('white')
                    ax_evol.patch.set_facecolor('white')
                    
                    fechas = [log['created_at'][:10] for log in logs[-5:]]
                    riesgos_evol = [5, 7, 4, 8, 3] # Mapear datos reales aquí
                    
                    ax_evol.plot(fechas, riesgos_evol[:len(fechas)], marker='o', color='#1C83E1', linewidth=2)
                    ax_evol.set_ylim(0, 10)
                    ax_evol.set_ylabel("Nivel de Riesgo", color='black')
                    ax_evol.tick_params(colors='black', labelsize=8)
                    ax_evol.spines['top'].set_visible(False)
                    ax_evol.spines['right'].set_visible(False)
                    
                    plt.tight_layout()
                    st.pyplot(fig_evol, use_container_width=True)

                with col_estado_hist:
                    st.markdown("### 📊 Estado Actual")
                    fig_est, ax_est = plt.subplots(figsize=(4, ALTURA_FIG)) 
                    fig_est.patch.set_facecolor('white')
                    ax_est.patch.set_facecolor('white')
                    
                    labels = ['Dolor', 'Urgencia', 'Riesgo']
                    colors = ['#FF4B4B', '#FFAA00', '#1C83E1']
                    
                    ax_est.bar(labels, st.session_state.metricas, color=colors, width=0.6)
                    ax_est.set_ylim(0, 10)
                    ax_est.set_ylabel("Escala", color='black')
                    ax_est.tick_params(colors='black', labelsize=8)
                    ax_est.spines['top'].set_visible(False)
                    ax_est.spines['right'].set_visible(False)
                    
                    plt.tight_layout()
                    st.pyplot(fig_est, use_container_width=True)

        except Exception as e:
            st.info("No hay consultas previas registradas.")