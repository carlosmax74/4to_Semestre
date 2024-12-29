var votes1 = {
    Maze: 0,
    Linea: 0,
    Simulation: 0,
    Major: 0
};

function updateProgressBar1() {
    var selectedOption = document.querySelector('input[name="option1"]:checked');

    if (selectedOption) {
        var optionValue = selectedOption.value;
        var progressBar = document.getElementById("myBar1");
        let percent = votes1[optionValue];
        progressBar.style.width = percent + '%';
        progressBar.textContent = percent + '%';
        progressBar.style.display = "block";
    }
}

function submitVote1() {
    var selectedOption = document.querySelector('input[name="option1"]:checked');

    if (selectedOption) {
        var optionValue = selectedOption.value;
        if (votes1[optionValue] === 0) {
            votes1[optionValue]++;
            document.getElementById("result1").innerHTML = "¡Has votado por " + optionValue + "!";
            updateProgressBar1();
            var radioButtons = document.getElementsByName('option1');
            for (var i = 0; i < radioButtons.length; i++) {
                radioButtons[i].disabled = true;
            }
        } else {
            alert("Ya has votado por esta opción.");
        }
    } else {
        alert("Por favor selecciona una opción antes de votar.");
    }
}

var votes2 = {
    Mayrin: 0,
    Martin: 0,
    Mayrinx2: 0,
    Karol: 0
};

function updateProgressBar2() {
    var selectedOption = document.querySelector('input[name="option2"]:checked');

    if (selectedOption) {
        var optionValue = selectedOption.value;
        var progressBar = document.getElementById("myBar2");
        let percent = votes2[optionValue];
        progressBar.style.width = percent + '%';
        progressBar.textContent = percent + '%';
        progressBar.style.display = "block";
    }
}

function submitVote2() {
    var selectedOption = document.querySelector('input[name="option2"]:checked');

    if (selectedOption) {
        var optionValue = selectedOption.value;
        if (votes2[optionValue] === 0) {
            votes2[optionValue]++;
            document.getElementById("result2").innerHTML = "¡Has votado por " + optionValue + "!";
            updateProgressBar2();
            var radioButtons = document.getElementsByName('option2');
            for (var i = 0; i < radioButtons.length; i++) {
                radioButtons[i].disabled = true;
            }
        } else {
            alert("Ya has votado por esta opción.");
        }
    } else {
        alert("Por favor selecciona una opción antes de votar.");
    }
}