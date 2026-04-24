# DD Workshop — Flujos de Demostración

Guía paso a paso para demostrar cada feature de Datadog en vivo durante el workshop.

---

## DEMO 1 — Test Optimization: Detectar un test fallido

### Objetivo
Mostrar cómo Datadog Test Optimization detecta y reporta un test roto antes de que el código llegue a producción.

### Rama
`demo/test-failing`

### Qué se modificó
`backend/test_main.py` — el test `test_health` espera un status code 500 en vez de 200, lo que lo hace fallar intencionalmente.

### Pasos para la demo

**Preparación (antes de la presentación):**
```bash
git checkout -b demo/test-failing
# el archivo test_main.py ya tiene el test roto
git push origin demo/test-failing
```

**En vivo:**

1. Mostrar el código del test roto en GitHub
2. El pipeline corre automáticamente en la rama → job `test` falla
3. Ir a Datadog → **Test Optimization → Test Runs**
4. Mostrar el test `test_health` en rojo con el error exacto
5. Mostrar la diferencia con runs anteriores (histórico verde vs rojo)

**Narrativa:**
> "El developer introdujo un cambio que rompió un test. GitHub Actions lo detectó, pero Datadog Test Optimization nos da visibilidad completa: qué test falló, en qué línea, cuánto tardó, y si este test ha sido inestable antes."

**Recuperación (fix en vivo):**
1. Crear PR de `demo/test-failing` → `main` para "mostrar el fix"
2. Revertir el test al valor correcto (200)
3. El pipeline vuelve a verde
4. Mostrar en Test Optimization cómo el test vuelve a pasar

---

## DEMO 2 — Continuous Testing: Detectar que la app cayó post-deploy

### Objetivo
Mostrar cómo el Synthetic test bloquea el pipeline cuando la app no responde correctamente después de un deploy.

### Rama
`demo/break-health` → merge a `main`

### Qué se modificó
`backend/main.py` — el endpoint `/api/health` retorna status 500 en vez de 200.

### Pasos para la demo

**Preparación (antes de la presentación):**
```bash
git checkout -b demo/break-health
# main.py ya tiene el health endpoint roto
# NO hacer merge todavía
```

**En vivo:**

1. Mostrar el endpoint `/api/health` funcionando en producción:
   ```
   https://workshop.mmonsalves.dev/api/health → {"status": "healthy"}
   ```
2. Mostrar el código del "bug" introducido en la rama
3. Hacer el merge a `main` en vivo
4. El pipeline corre → deploy exitoso → **Synthetic test FALLA**
5. Ir a Datadog → **Synthetic Monitoring → CI Batches**
6. Mostrar el batch en rojo con el error (esperaba 200, recibió 500)
7. El pipeline queda bloqueado — no se considera "deploy exitoso"

**Narrativa:**
> "El deploy técnicamente funcionó — Kubernetes levantó los pods. Pero Datadog Continuous Testing validó que la app responde correctamente desde dos regiones del mundo y detectó que el health check falla. El pipeline se bloqueó automáticamente."

**Recuperación (fix en vivo):**
1. Hacer un nuevo push con el fix del health endpoint
2. Pipeline corre → Synthetic pasa → deploy exitoso
3. Mostrar el nuevo batch en verde en Datadog

> ⚠️ **Advertencia:** Esta demo modifica producción temporalmente. La app mostrará errores durante 2-3 minutos mientras se despliega el fix. Tenerlo preparado de antemano.

---

## DEMO 3 — DORA Metrics: Mostrar el impacto de un deploy fallido

### Objetivo
Mostrar cómo DORA Metrics registra la frecuencia de deploys y cómo un incidente afecta las métricas del equipo.

### Estrategia
DORA Metrics no requiere una rama especial — se demuestra con el historial acumulado y explicando cada métrica en el dashboard.

### Pasos para la demo

**En vivo:**

1. Ir a Datadog → **Software Delivery → DORA Metrics → Explorer**

2. **Deployment Frequency** — mostrar la barra del período actual:
   > "Cada barra representa deploys exitosos. Podemos ver que deployamos X veces esta semana. Un equipo de alto rendimiento deploya múltiples veces al día."

3. **Change Lead Time** — explicar aunque esté vacío:
   > "Esta métrica mediría el tiempo desde que un developer hace un commit hasta que llega a producción. Requiere la integración GitHub↔Datadog para calcularse automáticamente."

4. **Change Failure Rate** — usar la Demo 2 como contexto:
   > "Si el deploy que rompimos antes hubiera llegado a usuarios, contaría aquí como un deployment fallido. La métrica ideal es menos del 15%."

5. **Failed Deployment Recovery Time** — explicar:
   > "Mide cuánto tardamos en recuperarnos de ese fallo. En nuestro caso, el fix tardó X minutos desde que detectamos el problema hasta que el nuevo deploy estaba sano."

6. Ir a **View Deployments** y mostrar el listado de todos los deploys con timestamps

**Narrativa:**
> "DORA Metrics no mide si la app funciona — mide qué tan bien trabaja el equipo de ingeniería. Son las 4 métricas que diferencian a los equipos de alto rendimiento de los demás, según investigación de Google."

---

## Orden recomendado para el workshop

```
1. Mostrar la app funcionando en producción (workshop.mmonsalves.dev)
        ↓
2. DEMO 1 — Test Optimization (rama separada, sin tocar producción)
        ↓
3. Mostrar APM en vivo — hacer requests a la app y ver trazas en Datadog
        ↓
4. DEMO 2 — Continuous Testing (romper y recuperar producción en vivo)
        ↓
5. DEMO 3 — DORA Metrics (explicar con el historial acumulado)
        ↓
6. Mostrar SAST — vulnerabilidades detectadas en Code Analysis
        ↓
7. Mostrar flujo de remediación Datadog → PR → merge → deploy
```

---

## Preparación previa al workshop

### Ramas a crear con anticipación
```bash
# Demo 1
git checkout -b demo/test-failing
# modificar test_main.py
git push origin demo/test-failing

# Demo 2
git checkout main
git checkout -b demo/break-health
# modificar main.py
git push origin demo/break-health
# NO mergear hasta la demo
```

### Verificar antes de empezar
- [ ] `workshop.mmonsalves.dev` responde correctamente
- [ ] Datadog APM muestra trazas recientes
- [ ] Test Optimization tiene historial de runs verdes
- [ ] DORA Metrics muestra Deployment Frequency con datos
- [ ] Synthetic test `tkm-8uj-cax` está en estado PASSED
- [ ] Rama `demo/test-failing` pusheada y pipeline fallido visible en GitHub
- [ ] Rama `demo/break-health` lista pero sin mergear

### Tabs de Datadog a tener abiertas
1. APM → Services → dd-workshop-api
2. Test Optimization → Test Runs
3. Synthetic Monitoring → Tests + CI Batches
4. DORA Metrics → Explorer
5. Code Analysis → Repositories → dd-workshop
