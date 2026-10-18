# Catálogo Técnico de PII y Guía de De-identificación (ISO/IEC 27701:2025 & ISO/IEC 20889:2018)

- **skill**: `data-minimization-checker`
- **estándares**: ISO/IEC 27701:2025 (A.1.4.2, A.1.4.5, A.1.4.6, A.1.4.7, A.1.4.8, A.1.4.9, A.2.4.2, A.3.20, A.3.21) e ISO/IEC 20889:2018
- **propósito**: Documento de referencia técnica exhaustiva para identificación de atributos PII, evaluación de proporcionalidad y aplicación de técnicas formales de desidentificación, retención y disposición segura.

---

## 1. Fundamentos Normativos de la Minimización de Datos

En el marco de **ISO/IEC 27701:2025**, la minimización de datos no es una recomendación estilística, sino un mandato arquitectónico articulado en el Anexo A.1 (Responsables) y Anexo A.2 (Encargados):

1. **A.1.4.2 - Limit collection**: La recopilación de PII debe limitarse estrictamente a lo indispensable para las finalidades explícitas identificadas. Privacidad por defecto: los campos optativos nunca deben ser obligatorios (`NOT NULL` o `required: true`).
2. **A.1.4.5 - PII minimization objectives**: Obligación de definir métricas y aplicar técnicas de reducción de exposición (seudonimización, enmascaramiento, agregación, truncamiento) durante todo el ciclo de vida del dato.
3. **A.1.4.6 - PII de-identification and deletion at the end of processing**: Una vez cumplida la finalidad legítima o vencido el periodo de conservación, la PII debe eliminarse irreversiblemente o anonimizarse de modo que la reidentificación sea inviable.
4. **A.1.4.7 y A.2.4.2 - Temporary files**: Los archivos temporales generados por la operación (cachés, swaps, volcados, logs de depuración) deben inventariarse, tener un Tiempo de Vida (*TTL*) acotado y purgarse de manera automatizada.
5. **A.1.4.8 y A.1.4.9 - Retention and disposal**: Calendarios de retención objetivamente fundados en plazos legales de prescripción y métodos certificados de destrucción física y lógica de medios.
6. **A.3.20 y A.3.21 - Storage media management & secure disposal**: Controles de infraestructura física y en la nube para garantizar que ningún residuo de datos persista en discos dados de baja o réplicas no controladas.

---

## 2. Taxonomía Exhaustiva de Atributos PII

La identificabilidad comprende tanto la identificación directa como la capacidad de individualizar a un titular mediante el enlace (*linkage*) o correlación de datos indirectos.

### 2.1 Identificadores Directos (Riesgo Alto a Crítico)
Atributos que identifican unívocamente a una persona física sin requerir información adicional o cruce con fuentes externas.

| Atributo | Ejemplos Comunes en Esquemas | Patrones Regex Típicos | Nivel de Riesgo Base | Justificación y Regla de Minimización |
|---|---|---|---|---|
| **Documento Nacional de Identidad** | `dni`, `ssn`, `curp`, `cpf`, `nie`, `rut`, `passport_no` | `\b(dni\|ssn\|curp\|cpf\|nie\|rut\|national_id\|passport)\b` | **CRÍTICO** | Solo admisible en obligaciones fiscales, laborales o prevención de fraude financiero regulado. Prohibido en registros web ordinarios o newsletters. |
| **Nombre Completo / Apellidos** | `first_name`, `last_name`, `full_name`, `apellidos` | `\b(first_name\|last_name\|full_name\|surname\|nombre\|apellido)\b` | **ALTO** | Separar en tabla de perfil; utilizar identificador sintético interno (UUID v4) en tablas transaccionales. |
| **Credenciales en Claro / Tokens** | `password`, `pin_code`, `cvv`, `pan`, `secret_key` | `\b(password\|passwd\|pin\|cvv\|card_number\|secret)\b` | **CRÍTICO** | Inaceptable en texto plano. Claves deben procesarse con Argon2id/bcrypt. Datos de tarjeta gobernados por PCI-DSS. |
| **Correo Electrónico Personal** | `email`, `correo`, `user_email`, `personal_email` | `\b(email\|correo\|mail)\b` | **ALTO** | Usar identificador seudónimo en logs y analítica. Enmascarar en UI (`u***r@domain.com`). |
| **Teléfono Móvil o Fijo** | `phone`, `mobile`, `cellphone`, `telefono`, `celular` | `\b(phone\|mobile\|cellphone\|telefono)\b` | **ALTO** | Solicitar solo si la comunicación SMS/voz es esencial para el servicio (ej. 2FA, confirmación logística). |
| **Dirección Física Completa** | `street_address`, `home_address`, `direccion_linea1` | `\b(street_address\|home_address\|direccion)\b` | **ALTO** | Excesivo para servicios puramente digitales. Limitar a país o región para tarificación e impuestos. |

### 2.2 Identificadores Indirectos y Cuasi-Identificadores (Riesgo Medio a Alto)
Datos que de forma aislada no identifican unívocamente, pero cuya combinación permite singularizar al individuo (Teorema de Sweeney: el cruce de fecha de nacimiento, sexo y código postal de 5 dígitos identifica al 87% de la población de EE.UU.).

| Atributo | Ejemplos Comunes en Esquemas | Patrones Regex Típicos | Nivel de Riesgo | Riesgo de Reidentificación y Medida |
|---|---|---|---|---|
| **Dirección IP** | `ip_address`, `client_ip`, `remote_addr`, `source_ip` | `\b(ip_address\|client_ip\|remote_addr)\b` | **MEDIO** | Considerada PII en RGPD y estándares globales. Truncar último octeto en IPv4 (`192.168.1.0/24`) o prefijo `/48` en IPv6. TTL de logs <= 30 días. |
| **Fecha de Nacimiento Exacta** | `birth_date`, `dob`, `fecha_nacimiento`, `f_nac` | `\b(birth_?date\|dob\|fecha_nacimiento)\b` | **ALTO** | Si el propósito es validar mayoría de edad (ej. +18), sustituir por flag booleano (`is_adult: true`) o almacenar año de nacimiento/rango etario. |
| **Geolocalización Precisa** | `latitude`, `longitude`, `gps_coords`, `geo_point` | `\b(latitude\|longitude\|gps_coord\|lat_long)\b` | **ALTO** | Limitar precisión decimal (reducir a 2 decimales para aproximación de ~1.1 km) o generalizar a nivel de código postal / municipio. |
| **Código Postal Específico** | `zip_code`, `postal_code`, `codigo_postal`, `cp` | `\b(zip_?code\|postal_?code\|codigo_postal)\b` | **MEDIO** | Truncar a los 2 o 3 primeros dígitos cuando se procese conjuntamente con edad o género en ambientes analíticos. |
| **Huella de Dispositivo / Navegador** | `device_id`, `imei`, `canvas_hash`, `user_agent_full` | `\b(device_id\|imei\|canvas_fingerprint\|user_agent)\b` | **MEDIO** | Desaconsejada la persistencia de huellas complejas por defecto. Anonimizar el User-Agent registrando únicamente `Family/Version` y OS principal. |
| **Metadatos Financieros / Salario** | `salary`, `income`, `wage`, `sueldo`, `ingresos` | `\b(salary\|income\|revenue\|wage\|sueldo)\b` | **MEDIO** | Si es para segmentación crediticia o estadística, convertir a bandas salariales o deciles agregados. |

### 2.3 Datos de Categoría Especial y Sensibles (Riesgo Crítico)
Atributos cuyo tratamiento indebido lesiona gravemente derechos fundamentales y libertades del titular (Art. 9 RGPD, ISO/IEC 27701:2025 Cláusula A.1.4.2).

- **Salud y Diagnósticos**: Datos de historial médico, grupo sanguíneo, recetas, tratamientos, discapacidades físicas o cognitivas.
- **Biometría y Genética**: Minucias de huella dactilar, vectores de reconocimiento facial, plantillas de iris, grabaciones biométricas de voz, perfiles de ADN.
- **Convicciones e Ideología**: Creencias religiosas, afiliación sindical, opiniones políticas, convicciones filosóficas.
- **Origen y Características Protegidas**: Origen racial o étnico, orientación sexual, vida sexual, datos de menores de edad.
- **Datos Judiciales**: Antecedentes penales, sanciones administrativas, procesos de litigio o medidas cautelares.

> [!CAUTION]
> Los datos de categoría especial **no deben recopilarse bajo premisas genéricas de "experiencia del usuario" o "personalización"**. Su presencia en esquemas relacionales estándar o cargas útiles JSON públicas constituye una presunción de no conformidad crítica con el control A.1.4.2, a menos que exista una base jurídica reforzada demostrada (consentimiento explícito estricto o mandato legal).

### 2.4 Telemetría Excesiva y Vigilancia de Interacción
- Mapas de calor y grabaciones de sesión (*session replay* como Hotjar, FullStory): Ingestionan accidentalmente contraseñas, saldos y nombres en campos de texto a menos que se apliquen filtros estrictos del lado del cliente (*client-side scrubbing*).
- Logs de eventos de teclado (*keystroke logging*): Prohibidos por principio de proporcionalidad en servicios no especializados de seguridad.
- Pila de llamadas y volcados de depuración (*stack traces / crash dumps*): Suelen atrapar variables de memoria con PII transaccional.

---

## 3. Catálogo Técnico de Técnicas de Desidentificación (ISO/IEC 20889:2018)

ISO/IEC 20889 clasifica las técnicas de desidentificación y mejora de la privacidad (*Privacy-Enhancing Technologies - PETs*) en familias formales:

```
                            TÉCNICAS ISO/IEC 20889
                                      |
         +----------------------------+----------------------------+
         |                                                         |
[Seudonimización & Criptografía]                         [Transformación de Datos]
  - Seudonimización basada en tokens                       - Supresión (Eliminación)
  - Hashing con sal criptográfica                          - Enmascaramiento (Masking)
  - Cifrado determinista / Homomórfico                      - Generalización (Rangos)
                                                           - Micro-agregación / Ruido
```

### 3.1 Seudonimización (ISO/IEC 20889 §6)
Consiste en la sustitución de un identificador directo por un seudónimo sintético de modo que los datos ya no puedan atribuirse a un interesado sin utilizar información adicional.

#### Requisitos Técnicos Obligatorios:
1. **Segregación física o lógica**: La tabla de mapeo de seudónimos (`user_id -> synthetic_uuid`) o la clave criptográfica debe almacenarse en un entorno o base de datos independiente, con control de acceso RBAC disjunto y auditoría de lecturas.
2. **Generación con entropía segura**: Uso de identificadores UUID v4 (`crypto.randomUUID()` o generadores CSPRNG). Nunca usar secuencias predecibles o IDs autoincrementales derivados de la identidad.
3. **Seudonimización con función criptográfica con clave (HMAC)**:
   $$\text{Pseudonym} = \text{HMAC-SHA256}(K, \text{Identifier})$$
   - La clave $K$ debe residir en un Módulo de Seguridad Hardware (HSM) o servicio KMS (Key Management Service) gestionado con rotación anual.

### 3.2 Hashing Criptográfico con Sal (*Salted Hashing*)
El hashing unidireccional convierte un identificador en un digesto de longitud fija.

- **Requisito mandatorio de Sal (*Salt*)**:
  - Un hash sin sal de un DNI o email es inmediatamente vulnerable a búsquedas precalculadas (*Rainbow Tables* o catálogos filtrados).
  - Cada registro debe incorporar una sal aleatoria única de al menos 128 bits:
    $$\text{HashRecord} = \text{Salt} \parallel \text{KDF}(\text{Identifier}, \text{Salt}, \text{Pepper})$$
  - La pimienta (*pepper*) es un secreto global almacenado fuera de la base de datos (e.g., variable de entorno cifrada en KMS).
- **Algoritmos Aceptables**:
  - Para identificadores (alta velocidad con salteado HMAC): HMAC-SHA256, HMAC-SHA512, BLAKE3.
  - Para contraseñas y secretos: Argon2id (recomendado), bcrypt (cost factor >= 12), PBKDF2 (>= 600,000 iteraciones en SHA-256).
- **Prohibiciones Absolutas**:
  - `MD5`, `SHA-1`: Prohibidos por colisiones conocidas y velocidad de ataque masivo por GPUs.
  - `Base64`, `Hex`, `ROT13`, `URL-encoding`: Son codificaciones reversibles sin clave; considerarlas técnicas de desidentificación constituye un hallazgo **Crítico**.

### 3.3 Tokenización con Bóveda (*Token Vault*)
Sustitución de datos sensibles por valores equivalentes funcionalmente no sensibles denominados "tokens":
- **Token determinista**: El mismo dato produce siempre el mismo token (permite indexación y joins en bases de datos analíticas, pero introduce riesgo de correlación de frecuencia).
- **Token no determinista**: Cada ocurrencia del dato sensible produce un token distinto generado aleatoriamente (máxima protección; requiere almacenar el contexto de la transacción en la bóveda).
- La Bóveda de Tokens (*Vault*) debe implementar controles de seguridad de nivel PCI-DSS y doble factor para peticiones de destokenización autorizadas.

### 3.4 Enmascaramiento de Datos (*Data Masking*)

#### Enmascaramiento Estático (SDM):
Aplicado permanentemente en la base de datos de destino. Imprescindible para generar bases de datos de desarrollo, aseguramiento de calidad (QA) o formación a partir de respaldos de producción.
- Reemplazo de nombres por listas aleatorias generadas artificialmente.
- Sustitución de correos por dominios ficticios `@test-internal.invalid`.

#### Enmascaramiento Dinámico (DDM):
Transformación en tiempo de consulta ejecutada en la capa de middleware o motor de base de datos según el rol del usuario conectado:
- Tarjeta de crédito (PCI-DSS): `4532 12** **** 8901` (solo primeros 6 dígitos de red y últimos 4 de cuenta).
- Correo electrónico: `m****o@empresa.com`
- DNI / SSN: `***-**-1234`
- Teléfono: `+34 *** *** 789`

### 3.5 Generalización y Supresión (ISO/IEC 20889 §7)
Consiste en reducir la escala o granularidad del dato para aumentar la cantidad de sujetos que comparten los mismos atributos:

1. **Jerarquías de Generalización**:
   - Fecha de nacimiento exacta (`1992-07-14`) $\rightarrow$ Mes/Año (`1992-07`) $\rightarrow$ Año (`1992`) $\rightarrow$ Rango etario (`30-39 años`).
   - Dirección física (`Calle Gran Vía 28, Piso 4B, Madrid, 28013`) $\rightarrow$ Código postal (`28013`) $\rightarrow$ Provincia (`Madrid`) $\rightarrow$ País (`España`).
2. **Modelos de Privacidad Cuantitativos**:
   - **$k$-Anonimato ($k$-anonymity)**: Cada registro en un conjunto de datos desidentificado debe ser indistinguible de al menos $k-1$ otros registros respecto a sus cuasi-identificadores (recomendado $k \ge 5$).
   - **$l$-Diversidad ($l$-diversity)**: Extensión que garantiza que para cada grupo homogéneo de cuasi-identificadores existan al menos $l$ valores bien representados en el atributo sensible, previniendo ataques de homogeneidad.
   - **$t$-Cercanía ($t$-closeness)**: Exige que la distribución de un atributo sensible en cualquier clase de equivalencia sea cercana a la distribución global del atributo.

### 3.6 Privacidad Diferencial ($\epsilon$-Differential Privacy)
Mecanismo matemático que introduce ruido estadístico controlado (ej. distribución de Laplace o Gauss) en las respuestas a consultas agregadas:
$$\Pr[\mathcal{M}(D_1) \in S] \le e^{\epsilon} \times \Pr[\mathcal{M}(D_2) \in S]$$
Donde $D_1$ y $D_2$ difieren en un único registro individual. Garantiza que la presencia o ausencia de cualquier persona física individual no altera perceptiblemente el resultado de la analítica.

---

## 4. Gobernanza del Ciclo de Vida: Retención, Archivos Temporales y Disposición Segura

### 4.1 Gobernanza de Archivos Temporales (A.1.4.7 y A.2.4.2)
Toda infraestructura que manipule PII genera copias transitorias en capas intermedias.

| Origen Temporal | Riesgo de Fuga de PII | Control Técnico Mandatorio | TTL Recomendado |
|---|---|---|---|
| **Cachés de Aplicación (Redis / Memcached)** | PII en memoria accesible en red interna sin cifrado | Cifrado en reposo (TLS in-transit), llaves segregadas por sesión, directiva `EXPIRE` obligatoria. | Máx. 24 horas |
| **Archivos en `/tmp` o almacenamiento local** | Volcados de reportes CSV/Excel generados por usuarios | Tarea automatizada `cron` / `systemd-tmpfiles` con purga forzosa (`tmpwatch`). | Máx. 12 horas |
| **Logs de Servidor Web (Nginx / Apache)** | URLs con parámetros GET conteniendo emails o tokens | Reescritura de log para filtrar querystrings de autenticación. Almacenar únicamente IP truncada. | 14 a 30 días |
| **Logs de Depuración / Traces de Error** | Volcados de excepciones con datos de formulario completos | Desactivar logs en modo `DEBUG` en entornos productivos. Filtro Regex en middleware sanitizador. | Inmediato / 48 h |
| **Archivos de Intercambio (Swap) y Crash Dumps** | Extracción forense de memoria RAM de procesos | Swap cifrado (`dm-crypt`) y deshabilitación de volcados de núcleo de usuarios (`limits.conf`). | Purgado en reinicio |

### 4.2 Calendario Maestro de Retención de PII (A.1.4.8)
La conservación de datos personales no puede sustentarse en fórmulas vagas como "mientras la cuenta esté activa y un tiempo prudencial después". Debe establecerse un calendario fundamentado:

```
[Inicio: Captura / Contrato] ---> [Fase Activa: Finalidad Principal]
                                                |
                                    (Cese de la Finalidad)
                                                v
[Destrucción Irreversible / Anonimización] <--- [Fase Pasiva: Bloqueo Legal / Prescripción]
```

- **Fase Activa**: Tratamiento directo para la prestación del servicio acordado.
- **Fase de Bloqueo Legal (Retención Pasiva)**:
  - Los datos dejan de estar disponibles para operaciones comerciales o técnicas ordinarias.
  - Se restringe el acceso exclusivamente a los responsables jurídicos para la atención de reclamaciones o responsabilidades ante tribunales o autoridades tributarias.
  - La base de datos debe almacenar una marca de bloqueo y fecha límite de caducidad (`retention_expires_at`).
- **Plazos Comunes de Referencia Legal**:
  - Datos de navegación web y cookies: Máximo 6 a 13 meses.
  - Registros de facturación y transacciones económicas: 4 a 6 años (según código fiscal/mercantil territorial).
  - Expedientes laborales y de seguridad social: 5 a 10 años tras la desvinculación laboral.
  - Logs de accesos de seguridad a sistemas: 12 meses (normativa de telecomunicaciones y ciberseguridad).

### 4.3 Supresión al Término del Tratamiento: Borrado Lógico vs Físico (A.1.4.6)
> [!WARNING]
> La práctica de **Borrado Lógico Simple** (ej. actualizar la columna `is_deleted = true` o `deleted_at = NOW()`) donde todos los atributos de PII continúan existiendo en texto plano de por vida en la tabla productiva **es un incumplimiento directo del control A.1.4.6**.

#### Estrategia Conforme con A.1.4.6:
1. **Borrado en Dos Fases**:
   - Fase 1 (Inmediata): El registro se marca como inactivo (`status = 'DEACTIVATED'`) y se inicia el periodo de prescripción legal.
   - Fase 2 (Vencimiento de retención): Disparo de rutina nocturna que ejecuta la sobrescritura criptográfica o purga física de las columnas identificables:
     ```sql
     UPDATE users 
     SET first_name = 'ANONYMIZED',
         last_name = 'ANONYMIZED',
         email = CONCAT('anon_', id, '@purged.invalid'),
         phone = NULL,
         dni = NULL,
         address = NULL,
         status = 'PURGED',
         purged_at = NOW()
     WHERE id = :target_user_id AND retention_expires_at <= NOW();
     ```
2. **Propagación a Réplicas y Respaldos (*Backups*)**:
   - En sistemas de copias de seguridad de solo lectura, la norma ISO/IEC 27701:2025 admite que la purga física se efectúe mediante la rotación natural del ciclo de vida de los backups (máx. 30 a 90 días), siempre que los datos estén cifrados y no se restauren selectivamente registros marcados para borrado.

### 4.4 Disposición Segura de Medios Físicos y Digitales (A.1.4.9, A.3.20, A.3.21)

#### Cumplimiento con NIST SP 800-88 Rev. 1:
- **Sanitización Lógica (Clear)**: Sobrescritura de sectores lógicos de almacenamiento con ceros o secuencias seudoaleatorias mediante herramientas auditadas (e.g. `shred`, `srm`, directivas de motor).
- **Sanitización Criptográfica (Purge / Cryptographic Erase)**:
  - Indispensable en infraestructuras de nube pública (AWS EBS/S3, Azure Blob, Google Cloud Storage) donde no se tiene acceso físico a los discos.
  - Los volúmenes se crean con cifrado obligatorio mediante clave administrada por KMS. Para destruir los datos, se elimina la clave KMS asociada (*Crypto-shredding*), dejando los datos en el medio físico matemáticamente indescifrables e irrecuperables.
- **Destrucción Física (Destroy)**:
  - Aplicable a discos duros locales, cintas y dispositivos dados de baja.
  - Desmagnetización (*degaussing*) de discos magnéticos o trituración mecánica de estado sólido (SSD) a partículas no mayores a 2 mm.
  - Soportes en papel: Triturado conforme a **DIN 66399** nivel P-4 (partículas $\le 160\text{ mm}^2$) o P-5 para datos altamente confidenciales. Todo descarte debe documentarse con certificado de destrucción emitido por gestor homologado.

---

## 5. Resumen de Criterios de Evaluación para el Auditor

Al auditar esquemas, APIs y repositorios, formule sistemáticamente las siguientes 5 preguntas de control:

1. **¿Es indispensable el dato para la finalidad principal?** (A.1.4.2) Si la finalidad es autenticar al usuario, ¿por qué se solicitan DNI o fecha de nacimiento?
2. **¿Está el campo marcado como obligatorio por defecto?** (A.1.4.2) Los atributos no esenciales marcados como `NOT NULL` o `required: true` constituyen un hallazgo de severidad Alta.
3. **¿Puede reducirse la granularidad del atributo?** (A.1.4.5) ¿Es viable guardar un rango de edad en vez de una fecha exacta, o una ciudad en vez de coordenadas GPS?
4. **¿Existen mecanismos de seudonimización o enmascaramiento definidos?** (A.1.4.5 / ISO 20889) ¿Dónde reside la clave de desanonimización? ¿Existe segregación estricta?
5. **¿Cuál es el mecanismo de expiración y purga?** (A.1.4.6, A.1.4.7, A.1.4.8) ¿Hay rutinas programadas de purga física o solo hay banderas de borrado lógico permanente?
