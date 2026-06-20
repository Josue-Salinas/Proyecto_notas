from flask import Flask, request, render_template_string

app = Flask(__name__)

PESOS = [10, 20, 30, 40, 50]

PLANTILLA = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Calculadora de Promedio Academico</title>
<style>
    * { box-sizing: border-box; }
    body {
        font-family: 'Segoe UI', Arial, sans-serif;
        background: #eef1f7;
        min-height: 100vh;
        margin: 0;
        padding: 30px;
        display: flex;
        justify-content: center;
    }
    .contenedor {
        background: white;
        padding: 35px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        width: 100%;
        max-width: 700px;
    }
    h1 {
        text-align: center;
        color: #1f2d3d;
        margin-bottom: 5px;
        font-size: 24px;
    }
    .subtitulo {
        text-align: center;
        color: #8a94a6;
        font-size: 13px;
        margin-bottom: 25px;
    }
    label {
        font-weight: 600;
        color: #4a5568;
        font-size: 13px;
        display: block;
        margin-bottom: 5px;
    }
    select, input {
        padding: 10px;
        border: 1px solid #d1d6e0;
        border-radius: 6px;
        font-size: 14px;
        width: 100%;
    }
    .config {
        margin-bottom: 20px;
        max-width: 280px;
    }
    .fila {
        display: grid;
        grid-template-columns: 2fr 1.2fr 1fr 1fr auto;
        gap: 8px;
        margin-bottom: 12px;
        align-items: end;
    }
    .fila .otro {
        display: none;
    }
    .fila.mostrar-otro .otro {
        display: block;
    }
    .btn-quitar {
        background: #fde8e8;
        color: #c0392b;
        border: 1px solid #f5c6c6;
        border-radius: 6px;
        padding: 10px;
        cursor: pointer;
        font-weight: bold;
        height: 42px;
    }
    .btn-quitar:hover { background: #f8d0d0; }
    .btn-quitar:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }
    .acciones {
        display: flex;
        gap: 10px;
        margin: 20px 0 10px;
    }
    button {
        padding: 12px 18px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 600;
        transition: 0.15s;
    }
    .btn-agregar {
        background: #eef1f7;
        color: #2c5282;
        border: 1px solid #c3cfe2;
    }
    .btn-agregar:hover { background: #dbe4f3; }
    .btn-agregar:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    .btn-calcular {
        background: #2c5282;
        color: white;
        flex: 1;
    }
    .btn-calcular:hover { background: #244569; }
    .info-pesos {
        font-size: 12px;
        color: #8a94a6;
        margin-bottom: 15px;
    }
    .error {
        background: #fde8e8;
        color: #c0392b;
        border: 1px solid #f5c6c6;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 15px;
        font-size: 14px;
    }
    .resultado {
        margin-top: 25px;
        padding: 22px;
        border-radius: 10px;
        border: 1px solid;
    }
    .aprobado {
        background: #eafaf1;
        color: #1e7e44;
        border-color: #a3e4bf;
    }
    .reprobado {
        background: #fdecea;
        color: #b3261e;
        border-color: #f5b8b2;
    }
    .resultado-titulo {
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 12px;
        text-align: center;
    }
    .nota-redondeada {
        font-size: 28px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 4px;
    }
    .estado {
        text-align: center;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .detalle-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        font-size: 13px;
        color: #44505e;
        background: rgba(255,255,255,0.5);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 15px;
    }
    .detalle-grid div span {
        display: block;
        font-weight: 700;
        font-size: 15px;
        color: #1f2d3d;
    }
    .desglose {
        font-size: 13px;
        color: #44505e;
        background: rgba(255,255,255,0.5);
        border-radius: 8px;
        padding: 12px 16px;
    }
    .desglose table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 8px;
    }
    .desglose th, .desglose td {
        text-align: left;
        padding: 6px 4px;
        font-size: 12px;
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }
    .desglose th {
        color: #8a94a6;
        font-weight: 600;
    }
</style>
</head>
<body>
<div class="contenedor">
    <h1>Calculadora de Promedio Academico</h1>
    <div class="subtitulo">Ingresa tus componentes evaluativos y revisa tu situacion en el curso</div>

    <form method="POST" id="formulario">
        <div class="config">
            <label>Nota minima aprobatoria</label>
            <input type="number" step="0.1" min="0" max="20" name="nota_minima" value="11" required>
        </div>

        <label>Componentes evaluativos</label>
        <div class="info-pesos">Los pesos de todos los componentes deben sumar 100%. Nota maxima por componente: 20.</div>
        <div id="componentes"></div>

        <div class="acciones">
            <button type="button" class="btn-agregar" id="btnAgregar" onclick="agregarFila()">Agregar componente</button>
            <button type="submit" class="btn-calcular">Calcular</button>
        </div>

        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </form>

    {% if resultado %}
    <div class="resultado {{ 'aprobado' if resultado.aprobado else 'reprobado' }}">
        <div class="resultado-titulo">Resultado de la evaluacion</div>
        <div class="nota-redondeada">{{ resultado.nota_redondeada }} / 20</div>
        <div class="estado">
            {% if resultado.aprobado %}
                Curso aprobado considerando lo evaluado hasta ahora
            {% else %}
                Curso no aprobado considerando lo evaluado hasta ahora
            {% endif %}
        </div>

        <div class="detalle-grid">
            <div>Nota exacta (con decimales)<span>{{ resultado.nota_actual }}</span></div>
            <div>Nota minima para aprobar<span>{{ resultado.nota_minima }}</span></div>
            {% if resultado.pendientes %}
            <div>Nota minima posible al final<span>{{ resultado.nota_minima_posible }}</span></div>
            <div>Nota maxima posible al final<span>{{ resultado.nota_maxima_posible }}</span></div>
            {% else %}
            <div>Peso evaluado<span>100%</span></div>
            <div>Componentes evaluados<span>{{ resultado.total_componentes }}</span></div>
            {% endif %}
        </div>

        {% if resultado.pendientes %}
        <div class="desglose">
            <strong>Componentes pendientes de rendir</strong>
            <table>
                <tr>
                    <th>Componente</th>
                    <th>Peso</th>
                    <th>Nota necesaria para aprobar</th>
                </tr>
                {% for p in resultado.pendientes %}
                <tr>
                    <td>{{ p.nombre }}</td>
                    <td>{{ p.porcentaje }}%</td>
                    <td>{{ p.nota_necesaria }}</td>
                </tr>
                {% endfor %}
            </table>
            <p style="margin-top:10px; font-size:12px; color:#8a94a6;">
                La nota necesaria de cada componente pendiente se calcula asumiendo que en los demas componentes pendientes obtienes exactamente la nota minima aprobatoria.
                La nota minima y maxima posible al final asumen 0 y 20 respectivamente en todos los componentes pendientes.
            </p>
        </div>
        {% endif %}
    </div>
    {% endif %}
</div>

<script>
const pesos = {{ pesos | tojson }};
const MAX_COMPONENTES = 6;
const MIN_COMPONENTES = 2;

function actualizarBotones() {
    const total = document.querySelectorAll(".fila").length;
    document.getElementById("btnAgregar").disabled = total >= MAX_COMPONENTES;
    document.querySelectorAll(".btn-quitar").forEach(btn => {
        btn.disabled = total <= MIN_COMPONENTES;
    });
}

function crearFila(nombre, porcentaje, nota) {
    const fila = document.createElement("div");
    fila.className = "fila";

    let opciones = '<option value="">Elegir</option>';
    pesos.forEach(p => {
        const sel = String(p) === String(porcentaje) ? "selected" : "";
        opciones += `<option value="${p}" ${sel}>${p}%</option>`;
    });
    const esOtro = porcentaje && !pesos.includes(Number(porcentaje));
    opciones += `<option value="otro" ${esOtro ? "selected" : ""}>Otro...</option>`;

    fila.innerHTML = `
        <div>
            <label>Componente</label>
            <input type="text" name="nombre" placeholder="Ej: Exposicion" value="${nombre || ''}" required>
        </div>
        <div>
            <label>Peso</label>
            <select name="porcentaje" onchange="cambioPeso(this)" required>${opciones}</select>
        </div>
        <div class="otro" style="${esOtro ? 'display:block' : ''}">
            <label>% personalizado</label>
            <input type="number" step="1" min="1" max="100" name="porcentaje_otro" value="${esOtro ? porcentaje : ''}">
        </div>
        <div>
            <label>Nota</label>
            <input type="number" step="1" min="0" max="20" name="nota" placeholder="Sin rendir" value="${nota !== undefined ? nota : ''}">
        </div>
        <div>
            <label>&nbsp;</label>
            <button type="button" class="btn-quitar" onclick="quitarFila(this)">Quitar</button>
        </div>
    `;
    if (esOtro) fila.classList.add("mostrar-otro");

    document.getElementById("componentes").appendChild(fila);
    actualizarBotones();
}

function quitarFila(boton) {
    const total = document.querySelectorAll(".fila").length;
    if (total <= MIN_COMPONENTES) return;
    boton.closest(".fila").remove();
    actualizarBotones();
}

function cambioPeso(select) {
    const fila = select.closest(".fila");
    const campoOtro = fila.querySelector('input[name="porcentaje_otro"]');
    if (select.value === "otro") {
        fila.classList.add("mostrar-otro");
        campoOtro.required = true;
    } else {
        fila.classList.remove("mostrar-otro");
        campoOtro.required = false;
        campoOtro.value = "";
    }
}

function agregarFila() {
    const total = document.querySelectorAll(".fila").length;
    if (total >= MAX_COMPONENTES) return;
    crearFila();
}

document.getElementById("formulario").addEventListener("invalid", function(e) {
    e.preventDefault();
}, true);

document.getElementById("formulario").addEventListener("submit", function(e) {
    const invalidos = document.querySelectorAll(".fila input:invalid, .fila select:invalid");
    if (invalidos.length > 0) {
        e.preventDefault();
        alert("Por favor completa todos los campos obligatorios antes de calcular.");
    }
});

const valoresPrevios = {{ valores_previos | tojson }};
if (valoresPrevios && valoresPrevios.length > 0) {
    valoresPrevios.forEach(c => crearFila(c.nombre, c.porcentaje, c.nota));
} else {
    crearFila();
    crearFila();
}
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    error = None
    valores_previos = []

    if request.method == "POST":
        nota_minima = float(request.form.get("nota_minima"))
        nombres = request.form.getlist("nombre")
        porcentajes = request.form.getlist("porcentaje")
        porcentajes_otro = request.form.getlist("porcentaje_otro")
        notas = request.form.getlist("nota")

        if len(nombres) < 2:
            error = "Debe haber al menos 2 componentes."
        elif len(nombres) > 6:
            error = "No se permiten mas de 6 componentes."

        componentes = []

        if not error:
            suma_porcentaje_total = 0

            for nombre, porcentaje, porcentaje_otro, nota in zip(nombres, porcentajes, porcentajes_otro, notas):
                if porcentaje == "" or porcentaje is None:
                    error = "Todos los componentes deben tener un peso asignado."
                    break

                if porcentaje == "otro":
                    if porcentaje_otro.strip() == "":
                        error = "Falta especificar el porcentaje personalizado en uno de los componentes."
                        break
                    porcentaje = float(porcentaje_otro)
                else:
                    porcentaje = float(porcentaje)

                if porcentaje <= 0 or porcentaje > 100:
                    error = "Los pesos deben estar entre 1% y 100%."
                    break

                valores_previos.append({"nombre": nombre, "porcentaje": porcentaje, "nota": nota})
                suma_porcentaje_total += porcentaje

                nota_val = None
                if nota.strip() != "":
                    nota_val = float(nota)
                    if nota_val < 0 or nota_val > 20:
                        error = "Las notas deben estar entre 0 y 20."
                        break

                componentes.append({"nombre": nombre, "porcentaje": porcentaje, "nota": nota_val})

            if not error and round(suma_porcentaje_total) != 100:
                error = f"Los pesos de los componentes suman {round(suma_porcentaje_total)}%, pero deben sumar exactamente 100%."

        if not error:
            puntos_obtenidos = sum(c["nota"] * c["porcentaje"] for c in componentes if c["nota"] is not None)
            peso_pendiente_total = sum(c["porcentaje"] for c in componentes if c["nota"] is None)
            peso_rendido_total = 100 - peso_pendiente_total

            nota_actual = puntos_obtenidos / 100

            pendientes = []
            for c in componentes:
                if c["nota"] is None:
                    otros_pendientes = peso_pendiente_total - c["porcentaje"]
                    puntos_restantes_necesarios = (nota_minima * 100) - puntos_obtenidos - (nota_minima * otros_pendientes)
                    nota_necesaria = puntos_restantes_necesarios / c["porcentaje"] if c["porcentaje"] > 0 else 0
                    nota_necesaria = max(0, min(20, nota_necesaria))
                    pendientes.append({
                        "nombre": c["nombre"],
                        "porcentaje": c["porcentaje"],
                        "nota_necesaria": round(nota_necesaria, 2),
                    })

            if peso_pendiente_total > 0:
                nota_minima_posible = puntos_obtenidos / 100
                nota_maxima_posible = (puntos_obtenidos + 20 * peso_pendiente_total) / 100
            else:
                nota_minima_posible = None
                nota_maxima_posible = None

            nota_redondeada = round(nota_actual)
            aprobado = nota_redondeada >= nota_minima

            resultado = {
                "nota_actual": round(nota_actual, 2),
                "nota_redondeada": nota_redondeada,
                "aprobado": aprobado,
                "nota_minima": nota_minima,
                "pendientes": pendientes,
                "nota_minima_posible": round(nota_minima_posible, 2) if nota_minima_posible is not None else None,
                "nota_maxima_posible": round(nota_maxima_posible, 2) if nota_maxima_posible is not None else None,
                "total_componentes": len(componentes),
            }

    return render_template_string(PLANTILLA, resultado=resultado, error=error, pesos=PESOS, valores_previos=valores_previos)


if __name__ == "__main__":
    app.run(debug=True)