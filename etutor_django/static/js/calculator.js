let calcDisplay = document.getElementById('calc-display')
let resultDisplay = document.getElementById('result-display')
let specialSymbolUsed = false

function display(num) {
    if(specialSymbolUsed) {
        specialSymbolUsed = false
        calcDisplay.innerText = ''
    }
    calcDisplay.innerText += num;
}

function display_special(symbol) {
    specialSymbolUsed = true
    let value = eval(calcDisplay.innerText)
    calcDisplay.innerText = value
    calcDisplay.innerText = `${symbol}(${value})`

    if(symbol != 'sqrt') {
        value *= Math.PI/180
    }

    resultDisplay.innerText = String(eval(`with(Math) Math.${symbol}(value)`)).substring(0, 12)
}

function allClear() {
    calcDisplay.innerHTML = "";
    resultDisplay.innerHTML = "0";
}

function del() {
    calcDisplay.innerText = calcDisplay.innerText.slice(0,-1);
}

function calculate() {
    resultDisplay.innerText = String(eval(calcDisplay.innerText)).substring(0, 12);
}