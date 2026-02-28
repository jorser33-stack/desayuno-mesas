# -*- coding: utf-8 -*-
import os
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambia_esta_clave')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///desayuno.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SLOTS = ['07:00', '08:00', '09:00', '10:00']
TOTAL_MESAS = int(os.environ.get('TOTAL_MESAS', '30'))
NOMBRE = os.environ.get('BUSINESS_NAME', 'Smart Hotel – Desayuno')

db = SQLAlchemy(app)

class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, index=True)
    turno = db.Column(db.String(5), nullable=False)
    mesas = db.Column(db.Integer, nullable=False, default=1)
    nombre = db.Column(db.String(120), nullable=True)
    habitacion = db.Column(db.String(20), nullable=True)
    nota = db.Column(db.String(255), nullable=True)

    __table_args__ = (
        db.Index('idx_fecha_turno', 'fecha', 'turno'),
    )


def parse_date_ddmmyyyy(s: str) -> date:
    return datetime.strptime(s, '%d-%m-%Y').date()


def daterange(start: date, end: date):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


def mesas_ocupadas(fecha: date, turno: str) -> int:
    total = db.session.query(db.func.coalesce(db.func.sum(Reserva.mesas), 0)).filter(
        Reserva.fecha == fecha,
        Reserva.turno == turno
    ).scalar() or 0
    return int(total)


def mesas_disponibles(fecha: date, turno: str) -> int:
    return max(0, TOTAL_MESAS - mesas_ocupadas(fecha, turno))

@app.route('/')
def home():
    hoy = date.today()
    dias = [hoy + timedelta(days=i) for i in range(7)]
    tabla = []
    for d in dias:
        fila = {'fecha': d, 'turnos': []}
        for t in SLOTS:
            fila['turnos'].append({
                'turno': t,
                'ocupadas': mesas_ocupadas(d, t),
                'disponibles': mesas_disponibles(d, t)
            })
        tabla.append(fila)
    return render_template('home.html', tabla=tabla, slots=SLOTS, nombre=NOMBRE, total=TOTAL_MESAS)

@app.route('/reservar', methods=['GET', 'POST'])
def reservar():
    if request.method == 'POST':
        try:
            fecha_desde = parse_date_ddmmyyyy(request.form.get('fecha_desde'))
            fecha_hasta = parse_date_ddmmyyyy(request.form.get('fecha_hasta'))
            turno = request.form.get('turno')
            mesas = int(request.form.get('mesas', 1))
            nombre = (request.form.get('nombre') or '').strip()
            habitacion = (request.form.get('habitacion') or '').strip()
            nota = (request.form.get('nota') or '').strip()
        except Exception:
            flash('Datos inválidos. Revisá el formulario (fechas DD-MM-AAAA).', 'danger')
            return redirect(url_for('reservar'))

        if turno not in SLOTS:
            flash('Turno inválido.', 'warning')
            return redirect(url_for('reservar'))
        if mesas < 1:
            flash('La cantidad de mesas debe ser al menos 1.', 'warning')
            return redirect(url_for('reservar'))
        if fecha_hasta < fecha_desde:
            flash('La fecha hasta debe ser >= fecha desde.', 'warning')
            return redirect(url_for('reservar'))

        faltantes = []
        for d in daterange(fecha_desde, fecha_hasta):
            if mesas_disponibles(d, turno) < mesas:
                faltantes.append({'fecha': d, 'disp': mesas_disponibles(d, turno)})
        if faltantes:
            msg = 'Sin cupo suficiente en: ' + ', '.join([f"{f['fecha'].strftime('%d-%m-%Y')} (disp {f['disp']})" for f in faltantes])
            flash(msg, 'danger')
            return redirect(url_for('reservar'))

        for d in daterange(fecha_desde, fecha_hasta):
            r = Reserva(fecha=d, turno=turno, mesas=mesas, nombre=nombre, habitacion=habitacion, nota=nota)
            db.session.add(r)
        db.session.commit()
        flash('Reserva creada correctamente para el rango indicado.', 'success')
        return redirect(url_for('home'))

    hoy = date.today()
    manana = hoy + timedelta(days=1)
    return render_template('reservar.html', hoy=hoy, manana=manana, slots=SLOTS, nombre=NOMBRE)

@app.route('/detalle/<string:fecha_str>')
def detalle_dia(fecha_str):
    try:
        d = parse_date_ddmmyyyy(fecha_str)
    except Exception:
        return redirect(url_for('home'))
    por_turno = {}
    for t in SLOTS:
        por_turno[t] = Reserva.query.filter_by(fecha=d, turno=t).order_by(Reserva.id.desc()).all()
    return render_template('detalle.html', fecha=d, por_turno=por_turno, slots=SLOTS, nombre=NOMBRE, total=TOTAL_MESAS)

@app.route('/cancelar/<int:reserva_id>', methods=['POST'])
def cancelar(reserva_id):
    r = Reserva.query.get_or_404(reserva_id)
    d = r.fecha
    db.session.delete(r)
    db.session.commit()
    flash('Reserva cancelada.', 'info')
    return redirect(url_for('detalle_dia', fecha_str=d.strftime('%d-%m-%Y')))

@app.before_first_request
def init_db():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=True)
