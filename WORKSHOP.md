# DD Workshop v2 — Implementación Completa

Documentación técnica de todo lo implementado en el workshop de Datadog sobre observabilidad, monitoreo y entrega de software.

---

## Arquitectura General

```
GitHub (código + CI/CD)
    │
    ├── GitHub Actions (.github/workflows/ci-cd.yml)
    │       ├── Job: test       → Test Optimization (Datadog)
    │       ├── Job: sast       → Code Analysis / SAST (Datadog)
    │       ├── Job: claude     → Análisis de PR con Claude AI
    │       └── Job: deploy     → GKE + DORA Metrics + Continuous Testing
    │
    └── Google Kubernetes Engine (GKE)
            ├── dd-workshop-backend   (FastAPI + ddtrace APM)
            ├── dd-workshop-frontend  (React + nginx)
            ├── nginx ingress controller
            └── Datadog Agent (Helm) → APM, métricas, logs
```

**Dominio:** `workshop.mmonsalves.dev` (Cloudflare proxy + SSL)  
**Cluster:** `dd-workshop-cluster` en `us-central1` (GCP)  
**Registro de imágenes:** `us-central1-docker.pkg.dev/electric-loader-308712/dd-workshop`

---

## 1. Frontend + Backend (Aplicación)

### Qué se implementó

- **Backend:** FastAPI (Python) con SQLite in-memory, instrumentado con `ddtrace`
- **Frontend:** React 18 con React Router v6, Axios, tema dark luxury, login con credenciales
- **Servidor web:** nginx como reverse proxy del frontend, expuesto vía ingress

### Stack técnico

| Componente | Tecnología | Versión |
|---|---|---|
| Backend | FastAPI + uvicorn | 0.111.0 / 0.29.0 |
| ORM/DB | SQLite in-memory | — |
| Trazado | ddtrace | 2.10.0 |
| Frontend | React + React Router | 18.3.1 / 6.23.1 |
| HTTP client | Axios | 1.7.2 |
| Web server | nginx:alpine | latest |

### Cómo se implementó

**Backend (`backend/main.py`):**
- Login con credenciales hardcodeadas en SQLite (intencional para demo)
- Endpoint `/api/health` para health checks y Synthetic tests
- Endpoint `/api/products/report/slow` intencionalmente lento para demo de APM (N+1 queries + sleeps artificiales)
- Vulnerabilidades intencionales para demo de SAST: SQL injection, command injection, path traversal, MD5 débil, secrets hardcodeados

**Frontend (`frontend/src/`):**
- Login con token JWT almacenado en `localStorage`
- Listado de productos con paginación y filtro por categoría
- Manejo de errores visible en UI

**Infraestructura (`k8s/manifests.yaml`):**
- Deployments con `livenessProbe` y `readinessProbe`
- `ingressClassName: nginx` (spec moderno, no anotación deprecada)
- Cloudflare como proxy SSL frente al ingress de GKE

---

## 2. APM — Application Performance Monitoring

### Qué observabilidad entrega

- Trazas distribuidas de cada request HTTP al backend
- Latencia por endpoint, errores, throughput
- Flame graphs para identificar cuellos de botella
- Correlación entre servicios, hosts y logs

### Tipo de monitoreo

**Observabilidad de aplicación en tiempo real** — permite ver qué está pasando dentro del código mientras corre en producción.

### Cómo se implementó

**Datadog Agent en GKE (Helm):**
```bash
helm repo add datadog https://helm.datadoghq.com
helm install datadog-agent datadog/datadog \
  --set datadog.apiKey=<DD_API_KEY> \
  --set datadog.apm.enabled=true \
  --set datadog.apm.socketEnabled=true \
  --set datadog.logs.enabled=true \
  --namespace datadog --create-namespace
```

**Instrumentación del backend (`backend/main.py`):**
```python
# ddtrace se activa vía ddtrace-run al iniciar el proceso
# Variables de entorno en el pod:
# DD_SERVICE=dd-workshop-api
# DD_ENV=workshop
# DD_VERSION=<git-sha>
```

**`backend/requirements.txt`:**
```
ddtrace==2.10.0
wrapt>=1.11.0
```

### Dónde verlo en Datadog

`APM → Services → dd-workshop-api`

---

## 3. Test Optimization (CI Visibility)

### Qué observabilidad entrega

- Visibilidad de cada test unitario en cada run del pipeline
- Historial de duración por test
- Detección de tests flaky (inestables)
- Correlación entre tests y commits/deployments

### Tipo de monitoreo

**Observabilidad del proceso de calidad de software** — saber si los tests son confiables y cuánto tardan a lo largo del tiempo.

### Cómo se implementó

**`.github/workflows/ci-cd.yml` — Job `test`:**
```yaml
- name: Configure Datadog Test Optimization
  uses: datadog/test-visibility-github-action@v2
  with:
    languages: python
    api_key: ${{ secrets.DD_API_KEY }}
    site: datadoghq.com
    service: dd-workshop-api
    python-tracer-version: "2.10.0"

- name: Run tests
  env:
    DD_ENV: workshop
  run: |
    cd backend
    pytest test_main.py -v \
      --cov=. \
      --cov-report=xml:coverage.xml
```

La action `test-visibility-github-action@v2` instrumenta pytest automáticamente en modo **agentless** (envía datos directo a Datadog sin necesidad de un agente local).

### Dónde verlo en Datadog

`Test Optimization → Test Runs / Test Health / Flaky Management`

**Resultado:** 15 tests visibles, todos passed, en modo agentless desde GitHub Actions.

---

## 4. SAST — Static Application Security Testing (Code Analysis)

### Qué observabilidad entrega

- Análisis estático del código en busca de vulnerabilidades de seguridad
- Detección de secrets expuestos, SQL injection, path traversal, etc.
- Resultados por archivo, línea y severidad
- Bloquea PRs si se detectan vulnerabilidades críticas

### Tipo de monitoreo

**Seguridad de código en tiempo de desarrollo** — encuentra problemas antes de que lleguen a producción.

### Cómo se implementó

**`.github/workflows/ci-cd.yml` — Job `sast`:**
```yaml
sast:
  name: SAST Scan
  runs-on: ubuntu-latest
  if: github.event_name == 'push'   # solo en push, no en pull_request
  steps:
    - name: Datadog SAST
      uses: datadog/datadog-static-analyzer-github-action@v3
      with:
        dd_api_key: ${{ secrets.DD_API_KEY }}
        dd_app_key: ${{ secrets.DD_APP_KEY }}
        dd_site: datadoghq.com
        cpu_count: 2
```

> **Nota:** La condición `if: github.event_name == 'push'` es necesaria porque la GitHub Action de Datadog SAST no soporta el evento `pull_request` — falla con error si se intenta correr en ese contexto. El análisis siempre ocurre sobre el código que llega a `main` después del merge.

Corre en cada push a `main` (incluyendo merges de PRs).

### Dónde verlo en Datadog

`Code Analysis → Repositories → dd-workshop`

### Flujo de remediación desde Datadog

Cuando Datadog detecta una vulnerabilidad, permite aplicar la remediación directamente desde la UI:

1. `Code Analysis → Repositories → dd-workshop` → seleccionar la vulnerabilidad
2. Datadog crea automáticamente una **rama nueva** (ej. `dd/fix-sql-injection-category-filter`) con el fix aplicado y abre un **Pull Request**
3. El PR activa el pipeline en esa rama: `test` ✅ + `sast` (se salta) + `claude-analysis` ✅
4. Claude comenta el análisis de seguridad del diff en el PR
5. Se hace merge → push a `main` → pipeline completo: `test` + `sast` + `deploy`

---

## 5. Claude AI — Análisis de PR

### Qué entrega

- Comentario automático en cada Pull Request con análisis de seguridad del diff
- Identifica vulnerabilidades, línea exacta, riesgo y código corregido sugerido
- Complementa el SAST con análisis en lenguaje natural en español

### Cómo se implementó

**`.github/workflows/ci-cd.yml` — Job `claude-analysis` (solo en PRs):**
```yaml
- name: Analyze and comment PR
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    pip install anthropic requests
    python3 << 'PYTHON'
    # Obtiene el diff del PR (solo archivos .py)
    # Envía a Claude claude-opus-4-7 para análisis de seguridad
    # Publica el resultado como comentario en el PR via GitHub API
    PYTHON
```

**Secrets requeridos:** `ANTHROPIC_API_KEY`, `GITHUB_TOKEN` (automático)

### Dónde verlo

En cada Pull Request → sección Comments → `## 🤖 Análisis — Claude AI`

---

## 6. Continuous Testing (Synthetic Tests en pipeline)

### Qué observabilidad entrega

- Validación automática de que la app responde correctamente después de cada deploy
- Tests ejecutados desde múltiples ubicaciones geográficas (AWS Canada Central + AWS São Paulo)
- Bloquea el pipeline si la app no responde tras el deploy
- Correlación de resultados con commit y branch

### Tipo de monitoreo

**Verificación activa post-deploy** — no es monitoreo pasivo, es un gate de calidad que forma parte del proceso de entrega.

### Cómo se implementó

**Paso 1 — Crear el Synthetic test en Datadog UI:**
- `Synthetic Monitoring → Tests → New Test → API Test`
- URL: `https://workshop.mmonsalves.dev/api/health`
- Método: GET
- Assertion: Status code = 200
- Public ID obtenido: `tkm-8uj-cax`

**Paso 2 — `.github/workflows/ci-cd.yml` — Job `deploy` (después del rollout):**
```yaml
- name: Run Synthetic Tests
  uses: DataDog/synthetics-ci-github-action@v4.0.0
  with:
    api-key: ${{ secrets.DD_API_KEY }}
    app-key: ${{ secrets.DD_APP_KEY }}
    public-ids: "tkm-8uj-cax"
    datadog-site: datadoghq.com
```

### Dónde verlo en Datadog

`Synthetic Monitoring & Testing → Results Explorer → CI Batches`

**Resultado:** 2 test runs por batch (una por región), PASSED, correlacionados con pipeline #17, branch `main`.

---

## 7. DORA Metrics

### Las 4 métricas

| Métrica | Qué mide | Estado |
|---|---|---|
| **Deployment Frequency** | Frecuencia de deploys exitosos a producción | ✅ Activa — 0.2/semana |
| **Change Lead Time** | Tiempo desde un commit hasta producción | Requiere integración GitHub↔DD |
| **Change Failure Rate** | % de deploys que rompen algo | Se llena con deploys fallidos |
| **Failed Deployment Recovery Time** | Tiempo de recuperación ante fallo | Requiere incidents linkados |

### Tipo de monitoreo

**Métricas de rendimiento del equipo de ingeniería** — miden la velocidad y estabilidad del proceso de entrega de software, no de la aplicación en sí.

### Cómo se implementó

**`.github/workflows/ci-cd.yml` — Job `deploy`:**

```yaml
# Al inicio del job — captura timestamp de inicio
- name: Record deploy start time
  run: echo "DEPLOY_START=$(date +%s)" >> $GITHUB_ENV

# Después del rollout de Kubernetes — envía evento a Datadog
- name: Report deployment to Datadog DORA
  run: |
    npm install -g @datadog/datadog-ci
    datadog-ci dora deployment \
      --service dd-workshop-api \
      --env workshop \
      --started-at ${{ env.DEPLOY_START }} \
      --finished-at $(date +%s) \
      --git-repository-url https://github.com/${{ github.repository }} \
      --git-commit-sha ${{ github.sha }}
  env:
    DATADOG_API_KEY: ${{ secrets.DD_API_KEY }}
```

Cada deploy envía a Datadog: servicio, entorno, timestamps de inicio/fin y referencia al commit exacto.

### Dónde verlo en Datadog

`Software Delivery → DORA Metrics → Explorer`

---

## Pipeline completo — Flujo

```
git push → main
    │
    ├─► Job: test (paralelo)
    │       └── pytest 15 tests → Test Optimization (Datadog) ✅
    │
    ├─► Job: sast (paralelo)
    │       └── Static analysis → Code Analysis (Datadog) ✅
    │
    └─► Job: deploy (después de test + sast)
            ├── Build Docker images (backend + frontend)
            ├── Push a Artifact Registry (GCP)
            ├── kubectl apply → GKE
            ├── kubectl rollout status (espera pods listos)
            ├── datadog-ci dora deployment → DORA Metrics ✅
            ├── synthetics-ci-github-action → Continuous Testing ✅
            └── App live en workshop.mmonsalves.dev ✅

git pull_request → main
    └─► Job: claude-analysis
            └── Claude claude-opus-4-7 analiza diff → comentario en PR ✅
```

---

## Secrets configurados en GitHub

| Secret | Uso |
|---|---|
| `DD_API_KEY` | Datadog — todos los jobs |
| `DD_APP_KEY` | Datadog — SAST + Continuous Testing |
| `ANTHROPIC_API_KEY` | Claude AI — análisis de PR |
| `GCP_SA_KEY` | Google Cloud — auth para deploy |
| `GCP_PROJECT_ID` | Google Cloud — proyecto |

---

## Resumen de observabilidad implementada

| Capa | Herramienta | Qué monitorea |
|---|---|---|
| Código | SAST (Datadog) | Vulnerabilidades estáticas en el código fuente |
| Tests | Test Optimization (Datadog) | Calidad y estabilidad de la suite de tests |
| Deploy | DORA Metrics (Datadog) | Velocidad y estabilidad del proceso de entrega |
| Post-deploy | Continuous Testing (Datadog) | Disponibilidad y correctitud de la app tras cada deploy |
| Runtime | APM (Datadog Agent) | Rendimiento y trazas de la app en producción |
| Seguridad PR | Claude AI | Análisis de seguridad en lenguaje natural por PR |
