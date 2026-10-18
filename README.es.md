<p align="center">
  <a href="https://github.com/audicode/audicode">
    <picture>
      <source srcset="assets/audicodelogo.png" media="(prefers-color-scheme: dark)">
      <source srcset="assets/audicodelogo.png" media="(prefers-color-scheme: light)">
      <img src="assets/audicodelogo.png" alt="AudiCode logo" width="380">
    </picture>
  </a>
</p>
<p align="center">El agente autónomo open source de auditoría PIMS e IA (ISO/IEC 27701:2025).</p>
<p align="center">
  <a href="https://github.com/audicode/audicode"><img alt="ISO/IEC 27701:2025" src="https://img.shields.io/badge/ISO%2FIEC-27701%3A2025-7a182c?style=flat-square&labelColor=191918" /></a>
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/python-3.12%2B-f1ecec?style=flat-square&labelColor=191918&color=444243" /></a>
  <a href="https://ollama.com/"><img alt="Local & Cloud LLMs" src="https://img.shields.io/badge/modelos-Ollama%20%7C%20Gemini%20%7C%20OpenAI-7a182c?style=flat-square&labelColor=191918" /></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-AGPL--3.0-444243?style=flat-square&labelColor=191918" /></a>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.es.md">Español</a>
</p>

[![AudiCode Desktop UI](assets/screenshot.png)](https://github.com/audicode/audicode)

---

### Instalación

```bash
# Inicio Rápido (Clonar e Iniciar App de Escritorio)
git clone https://github.com/audicode/audicode.git
cd audicode
python -m venv venv
venv\Scripts\activate             # Windows (o source venv/bin/activate en macOS/Linux)
pip install -r requirements.txt
python audicode_desktop.py
```

```bash
# Gestores de paquetes
pipx install git+https://github.com/audicode/audicode.git
uv tool install git+https://github.com/audicode/audicode.git
```

> [!TIP]
> Asegúrate de tener [Ollama](https://ollama.com) ejecutándose localmente (`ollama pull qwen2.5-coder:7b`) o configura tus claves API en la nube (`GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) dentro de `.env` antes de iniciar una sesión de auditoría.

### Desktop App (BETA)

AudiCode está diseñado como una **Aplicación Nativa de Escritorio** impulsada por `pywebview` (Edge WebView2 / WebKit), sin barra de direcciones de navegador, con ejecución de controles ISO/IEC 27701:2025 en un solo clic y privacidad local por defecto.

| Plataforma            | Descarga / Ejecutable                |
| --------------------- | ------------------------------------ |
| Windows (x64)         | [`AudiCode-v0.1.0-windows-x64.zip`](https://github.com/MarcoXMarquez/audicode/releases/download/v0.1.0-beta/AudiCode-v0.1.0-windows-x64.zip) (Ejecutable `AudiCode.exe`) |
| macOS (Apple Silicon) | `audicode-desktop-mac-arm64.dmg`     |
| macOS (Intel)         | `audicode-desktop-mac-x64.dmg`       |
| Linux                 | `.deb`, `.rpm`, o `.AppImage`        |

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

### Contribuir

Si deseas contribuir a AudiCode:

1. Haz un fork del repositorio y crea tu rama (`git checkout -b feat/nuevo-control-iso`).
2. Asegúrate de que cualquier nueva skill bajo `skills/<nombre-skill>/` incluya su especificación `SKILL.md` mapeada a controles de **ISO/IEC 27701:2025**.
3. Verifica que la aplicación de escritorio inicie correctamente con `python audicode_desktop.py`.
