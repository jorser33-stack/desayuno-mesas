FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8000
EXPOSE 8000
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers=2 --threads=4 --timeout=60

web: gunicorn app:app --workers=2 --threads=4 --timeout=60
# Desayuno – Control de Mesas (Web Completa)

App web (Flask) para 4 turnos (07,08,09,10) y 30 mesas totales.
- Reservas por **rango de fechas** (mismo turno)
- Validación de cupo total por fecha+turno
- Vista de próximos 7 días con libres/ocupadas
- Detalle por día y **cancelación**

## Variables de entorno
- `TOTAL_MESAS` (default 30)
- `BUSINESS_NAME` (texto del header)
- `SECRET_KEY`
- `DATABASE_URL` (usar `sqlite:////data/desayuno.db` en Render con Disk `/data`)

Flask==2.3.3
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.21
Werkzeug==2.3.7
gunicorn==21.2.0

python-3.11.8
body{background:#fafafa}
.table td,.table th{vertical-align:middle}

{% extends 'base.html' %}
{% block content %}
<h2>Detalle del día {{ fecha.strftime('%d-%m-%Y') }}</h2>
<div class="row g-3">
  {% for t in slots %}
  <div class="col-md-6">
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <strong>Turno {{ t }}</strong>
        <span class="badge bg-secondary">{{ total - (por_turno[t]|sum(attribute='mesas')) }} libres</span>
      </div>
      <div class="card-body">
        {% set lista = por_turno[t] %}
        {% if lista %}
        <div class="table-responsive">
          <table class="table table-sm">
            <thead><tr><th>#</th><th>Mesas</th><th>Nombre</th><th>Hab.</th><th>Nota</th><th></th></tr></thead>
            <tbody>
            {% for r in lista %}
              <tr>
                <td>{{ r.id }}</td>
                <td>{{ r.mesas }}</td>
                <td>{{ r.nombre or '-' }}</td>
                <td>{{ r.habitacion or '-' }}</td>
                <td>{{ r.nota or '-' }}</td>
                <td>
                  <form method="post" action="/cancelar/{{ r.id }}" onsubmit="return confirm('¿Cancelar la reserva {{ r.id }}?');">
                    <button class="btn btn-sm btn-outline-danger">Cancelar</button>
                  </form>
                </td>
              </tr>
            {% endfor %}
            </tbody>
          </table>
        </div>
        {% else %}
          <div class="text-muted">Sin reservas.</div>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
</div>
{% endblock %}

{% extends 'base.html' %}
{% block content %}
<h2>Nueva reserva (rango de fechas)</h2>
<form method="post" class="row g-3 mt-1">
  <div class="col-md-3">
    <label class="form-label">Desde (DD-MM-AAAA)</label>
    <input name="fecha_desde" class="form-control" value="{{ hoy.strftime('%d-%m-%Y') }}" required>
  </div>
  <div class="col-md-3">
    <label class="form-label">Hasta (DD-MM-AAAA)</label>
    <input name="fecha_hasta" class="form-control" value="{{ manana.strftime('%d-%m-%Y') }}" required>
  </div>
  <div class="col-md-3">
    <label class="form-label">Turno</label>
    <select name="turno" class="form-select">
      {% for t in slots %}<option value="{{ t }}">{{ t }}</option>{% endfor %}
    </select>
  </div>
  <div class="col-md-3">
    <label class="form-label">Mesas</label>
    <input type="number" min="1" name="mesas" value="1" class="form-control">
  </div>
  <div class="col-md-4">
    <label class="form-label">Nombre (opcional)</label>
    <input name="nombre" class="form-control">
  </div>
  <div class="col-md-2">
    <label class="form-label">Habitación (opcional)</label>
    <input name="habitacion" class="form-control">
  </div>
  <div class="col-md-6">
    <label class="form-label">Nota (opcional)</label>
    <input name="nota" class="form-control">
  </div>
  <div class="col-12">
    <button class="btn btn-primary">Guardar</button>
  </div>
</form>
<p class="small text-muted mt-3">El sistema valida que haya cupo suficiente en <strong>todas</strong> las fechas del rango antes de crear la reserva.</p>
{% endblock %}
