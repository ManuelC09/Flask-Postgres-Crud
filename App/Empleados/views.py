from flask import render_template, Blueprint, request, redirect, url_for  
from App.Empleados.models import Empleados
from App import db
import os
import dropbox


empleados = Blueprint('empleados', __name__)

dbx = dropbox.Dropbox(os.environ.get('DROPBOX_TOKEN'))

@empleados.route('/index')
def index():
    empleados = Empleados.query.order_by(Empleados.id).all()
    return render_template('index.html', empleados=empleados)

@empleados.route('/registro', methods = ['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        puesto = request.form.get('puesto')
        foto = request.files['archivo']
        sueldo = request.form.get('sueldo')
        
        if not nombre:
            return render_template('empleados/registro.html', alert = 'Ingrese un nombre')
        
        if not puesto:
            return render_template('empleados/registro.html', alert = 'Ingrese un puesto')
        
        if not foto:
            foto = os.environ.get('DROPBOX_IMAGE_PREDETERMINADA')

        if not sueldo:
            return render_template('empleados/registro.html', alert='Ingrese un sueldo')

        if isinstance(foto, str):  
            url_foto = foto 
            nombre_foto = 'predeterminada.png'
        else:
            foto.seek(0)  
            dbx.files_upload(foto.read(), f"/{foto.filename}")
            nombre_foto = foto.filename
            
            shared_link = dbx.sharing_create_shared_link(f"/{foto.filename}")
            url_foto = shared_link.url.replace('&dl=0', '&raw=1')

        empleado = Empleados(nombre, puesto, nombre_foto, url_foto, sueldo)
        db.session.add(empleado)
        db.session.commit()
        db.session.close()
        
        return redirect(url_for('base.index'))
    
    else:
        return render_template('empleados/registro.html')
    
@empleados.route('/editar/<int:id>')
def editar(id):
    empleado = Empleados.query.get_or_404(id)
    return render_template('empleados/actualizar.html', empleado=empleado)

@empleados.route('/actualizar/<int:id>', methods = ['POST'])
def actualizar(id):
    empleado = Empleados.query.get_or_404(id)
    
    empleado.nombre = request.form.get('nombre')
    empleado.puesto = request.form.get('puesto')
    foto = request.files['archivo']
    empleado.sueldo = request.form.get('sueldo')
    
    if foto:
        foto.seek(0)  
        dbx.files_upload(foto.read(), f"/{foto.filename}")

        shared_link = dbx.sharing_create_shared_link(f"/{foto.filename}")
        url_foto = shared_link.url.replace('&dl=0', '&raw=1')
        empleado.urlFoto = url_foto
           
    
    db.session.add(empleado)
    db.session.commit()
    db.session.close()
        
    return redirect(url_for('base.index'))

@empleados.route('/eliminar/<int:id>')
def eliminar(id):
    empleado = Empleados.query.get_or_404(id)
    
    if empleado.nombre_foto != 'predeterminada.png':    
        dbx.files_delete_v2(f"/{empleado.nombre_foto}")
    
    db.session.delete(empleado)
    db.session.commit()
    db.session.close()
        
    return redirect(url_for('base.index'))     
