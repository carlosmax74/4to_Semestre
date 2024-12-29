from werkzeug.security import generate_password_hash, check_password_hash

class Register():

    def __init__(self, id, nombrec, numcel, dire, contraseña, contraseña1, correo) -> None:
        self.id = id
        self.nombrec = nombrec
        self.numcel = numcel
        self.dire = dire
        self.contraseña = contraseña
        self.contraseña1 = contraseña1
        self.correo = correo

        if contraseña == contraseña1:
            self.contraseña_encriptada = generate_password_hash(contraseña1, 'sha256', 30)
