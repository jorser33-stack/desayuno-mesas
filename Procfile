{% extends 'base.html' %}
{% block content %}
<h1 class="mb-3">Disponibilidad (próximos 7 días)</h1>
<p class="text-muted">Capacidad total: {{ total }} mesas por turno</p>
<div class="table-responsive">
<table class="table table-bordered align-middle">
  <thead>
    <tr>
      <th>Fecha</th>
      {% for t in slots %}<th class="text-center">{{ t }}</th>{% endfor %}
    </tr>
  </thead>
  <tbody>
    {% for fila in tabla %}
      <tr>
        <td><a href="/detalle/{{ fila.fecha.strftime('%d-%m-%Y') }}">{{ fila.fecha.strftime('%d-%m-%Y') }}</a></td>
        {% for item in fila.turnos %}
          {% set disp = item.disponibles %}
          {% set ocup = item.ocupadas %}
          <td class="text-center {{ 'table-success' if disp > total*0.5 else ('table-warning' if disp>0 else 'table-danger') }}">
            <div><strong>{{ disp }}</strong> libres</div>
            <div class="small text-muted">({{ ocup }} ocupadas)</div>
          </td>
        {% endfor %}
      </tr>
    {% endfor %}
  </tbody>
</table>
</div>
{% endblock %}
