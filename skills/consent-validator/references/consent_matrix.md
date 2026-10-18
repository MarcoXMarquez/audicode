# Matriz Normativa de Validez del Consentimiento y Registro Probatorio (ISO/IEC 27701:2025)

## 1. Alcance y Fundamentación Normativa

Esta referencia técnica complementa la skill `consent-validator`, proporcionando los criterios de evaluación y tablas de validación exhaustivas conforme a la norma **ISO/IEC 27701:2025**:
- **A.1.2.4 / B.1.2.4**: Determinación de cuándo y cómo obtener el consentimiento (*Determine when and how consent is to be obtained*).
- **A.1.2.5 / B.1.2.5**: Obtención y registro del consentimiento (*Obtain and record consent*).
- **A.1.3.5 / B.1.3.5**: Mecanismo para modificar o revocar el consentimiento (*Providing mechanism to modify or withdraw consent*).
- **A.2.2.4 / B.2.2.4**: Uso para mercadotecnia y publicidad por encargados (*Marketing and advertising use*).
- **Equivalencias ISO/IEC 27701:2019**: Cláusulas 7.2.4, 7.2.5, 7.3.4 y 8.2.3.

---

## 2. Matriz de Requisitos de Validez del Consentimiento

Para que el consentimiento constituya una base jurídica legítima de tratamiento, debe satisfacer de forma concurrente los siguientes atributos esenciales:

| Criterio de Validez | Control ISO 27701:2025 | Requisito Técnico y Operativo | Criterio de Falla (No Conformidad) |
|---|---|---|---|
| **1. Libre (*Freely Given*)** | A.1.2.4, A.1.2.5 | Ausencia de coacción, intimidación, penalización o desequilibrio manifiesto de poder. El acceso al servicio básico no puede supeditarse a aceptar tratamientos accesorios (ej. mercadotecnia o cesión a terceros). | - Bloqueo de la prestación del servicio si el usuario rechaza publicidad.<br>- Penalización de precio o degradación arbitraria de funcionalidades esenciales.<br>- Cláusulas de aceptación forzada en contratos laborales o de consumo. |
| **2. Específico (*Specific*)** | A.1.2.4, A.1.2.5 | Granularidad por finalidad. Cada propósito de tratamiento independiente debe contar con una opción de elección separada e individualizada. | - Casilla única para aceptar "Términos, Publicidad y Cesión a Socios Comerciales" (*bundled consent*).<br>- Consentimientos generales e indeterminados ("para mejorar su experiencia y otros fines afines"). |
| **3. Informado (*Informed*)** | A.1.2.4, A.1.2.5, A.1.3.3 | Información previa, clara, accesible y en lenguaje llano antes de la captura: identidad del responsable, finalidades exactas, transferencias, y el derecho a revocar en cualquier momento. | - Solicitud de consentimiento sin hipervínculo directo al aviso de privacidad.<br>- Lenguaje legalista, ambiguo o deliberadamente confuso.<br>- Ocultar la existencia de cesiones o transferencias internacionales de datos. |
| **4. Inequívoco (*Unambiguous*)** | A.1.2.5 | Declaración de voluntad manifestada mediante una acción afirmativa clara (ej. clic deliberado, marcación manual de casilla, firma digital). Se prohíbe el consentimiento tácito o por omisión. | - Casillas premarcadas (*pre-ticked checkboxes*).<br>- Deducir consentimiento de la simple navegación ("Si continúa navegando, consideramos que acepta...").<br>- Silencio o inacción del usuario considerado como aceptación. |
| **5. Explícito (*Explicit*)** | A.1.2.4, A.1.2.5 | Declaración afirmativa expresa y reforzada requerida para categorías especiales de PII (datos de salud, biométricos, origen étnico, convicciones), decisiones automatizadas/perfilado de alto impacto o transferencias internacionales sin decisión de adecuación. | - Tratar datos sensibles amparándose en casillas genéricas o consentimiento implícito.<br>- No requerir doble factor de verificación o confirmación reforzada cuando el riesgo es elevado. |
| **6. Simetría y Revocabilidad** | A.1.3.5 | El consentimiento debe poder retirarse en cualquier momento con la misma facilidad y por el mismo canal por el que fue concedido ("*as easy to withdraw as to give*"). | - Otorgamiento con 1 clic en web, pero exigencia de llamada telefónica, carta postal o comparecencia física para cancelar.<br>- Portales de preferencias ocultos o enlaces rotos de desuscripción (*opt-out*).<br>- Demoras injustificadas para procesar la baja. |
| **7. Protección de Menores** | A.1.2.4 | Procedimientos técnicos de verificación de edad y obtención de autorización parental o de tutores cuando el tratamiento involucra a titulares menores de la edad legal permitida. | - Formularios dirigidos a menores sin filtro de edad.<br>- Ausencia de canal verificable de autorización parental.<br>- Exigir datos innecesarios del menor para habilitar la verificación. |
| **8. Restricciones a Encargados** | A.2.2.4 | El encargado del tratamiento (*PII Processor*) no puede emplear la PII del cliente para sus propios fines de publicidad o marketing sin consentimiento directo, independiente y no condicionado. | - Proveedor SaaS que envía promociones propias a los usuarios de sus clientes corporativos sin base legal válida ni consentimiento explícito previo. |

---

## 3. Catálogo de Patrones Oscuros (*Dark Patterns*) Prohibidos

El auditor debe identificar y calificar como no conformidades críticas o mayores la presencia de patrones de diseño engañosos en interfaces de usuario (formularios, banners CMP, cuadros de diálogo modal):

1. **Pre-ticked Checkboxes (Casillas Premarcadas)**:
   - Casillas de aceptación comercial marcadas por defecto en formularios de checkout, registro o suscripción.
   - *Severidad ISO 27701*: Crítica (vulnera A.1.2.4 y A.1.2.5).

2. **Asymmetric Choice / Visual Bias (Desbalance Visual)**:
   - Resaltar el botón "Aceptar Todo" con colores llamativos y tamaño predominante, mientras que "Rechazar" o "Configurar" se presenta como enlace de texto gris apenas perceptible o requiere navegar por múltiples submenús.
   - *Severidad ISO 27701*: Mayor (vulnera A.1.2.5 y A.1.3.4).

3. **Confirmshaming (Culpabilización Emocional)**:
   - Redacción que ridiculiza o manipula emocionalmente al usuario que decide no consentir (ej. *"No, prefiero perderme las mejores ofertas y pagar más"*).
   - *Severidad ISO 27701*: Mayor (vulnera A.1.2.4).

4. **Roach Motel / Obstruction (Fricción Asimétrica)**:
   - El alta o suscripción se ejecuta en un solo paso, pero la baja o revocación requiere responder cuestionarios obligatorios, navegar más de 3 niveles de menús o llamar en horarios restringidos.
   - *Severidad ISO 27701*: Crítica (vulnera A.1.3.5).

5. **Bundled / Tying Consent (Consentimiento Vinculado Forzado)**:
   - Condicionar la entrega de un material gratuito (ej. *whitepaper* o webinar) a la aceptación obligatoria de recibir llamadas de prospección comercial de terceros patrocinadores.
   - *Severidad ISO 27701*: Mayor (vulnera A.1.2.4).

---

## 4. Especificación Técnica del Registro Probatorio (*Consent Ledger*)

Conforme al control **A.1.2.5**, el responsable debe demostrar fehacientemente que el titular consintió un tratamiento específico. Un indicador booleano aislado (`is_consented = true`) en una tabla de usuarios es **insuficiente** y constituye una no conformidad mayor.

### 4.1 Campos Mandatorios y Recomendados del Registro

| Campo | Tipo de Dato | Obligatoriedad | Descripción Técnica y Finalidad Probatoria |
|---|---|---|---|
| `consent_id` | UUID v4 / String | Mandatorio | Identificador único e inmutable del evento de consentimiento. |
| `subject_identifier` | String (Hash/UUID) | Mandatorio | Identificador unívoco del titular (ID de cuenta pseudonimizado o email hasheado en reposo). |
| `timestamp_utc` | String (ISO 8601 UTC) | Mandatorio | Marca temporal exacta de la concesión (ej. `2026-10-01T14:32:05.123Z`). |
| `purpose_id` | String / Array[String] | Mandatorio | Identificador(es) unívoco(s) de las finalidades aceptadas (ej. `marketing_email`, `profiling_analytics`). |
| `consent_status` | Enum | Mandatorio | Estado del consentimiento: `GRANTED`, `WITHDRAWN`, `MODIFIED`, `EXPIRED`. |
| `legal_text_version` | String | Mandatorio | Identificador de versión del texto o cláusula legal mostrada al usuario (ej. `v2.4.1`). |
| `legal_text_hash` | String (SHA-256) | Mandatorio | Hash criptográfico del texto legal exacto presentado en la interfaz en el momento de la aceptación. |
| `capture_channel` | String | Mandatorio | Canal o punto de contacto: `WEB_FORM`, `MOBILE_APP_IOS`, `MOBILE_APP_ANDROID`, `CMP_BANNER`, `CALL_CENTER_IVR`, `PHYSICAL_FORM`. |
| `ip_address` | String | Recomendado | Dirección IP de origen (con enmascaramiento o anonimización parcial para balance de minimización). |
| `user_agent` | String | Recomendado | Cabecera del navegador o identificador de compilación de la app móvil. |
| `withdrawal_timestamp_utc` | String (ISO 8601 UTC) | Condicional (si revocado) | Marca temporal de la revocación del consentimiento. |
| `withdrawal_channel` | String | Condicional (si revocado) | Canal utilizado para la revocación (`PREFERENCE_CENTER`, `ONE_CLICK_UNSUBSCRIBE`, `API`). |
| `proof_token` | String (HMAC / JWT) | Recomendado | Firma criptográfica que garantiza la integridad e inmutabilidad del registro frente a modificaciones internas. |

### 4.2 Modelo de Datos JSON Recomendado (*Consent Event Record*)

```json
{
  "consent_id": "c7a8b912-34e5-4f67-89ab-0123456789cd",
  "subject_identifier": "usr_998124a9e2f",
  "timestamp_utc": "2026-10-01T15:04:12.871Z",
  "purposes": [
    {
      "purpose_id": "commercial_newsletter",
      "granted": true
    },
    {
      "purpose_id": "third_party_transfers",
      "granted": false
    }
  ],
  "status": "GRANTED",
  "legal_context": {
    "policy_version": "v3.1.0",
    "text_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "notice_url": "https://example.com/privacy?v=3.1.0"
  },
  "collection_channel": "WEB_CHECKOUT_MODAL",
  "network_context": {
    "ip_pseudonymized": "198.51.100.xxx",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  },
  "revocation_metadata": null
}
```

---

## 5. Protocolo de Auditoría de Revocación y Simetría (A.1.3.5)

El auditor debe verificar las siguientes fases operativas para dictaminar la conformidad del proceso de revocación:

1. **Accesibilidad del enlace/mecanismo**:
   - En correos electrónicos publicitarios: enlace de desuscripción de 1 clic en el pie de página (*RFC 8058 - List-Unsubscribe header* y botón directo).
   - En plataformas web / aplicaciones: acceso directo al Centro de Privacidad o Menú de Preferencias sin necesidad de reautenticarse excesivamente ni sortear advertencias disuasorias.

2. **Simetría funcional**:
   - Pasos para otorgar: Máximo 1 a 2 interacciones.
   - Pasos para revocar: Máximo 1 a 2 interacciones. Si revocar exige más pasos o fricción que otorgar, se emitirá una no conformidad mayor.

3. **Plazo perentorio de propagación**:
   - Suspensión técnica de envíos comerciales directos: Máximo 24 a 48 horas hábiles.
   - Propagación de revocación a terceros cesionarios o encargados del tratamiento (A.1.3.8 / A.2.2.4): Máximo 72 horas con evidencia de confirmación sincrónica o webhook documentado.

4. **Persistencia del rastro probatorio**:
   - El sistema debe conservar el registro histórico de la revocación para acreditar que la organización detuvo el tratamiento a partir de esa fecha, sin suprimir el histórico de licitud previa.
