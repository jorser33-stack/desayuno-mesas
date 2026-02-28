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
