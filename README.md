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
