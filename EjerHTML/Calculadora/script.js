document.getElementById('num1').addEventListener('click', function () {
    agregar('1');
});

document.getElementById('num2').addEventListener('click', function () {
    agregar('2');
});

document.getElementById('num3').addEventListener('click', function () {
    agregar('3');
});

document.getElementById('num4').addEventListener('click', function () {
    agregar('4');
});

document.getElementById('num5').addEventListener('click', function () {
    agregar('5');
});

document.getElementById('num6').addEventListener('click', function () {
    agregar('6');
});

document.getElementById('num7').addEventListener('click', function () {
    agregar('7');
});

document.getElementById('num8').addEventListener('click', function () {
    agregar('8');
});

document.getElementById('num9').addEventListener('click', function () {
    agregar('9');
});

document.getElementById('num0').addEventListener('click', function () {
    agregar('0');
});

document.getElementById('divi').addEventListener('click', function () {
    agregar('/');
});

document.getElementById('multi').addEventListener('click', function () {
    agregar('*');
});

document.getElementById('rest').addEventListener('click', function () {
    agregar('-');
});

document.getElementById('suma').addEventListener('click', function () {
    agregar('+');
});

document.getElementById('punto').addEventListener('click', function () {
    agregar('.');
});

document.getElementById('limpiar').addEventListener('click', function () {
    document.getElementById('ps').value = '';
});

document.getElementById('resultado').addEventListener('click', function () {
    operaciones();
})

function agregar(numero) {
    var entrada = document.getElementById('ps');
    entrada.value += numero;
}

function operaciones() {
    var campoentrada = document.getElementById('ps');
    var expresion = campoentrada.value;
    var resultado;

    try {
        resultado = calcularExpresion(expresion);
        campoentrada.value = resultado;
    } catch (error) {
        campoentrada.value = 'Error';
    }
}

function calcularExpresion(expresion) {
    var numeros = expresion.split(/\+|\-|\*|\//);
    var operadores = expresion.replace(/[0-9]|\./g, "").split("");

    var resultado = parseFloat(numeros[0]);

    for (var i = 0; i < operadores.length; i++) {
        var num = parseFloat(numeros[i + 1]);
        var operador = operadores[i];

        if (operador === '+') {
            resultado += num;
        } else if (operador === '-') {
            resultado -= num;
        } else if (operador === '*') {
            resultado *= num;
        } else if (operador === '/') {
            if (num !== 0) {
                resultado /= num;
            } else {
                throw "Division por cero";
            }
        }
    }

    return resultado;
}