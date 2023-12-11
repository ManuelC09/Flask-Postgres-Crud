from App import db

class Empleados(db.Model):
    __tablename__ = "Empleados"
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50))
    puesto = db.Column(db.String(50))
    nombre_foto = db.Column(db.String(50))
    url_foto = db.Column(db.String(150))
    sueldo = db.Column(db.Integer)
    
    def __init__(self, nombre, puesto, nombre_foto, url_foto, sueldo) -> None:
        self.nombre = nombre
        self.puesto = puesto
        self.nombre_foto = nombre_foto
        self.url_foto = url_foto
        self.sueldo = sueldo
        
    def __str__(self) -> str:
        return f"Empleado: {self.nombre} {self.puesto}"