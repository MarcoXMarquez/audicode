# Reglas de Notificación de Brechas de Datos Personales (PII Breaches)

- **Estándar de referencia**: ISO/IEC 27701:2025 (A.3.11, A.3.12, B.3.11, B.3.12, B.2.2.2)
- **Normas técnicas complementarias**: ISO/IEC 27035 (partes 1-3), Directrices EDPB 01/2021, Marco de Severidad ENISA
- **Ámbito**: Responsables (*PII Controllers*) y Encargados (*PII Processors*)

---

## 1. Criterios Objetivos de Evaluación del Riesgo del Incidente

La determinación de si una brecha de datos personales debe ser notificada a las autoridades de supervisión y a las personas físicas afectadas exige una apreciación rigurosa y objetiva del riesgo para los derechos y libertades de los titulares (*PII principals*).

### 1.1 Factores Clave de Ponderación del Riesgo

1. **Tipología y Naturaleza de los Datos Comprometidos**:
   - *Riesgo Bajo*: Datos de contacto corporativos generales o información que ya es legalmente pública sin mayor impacto.
   - *Riesgo Medio*: Nombres, correos personales, números de teléfono o identificadores comunes sin datos sensibles o de pago asociados.
   - *Riesgo Alto*: Contraseñas o credenciales de acceso a plataformas críticas, números de identificación oficial (DNI, SSN, RFC, CPF), información financiera o datos de localización continua.
   - *Riesgo Extremo / Crítico*: Categorías especiales de datos (salud física o mental, expedientes médicos, datos genéticos, datos biométricos para autenticación inequívoca, vida u orientación sexual, convicciones religiosas o políticas, afiliación sindical), datos sobre condenas o infracciones penales, y cualquier dato de **menores de edad** o colectivos en situación de vulnerabilidad extrema.

2. **Facilidad de Identificación del Titular**:
   - *Directa*: El atacante o receptor tiene acceso directo a nombres, apellidos, documentos de identidad o números de cuenta en texto plano.
   - *Indirecta / Reidentificación*: Los datos están pseudonimizados o agregados, pero el atacante posee o puede obtener razonablemente la clave de correspondencia o información contextual que permita revertir el enmascaramiento.
   - *Mitigada por Criptografía Robusta*: La PII expuesta estaba cifrada con algoritmos criptográficos modernos de última generación (ej. AES-256) y las claves de descifrado permanecieron bajo custodia segura e inalterada, haciendo que los datos sean completamente ininteligibles para terceros no autorizados.

3. **Gravedad y Reversibilidad de las Consecuencias Potenciales**:
   - *Daños Económicos o Materiales*: Pérdida monetaria directa, cargos no autorizados, fraude bancario, pérdida de empleo o vivienda.
   - *Suplantación de Identidad (*Identity Theft*)*: Posibilidad real de apertura de líneas de crédito falsas o comisión de ilícitos a nombre de la víctima.
   - *Daños Físicos o a la Seguridad Personal*: Violencia de género, acoso, persecución personal o extorsión.
   - *Daño Moral, Reputacional o Discriminación*: Pérdida de confidencialidad de datos médicos o íntimos que provoque estigma social, exclusión laboral o angustia psicológica grave.

4. **Volumen y Extensión del Compromiso**:
   - *Micro / Singular*: Incidente aislado que afecta a 1 o pocos individuos sin exposición pública.
   - *Moderado*: Decenas a cientos de titulares.
   - *Masivo / Sistémico*: Decenas de miles o millones de titulares, o afectación de bases de datos centrales de una infraestructura crítica.

5. **Características y Vulnerabilidad de los Titulares**:
   - Personas físicas en situación de asimetría o desprotección (menores, ancianos, pacientes oncológicos o psiquiátricos, empleados bajo relaciones de subordinación).

---

### 1.2 Matriz Cuantitativa de Severidad del Riesgo (Marco Adaptado EDPB / ENISA)

$$\text{Puntaje de Severidad (SEV)} = (\text{Ponderación de Datos} \times 0.40) + (\text{Impacto en Libertades} \times 0.35) + (\text{Vulnerabilidad y Volumen} \times 0.25)$$

| Nivel de Riesgo | Rango de Severidad | Criterio de Activación Operativa | Obligaciones de Notificación |
|---|---|---|---|
| **Bajo** | 1.0 – 1.9 | Evento o brecha sin afectación perceptible para los titulares; PII cifrada con clave intacta o recuperación inmediata y confirmada de respaldos sin exfiltración. | - Registrar internamente en el Libro de Incidentes (A.3.12).<br>- **NO** requiere notificación a la Autoridad ni a los titulares. |
| **Medio** | 2.0 – 2.9 | Brecha con posible afectación menor o incomodidad (ej. spam temporal, necesidad de verificar transacciones habituales) sin riesgo de suplantación o pérdidas financieras. | - Notificar a la Autoridad de Control si la ley jurisdiccional no fija excepción por falta de riesgo.<br>- Aviso optativo/recomendado a los titulares. |
| **Alto** | 3.0 – 3.9 | Probable perjuicio significativo para los derechos de los titulares (exfiltración de credenciales, datos financieros o categorías especiales sin cifrado). | - **Notificación obligatoria a la Autoridad de Control en un plazo máximo de 72 horas**.<br>- **Notificación directa y obligatoria a los titulares sin dilación indebida**. |
| **Extremo / Crítico** | 4.0 – 5.0 | Riesgo inminente de fraude masivo, suplantación de identidad grave, daño físico o afectación a datos médicos/menores de edad a gran escala. | - **Notificación urgente e inmediata a la Autoridad**.<br>- **Notificación prioritaria multicanal inmediata a todos los titulares afectados** con medidas activas de mitigación. |

---

## 2. Plazos Legales de Notificación por Jurisdicción

Las regulaciones globales de protección de datos imponen plazos y umbrales dispares. La siguiente tabla sistematiza los marcos obligatorios más relevantes:

| Jurisdicción / Norma | Sujeto Obligado | Plazo de Notificación a la Autoridad de Control | Plazo de Notificación a los Titulares de PII | Umbral de Activación / Observaciones |
|---|---|---|---|---|
| **Unión Europea / EEE**<br>*(RGPD Arts. 33 y 34)* | Responsable (*Controller*) | **Máximo 72 horas** a partir del momento en que se tenga constancia (*awareness*). Si se supera, justificar las razones de la demora. | **Sin dilación indebida** (*without undue delay*). | A la autoridad: salvo que sea improbable que la brecha entrañe riesgo.<br>A titulares: obligatorio cuando sea probable un **alto riesgo**. Excepción: cifrado eficaz previo o mitigación total posterior. |
| **Unión Europea / EEE**<br>*(RGPD Art. 33.2 / ISO 27701 B.3.12)* | Encargado (*Processor*) | No notifica a la autoridad; **notifica al Responsable sin dilación indebida** tras tener conocimiento. | No notifica a titulares directamente (salvo delegación contractual expresa). | Se materializa en plazos contractuales típicos de **24 a 48 horas** en el DPA. |
| **Reino Unido**<br>*(UK GDPR / DPA 2018)* | Responsable (*Controller*) | **Máximo 72 horas** ante la Information Commissioner's Office (ICO). | Sin dilación indebida ante alto riesgo. | Mismo estándar sustantivo que el RGPD de la UE. |
| **Brasil**<br>*(LGPD Art. 48)* | Responsable (*Controlador*) | **Plazo razonable** (fijado reglamentariamente por la ANPD en **3 días hábiles** desde el conocimiento). | **3 días hábiles** de forma simultánea si puede causar riesgo relevante. | Se evalúa afectación relevante a los titulares y medidas inmediatas adoptadas. |
| **Estados Unidos (California)**<br>*(CCPA / CPRA / Cal. Civ. Code § 1798.82)* | Empresa (*Business*) | Si afecta a más de **500 residentes de California**, remitir copia electrónica formal al Fiscal General del Estado. | En el plazo más oportuno y sin demoras irrazonables (*most expedient time possible*). | Activación cuando se compromete información personal no cifrada ni redactada. |
| **México**<br>*(LFPDPPP Art. 20)* | Responsable | No se contempla plazo en horas expreso para la autoridad en ley federal ordinaria, pero se debe informar inmediatamente al titular. | **De forma inmediata** cuando las vulneraciones afecten de forma significativa los derechos patrimoniales o morales. | Notificación obligatoria al titular para que adopte medidas de defensa de sus derechos. |
| **Colombia**<br>*(Ley 1581 / SIC)* | Responsable y Encargado | Reportar ante la Superintendencia de Industria y Comercio (SIC - RNBD) dentro de los **15 días hábiles** siguientes a la detección. | Según instrucciones de la SIC o cuando exista riesgo inminente de perjuicio. | Reporte a través de la plataforma RNBD de la SIC. |
| **Argentina**<br>*(Resolución AAIP 47/2018)* | Responsable | Comunicación recomendada a la Agencia de Acceso a la Información Pública (AAIP) en **48 horas**. | Notificación directa sin dilación si genera daño inminente. | Régimen de mejores prácticas vinculantes en directrices de seguridad. |

---

## 3. Plantilla Estructurada de Notificación a la Autoridad de Control

A continuación se establece la estructura formal exigida para presentar notificaciones regulatorias (válida para presentación por fases: **Inicial**, **Complementaria / Seguimiento** o **Final**):

```markdown
# FORMULARIO OFICIAL DE NOTIFICACIÓN DE BRECHA DE DATOS PERSONALES
(Conforme a ISO/IEC 27701:2025 A.3.11, B.3.11 y Normativa Aplicable de Privacidad)

## SECCIÓN 1: DATOS GENERALES Y TIPO DE NOTIFICACIÓN
- **Código Interno del Incidente**: INC-YYYYMMDD-XXXX
- **Tipo de Notificación**: [ ] Notificación Inicial (dentro de 72h) | [ ] Notificación Complementaria / Interina | [ ] Informe Final de Cierre
- **Fecha y Hora de la Notificación**: AAAA-MM-DD HH:MM (UTC)
- **Identificación de la Entidad Responsable**:
  - Razón Social: [Nombre Legal de la Organización]
  - NIF / Identificador Fiscal: [Identificador Legal]
  - Dirección Sede Central: [Dirección Postal]
- **Datos del Delegado de Protección de Datos (DPO) / Punto de Contacto**:
  - Nombre Completo: [Nombre del DPO / Enlace de Privacidad]
  - Correo Electrónico: dpo@organizacion.com
  - Teléfono Directo de Crisis: +XX XXX XXX XXX

---

## SECCIÓN 2: CRONOLOGÍA DE LA BRECHA
- **Fecha y Hora Estimada de Ocurrencia / Inicio**: AAAA-MM-DD HH:MM (UTC)
- **Fecha y Hora de Detección Inicial**: AAAA-MM-DD HH:MM (UTC)
- **Fecha y Hora de Confirmación Formal de la Brecha**: AAAA-MM-DD HH:MM (UTC)
- **Tiempo Transcurrido desde Confirmación hasta Notificación**: [XX] Horas
- **Justificación de la Demora** (Obligatorio si supera las 72 horas):
  [Explicación fundada de los motivos técnicos u operativos que impidieron la notificación en 72h].

---

## SECCIÓN 3: NATURALEZA Y CIRCUNSTANCIAS DE LA BRECHA
- **Tipo de Impacto sobre la PII**:
  - [ ] Confidencialidad (Acceso ilegítimo / Divulgación no autorizada / Exfiltración)
  - [ ] Integridad (Modificación no autorizada / Corrupción de registros)
  - [ ] Disponibilidad (Pérdida permanente / Destrucción / Cifrado por ransomware / Indisponibilidad)
- **Vector del Incidente**:
  - [ ] Ataque Externo / Ciberataque (Ransomware, Inyección SQL, Phishing, Exploitation de 0-Day)
  - [ ] Error Interno Involuntario (Envío de correo a destinatario erróneo, desconfiguración cloud / S3 bucket abierto)
  - [ ] Acción Maliciosa Interna (Exfiltración por empleado con privilegios)
  - [ ] Robo o Extravío Físico (Pérdida de portátil, soporte extraíble sin cifrar, documentación en papel)
- **Descripción Breve y Objetiva de los Hechos**:
  [Descripción de los sistemas afectados, componentes tecnológicos vulnerados y cronología de la explotación].

---

## SECCIÓN 4: CATEGORÍAS Y VOLUMEN DE PII AFECTADA
- **Número Aproximado de Titulares Afectados**: [Número exacto o estimado de personas físicas]
- **Número Aproximado de Registros de PII Involucrados**: [Número exacto o estimado de registros]
- **Categorías de Titulares Afectados**:
  - [ ] Clientes / Usuarios finales
  - [ ] Empleados / Colaboradores internos
  - [ ] Proveedores / Socios comerciales
  - [ ] Menores de edad
  - [ ] Colectivos vulnerables / Pacientes
- **Tipología de Datos Personales Comprometidos**:
  - [ ] Datos Identificativos Básicos (Nombre, apellidos, dirección postal, teléfono, email)
  - [ ] Identificadores Oficiales (DNI, Pasaporte, Carnet de conducir, Número de Seguridad Social)
  - [ ] Credenciales de Autenticación (Nombres de usuario, contraseñas hash/saladas, preguntas de seguridad)
  - [ ] Datos Financieros / Económicos (Números de tarjeta bancaria, IBAN, historial crediticio)
  - [ ] Categorías Especiales de Datos (Salud, genética, biometría, vida sexual, opiniones políticas, creencias)

---

## SECCIÓN 5: EVALUACIÓN DE CONSECUENCIAS E IMPACTO PROBABLE
- **Nivel de Riesgo Estimado para los Titulares**: [ ] Bajo | [ ] Medio | [ ] Alto | [ ] Extremo
- **Consecuencias Potenciales**:
  [Detalle de los daños previsibles: suplantación de identidad, daño económico, extorsión, afectación a la intimidad].

---

## SECCIÓN 6: MEDIDAS DE CONTENCIÓN, REMEDIACIÓN Y PRESERVACIÓN
- **Medidas de Contención Inmediatas Adoptadas**:
  [Aislamiento de sistemas, revocación de credenciales, bloqueo de IPs, desconexión de interfaces de red].
- **Medidas de Preservación de Evidencias Forenses (A.3.14)**:
  [Clonación bit a bit de discos, volcados de memoria volátil, copias de seguridad de logs con hash criptográfico SHA-256].
- **Medidas de Resiliencia y Recuperación desde Backups (A.3.25)**:
  [Estado de integridad de respaldos, procesos de restauración en entornos controlados y saneamiento de vulnerabilidades].
- **Medidas Correctivas y Preventivas a Medio Plazo**:
  [Parcheo de vulnerabilidades, auditorías de código, fortalecimiento de políticas de contraseñas y MFA].

---

## SECCIÓN 7: COMUNICACIÓN A LOS TITULARES AFECTADOS
- **¿Se ha comunicado la brecha a los titulares?**:
  - [ ] Sí, se ha notificado individualmente (indicar fecha y canal empleado).
  - [ ] No, pero está planificado hacerlo en fecha [AAAA-MM-DD].
  - [ ] No es necesario notificar (Justificar: riesgo evaluado como bajo, o aplicación de medidas criptográficas previas que hacen ininteligibles los datos según A.3.11).
- **Canales Empleados**: [Correo electrónico directo, SMS, notificación en aplicación, comunicado público en web].

---

## SECCIÓN 8: FIRMA Y RESPONSABILIDAD
- **Nombre del Declarante**: [Nombre y Apellidos]
- **Cargo / Función**: Delegado de Protección de Datos / Representante Legal Autorizado
- **Firma Electrónica / Sello de Tiempo**: [Huella digital / Certificado de firma digital]
```

---

## 4. Plantilla Estructurada de Notificación a los Titulares de PII

Cuando una brecha entrañe un **riesgo alto o extremo** para los derechos y libertades de las personas, la organización debe comunicar directamente a cada titular afectado. La comunicación debe redactarse en **lenguaje sencillo, comprensible, accesible y libre de tecnicismos oscuros**.

```markdown
Asunto: [IMPORTANTE] Aviso de seguridad sobre sus datos personales en [Nombre de la Organización]

Estimado/a [Nombre del Titular]:

Nos ponemos en contacto con usted para informarle con total transparencia sobre un incidente de seguridad que ha afectado a una parte de nuestros sistemas y que podría haber comprometido ciertos datos personales vinculados a su cuenta.

### 1. ¿Qué ocurrió?
El día [Fecha de confirmación], nuestros sistemas de monitorización detectaron [descripción clara y breve: ej. un acceso no autorizado a uno de nuestros servidores de base de datos / un ataque cibernético]. Tan pronto como se identificó la anomalía, nuestro equipo técnico y de seguridad activó el protocolo de emergencia, aislando los sistemas comprometidos y neutralizando la amenaza.

### 2. ¿Qué datos personales se vieron involucrados?
La información sobre usted que pudo verse expuesta incluye:
- [Listar concretamente: Nombre completo y correo electrónico]
- [Número de teléfono]
- [Contraseña de acceso (almacenada mediante técnicas de cifrado unidireccional / hash)]
- **IMPORTANTE**: Deseamos confirmarle expresamente que [NO se han visto afectados sus datos de tarjetas bancarias / NO se expuso información sensible o médica].

### 3. ¿Qué hemos hecho para protegerle?
Inmediatamente tras confirmar el incidente, hemos adoptado las siguientes acciones:
1. Bloqueamos el acceso no autorizado y parchamos la vulnerabilidad técnica detectada.
2. Hemos preservado todos los registros digitales forenses e iniciado una investigación pericial exhaustiva.
3. Hemos notificado formalmente este suceso a la Autoridad de Protección de Datos [Nombre de la autoridad competente].
4. Por precaución, hemos forzado el restablecimiento de su sesión y contraseña en nuestra plataforma.

### 4. ¿Qué acciones le recomendamos tomar de inmediato?
Para salvaguardar su seguridad y evitar cualquier uso indebido de sus datos, le sugerimos seguir estas pautas:
- **Cambie su contraseña de inmediato**: Cree una nueva contraseña robusta en nuestro portal. Si utiliza esta misma contraseña en otros servicios de internet, cámbiela en ellos de forma prioritaria.
- **Active la autenticación en dos factores (2FA / MFA)**: Ingrese a la configuración de su cuenta para activar la verificación en dos pasos.
- **Desconfíe de comunicaciones sospechosas**: Preste especial atención a correos electrónicos, llamadas o mensajes de texto no solicitados que le soliciten datos bancarios o códigos de seguridad. Recuerde que [Nombre de la Organización] NUNCA le solicitará su contraseña por teléfono ni por correo electrónico.
- **Revise sus estados financieros**: Si sospecha cualquier anomalía, comuníquese con su entidad bancaria.

### 5. Canales de soporte y contacto
Entendemos la preocupación que este suceso puede ocasionar y lamentamos sinceramente los inconvenientes. Hemos habilitado un canal exclusivo atendido por nuestro Delegado de Protección de Datos para resolver cualquier inquietud:
- **Correo electrónico dedicado**: privacidad-soporte@organizacion.com
- **Línea telefónica gratuita de asistencia**: +XX 800 XXX XXXX (Lunes a Viernes de 8:00 a 20:00)
- **Portal de preguntas frecuentes**: https://www.organizacion.com/seguridad-incidente

Atentamente,

**[Nombre y Cargo del Responsable / DPO]**  
[Nombre de la Organización]  
[Fecha de la Notificación]
```

---

## 5. Protocolo de Notificación B2B: Encargado a Responsable (B.3.12 y B.2.2.2)

Cuando la organización actúa como **Encargada del Tratamiento (*PII Processor*)**, sus obligaciones operativas se rigen por las siguientes pautas:

1. **Plazo Estricto de Notificación Contractual**:
   - Notificar al Responsable del tratamiento **inmediatamente tras tomar conocimiento** de cualquier brecha confirmada o sospecha fundada (ventana contractual típica: **24 a 48 horas máximo**).
2. **Prohibición de Notificación Directa No Autorizada**:
   - El encargado **no debe** notificar por cuenta propia a la Autoridad de Protección de Datos ni a los titulares afectados, salvo que exista delegación formal por escrito o mandato judicial vinculante.
3. **Contenido Obligatorio del Reporte al Cliente**:
   - Resumen del incidente y cronología de detección.
   - Identificación de las bases de datos o entornos de procesamiento del cliente comprometidos.
   - Tipología y volumen preliminar de registros y titulares del cliente afectados.
   - Medidas técnicas inmediatas de contención adoptadas por el proveedor.
   - Datos de contacto del punto focal técnico de respuesta a incidentes del encargado.
