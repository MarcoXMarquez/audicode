# Metodología de Matriz de Riesgos de Privacidad (ISO/IEC 27701:2025)

- **Referencias Normativas**: Cláusula 6.1.2 (Planificación del riesgo), Cláusula 8.2 (Operación de apreciación del riesgo), Control A.1.2.6 (PIA) e ISO/IEC 27557:2022.
- **Principio Esencial**: La evaluación del riesgo en el SGIP debe ser bipolar, diferenciando explícitamente el impacto sobre los **titulares de datos (*PII principals*)** del impacto sobre la **organización**.

---

## 1. Escala de Impacto en los Derechos del Titular (*PII Principal*)

| Nivel | Severidad | Descripción del Daño al Titular | Ejemplos Operativos |
|:---:|---|---|---|
| **1** | **Insignificante** | Inconvenientes menores o molestias temporales que no afectan los derechos ni causan perjuicios tangibles. | Recibir un correo duplicado de confirmación; reingresar datos básicos de perfil. |
| **2** | **Limitado** | Malestar moderado, pérdida menor de tiempo, divulgación de datos no sensibles sin riesgo de discriminación. | Filtración interna de nombre y cargo corporativo; retraso temporal en atención a peticiones. |
| **3** | **Significativo** | Perjuicio material o moral perceptible, daño reputacional, discriminación, denegación injustificada de servicios o pérdida económica moderada. | Revelación de salarios o evaluaciones de desempeño; filtración de dirección física y teléfono privado; scoring erróneo que encarece una tarifa. |
| **4** | **Catastrófico / Crítico** | Daño grave e irreparable a los derechos fundamentales: usurpación de identidad, pérdidas financieras masivas, discriminación por datos sensibles, riesgo físico o pérdida de empleo. | Filtración masiva de diagnósticos médicos o datos biométricos; revocación de derechos de custodia o asilo; estafas financieras por brecha de datos bancarios. |

---

## 2. Escala de Probabilidad (*Likelihood*)

| Nivel | Nivel de Ocurrencia | Frecuencia Estimada / Contexto |
|:---:|---|---|
| **1** | **Remota** | La amenaza requiere capacidades extremas y no se conocen precedentes; salvaguardas avanzadas activas. |
| **2** | **Baja** | La amenaza es conocida pero las defensas implementadas reducen sustancialmente la viabilidad de explotación. |
| **3** | **Media** | Escenario factible en el curso ordinario de las operaciones; vulnerabilidades conocidas o controles imperfectos. |
| **4** | **Alta** | Altamente probable que ocurra en el corto plazo; controles deficientes, flujos expuestos o amenazas frecuentes. |

---

## 3. Matriz Bipolar de Riesgo (Probabilidad x Impacto)

$$Riesgo = Probabilidad \times Impacto$$

| Probabilidad \ Impacto | 1 (Insignificante) | 2 (Limitado) | 3 (Significativo) | 4 (Catastrófico) |
|---|:---:|:---:|:---:|:---:|
| **4 (Alta)** | Medio (4) | Alto (8) | **Crítico (12)** | **Crítico (16)** |
| **3 (Media)** | Bajo (3) | Medio (6) | Alto (9) | **Crítico (12)** |
| **2 (Baja)** | Bajo (2) | Bajo (4) | Medio (6) | Alto (8) |
| **1 (Remota)** | Bajo (1) | Bajo (2) | Bajo (3) | Medio (4) |

### 3.1 Niveles de Severidad y Acciones Requeridas

- **Bajo (1 - 4)**: Riesgo aceptable bajo salvaguardas estándar. Monitoreo regular en revisiones anuales del SGIP.
- **Medio (5 - 7)**: Riesgo tolerable con medidas de mitigación adicionales implementadas antes del pase a producción.
- **Alto (8 - 11)**: Riesgo no aceptable. Exige rediseño de arquitectura (*Privacy by Design*), controles reforzados y reevaluación.
- **Crítico (12 - 16)**: Tratamiento prohibido en su diseño actual. Si tras mitigación exhaustiva el riesgo residual se mantiene en **Alto** o **Crítico**, se activa la **Consulta Previa Obligatoria** ante la Autoridad de Protección de Datos competente antes de cualquier operación.

---

## 4. Comparativa Bipolar: Titular vs Organización

La Cláusula 6.1.2 exige que ambos análisis coexistan sin que el riesgo corporativo opaque el riesgo humano:

| Dimensión | Enfoque Titular (*PII Principal*) | Enfoque Organización (*PIMS*) |
|---|---|---|
| **Daño evaluado** | Discriminación, daño físico/moral, pérdida de control, estafa. | Sanciones de autoridades (multas RGPD/LGPD), demandas civiles, daño de marca. |
| **Aceptación** | Un riesgo alto para el titular **NO puede ser aceptado** unilateralmente por la empresa para ahorrar costos. | La empresa puede asumir costos comerciales, pero no puede transferir el riesgo a la persona. |
| **Prioridad de mitigación** | Primaria (diseño ético, minimización, cifrado de origen). | Secundaria (seguros de ciberriesgo, planes de RRPP de crisis). |
