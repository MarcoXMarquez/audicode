# Expediente Formal de Brecha de Datos Personales (PII Breach Record)

- **ID del Incidente**: `INC-20261001-0842`
- **Título**: Ataque de Ransomware con Exfiltración de Base de Datos de Clientes y Nómina
- **Norma de Referencia**: ISO/IEC 27701:2025 Controles A.3.11, A.3.12 y Guía B.3.12
- **Entidad**: Financiera Global S.A. (Rol: PII Controller)
- **DPO / Contacto**: dpo@financieraglobal.example.com
- **Fecha de Emisión del Expediente**: 2026-10-01 05:14:43 UTC

---

## 1. Cronología Oficial del Incidente (B.3.12)

| Hito Temporal | Marca de Tiempo (UTC) | Notas de Auditoría |
|---|---|---|
| **Ocurrencia Estimada** | `2026-09-30T18:20:00Z` | Inicio presunto del vector de ataque |
| **Detección Inicial** | `2026-10-01T02:15:00Z` | Detección por monitorización / reporte |
| **Confirmación Formal de Brecha PII** | `2026-10-01T04:30:00Z` | **Punto de inicio para el cómputo de 72 horas** |
| **Contención Técnica** | `2026-10-01T07:45:00Z` | Aislamiento y neutralización de la amenaza |
| **Resolución y Cierre** | `None` | Estado: CONTENIDO - EN PROCESO DE RESTAURACIÓN Y FORENSE |

### Verificación de Plazo Legal de Notificación (Regla de 72 Horas)
- **Horas transcurridas hasta notificación**: `6.5` horas.
- **Dictamen de Cumplimiento**: **COMPLIANT** (Notificado en 6.5 horas. CONFORME con el límite de 72h)

---

## 2. Identificación del Informante y Receptores (B.3.12)

- **Informante**: Carlos Mendoza (Analista Senior SOC Nivel 2)
- **Canal de Reporte**: Alerta SIEM automatizada + Escalamiento telefónico de emergencia
- **Órgano Receptor Interno**: Equipo de Respuesta a Incidentes de Privacidad (CSIRT / CIRT)
- **Líderes de Respuesta**: Elena Valenzuela (CISO) y Roberto Arismendi (DPO)

---

## 3. Naturaleza, Causa Raíz y Afectación de Seguridad de la Información (B.3.12)

### 3.1 Descripción de los Hechos y Causa Raíz
Se detectó movimiento lateral y ejecución de ransomware tipo BlackByte sobre dos servidores de bases de datos. Los atacantes comprometieron credenciales privilegiadas de VPN y lograron exfiltrar fragmentos de tablas antes de cifrar los volúmenes de almacenamiento.

**Causa Raíz / Vulnerabilidad Explotada**: Explotación de credencial de acceso remoto sin segundo factor (MFA) en cuenta de servicio huérfana y falta de segmentación estricta de red interna.

### 3.2 Clasificación de la Afectación a la PII (Tríada CIA)

| Dimensión de Seguridad | ¿Afectada? | Detalle de la Evidencia |
|---|---|---|
| **Confidencialidad** (Divulgación / Acceso No Autorizado) | `SÍ` | Exfiltración confirmada de 1.8 GB de tablas con datos de clientes. |
| **Integridad** (Alteración / Falsificación) | `NO` | No se evidenció alteración ni corrupción de transacciones previas al cifrado. |
| **Disponibilidad** (Pérdida / Destrucción / Cifrado) | `SÍ` | Indisponibilidad temporal del sistema de gestión durante 5 horas tras el cifrado. |

---

## 4. Alcance y Categorías de PII Comprometidas (B.3.12)

- **Número Estimado de Titulares Afectados**: `12,500` personas
- **Número Estimado de Registros Involucrados**: `45,000` registros
- **¿Involucra Datos Sensibles / Especiales?**: `SÍ`
- **Detalle de Datos Sensibles**: Datos económicos y salarios de 350 empleados internos.

**Categorías Específicas de PII Identificadas**:
- Nombres y apellidos completos
- Números de documento de identidad (DNI / RFC)
- Correos electrónicos y números de teléfono
- Datos bancarios (números de cuenta CLABE / IBAN sin CVV)
- Datos de salarios de empleados

---

## 5. Evaluación de Consecuencias y Nivel de Riesgo (B.3.11 / B.3.12)

- **Nivel Global de Riesgo para los Titulares**: **Alto**
- **Consecuencias para los Titulares**: Riesgo alto de phishing dirigido, intentos de extorsión y fraude financiero.
- **Consecuencias para la Organización**: Afectación reputacional temporal, suspensión preventiva de servicios en línea y costos forenses.

---

## 6. Preservación Forense y Resiliencia de Respaldos (A.3.14 y A.3.25)

### 6.1 Cadena de Custodia y Evidencias Digitales (A.3.14)
- **Registro de Cadena de Custodia**: `ACTIVO Y CONFORME`
- **Custodio Asignado**: Ing. Fernando Morales (Perito Forense Digital)
- **Acciones de Preservación Ejecutadas**:
  * Volcado de memoria RAM previo al aislamiento lógico.
  * Clonación forense bit a bit de los discos virtuales en formato raw/dd.
  * Cálculo y depósito de hashes criptográficos SHA-256 de todas las imágenes.
  * Extracción y congelamiento inmutable de registros de syslog y firewall (Control A.3.14).

### 6.2 Resiliencia y Restauración desde Backups (A.3.25)
- **Verificación de Integridad de Respaldos**: `VERIFICADO`
- **Tecnología de Respaldo**: Repositorio inmutable fuera de línea (Air-gapped) con snapshots WORM
- **Datos Recuperados**: 100% de la base de datos operativa restaurada a las 06:30Z (Control A.3.25)
- **RTO Logrado**: 4.25 horas

---

## 7. Pasos de Resolución y Mitigación Adoptados (B.3.12)

| Paso / Acción Ejecutada | Responsable Asignado | Marca de Tiempo (UTC) |
|---|---|---|
| Aislamiento inmediato de los servidores afectados del resto de la LAN/WAN | Carlos Mendoza (SOC) | `2026-10-01T02:40:00Z` |
| Revocación masiva de credenciales de acceso remoto y tokens de sesión activos | Marcos Silva (Administrador de Directorio Activo) | `2026-10-01T03:00:00Z` |
| Verificación y escaneo de integridad de copias de seguridad inmutables | Laura Gómez (Infraestructura y Backup) | `2026-10-01T05:00:00Z` |
| Reinstalación limpia del sistema operativo y restauración desde copia saneada | Laura Gómez (Infraestructura) | `2026-10-01T06:30:00Z` |

---

## 8. Registro de Notificaciones Realizadas (B.3.11 / B.3.12)

### 8.1 Notificación a la Autoridad de Supervisión
- **Exigibilidad**: `OBLIGATORIA`
- **Autoridad**: Agencia de Protección de Datos Competente
- **Fecha/Hora de Envío**: `2026-10-01T11:00:00Z`
- **Estado / Expediente**: NOTIFICACIÓN INICIAL ENVIADA (FASE 1) (Ref: `EXP-APD-2026-98124`)

### 8.2 Notificación a los Titulares de PII
- **Exigibilidad**: `OBLIGATORIA (Alto Riesgo)`
- **Fundamento**: Riesgo alto para derechos y libertades debido a datos bancarios y salarios expuestos
- **Estado y Canal**: EN PREPARACIÓN - ENVÍO PROGRAMADO PARA HOY 16:00Z | Canal: Correo electrónico directo individual y portal de ayuda al cliente

---

## 9. Lecciones Aprendidas y Acciones Preventivas Post-Mortem (A.3.12)

- **Fecha de Sesión de Revisión**: `2026-10-01T14:00:00Z`

| Acción Preventiva / Correctiva | Responsable | Fecha Límite |
|---|---|---|
| Obligatoriedad incondicional de MFA en el 100% de accesos VPN y cuentas de servicio | CISO | `2026-10-03` |
| Segmentación micro-granular de VLANs de base de datos con reglas Zero-Trust | Jefe de Redes | `2026-10-15` |
| Actualización del análisis de riesgos del SGIP (Cláusulas 6.1.2 y 8.2) | DPO | `2026-10-20` |

---
*Expediente archivado conforme al Control A.3.14 (Protección de Registros del SGIP) con retención mínima reglamentaria.*