<p align="center">
  <a href="https://github.com/MarcoXMarquez/audicode">
    <picture>
      <source srcset="assets/audicodelogo.png" media="(prefers-color-scheme: dark)">
      <source srcset="assets/audicodelogo.png" media="(prefers-color-scheme: light)">
      <img src="assets/audicodelogo.png" alt="AudiCode logo" width="380">
    </picture>
  </a>
</p>
<p align="center">El agente autónomo open source de auditoría PIMS e IA (ISO/IEC 27701:2025).</p>
<p align="center">
  <a href="https://github.com/MarcoXMarquez/audicode"><img alt="ISO/IEC 27701:2025" src="https://img.shields.io/badge/ISO%2FIEC-27701%3A2025-7a182c?style=flat-square&labelColor=191918" /></a>
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/python-3.12%2B-f1ecec?style=flat-square&labelColor=191918&color=444243" /></a>
  <a href="https://ollama.com/"><img alt="Local & Cloud LLMs" src="https://img.shields.io/badge/modelos-Ollama%20%7C%20Gemini%20%7C%20OpenAI-7a182c?style=flat-square&labelColor=191918" /></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-AGPL--3.0-444243?style=flat-square&labelColor=191918" /></a>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.es.md">Español</a>
</p>

[![AudiCode Desktop UI](assets/screenshot.png)](https://github.com/MarcoXMarquez/audicode)

---

### Instalación

```bash
# Inicio Rápido (Clonar e Iniciar App de Escritorio)
git clone https://github.com/MarcoXMarquez/audicode.git
cd audicode
python -m venv venv
venv\Scripts\activate             # Windows (o source venv/bin/activate en macOS/Linux)
pip install -r requirements.txt
python audicode_desktop.py
```

```bash
# Gestores de paquetes
pipx install git+https://github.com/MarcoXMarquez/audicode.git
uv tool install git+https://github.com/MarcoXMarquez/audicode.git
```

> [!IMPORTANT]
> AudiCode necesita un modelo de lenguaje. Ejecuta [Ollama](https://ollama.com) en local (`ollama pull qwen2.5-coder:7b`) **o** añade una clave API de un proveedor en la nube desde la interfaz (ver [Primeros pasos](#primeros-pasos--requisitos)).

### Primeros pasos / Requisitos

- **Python 3.12+** (si ejecutas desde el código fuente) y `pip`.
- **Windows 10/11** para el `.exe` independiente (runtime Edge WebView2). En macOS/Linux, ejecuta desde el código fuente.
- **Un backend de modelo (uno de los dos):**
  1. **Local y privado:** instala [Ollama](https://ollama.com), ejecuta `ollama pull qwen2.5-coder:7b` y mantenlo activo (por defecto `http://localhost:11434`).
  2. **Nube:** abre la configuración de modelos/proveedores en la app y pega tu clave API (Gemini, OpenAI, Anthropic, ...). Las claves se cifran (Fernet) y se guardan en `data/api_keys.json`, con la llave de cifrado en `data/.key`; mantén `data/` fuera del control de versiones. Las claves de proveedor se configuran **en la interfaz**: `GEMINI_API_KEY` y `ANTHROPIC_API_KEY` **no** se leen del entorno. Solo `OPENAI_API_KEY` se lee de `.env`/entorno (para descubrir modelos compatibles con OpenAI).
- Opcional: copia `.env.example` a `.env` para ajustar la configuración.

### Desktop App (BETA)

AudiCode está diseñado como una **Aplicación Nativa de Escritorio** impulsada por `pywebview` (Edge WebView2 / WebKit), sin barra de direcciones de navegador, con ejecución de controles ISO/IEC 27701:2025 en un solo clic y privacidad local por defecto.

| Plataforma            | Descarga / Ejecutable                |
| --------------------- | ------------------------------------ |
| Windows (x64)         | [`AudiCode-v0.1.0-windows-x64.zip`](https://github.com/MarcoXMarquez/audicode/releases/download/v0.1.0-beta/AudiCode-v0.1.0-windows-x64.zip) (Ejecutable `AudiCode.exe`) |
| macOS (Apple Silicon / Intel) | Próximamente (mientras tanto, ejecutar desde el código fuente) |
| Linux                 | Próximamente (mientras tanto, ejecutar desde el código fuente) |

```bash
# Ejecutar ventana nativa de escritorio directamente
python audicode_desktop.py

# O en Windows mediante el lanzador sin consola
AudiCode_Desktop.bat
```

#### Directorio de Instalación y Prioridad de Configuración

AudiCode respeta el siguiente orden de prioridad para el descubrimiento de skills y configuración:

1. `$AUDICODE_SKILLS_DIR` - Directorio personalizado para módulos de auditoría ISO/IEC 27701:2025
2. `./skills` - Catálogo integrado de skills del repositorio
3. `./data/skills` - Skills de usuario en tiempo de ejecución
4. `.env` - Configuración del entorno local (`AUTH_ENABLED=false` por defecto para modo Desktop)

```bash
# Ejemplo
cp .env.example .env
python audicode_desktop.py
```

### Despliegue

AudiCode también puede ejecutarse como servicio web con Docker (`Dockerfile` / `docker-compose.yml`):

```bash
cp .env.example .env
docker compose up -d --build          # sirve en http://localhost:7000
docker compose --profile ollama up -d # además inicia un contenedor Ollama
```

- Puerto y dirección de enlace: `APP_PORT` (por defecto `7000`) y `APP_BIND`. Los datos persisten en el volumen `./data`.
- **Define `AUTH_ENABLED=true` antes de exponerlo fuera de localhost** y crea credenciales. Nunca lo publiques sin autenticación: puede leer archivos y ejecutar herramientas.
- Ponlo detrás de un reverse proxy con **HTTPS** (Caddy, nginx, Traefik) y define `SECURE_COOKIES=true`.
- Respalda `./data` (incluida `.key`) y manténla fuera del control de versiones.

### Agentes

AudiCode incluye dos agentes integrados entre los que puedes alternar presionando la tecla `Tab` directamente desde la barra de entrada:

- **audit** - Agente de inspección de solo lectura para evaluaciones de conformidad ISO/IEC 27701:2025
  - Analiza esquemas SQL DDL, avisos de privacidad, banners de cookies (CMP), contratos DPA y evaluaciones TIA sin modificar archivos
  - Genera matrices formales de No Conformidades (`PASS` / `FAIL`), validación de bases jurídicas y registros de evidencia normativa
  - Ideal para auditorías formales PIMS y análisis de brechas (Gap Analysis)
- **remediate** - Agente con acceso completo para remediación e ingeniería de privacidad
  - Genera migraciones SQL DDL minimizadas/seudonimizadas (ISO/IEC 20889), redacta adendas contractuales DPA conformes a la Tabla A.2 y ejecuta validaciones deterministas
  - Automatiza correcciones técnicas de Privacidad desde el Diseño (Privacy by Design)

También incluye el subagente **general** (`@general`) para correlaciones normativas multipaso (GDPR, LFPDPPP, LPDP, LGPD, EU AI Act) y búsquedas complejas de evidencia.

### Skills Deterministas (ISO/IEC 27701:2025)

AudiCode integra **8 módulos especializados de auditoría PIMS** listos para usar con un solo clic desde la interfaz (sin que el auditor tenga que invocar scripts de Python manualmente):

| Módulo Skill                  | Control ISO/IEC 27701:2025          | Alcance y Objeto de Auditoría                                                |
| ----------------------------- | ----------------------------------- | ---------------------------------------------------------------------------- |
| **privacy-policy-reviewer**   | Cláusula 5.2, A.1.3.3, A.1.3.4, A.3.3 | Audita avisos de privacidad, información por capas, bases legales y PIMS   |
| **consent-validator**         | A.1.2.4, A.1.2.5, A.1.3.5, A.2.2.4  | Valida banners CMP, casillas premarcadas, Consent Ledger y simetría opt-out  |
| **data-minimization-checker** | A.1.4.2, A.1.4.5–A.1.4.9, A.3.20    | Inspecciona esquemas SQL DDL, payloads JSON, biometría y purga de temporales |
| **pii-rights-manager**        | A.1.3.6–A.1.3.10, A.2.3.2           | Audita plazos de respuesta ARCO/DSAR, borrado físico y aviso a encargados    |
| **pia-reviewer**              | Cláusula 6.1.2, 8.2, A.1.2.6, A.2.2.2 | Evalúa Evaluaciones de Impacto en la Privacidad (PIA/EIPD) en proyectos IA |
| **pii-transfer-auditor**      | A.1.5.2, A.1.5.3, A.1.5.4, A.2.5.2  | Audita transferencias internacionales de PII, cláusulas SCC, BCR y TIA       |
| **processor-contract-validator** | A.1.2.7, A.1.2.8, A.2.2.2–A.2.2.7 | Verifica contratos B2B Cloud/SaaS frente a las cláusulas de la Tabla A.2     |
| **incident-response-planner** | A.3.11, A.3.12, B.3.12              | Genera planes de respuesta y notificación de brechas en 72 horas             |

### Documentación

- **Arquitectura Agnóstica de Modelos**: Conéctate a modelos locales vía **Ollama** (`qwen2.5-coder:7b`, `llama3.1`, `deepseek-r1`) para auditorías 100% privadas sin salida de datos, o alterna en tiempo real con modelos en la nube (**Google Gemini**, **OpenAI**, **Anthropic Claude**).
- **Experiencia Dummy-Proof para el Auditor**: Diseñada específicamente para auditores líderes, DPOs e ingenieros de privacidad: selecciona cualquier control ISO/IEC 27701:2025 desde la barra lateral o las píldoras de acción para ejecutar la auditoría al instante.

### Solución de problemas

| Problema | Solución |
| -------- | -------- |
| "No hay modelo disponible" / lista de modelos vacía | Inicia Ollama (`ollama serve`) y ejecuta `ollama pull qwen2.5-coder:7b`, o añade una clave API en la interfaz. |
| Una clave de Gemini/Anthropic en `.env` se ignora | Solo `OPENAI_API_KEY` se lee del entorno; introduce las demás claves en la interfaz. |
| La ventana de escritorio queda en blanco (Windows) | Instala el runtime Edge WebView2; como alternativa ejecuta `python app.py` y abre `http://localhost:7000`. |
| El puerto 7000 está ocupado | Cambia `APP_PORT` en `.env`. |
| Las claves no se descifran tras mover `data/` | Copia `data/.key` junto con `data/api_keys.json`, o vuelve a introducir las claves. |

### Contribuir

Consulta también [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) y [CHANGELOG.md](CHANGELOG.md).

Si deseas contribuir a AudiCode:

1. Haz un fork del repositorio y crea tu rama (`git checkout -b feat/nuevo-control-iso`).
2. Asegúrate de que cualquier nueva skill bajo `skills/<nombre-skill>/` incluya su especificación `SKILL.md` mapeada a controles de **ISO/IEC 27701:2025**.
3. Verifica que la aplicación de escritorio inicie correctamente con `python audicode_desktop.py`.

---

### Licencia, atribución y aviso

AudiCode es un fork del proyecto open source Odysseus y se distribuye bajo la licencia **GNU AGPL-3.0** (ver [LICENSE](LICENSE)). Si ejecutas una versión modificada como servicio de red, debes ofrecer su código fuente a sus usuarios. Créditos y agradecimiento a los autores originales de Odysseus.

AudiCode es una herramienta de apoyo, no constituye asesoría legal ni certifica por sí sola la conformidad con ISO/IEC 27701. Haz revisar sus resultados por un profesional cualificado.
