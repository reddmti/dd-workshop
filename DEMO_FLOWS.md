# DD Workshop — Flujos de Demostración

Guía paso a paso para ejecutar cada demo **solo**, sin ayuda externa.
El fix de cada demo usa el botón **"Revert"** de GitHub — sin git, sin código.

---

## Estado de ramas antes de empezar

| Rama | Propósito |
|------|-----------|
| `main` | Código limpio — app funcionando correctamente |
| `demo/test-failing` | Introduce test roto (Demo 1) |
| `demo/break-health` | Rompe el health endpoint (Demo 2) |

---

## DEMO 1 — Test Optimization: test fallido en CI

### Qué muestra
Un developer rompió un test. Datadog Test Optimization lo detecta con detalle antes de que llegue a producción.

### Pasos

**PARTE A — Introducir el bug (1 min)**

1. Ir a GitHub → **Pull requests → New pull request**
2. Base: `main` ← Compare: `demo/test-failing`
3. Título: `demo: test roto para Test Optimization`
4. Crear PR y **hacer merge inmediatamente**
5. El pipeline de GitHub Actions arranca solo

**PARTE B — Mostrar en Datadog (3-4 min)**

Mientras corre el pipeline:

6. Ir a Datadog → **Test Optimization → Test Runs**
7. Filtrar por `Service: dd-workshop-api` y `Branch: main`
8. Esperar que aparezca el run en rojo (2-3 min)
9. Abrir el run → mostrar `test_health` fallando
10. Mostrar el error exacto: `AssertionError: assert 500 == 200`
11. Mostrar el historial: runs anteriores en verde vs este en rojo

**Narrativa:**
> "El developer introdujo un cambio que rompió un test. Datadog no solo dice que falló — muestra qué test, en qué línea, cuánto tardó, y si históricamente este test ha sido inestable."

**PARTE C — Fix en vivo (1 min)**

12. Ir a GitHub → **Pull requests → pestaña "Closed"**
13. Abrir el PR que acabas de mergear
14. Hacer clic en el botón **"Revert"** (aparece al final del PR cerrado)
15. GitHub crea un PR de revert automáticamente → **hacer merge**
16. El pipeline vuelve a correr → todo verde
17. Volver a Test Optimization → mostrar el run verde

---

## DEMO 2 — Continuous Testing: deploy que rompe producción

### Qué muestra
El deploy técnicamente funcionó (Kubernetes levantó los pods), pero Datadog Synthetic detectó que la app no responde bien. El pipeline se bloqueó.

### Pasos

**PARTE A — Introducir el bug (1 min)**

1. Ir a GitHub → **Pull requests → New pull request**
2. Base: `main` ← Compare: `demo/break-health`
3. Título: `demo: health endpoint roto para Continuous Testing`
4. Crear PR y **hacer merge inmediatamente**
5. El pipeline arranca: build → deploy a GKE → Synthetic test

**PARTE B — Mostrar en Datadog (5-6 min)**

Mientras se despliega (tarda ~3-4 min):

6. Mostrar el endpoint funcionando actualmente en producción:
   `https://workshop.mmonsalves.dev/api/health` → responde `{"status":"healthy"}`
7. Mostrar el código del bug en la rama (en GitHub)
8. Ir a Datadog → **Synthetic Monitoring → CI Batches**
9. Esperar que aparezca el batch del pipeline actual
10. Mostrar el resultado: **FAILED** — esperaba 200, recibió 500
11. Ir a GitHub Actions → mostrar el pipeline bloqueado en el paso "Run Synthetic Tests"
12. Mostrar la app en producción rota: `https://workshop.mmonsalves.dev/api/health`

**Narrativa:**
> "El deploy técnicamente funcionó — Kubernetes levantó los pods sin problema. Pero Datadog Continuous Testing validó que la app responde correctamente desde distintas regiones y detectó el fallo. El pipeline quedó bloqueado — el sistema consideró este deploy como fallido."

**PARTE C — Fix en vivo (1 min)**

13. Ir a GitHub → **Pull requests → pestaña "Closed"**
14. Abrir el PR que acabas de mergear
15. Hacer clic en **"Revert"** → GitHub crea PR de revert
16. **Hacer merge** del revert PR
17. El pipeline vuelve a correr → deploy → Synthetic test pasa
18. Mostrar la app funcionando: `https://workshop.mmonsalves.dev/api/health`
19. Ir a **Synthetic → CI Batches** → mostrar el nuevo batch en verde

---

## DEMO 3 — DORA Metrics: visibilidad del equipo

### Qué muestra
Las 4 métricas que miden la salud de un equipo de ingeniería según Google.
No requiere ramas — se muestra con el historial acumulado de deploys.

### Pasos

1. Ir a Datadog → **Software Delivery → DORA Metrics → Explorer**

2. **Deployment Frequency**
   > "Cada barra representa deploys exitosos. Podemos ver cuántas veces deployamos esta semana. Los equipos de alto rendimiento deployean múltiples veces al día."

3. **Change Lead Time**
   > "Tiempo desde que el developer hace commit hasta que llega a producción. Requiere la integración GitHub↔Datadog para calcularse automáticamente."

4. **Change Failure Rate** — usar Demo 2 como contexto
   > "El deploy que rompimos antes contaría aquí como fallido. La métrica ideal es menos del 15%."

5. **Failed Deployment Recovery Time**
   > "Cuánto tardamos en recuperarnos del fallo. En nuestro caso, desde que Synthetic detectó el problema hasta que el fix estaba en producción."

6. Ir a **View Deployments** → mostrar el listado con timestamps de cada deploy

---

## DEMO 4 — SAST / Code Analysis: vulnerabilidades detectadas

### Qué muestra
Datadog escaneó el código en cada push y detectó vulnerabilidades reales en el backend.

### Pasos

1. Ir a Datadog → **Code Analysis → Repositories → dd-workshop**
2. Mostrar las vulnerabilidades detectadas (SQL Injection, credenciales hardcodeadas, MD5, etc.)
3. Abrir una vulnerabilidad → mostrar línea exacta, severidad, descripción
4. Mostrar la opción "Open Fix PR" si está disponible

**Narrativa:**
> "Datadog SAST scaneó el código automáticamente en cada push al repositorio. No necesitamos configurar nada extra — el scanner corre como un job en el pipeline y reporta directamente aquí."

---

## Orden recomendado para el workshop

```
1. Mostrar la app funcionando en producción
   → https://workshop.mmonsalves.dev

2. DEMO 1 — Test Optimization
   → PR de demo/test-failing → merge → ver fallo → Revert

3. APM en vivo
   → Hacer requests a la app → mostrar trazas en Datadog APM

4. DEMO 2 — Continuous Testing
   → PR de demo/break-health → merge → deploy → Synthetic falla → Revert

5. DEMO 3 — DORA Metrics
   → Explicar con el historial acumulado de deploys

6. DEMO 4 — Code Analysis / SAST
   → Mostrar vulnerabilidades detectadas en el repo
```

---

## Checklist de preparación (antes de la presentación)

### Ramas
- [ ] `main` → `test_health` espera `status_code == 200` ✅
- [ ] `main` → `/api/health` devuelve `{"status": "healthy"}` ✅
- [ ] `demo/test-failing` existe en remoto (push hecho) ✅
- [ ] `demo/break-health` existe en remoto (push hecho) ✅

### Datadog
- [ ] `workshop.mmonsalves.dev/api/health` responde correctamente
- [ ] APM → Services → `dd-workshop-api` muestra trazas recientes
- [ ] Test Optimization → historial de runs verdes visible
- [ ] DORA Metrics → Deployment Frequency con datos
- [ ] Synthetic Tests → ambos tests en estado PASSED
- [ ] Code Analysis → vulnerabilidades visibles en el repo

### Tabs de Datadog a tener abiertas
1. APM → Services → dd-workshop-api
2. Test Optimization → Test Runs
3. Synthetic Monitoring → Tests + CI Batches
4. DORA Metrics → Explorer
5. Code Analysis → Repositories → dd-workshop

---

## El botón "Revert" de GitHub

Este es el mecanismo de fix para Demo 1 y Demo 2:

1. Ir a **github.com/reddmti/dd-workshop/pulls**
2. Clic en **"Closed"** para ver PRs mergeados
3. Abrir el PR de la demo
4. Bajar hasta el final → botón **"Revert"**
5. GitHub crea un nuevo PR con el revert automáticamente
6. Hacer merge del revert → el pipeline restaura todo

**No se toca código. No se usa git. No se necesita ayuda.**
