---
name: data-minimization-checker
description: >
  Inspecciona y audita la minimización técnica de datos, privacidad por diseño y por defecto,
  técnicas de desidentificación y retención (A.1.4.2, A.1.4.5, A.1.4.6, A.1.4.7, A.1.4.8, A.1.4.9,
  A.2.4.2, A.3.20) bajo ISO/IEC 27701:2025. Se activa al auditar esquemas DDL SQL, modelos de datos,
  endpoints JSON/REST, cargas útiles de APIs (over-fetching), formularios de captura, mecanismos de
  seudonimización/enmascaramiento (ISO 20889), purga de temporales y disposición segura de medios.
  Use when user says "audita este esquema SQL", "revisa esta API por recolección excesiva", "verifica
  la minimización de este payload JSON", "evalúa técnicas de seudonimización o enmascaramiento",
  "comprueba la retención y purga de temporales". No realiza evaluaciones de impacto de alto nivel
  (use pia-reviewer) ni gestiona consentimientos o quejas ARCO.
---

# Data Minimization Checker

## 1. Propósito y Alcance Normativo

Esta skill audita técnicamente la implementación de los principios de **Minimización de Datos** y **Privacidad por Diseño y por Defecto** (*Privacy by Design & Default*) conforme al estándar internacional **ISO/IEC 27701:2025**, asistida por las directrices de desidentificación de **ISO/IEC 20889:2018**.

### Controles Auditados:
- **A.1.4.2 - Limit collection**: Recopilar únicamente los datos personales indispensables, adecuados y pertinentes para el propósito comercial declarado. Los campos opcionales no pueden ser obligatorios (`NOT NULL` o `required: true`).
- **A.1.4.5 - PII minimization objectives**: Aplicación documentada y técnica de mecanismos de reducción de exposición (seudonimización, hashing salteado, enmascaramiento, truncamiento, generalización).
- **A.1.4.6 - PII de-identification and deletion at the end of processing**: Anonimización irreversible o purga física de PII al finalizar la finalidad o el plazo de conservación.
- **A.1.4.7 / A.2.4.2 - Temporary files**: Control de ciclo de vida, TTL estricto (máximo 24-48 horas) y purga programada de archivos temporales, colas y logs.
- **A.1.4.8 / A.1.4.9 - Retention and Disposal**: Calendarios maestros de retención objetivamente fundados y destrucción segura certificada de soportes físicos y lógicos.
- **A.3.20 / A.3.21 - Storage media management & secure disposal**: Gestión y descarte seguro de medios de almacenamiento (NIST SP 800-88 / DIN 66399).

> [!NOTE]
> Para el catálogo exhaustivo de patrones PII, algoritmos formales de ISO/IEC 20889 y directrices de destrucción, consulte `references/pii_catalog.md`.

---

## 2. Entradas Aceptadas y Modo de Operación

La skill procesa los siguientes artefactos:
1. **Esquemas DDL SQL**: Sentencias `CREATE TABLE`, definiciones de campos, llaves foráneas y restricciones `NOT NULL`.
2. **Esquemas y Payloads JSON**: Documentos JSON Schema (`properties`, `required`), respuestas o cuerpos de petición de APIs REST / GraphQL.
3. **Formularios y Modelos de Entidad**: Definiciones de ORM (Django, Prisma, SQLAlchemy, TypeORM), interfaces TypeScript o formularios UI.
4. **Políticas de Retención y Scripts de Purga**: Tareas cron, directivas de retención de base de datos o procedimientos de sanitización de medios.

### Soporte Determinista:
Para el análisis automatizado de esquemas masivos, invoque el script determinista:
```bash
python skills/data-minimization-checker/scripts/schema_minimization_checker.py <ruta_archivo_o_directorio> [--purpose "<proposito>"] [--json]
```

---

## 3. Flujo de Auditoría Paso a Paso

```
[1. Ingesta de Artefactos]
           |
[2. Catalogación de Atributos PII]
           |
[3. Análisis de Pertinencia y Finalidad]
           |
[4. Detección de Sobre-Recolección (Over-fetching / Required)]
           |
[5. Selección de Técnicas de De-identificación (ISO 20889)]
           |
[6. Verificación de Retención, Temporales (TTL) y Purga]
           |
[Generación de Reporte y Matriz de Hallazgos]
```

### Paso 1: Ingesta e Inspección de Estructura
- Cargar el esquema SQL, esquema JSON, payload API o modelo de datos presentado por el usuario.
- Si el usuario no especificó el propósito funcional del sistema o servicio, **preguntar explícitamente** cuál es la finalidad del negocio (ej. facturación electrónica, envío físico de productos, boletín por correo, autenticación de usuarios).

### Paso 2: Catalogación de Atributos PII
Clasificar cada campo detectado según su nivel de exposición conforme a `references/pii_catalog.md`:
- **Categoría Especial / Sensibles**: Salud, biometría, genética, opiniones políticas, convicciones religiosas, datos penales, orientación sexual.
- **Identificadores Directos**: DNI, SSN, pasaporte, nombre completo, correo electrónico, teléfono móvil, dirección residencial precisa.
- **Identificadores Indirectos / Cuasi-identificadores**: Dirección IP, User-Agent detallado, Device ID, fecha de nacimiento exacta, coordenadas GPS precisas, código postal completo.
- **Telemetría / Artefactos Temporales**: Volcados de depuración, grabaciones de sesión, logs transaccionales con payloads.

### Paso 3: Análisis de Adecuación, Pertinencia y Necesidad Estricta
Evaluar si cada atributo PII es estrictamente indispensable para el propósito del negocio:
- ¿Es necesario solicitar el DNI para registrarse en un foro o boletín informativo? (No: violación de A.1.4.2).
- ¿Es necesaria la fecha de nacimiento exacta con hora para verificar si un cliente es mayor de 18 años? (No: basta el año de nacimiento o una validación booleana).
- ¿Es indispensable almacenar las coordenadas GPS con 6 decimales de precisión para mostrar tiendas cercanas? (No: basta una resolución a nivel de código postal o municipio).

### Paso 4: Detección de Sobre-Recolección y Privacidad por Defecto
Identificar configuraciones que vulneran la privacidad por defecto:
- **Campos obligatorios desproporcionados**: Campos no esenciales marcados como `NOT NULL` en SQL o en la lista `required: [...]` en JSON Schema.
- **Sobre-recolección en APIs (*Over-fetching*)**: Endpoints REST que devuelven el objeto de usuario completo (`SELECT * FROM users`) exponiendo contraseñas, salarios o teléfonos cuando el cliente solo solicitó el nombre público.
- **Tipos de datos sobredimensionados**: Tipos `TIMESTAMP` para almacenar solo fechas de nacimiento, o campos `VARCHAR(255)` abiertos que invitan a ingresar datos libres no estructurados sin control.

### Paso 5: Formulación de Técnicas de De-identificación (ISO/IEC 20889)
Recomendar la técnica técnica de desidentificación adecuada según el caso de uso:
- **Seudonimización**: Reemplazar identificadores directos por identificadores sintéticos aleatorios (UUID v4) en bases de datos analíticas, manteniendo la tabla de correspondencia en un repositorio separado y cifrado (A.1.4.5).
- **Hashing con Sal Criptográfica**: Utilizar HMAC-SHA256 con clave en KMS para deduplicación, o Argon2id para contraseñas. Prohibir formalmente MD5, SHA-1 o hashing sin sal.
- **Tokenización**: Utilizar una bóveda segura (*Token Vault*) para aislar identificadores de alta sensibilidad (e.g., PAN financiero según PCI-DSS).
- **Truncamiento**: Reducir granularidad (truncar último octeto en IPv4 `/24`, prefijo `/48` en IPv6, enmascarar tarjetas a últimos 4 dígitos).
- **Generalización y Agregación**: Sustituir valores exactos por intervalos (rangos de edad, bandas salariales, divisiones geográficas amplias) para satisfacer criterios de $k$-anonimato ($k \ge 5$).

### Paso 6: Verificación de Retención, Temporales y Destrucción Segura
- **Archivos Temporales (A.1.4.7 / A.2.4.2)**: Exigir inventario y tiempo de vida útil (TTL) configurado a un máximo de 24 a 48 horas con purga automatizada.
- **Calendario de Retención (A.1.4.8)**: Verificar que ningún dato se conserve "indefinidamente". Cada tipología debe tener un plazo fundamentado en prescripciones legales.
- **Purga Efectiva vs Borrado Lógico (A.1.4.6)**: El borrado lógico simple (`is_deleted = true`) es insuficiente por sí solo; debe existir una rutina de purga física o anonimización destructiva programada.
- **Destrucción de Medios (A.1.4.9 / A.3.20 / A.3.21)**: Sanitización lógica (NIST SP 800-88 Clear/Purge) o borrado criptográfico (*crypto-shredding*) de claves KMS para nubes públicas.

---

## 4. Matriz de Hallazgos y Criterios de Severidad

| Nivel de Severidad | Criterio de Activación Técnica | Control Principal | Plazo de Remediación Típico |
|---|---|---|---|
| **CRÍTICA** | Datos de categoría especial (salud, biometría, religión, etnia) recopilados sin justificación; credenciales en texto plano; borrado lógico permanente sin purga física de datos confidenciales expuestos; hashing sin sal o uso de MD5/SHA-1 para PII directa. | A.1.4.2, A.1.4.5, A.1.4.6 | Inmediato (< 24-48 horas) |
| **MAYOR** | Identificadores directos no esenciales marcados como obligatorios (`NOT NULL`, `required: true`); APIs que devuelven payloads con PII completa (*over-fetching*); ausencia total de política de retención o TTL en archivos temporales; tablas de seudonimización sin segregación de llaves. | A.1.4.2, A.1.4.7, A.1.4.8 | Corto plazo (< 15 días) |
| **MENOR** | Cuasi-identificadores (IPs, User-Agents, geolocalización) almacenados con precisión innecesariamente alta; falta de enmascaramiento dinámico en vistas de auditoría o administración; ausencia de certificados formales de descarte de medios. | A.1.4.5, A.3.20 | Medio plazo (< 30 días) |
| **OPORTUNIDAD DE MEJORA** | Oportunidad de aplicar agregación estadística o privacidad diferencial en reportes analíticos; optimización de tipos de datos en esquemas SQL para prevenir captura libre. | A.1.4.5 | Ciclo de mejora continua |

---

## 5. Formato Estándar del Informe de Minimización

Al finalizar la auditoría, emita el informe estructurado bajo la siguiente plantilla:

```markdown
# Informe de Auditoría de Minimización de Datos y Privacidad por Defecto

- **Artefacto Auditado**: [Nombre del archivo SQL, JSON o especificación]
- **Propósito Declarado**: [Finalidad operativa del sistema / servicio]
- **Fecha de Auditoría**: [AAAA-MM-DD]
- **Normativa Aplicada**: ISO/IEC 27701:2025 (A.1.4.2, A.1.4.5, A.1.4.6, A.1.4.7, A.1.4.8, A.1.4.9) & ISO/IEC 20889:2018

---

## 1. Resumen Ejecutivo
[Breve diagnóstico sobre la proporcionalidad general y nivel de madurez técnica del esquema analizado]

## 2. Tabla Consolidada de Hallazgos

| ID | Control ISO 27701 | Severidad | Atributo / Campo | Evidencia Técnica Detectada | Recomendación Técnica de Minimización (ISO 20889) |
|---|---|---|---|---|---|
| H-01 | A.1.4.2 | CRÍTICA | `users.ssn` | Campo NOT NULL en registro de foro web | Suprimir columna; sustituir por UUID interno seudónimo |
| H-02 | A.1.4.5 | MAYOR | `logs.client_ip` | IP IPv4 completa persistida sin enmascarar | Truncar último octeto (/24) y fijar TTL en 14 días |

## 3. Plan de Acción y Medidas Técnicas Recomendadas
1. **Modificaciones de Esquema Inmediatas**: [Sentencias ALTER TABLE o ajustes de JSON Schema sugeridos]
2. **Implementación de Técnicas de Desidentificación**: [Detalle de hashing con sal, DDM o tokenización requerida]
3. **Gobernanza de Retención y Purga**: [Definición de TTL y rutinas automatizadas de supresión segura]
```

---

## 6. Qué NO Hacer (Reglas Negativas Estrictas)

> [!CAUTION]
> Para garantizar el rigor pericial y evitar invasión de competencias de otras skills, respete estrictamente los siguientes límites:

1. **NO dictaminar asesoría legal definitiva**: Esta skill evalúa la conformidad técnica y arquitectónica contra estándares ISO/IEC 27701 y 20889; no sustituye la asesoría jurídica territorial formal de un abogado o DPO matriculado.
2. **NO asumir propósitos de negocio**: No juzgue si un campo es "excesivo" sin conocer la finalidad del sistema. Si la finalidad no fue declarada, solicítela explícitamente al usuario antes de emitir un dictamen final.
3. **NO realizar Evaluaciones de Impacto integrales (PIA / EIPD)**: Si el proyecto involucra un macro-análisis de riesgos a derechos y libertades, uso de inteligencia artificial o biometría masiva a nivel organizacional, derive a `pia-reviewer`.
4. **NO auditar mecánicas de consentimiento ni checkboxes**: La validación de cómo el usuario aceptó las condiciones o cómo se configuran las CMP de cookies corresponde exclusivamente a `consent-validator`.
5. **NO validar cláusulas contractuales con proveedores (DPA)**: Si se analiza la relación jurídica o SLA con un encargado externo, derive a `processor-contract-validator`.
6. **NO considerar ofuscaciones reversibles (Base64, Hex) como desidentificación válida**: Reporte siempre como hallazgo crítico la pretensión de usar codificaciones sin clave como mecanismos de privacidad.

---

## 7. Recursos y Referencias Progresivas

- **Catálogo de PII y Guía de De-identificación**: Consulte [`references/pii_catalog.md`](references/pii_catalog.md) para acceder a los patrones regex, directrices cuantitativas de $k$-anonimato, modelos de retención pasiva y requisitos de NIST SP 800-88.
- **Herramienta Determinista de Auditoría**: Utilice [`scripts/schema_minimization_checker.py`](scripts/schema_minimization_checker.py) para auditar rápidamente archivos `.sql`, `.ddl` y `.json`.
