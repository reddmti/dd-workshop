"""Genera WORKSHOP_FLUJOS.pdf - guion corto para el presentador."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

OUT = r"C:\Users\matia\Documents\GitHub\dd-workshop\WORKSHOP_FLUJOS.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body', alignment=TA_JUSTIFY, fontSize=10, leading=13))
styles.add(ParagraphStyle(name='H1Custom', fontSize=18, leading=22, spaceAfter=10,
                          textColor=colors.HexColor('#632ca6'), fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='H2Custom', fontSize=13, leading=16, spaceAfter=6, spaceBefore=10,
                          textColor=colors.HexColor('#632ca6'), fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='H3Custom', fontSize=11, leading=14, spaceAfter=4, spaceBefore=8,
                          textColor=colors.HexColor('#333333'), fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='Note', fontSize=9, leading=12, textColor=colors.HexColor('#555555'),
                          leftIndent=8, rightIndent=8, backColor=colors.HexColor('#fff8dc'),
                          borderPadding=5, spaceAfter=6))

def H1(t): return Paragraph(t, styles['H1Custom'])
def H2(t): return Paragraph(t, styles['H2Custom'])
def H3(t): return Paragraph(t, styles['H3Custom'])
def P(t): return Paragraph(t, styles['Body'])
def N(t): return Paragraph("<b>Tip:</b> " + t, styles['Note'])
def SP(h=5): return Spacer(1, h)

story = []

# ============ PORTADA ============
story.append(Spacer(1, 2.2*inch))
story.append(Paragraph("Workshop Datadog", ParagraphStyle(
    'cover', fontSize=30, leading=36, alignment=TA_CENTER,
    textColor=colors.HexColor('#632ca6'), fontName='Helvetica-Bold')))
story.append(Spacer(1, 0.25*inch))
story.append(Paragraph("Guion del presentador", ParagraphStyle(
    'sub', fontSize=16, leading=20, alignment=TA_CENTER,
    textColor=colors.HexColor('#333333'))))
story.append(Spacer(1, 0.4*inch))
story.append(Paragraph("dd-workshop (con gates)  vs  dd-workshop-nogates", ParagraphStyle(
    'sub2', fontSize=12, leading=15, alignment=TA_CENTER,
    textColor=colors.HexColor('#666666'))))
story.append(Spacer(1, 1.8*inch))
story.append(Paragraph("Matias Monsalves &bull; Tekservicios", ParagraphStyle(
    'aut', fontSize=10, leading=13, alignment=TA_CENTER,
    textColor=colors.HexColor('#888888'))))
story.append(PageBreak())

# ============ 1. IDEA CENTRAL ============
story.append(H1("1. Idea central de la workshop"))
story.append(P("Dos repositorios identicos, dos pipelines opuestos. El objetivo es mostrar, en vivo, "
               "el contraste entre un equipo que usa <b>gates de calidad</b> y otro que no."))
story.append(SP())
story.append(H3("Lo que vamos a demostrar"))
story.append(P("&bull; <b>Code Security (SAST)</b> &mdash; Datadog encuentra vulnerabilidades sin ejecutar el codigo."))
story.append(P("&bull; <b>Test Optimization</b> &mdash; visibilidad de los tests unitarios en cada push."))
story.append(P("&bull; <b>Continuous Testing</b> &mdash; sinteticos que validan la app ya desplegada."))
story.append(P("&bull; <b>DORA Metrics</b> &mdash; las 4 metricas de performance de entrega."))
story.append(P("&bull; <b>PR Gates</b> &mdash; bloqueo automatico del merge cuando algo no cumple las reglas."))
story.append(SP())
story.append(H3("Por que dos repos"))
story.append(P("Con un solo repo tendriamos que hacer merge y revert continuamente para mostrar ambos "
               "comportamientos. Con dos, cada escenario esta siempre listo para presentar en menos de un minuto."))
story.append(SP())

data = [
    ["", "dd-workshop", "dd-workshop-nogates"],
    ["URL", "workshop.mmonsalves.dev", "workshop2.mmonsalves.dev"],
    ["Pipeline", "Tests y SAST bloquean deploy", "Todo pasa, aunque este roto"],
    ["Proposito", "Mostrar que se previene", "Mostrar que se detecta post-deploy"],
]
t = Table(data, colWidths=[1.2*inch, 2.6*inch, 2.6*inch])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#632ca6')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f0fa')]),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t)
story.append(PageBreak())

# ============ 2. LOS DOS REPOS ============
story.append(H1("2. Los dos repositorios"))

story.append(H2("dd-workshop (con gates)"))
story.append(P("Representa al equipo maduro: el deploy depende de tests y SAST, y Datadog PR Gates impide "
               "que un pull request rompa main. Si algo falla en el pipeline, nunca llega a produccion."))
story.append(P("Tiene dos ramas de demo listas para usar: una que rompe un test unitario, y otra que "
               "rompe el endpoint de health."))
story.append(SP())

story.append(H2("dd-workshop-nogates"))
story.append(P("Representa al equipo sin disciplina: el pipeline siempre despliega, aunque tests y sinteticos "
               "fallen. El valor aca es mostrar que, incluso en ese escenario, Datadog detecta el problema en "
               "produccion y lo reporta en DORA como despliegue fallido."))
story.append(P("Tiene una rama de demo que rompe el endpoint de health."))

story.append(PageBreak())

# ============ 3. QUE VALIDAN LOS TESTS ============
story.append(H1("3. Que validan los tests"))
story.append(P("Son tests de pytest sobre la API FastAPI. Datadog no los ejecuta, solo los instrumenta "
               "para enviar resultados a Test Optimization. Son 15 en total, agrupados por area:"))
story.append(SP())

story.append(H3("Salud y landing"))
story.append(P("&bull; <b>test_health</b> / <b>test_root</b>: verifican que la app responde."))

story.append(H3("Login y autorizacion"))
story.append(P("&bull; <b>test_login_valid</b>: usuario correcto obtiene token."))
story.append(P("&bull; <b>test_login_invalid</b>: credenciales erroneas devuelven 401."))
story.append(P("&bull; <b>test_login_returns_role</b>: el JSON del login incluye el rol del usuario."))
story.append(P("&bull; <b>test_me_authorized</b> / <b>test_me_unauthorized</b>: endpoint protegido con y sin token."))

story.append(H3("Productos (CRUD)"))
story.append(P("&bull; <b>test_products_list_unauthorized</b>: sin token se rechaza."))
story.append(P("&bull; <b>test_products_list_authorized</b>: con token se listan productos."))
story.append(P("&bull; <b>test_products_pagination</b>: el parametro limit se respeta."))
story.append(P("&bull; <b>test_product_get_single</b>: trae un producto por id."))
story.append(P("&bull; <b>test_product_not_found</b>: id inexistente devuelve 404."))
story.append(P("&bull; <b>test_product_create</b>: se puede crear un producto."))
story.append(P("&bull; <b>test_product_delete</b>: se puede borrar un producto."))

story.append(H3("Utilidades"))
story.append(P("&bull; <b>test_hash_endpoint</b>: el endpoint de hash responde. "
               "Ojo: pasa aunque use MD5 (inseguro). Quien detecta la debilidad es SAST, no el test."))
story.append(SP())

story.append(N("Punto para levantar en vivo: el test verde significa \"el contrato funciona\", no \"el codigo "
               "es seguro\". Por eso necesitamos tambien SAST."))
story.append(PageBreak())

# ============ 4. FEATURES DE DATADOG ============
story.append(H1("4. Features de Datadog que vamos a mostrar"))

story.append(H2("Test Optimization"))
story.append(P("Convierte cada ejecucion de pytest en telemetria. Ves que tests corrieron, cuales fallaron, "
               "cuales son flaky, y como evolucionan commit a commit."))
story.append(P("<b>Donde:</b> Software Delivery &rarr; Test Optimization."))

story.append(H2("Code Security (SAST)"))
story.append(P("Analiza el codigo fuente y detecta vulnerabilidades conocidas sin ejecutar la app. "
               "Nuestro backend tiene 7 bugs de seguridad intencionales listos para lucirse."))
story.append(P("<b>Donde:</b> Security &rarr; Code Security."))

story.append(H2("Continuous Testing (Synthetics)"))
story.append(P("Lanza un test sintetico contra el endpoint real desde el pipeline CI y tambien periodicamente. "
               "Si la URL no responde bien, queda en rojo."))
story.append(P("<b>Donde:</b> Digital Experience &rarr; Synthetic Monitoring."))

story.append(H2("DORA Metrics"))
story.append(P("Cada despliegue se registra con su resultado. Datadog calcula las 4 metricas clave: "
               "frecuencia de despliegue, lead time, change failure rate y MTTR."))
story.append(P("<b>Donde:</b> Software Delivery &rarr; DORA Metrics."))

story.append(H2("PR Gates"))
story.append(P("Reglas configuradas en Datadog que aparecen como required status check en el PR de GitHub. "
               "Si el gate esta rojo, GitHub no deja hacer merge."))
story.append(P("<b>Donde:</b> Software Delivery &rarr; Quality Gates."))

story.append(H2("APM y Logs"))
story.append(P("La app esta instrumentada con ddtrace. Cada request tiene trace, y los logs se correlacionan "
               "automaticamente. Buen complemento si alguien pregunta por observabilidad runtime."))
story.append(P("<b>Donde:</b> APM &rarr; Services &rarr; dd-workshop-api."))
story.append(PageBreak())

# ============ HELPERS para badges de repo ============
def repo_banner(repo_name, descripcion, color):
    data = [[f"REPOSITORIO: {repo_name}", descripcion]]
    t = Table(data, colWidths=[2.4*inch, 4.0*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor(color)),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#f5f0fa')),
        ('TEXTCOLOR', (0,0), (0,0), colors.white),
        ('TEXTCOLOR', (1,0), (1,0), colors.HexColor('#333333')),
        ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,0), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    return t

# ============ 5. DEMOS REPO 1 ============
story.append(H1("5. Demos del REPOSITORIO 1: dd-workshop"))
story.append(repo_banner("dd-workshop", "Pipeline CON gates &bull; workshop.mmonsalves.dev", '#2e7d32'))
story.append(SP(8))
story.append(P("Las siguientes 3 demos se hacen sobre el repositorio con gates. La idea es mostrar como "
               "Datadog <b>previene</b> que el codigo malo llegue a produccion."))
story.append(SP())

story.append(H2("Demo A &mdash; Code Security (SAST)"))
story.append(P("<b>Duracion:</b> 3 min &bull; <b>Feature:</b> Datadog Code Security"))
story.append(H3("Flujo"))
story.append(P("1. Abrir Datadog &rarr; Security &rarr; Code Security, filtrar por <i>dd-workshop-api</i>."))
story.append(P("2. Mostrar la lista de vulnerabilidades (SQL injection, command injection, MD5, secretos, etc)."))
story.append(P("3. Abrir una: Datadog indica archivo, linea, severidad y un fix sugerido."))
story.append(P("4. Saltar al mismo archivo en GitHub para confirmar la linea."))
story.append(P("5. Cerrar con: esto corre en cada push, sin que el dev tenga que hacer nada."))

story.append(H2("Demo B &mdash; Test Optimization + PR Gate"))
story.append(P("<b>Duracion:</b> 5 min &bull; <b>Rama:</b> demo/test-failing &bull; "
               "<b>Feature:</b> Test Optimization + Quality Gates"))
story.append(H3("Flujo"))
story.append(P("1. En GitHub, abrir Pull Request desde <i>demo/test-failing</i> hacia <i>main</i>."))
story.append(P("2. Los checks corren. El job de tests falla, y el check <b>Datadog Quality Gate</b> se pone en rojo."))
story.append(P("3. Ir a Datadog &rarr; Test Optimization, mostrar el test roto con stacktrace y contexto del commit."))
story.append(P("4. Volver al PR: el boton de merge esta bloqueado. Aca se levanta el valor del gate."))
story.append(P("5. \"Fix\": en GitHub, click en <b>Revert</b> del merge anterior &mdash; o cerrar el PR."))

story.append(H2("Demo C &mdash; PR Gates en detalle"))
story.append(P("<b>Duracion:</b> 4-5 min &bull; <b>Feature:</b> Datadog Quality Gates"))
story.append(H3("Flujo"))
story.append(P("1. Datadog &rarr; Quality Gates: mostrar las 6 reglas configuradas (tests, SAST, coverage, etc)."))
story.append(P("2. Abrir un PR que las viole (sirve el mismo demo/test-failing)."))
story.append(P("3. En el PR, mostrar el check <b>Datadog Quality Gate</b> en rojo con link a detalle."))
story.append(P("4. Click en <i>Details</i>: lleva al dashboard de Datadog con la regla que bloqueo."))
story.append(P("5. Merge esta deshabilitado porque el check es required en la branch protection."))

story.append(SP(8))
story.append(N("Mensaje al cerrar el bloque del repo 1: \"con gates, el codigo malo simplemente no llega a "
               "produccion\". Aca pasamos al repo 2 para mostrar lo opuesto."))
story.append(PageBreak())

# ============ 6. DEMOS REPO 2 ============
story.append(H1("6. Demos del REPOSITORIO 2: dd-workshop-nogates"))
story.append(repo_banner("dd-workshop-nogates", "Pipeline SIN gates &bull; workshop2.mmonsalves.dev", '#c62828'))
story.append(SP(8))
story.append(P("Aca el pipeline siempre despliega, aunque tests o sinteticos fallen. La narrativa cambia: "
               "Datadog ya no <b>previene</b>, ahora <b>detecta</b> el problema una vez en produccion."))
story.append(SP())

story.append(H2("Demo D &mdash; Continuous Testing (Synthetics)"))
story.append(P("<b>Duracion:</b> 5 min &bull; <b>Rama:</b> demo/break-health &bull; "
               "<b>Feature:</b> Synthetic Monitoring"))
story.append(H3("Flujo"))
story.append(P("1. Abrir PR desde <i>demo/break-health</i> y hacer merge. Los tests pasan porque nadie validaba el 200 del health."))
story.append(P("2. El pipeline despliega igual. El sintetico corre contra workshop2.mmonsalves.dev y falla."))
story.append(P("3. Como el step tiene continue-on-error, el pipeline aparece verde pero el sintetico esta rojo."))
story.append(P("4. Datadog &rarr; Synthetic Monitoring: mostrar la caida, el 500, y el historial de la ultima ejecucion."))
story.append(P("5. Enfatizar: sin gates, el problema llega a produccion. Datadog lo detecta igual."))
story.append(P("6. <b>Revert</b> en GitHub para volver a la version sana."))

story.append(SP(8))
story.append(N("Esta es la unica demo que se ejecuta en el repo 2. Su valor es comparativo: el mismo cambio "
               "que en el repo 1 quedaba bloqueado, aqui llega al usuario final."))
story.append(PageBreak())

# ============ 7. DEMO COMPARATIVA ============
story.append(H1("7. Demo comparativa: DORA Metrics"))
story.append(repo_banner("AMBOS REPOSITORIOS", "Comparacion lado a lado en una sola vista", '#1565c0'))
story.append(SP(8))
story.append(P("Esta demo no se hace sobre un repo en particular: se filtra por servicio dentro del mismo "
               "dashboard de Datadog para comparar resultados."))
story.append(SP())

story.append(H2("Demo E &mdash; DORA Metrics"))
story.append(P("<b>Duracion:</b> 3-4 min &bull; <b>Feature:</b> DORA Metrics"))
story.append(H3("Flujo"))
story.append(P("1. Datadog &rarr; Software Delivery &rarr; DORA Metrics."))
story.append(P("2. Filtrar por <i>dd-workshop-api</i> (repo 1, con gates): frecuencia sana, change failure rate bajo."))
story.append(P("3. Cambiar el filtro a <i>dd-workshop-nogates-api</i> (repo 2, sin gates): mismo volumen pero change failure rate alto."))
story.append(P("4. Cerrar con la narrativa: los gates se traducen directamente en mejores metricas DORA."))
story.append(PageBreak())

# ============ 8. ORDEN SUGERIDO ============
story.append(H1("8. Orden sugerido para la presentacion"))
story.append(P("La presentacion se estructura en tres bloques claros: primero todo lo del repo 1 (prevencion), "
               "luego el repo 2 (deteccion), y finalmente la comparativa con DORA."))
story.append(SP())

data = [
    ["#", "Demo", "Feature", "Repo", "Tiempo"],
    ["A", "Code Security", "SAST", "Repo 1: dd-workshop", "3 min"],
    ["B", "Test Optimization + Gate", "Test Opt + Quality Gate", "Repo 1: dd-workshop", "5 min"],
    ["C", "PR Gates en detalle", "Quality Gates", "Repo 1: dd-workshop", "5 min"],
    ["D", "Continuous Testing", "Synthetics", "Repo 2: nogates", "5 min"],
    ["E", "DORA Metrics", "DORA", "Comparativa ambos", "4 min"],
]
t = Table(data, colWidths=[0.3*inch, 1.6*inch, 1.7*inch, 2.0*inch, 0.7*inch])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#632ca6')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f0fa')]),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
]))
story.append(t)
story.append(SP(20))
story.append(N("Antes de la presentacion: recrear las ramas demo/test-failing y demo/break-health para que "
               "esten listas para abrir PR. Despues de cada demo, el Revert de GitHub deja main limpio."))

# ============ BUILD ============
doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=0.9*inch, rightMargin=0.9*inch,
                        topMargin=0.8*inch, bottomMargin=0.8*inch,
                        title="Workshop Datadog - Guion del presentador",
                        author="Matias Monsalves")
doc.build(story)
print(f"OK: {OUT}")
