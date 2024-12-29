let ubicacionPrincipal = document.documentElement.scrollHeight - window.pageYOffset;
let $nav = document.querySelector("nav");


window.addEventListener("scroll", function () {

    let desplazamientoActual = window.pageYOffset;

    if (ubicacionPrincipal >= desplazamientoActual) {

        $nav.style.top = "0px";
        console.log('Ubicacion Principal')
        console.log(ubicacionPrincipal)
        console.log('desplazamiento')
        console.log(desplazamientoActual)
    } else {

        $nav.style.top = "-80px";
        console.log('Ubicacion Principal')
        console.log(ubicacionPrincipal)
        console.log('desplazamiento')
        console.log(desplazamientoActual)
    }


    ubicacionPrincipal = desplazamientoActual;
});

