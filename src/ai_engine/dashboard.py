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
    # Usamos columnas para separar la App (izquierda) del Usuario (derecha)
    col_app, col_user = st.columns([3, 1.5])
    
    with col_app:
        # Logo y Nombre de la App alineados a la IZQUIERDA
        st.markdown("""
            <div style='display: flex; align-items: center; height: 100%; padding-top: 5px;'>
                <h1 style='margin: 0; font-size: 40px; line-height: 1;'>🏥 OmniCare AI</h1>
                <div style='margin-left: 15px; border-left: 3px solid #1C83E1; padding-left: 15px;'>
                    <span style='color: #1C83E1; font-weight: bold; font-size: 16px; display: block;'>SISTEMA MÉDICO</span>
                    <span style='color: #888; font-size: 12px; display: block;'>IA GENERATIVA</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_user:
        # Extraemos las variables del session_state
        dni_display = st.session_state.get("dni", "S/D")
        nombre_display = st.session_state.get("first_name", "Usuario")
        # Aseguramos que el rol esté en minúsculas para comparar bien
        rol_raw = st.session_state.get("role", "paciente").lower()
        rol_display = rol_raw.upper()
        
        # --- LÓGICA DE COLORES Y ETIQUETAS DIVIDIDA ---
        if rol_raw == "supervisor":
            id_name = "ID SUPERVISOR"
            color_rol = "#A200FF"  # Morado
        elif rol_raw == "medico":
            id_name = "ID MÉDICO"
            color_rol = "#1C83E1"  # Azul
        else:
            id_name = "ID PACIENTE"
            color_rol = "#28A745"  # Verde

        # ESTRUCTURA FINAL: Grande y sin espacios muertos
        st.markdown(f"""
            <div style="
                background-color: #262730; 
                padding: 8px 15px; 
                border-radius: 10px; 
                border-right: 8px solid {color_rol};
                display: flex;
                flex-direction: column;
                align-items: flex-end;
                justify-content: center;
                gap: 0px;
            ">
                <span style="color: {color_rol}; font-size: 13px; font-weight: bold; margin: 0; line-height: 0.8;">{id_name}</span>
                <span style="font-size: 35px; color: white; font-family: monospace; font-weight: bold; margin: 0; line-height: 1;">{dni_display}</span>
                <span style="font-size: 20px; color: #EEE; font-weight: bold; margin: 0; line-height: 0.9;">{nombre_display}</span>
                <div style="margin-top: 4px; line-height: 1;">
                    <span style="font-size: 14px; color: {color_rol}; font-weight: bold;">● {rol_display}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Ajuste para pegar el divisor al header
    st.markdown("<div style='margin-top: -15px;'></div>", unsafe_allow_html=True)
    st.divider()
    
    
# --- ESTADOS ---
if "authenticated" not in st.session_state:
    st.session_state.update({
        "authenticated": False, "token": None, "credential": None, 
        "role": None, "messages": [], "metricas": [0, 0, 0], "history_loaded": False
    })

# --- LOGIN ---
if not st.session_state.authenticated:
    _, col_center, _ = st.columns([1.2, 1, 1.2])
    with col_center:
        st.markdown("<br><br><h2 style='text-align: center;'>OmniCare AI</h2>", unsafe_allow_html=True)
        with st.form("login_form", border=True):
            u = st.text_input("DNI o Email")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Iniciar Sesión", width='stretch'):
                try:
                    payload = {"credential": u, "password": p}
                    resp = httpx.post(f"{DJANGO_URL}/login/", json=payload, timeout=10.0)
                    
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.update({
                            "token": data['access'], 
                            "dni": data['dni'],           # <--- Cambiado de 'credential' a 'dni' para el header
                            "first_name": data['first_name'],
                            "authenticated": True, 
                            "role": data['role']
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
        t1, t2 = st.tabs(["📋 Listado de Personal", "➕ Registrar Nuevo Médico"])
        
        with t1:
            st.markdown("### Panel de Gestión de Facultativos")
            
            resp = httpx.get(f"{DJANGO_URL}/medicos-list/", headers=headers)
            if resp.status_code == 200:
                medicos = resp.json()
                df_medicos = pd.DataFrame(medicos)

                if not df_medicos.empty:
                    # --- GRÁFICO DE CARGA DE TRABAJO ---
                    st.write("#### Distribución de Pacientes")
                    # Creamos un gráfico simple pero efectivo
                    chart_data = df_medicos[['first_name', 'num_pacientes']].set_index('first_name')
                    st.bar_chart(chart_data, color="#1C83E1")

                    st.divider()

                    # --- BUSCADOR ---
                    search = st.text_input("🔍 Buscar por DNI o Nombre", placeholder="Ej: 12345678X")

                    filtered_medicos = medicos
                    if search:
                        search_lower = search.lower()
                        filtered_medicos = [
                            m for m in medicos 
                            if search_lower in str(m.get('username', '')).lower() or 
                            search_lower in str(m.get('first_name', '')).lower()
                        ]

                    for m in filtered_medicos:
                        # Usamos .get('username') que es lo que ahora envía Django
                        dni_display = m.get('username', 'S/D') 
                        
                        with st.expander(f"Dr/a. {m.get('first_name')} {m.get('last_name')}"):
                            c1, c2 = st.columns(2)
                            c1.write(f"📧 **Email:** {m.get('email')}")
                            c1.write(f"🆔 **DNI:** {dni_display}")
                            c2.metric("Pacientes", m.get('num_pacientes', 0))
                            solicitar_baja("medico", m.get('id'), dni_display)
        with t2:
            st.markdown("### 👨‍⚕️ Registro de Personal Médico")
            
            # Inicializamos los campos en el session_state si no existen
            for key in ['dni', 'nom', 'ape', 'col', 'ema']:
                if key not in st.session_state:
                    st.session_state[key] = ""

            # Eliminamos 'clear_on_submit=True' para controlar la limpieza nosotros
            with st.form("add_med"):
                col1, col2 = st.columns(2)
                with col1:
                    dni = st.text_input("DNI (Identificador Único)", value=st.session_state.dni)
                    nombre = st.text_input("Nombre", value=st.session_state.nom)
                    colegiado = st.text_input("Nº Carnet de Médico", value=st.session_state.col)
                with col2:
                    apellidos = st.text_input("Apellidos", value=st.session_state.ape)
                    email = st.text_input("Email Corporativo", value=st.session_state.ema)
                    pass1 = st.text_input("Contraseña", type="password")
                    pass2 = st.text_input("Confirmar Contraseña", type="password")
                
                if st.form_submit_button("Dar de Alta en Sistema", width='stretch'):
                    # 1. Validación de campos vacíos
                    if not all([dni, nombre, apellidos, colegiado, email, pass1, pass2]):
                        st.error("⚠️ No se ha podido dar de alta: faltan campos obligatorios.")
                    
                    # 2. Validación de coincidencia y longitud (Aquí NO se borran los datos)
                    elif pass1 != pass2:
                        st.error("⚠️ Las contraseñas no coinciden.")
                    elif len(pass1) < 8:
                        st.error("⚠️ La contraseña debe tener al menos 8 caracteres.")
                        
                    else:
                        try:
                            payload = {
                                "credential": dni, "first_name": nombre, "last_name": apellidos,
                                "email": email, "password": pass1, "is_staff": True, "colegiado": colegiado
                            }
                            resp = httpx.post(f"{DJANGO_URL}/register/", json=payload)
                            
                            if resp.status_code == 201:
                                # 1. Guardamos el mensaje de éxito en el estado de la sesión
                                st.session_state.registro_exitoso = f"✅ ¡Éxito! El registro se ha completado correctamente."
                                
                                # 2. Limpiamos los campos del formulario
                                for key in ['dni', 'nom', 'ape', 'col', 'ema']:
                                    if key in st.session_state:
                                        st.session_state[key] = ""
                                
                                # 3. Recargamos la aplicación
                                st.rerun()
                            else:
                                error_msg = resp.json().get('error', 'Error en el servidor')
                                st.error(f"Fallo: {error_msg}")
                        except Exception as e:
                            st.error(f"Error de conexión: {e}")

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
                        if st.button(f"📥 Descargar PDF", key=f"pdf_{p['patient_id']}", use_container_width=True):
                            with st.spinner("Analizando historial y generando reporte..."):
                                try:
                                    pdf_r = httpx.get(f"{DJANGO_URL}/export-pdf/{p['patient_id']}/", headers=headers, timeout=15.0)
                                    
                                    if pdf_r.status_code == 200:
                                        st.download_button(
                                            label="✅ Confirmar Descarga PDF",
                                            data=pdf_r.content,
                                            file_name=f"historial_{p['patient_id']}.pdf",
                                            mime="application/pdf",
                                            use_container_width=True
                                        )
                                    elif pdf_r.status_code == 404:
                                        # Caso específico: El paciente existe pero no hay logs ni historial para el PDF
                                        st.warning("⚠️ No se puede generar el PDF: El paciente aún no tiene consultas ni historial registrado.")
                                    elif pdf_r.status_code == 204:
                                        st.info("ℹ️ El historial clínico está vacío.")
                                    else:
                                        # Error técnico real
                                        st.error(f"❌ Error técnico ({pdf_r.status_code}). El servicio de exportación no pudo procesar la solicitud.")
                                        
                                except httpx.ConnectError:
                                    st.error("📡 No se pudo conectar con el servidor. Verifica que el backend esté activo.")
                                except Exception as e:
                                    st.error(f"⚠️ Error inesperado: {str(e)}")

                    solicitar_baja("paciente", p['patient_id'], p['name'])

    elif menu == "➕ Alta de Paciente":
        st.subheader("Registrar Nuevo Paciente")
        
        # --- MENSAJE DE ÉXITO PERSISTENTE ---
        if "paciente_exitoso" in st.session_state:
            st.success(st.session_state.paciente_exitoso)
            del st.session_state.paciente_exitoso
            st.balloons()

        # Inicializamos session_state para pacientes si no existe
        for k in ['p_id', 'p_nm', 'p_em', 'p_hst']:
            if k not in st.session_state: st.session_state[k] = ""

        with st.form("alta_p"):
            col1, col2 = st.columns(2)
            with col1:
                pid = st.text_input("DNI/ID", value=st.session_state.p_id)
                pnm = st.text_input("Nombre Completo", value=st.session_state.p_nm)
            with col2:
                pem = st.text_input("Email", value=st.session_state.p_em)
                pps = st.text_input("Contraseña Temporal", type="password")
            
            phst = st.text_area("Historial Clínico Inicial", value=st.session_state.p_hst)
            
            if st.form_submit_button("Finalizar Alta", width='stretch'):
                if not all([pid, pnm, pem, pps, phst]):
                    st.error("⚠️ No se ha podido dar de alta al paciente porque hay campos vacíos.")
                elif len(pps) < 8:
                    st.error("⚠️ La contraseña temporal debe tener al menos 8 caracteres.")
                else:
                    try:
                        # 1. Crear usuario
                        r_user = httpx.post(f"{DJANGO_URL}/register/", json={"credential": pid, "password": pps, "email": pem})
                        # 2. Crear ficha médica
                        r_patient = httpx.post(f"{DJANGO_URL}/manage-patients/", 
                                               json={"patient_id": pid, "name": pnm, "clinical_history": phst}, 
                                               headers=headers)
                        
                        if r_patient.status_code == 201:
                            st.session_state.paciente_exitoso = f"Paciente {pnm} registrado con éxito."
                            # Limpiamos campos
                            for k in ['p_id', 'p_nm', 'p_em', 'p_hst']: st.session_state[k] = ""
                            st.rerun()
                        else:
                            st.error(f"Error en ficha médica: {r_patient.json().get('error', 'Error desconocido')}")
                    except Exception as e:
                        st.error(f"Error de conexión: {e}")
                        

    elif menu == "📊 Auditoría":
        st.subheader("🛡️ Auditoría Avanzada de Consultas IA")
        try:
            r_audit = httpx.get(f"{DJANGO_URL}/audit-logs/", headers=headers)
            
            if r_audit.status_code == 200:
                audit_data = r_audit.json()
                
                if audit_data:
                    df_audit = pd.DataFrame(audit_data)
                    
                    # 1. Aseguramos que los campos sean numéricos para poder compararlos
                    for col in ['riesgo', 'urgencia', 'dolor']:
                        if col in df_audit.columns:
                            df_audit[col] = pd.to_numeric(df_audit[col], errors='coerce').fillna(0)

                    # 2. FUNCIÓN DE CATEGORIZACIÓN (Tu lógica de negocio)
                    def categorizar_con_valor(valor):
                        # Aseguramos que el valor sea entero para la visualización
                        v = int(valor)
                        if v <= 3: 
                            return f"Bajo 🟢 ({v})"
                        elif v <= 7: 
                            return f"Medio 🟡 ({v})"
                        else: 
                            return f"Alto 🔴 ({v})"

                    # Creamos las columnas de texto basadas en los números
                    df_audit['riesgo_label'] = df_audit['riesgo'].apply(categorizar_con_valor)
                    df_audit['urgencia_label'] = df_audit['urgencia'].apply(categorizar_con_valor)

                    # --- PANEL DE CONTROL ---
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Volumen de Consultas", len(df_audit))
                    
                    # Contamos los "Altos" usando la nueva etiqueta
                    alertas_altas = len(df_audit[df_audit['riesgo'] >= 8])
                    c2.metric("Alertas de Riesgo Alto", alertas_altas, delta_color="inverse")
                    
                    if 'fecha' in df_audit.columns:
                        ultima = pd.to_datetime(df_audit['fecha']).max().strftime('%H:%M:%S')
                        c3.metric("Última Interacción", ultima)

                    st.divider()

                    # --- TABLA TÉCNICA ---
                    # Mapeamos las columnas incluyendo las nuevas etiquetas
                    columnas_config = {
                        "fecha": "Marca Temporal",
                        "paciente": "ID Paciente",
                        "dolor": "Dolor (Num)",
                        "urgencia_label": "Prioridad Urgencia",
                        "riesgo_label": "Nivel de Riesgo IA",
                        "mensaje_usuario": "Consulta",
                        "respuesta_ia": "Respuesta IA"
                    }

                    cols_presentes = [c for c in columnas_config.keys() if c in df_audit.columns]
                    df_visual = df_audit[cols_presentes].rename(columns=columnas_config)

                    # Mostramos la tabla
                    st.dataframe(
                        df_visual,
                        use_container_width=True,
                        column_config={
                            "Marca Temporal": st.column_config.DatetimeColumn(format="DD/MM/YYYY HH:mm"),
                            "Nivel de Riesgo IA": st.column_config.TextColumn(help="Bajo (0-3), Medio (4-7), Alto (8-10)"),
                            "Respuesta IA": st.column_config.TextColumn(width="large")
                        }
                    )
                else:
                    st.info("No se han registrado logs de auditoría aún.")
            else:
                st.error(f"Error: {r_audit.status_code}")
        except Exception as e:
            st.error(f"Error en el módulo de logs: {e}")
    
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
                            "patient_data": {"patient_id": st.session_state.dni}, # Usamos 'dni' aquí también
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
            st.info(f"**Usuario:** {st.session_state.credential}\n\n**Rol:** {st.session_state.role.capitalize()}")
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
