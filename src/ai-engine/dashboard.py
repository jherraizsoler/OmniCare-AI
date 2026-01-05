import streamlit as st
import httpx
import matplotlib.pyplot as plt
import asyncio
import pandas as pd
from langchain_core.messages import HumanMessage
from graph_engine import medical_graph

# --- CONFIGURACIÓN ---
DJANGO_URL = "http://localhost:8001/api"
st.set_page_config(page_title="OmniCare Pro", layout="wide", page_icon="🏥")

# --- FUNCIONES DE APOYO ---
def extraer_metricas(texto):
    texto = texto.lower()
    dolor = 8 if any(w in texto for w in ["fuerte", "intenso", "agudo", "10/10"]) else 4
    urgencia = 9 if any(w in texto for w in ["urgente", "emergencia", "inmediata"]) else 3
    riesgo = 7 if any(w in texto for w in ["grave", "crítico", "complicado"]) else 2
    return [dolor, urgencia, riesgo]

def solicitar_baja(tipo, id_entidad, nombre):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    endpoint = f"medicos-delete/{id_entidad}/" if tipo == "medico" else f"patients/{id_entidad}/"
    if st.button(f"Confirmar baja de {nombre}", key=f"del_{id_entidad}", type="primary", width='stretch'):
        try:
            r = httpx.delete(f"{DJANGO_URL}/{endpoint}", headers=headers)
            if r.status_code in [200, 204]:
                st.success(f"{nombre} eliminado."); st.rerun()
            else: st.error(f"Error: {r.text}")
        except Exception as e: st.error(f"Error de conexión: {e}")

def render_header():
    col_brand, _, col_user = st.columns([2, 1, 1.5])
    with col_brand:
        rol_display = st.session_state.role.upper() if st.session_state.role else ""
        st.markdown(f"### 🏥 OmniCare AI <span style='color: #1C83E1; font-size: 0.8em;'>[{rol_display}]</span>", unsafe_allow_html=True)
    with col_user:
        username = st.session_state.get('username', 'Usuario')
        emoji = "🛡️" if st.session_state.role == "supervisor" else "👨‍⚕️" if st.session_state.role == "medico" else "👤"
        st.markdown(f"<div style='text-align: right;'><strong>{username}</strong><br><span style='color: gray;'>{emoji} {st.session_state.role}</span></div>", unsafe_allow_html=True)
    st.divider()

# --- ESTADOS ---
if "authenticated" not in st.session_state:
    st.session_state.update({
        "authenticated": False, "token": None, "username": None, 
        "role": None, "messages": [], "metricas": [0, 0, 0], "history_loaded": False
    })

# --- LOGIN ---
if not st.session_state.authenticated:
    _, col_center, _ = st.columns([1.2, 1, 1.2])
    with col_center:
        st.markdown("<br><br><h2 style='text-align: center;'>OmniCare AI</h2>", unsafe_allow_html=True)
        with st.form("login_form", border=True):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Iniciar Sesión", width='stretch'):
                try:
                    resp = httpx.post(f"{DJANGO_URL}/login/", json={"username": u, "password": p}, timeout=10.0)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.update({
                            "token": data['access'], "username": u, 
                            "authenticated": True, "role": data['role']
                        })
                        st.success("¡Login exitoso!"); st.rerun()
                    else: st.error("Credenciales inválidas")
                except Exception as e: st.error(f"Error de conexión: {e}")
else:
    render_header()
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    # --- NAVEGACIÓN ---
    st.sidebar.title("🏥 Navegación")
    if st.session_state.role == "supervisor":
        opciones = ["👨‍⚕️ Médicos", "📊 Auditoría", "👤 Mi Perfil"]
    elif st.session_state.role == "medico":
        opciones = ["📋 Mis Pacientes", "➕ Alta de Paciente", "👤 Mi Perfil"]
    else:
        opciones = ["💬 Chat Médico", "👤 Mi Perfil"]

    menu = st.sidebar.radio("Ir a:", opciones)
    st.sidebar.divider()
    if st.sidebar.button("🚪 Cerrar Sesión", width='stretch'):
        st.session_state.clear(); st.rerun()

    # --- LÓGICA DE CONTENIDO ---

    if menu == "👨‍⚕️ Médicos":
        t1, t2 = st.tabs(["Personal", "Nuevo Médico"])
        with t1:
            resp = httpx.get(f"{DJANGO_URL}/medicos-list/", headers=headers)
            if resp.status_code == 200:
                for m in resp.json():
                    with st.expander(f"Dr/a. {m['username']}"):
                        st.write(f"Email: {m['email']}")
                        solicitar_baja("medico", m['id'], m['username'])
        with t2:
            with st.form("add_med"):
                nu, ne, np = st.text_input("User"), st.text_input("Email"), st.text_input("Pass", type="password")
                if st.form_submit_button("Crear Médico", width='stretch'):
                    httpx.post(f"{DJANGO_URL}/register/", json={"username": nu, "email": ne, "password": np, "is_staff": True})
                    st.success("Médico creado"); st.rerun()

    elif menu == "📋 Mis Pacientes":
        st.subheader("Mis Pacientes Asignados")
        resp = httpx.get(f"{DJANGO_URL}/manage-patients/", headers=headers)
        
        if resp.status_code == 200:
            for p in resp.json():
                with st.expander(f"👤 {p['name']} (ID: {p['patient_id']})"):
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        if st.button(f"📊 Ver Evolución", key=f"evol_{p['patient_id']}", width='stretch'):
                            # Ajuste del endpoint para historial específico
                            r_h = httpx.get(f"{DJANGO_URL}/historial-paciente/{p['patient_id']}/", headers=headers)
                            if r_h.status_code == 200 and r_h.json():
                                df = pd.DataFrame(r_h.json())
                                st.line_chart(df.set_index('fecha')[['dolor', 'urgencia', 'riesgo']])
                            else: st.info("Sin registros de IA.")

                    with col_btn2:
                        if st.button(f"📥 Descargar PDF", key=f"pdf_{p['patient_id']}", width='stretch'):
                            with st.spinner("Generando reporte..."):
                                pdf_r = httpx.get(f"{DJANGO_URL}/export-pdf/{p['patient_id']}/", headers=headers)
                                if pdf_r.status_code == 200:
                                    st.download_button(
                                        label="Confirmar Descarga PDF",
                                        data=pdf_r.content,
                                        file_name=f"historial_{p['patient_id']}.pdf",
                                        mime="application/pdf",
                                        width='stretch'
                                    )
                                else: st.error("Error al generar PDF. Revisa las URLs en Django.")

                    solicitar_baja("paciente", p['patient_id'], p['name'])

    elif menu == "➕ Alta de Paciente":
        st.subheader("Registrar Paciente")
        with st.form("alta_p"):
            pid, pnm, pem = st.text_input("DNI/ID"), st.text_input("Nombre"), st.text_input("Email")
            pps, phst = st.text_input("Pass Temporal", type="password"), st.text_area("Historial")
            if st.form_submit_button("Finalizar Alta", width='stretch'):
                httpx.post(f"{DJANGO_URL}/register/", json={"username": pid, "password": pps, "email": pem})
                r = httpx.post(f"{DJANGO_URL}/manage-patients/", json={"patient_id": pid, "name": pnm, "clinical_history": phst}, headers=headers)
                if r.status_code == 201: st.success("Registrado"); st.rerun()
    elif menu == "📊 Auditoría":
        st.subheader("🛡️ Auditoría Avanzada de Consultas IA")
        try:
            # Petición al endpoint de auditoría
            r_audit = httpx.get(f"{DJANGO_URL}/audit-logs/", headers=headers)
            if r_audit.status_code == 200:
                audit_data = r_audit.json()
                
                if audit_data:
                    df_audit = pd.DataFrame(audit_data)
                    
                    # --- PANEL DE CONTROL (BIG DATA) ---
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Volumen de Consultas", len(df_audit))
                    if 'model_used' in df_audit.columns:
                        c2.metric("LLM Principal", df_audit['model_used'].mode()[0])
                    c3.metric("Última Interacción", pd.to_datetime(df_audit['created_at']).max().strftime('%H:%M:%S'))

                    st.divider()

                    # --- TABLA TÉCNICA DINÁMICA ---
                    # Mapeamos los campos del serializador a nombres profesionales
                    columnas_config = {
                        "created_at": "Marca Temporal",
                        "patient": "ID Paciente",  # Gracias al SlugRelatedField aquí viene el patient_id
                        "model_used": "Motor LLM",
                        "agent_name": "Agente Emisor",
                        "input_query": "Input del Paciente",
                        "ai_response": "Respuesta Generada"
                    }

                    # Filtramos solo las columnas que realmente devuelve el JSON
                    cols_presentes = [c for c in columnas_config.keys() if c in df_audit.columns]
                    df_visual = df_audit[cols_presentes].rename(columns=columnas_config)

                    st.dataframe(
                        df_visual,
                        use_container_width=True,
                        column_config={
                            "Marca Temporal": st.column_config.DatetimeColumn(format="DD/MM/YYYY HH:mm"),
                            "Respuesta Generada": st.column_config.TextColumn(width="large"),
                            "ID Paciente": st.column_config.TextColumn(help="Identificador único del paciente (Slug)")
                        }
                    )
                else:
                    st.info("No se han registrado logs de auditoría aún.")
            else:
                st.error(f"Error de comunicación con la API: {r_audit.status_code}")
        except Exception as e:
            st.error(f"Error en el módulo de análisis de logs: {e}")
    
    elif menu == "💬 Chat Médico":
        if not st.session_state.history_loaded:
            try:
                r_hist = httpx.get(f"{DJANGO_URL}/historial-paciente/", headers=headers)
                if r_hist.status_code == 200:
                    for c in r_hist.json():
                        st.session_state.messages.append({"role": "user", "content": c['mensaje_usuario']})
                        st.session_state.messages.append({"role": "assistant", "content": c['respuesta_ia']})
                    st.session_state.history_loaded = True
            except: pass

        col_chat, col_viz = st.columns([2, 1])
        with col_chat:
            box = st.container(height=500)
            for m in st.session_state.messages:
                with box.chat_message(m["role"]): st.markdown(m["content"])

            if prmpt := st.chat_input("Describa sus síntomas..."):
                st.session_state.messages.append({"role": "user", "content": prmpt})
                with box.chat_message("user"): st.markdown(prmpt)
                
                with box.chat_message("assistant"):
                    ph = st.empty()
                    # Contenedor mutable para evitar problemas de scope (SyntaxError nonlocal)
                    res_container = {"text": ""} 
                    
                    async def run_chat():
                        state = {
                            "messages": [HumanMessage(content=prmpt)], 
                            "patient_data": {"patient_id": st.session_state.username}, 
                            "resource_focus": "Consulta"
                        }
                        async for ev in medical_graph.astream_events(state, version="v2"):
                            if ev["event"] == "on_chat_model_stream":
                                chunk = ev["data"]["chunk"].content
                                if chunk: 
                                    res_container["text"] += chunk
                                    ph.markdown(res_container["text"] + "▌")
                        return res_container["text"]

                    final = asyncio.run(run_chat())
                    st.session_state.messages.append({"role": "assistant", "content": final})
                    
                    # Persistencia de métricas
                    met = extraer_metricas(final)
                    st.session_state.metricas = met
                    try:
                        httpx.post(f"{DJANGO_URL}/guardar-consulta/", 
                                   json={"mensaje": prmpt, "respuesta": final, 
                                         "dolor": met[0], "urgencia": met[1], "riesgo": met[2]}, 
                                   headers=headers)
                    except: pass
                    st.rerun()

        with col_viz:
            st.markdown("#### Triaje Actual")
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.bar(['Dolor', 'Urgencia', 'Riesgo'], st.session_state.metricas, color=['#FF4B4B', '#FFAA00', '#1C83E1'])
            ax.set_ylim(0, 10)
            st.pyplot(fig)

    elif menu == "👤 Mi Perfil":
        st.subheader("Configuración de Perfil")
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**Usuario:** {st.session_state.username}\n\n**Rol:** {st.session_state.role.capitalize()}")
        with c2:
            st.markdown("#### Cambiar Contraseña")
            with st.form("f_pass"):
                n1, n2 = st.text_input("Nueva", type="password"), st.text_input("Confirmar", type="password")
                if st.form_submit_button("Actualizar", width='stretch'):
                    if n1 == n2 and len(n1) >= 4:
                        r = httpx.post(f"{DJANGO_URL}/change-password/", json={"new_password": n1}, headers=headers)
                        if r.status_code == 200: st.success("Contraseña actualizada")
                        else: st.error("Error en servidor")
                    else: st.error("Las contraseñas no coinciden")