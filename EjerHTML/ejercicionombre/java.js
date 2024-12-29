document.getElementById("enviar").addEventListener("click", function () {
    var contenido = document.getElementById("contenedor1");
    contenido.style.display = "block";
});

document.getElementById("si").addEventListener("click", function () {
    var contenido = document.getElementById("contenedor2");
    contenido.style.display = "block";
});

document.getElementById("no").addEventListener("click", function () {
    var contenido = document.getElementById("contenedor3");
    contenido.style.display = "block";
});

document.getElementById("enviar1").addEventListener("click", function () {

    // Obtener el valor ingresado en el input
    var nombre = document.getElementById("n").value;
    var nombre1 = document.getElementById("nom").value;

    var contenido = document.getElementById("contenedor4");
    contenido.style.display = "block";

    // Mostrar el nombre ingresado en el mensaje
    document.getElementById("mensajeImpreso").innerHTML = "¡¡¡Felicidades!!! <br>Antes eras:" + nombre + "<br> Ahora eres: " + nombre1;

});

