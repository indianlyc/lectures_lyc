/*
let fruits = {
    "u1": "Первый текст",
    "u2": "Второй текст",
    "u3": "Третий текст",
    "u4": "Четвертый текст <img class=\"dog\" src=\"https://fanibani.ru/wp-content/uploads/2022/12/1644866254_20-fikiwiki-com-p-shchenki-krasivie-kartinki-22.jpg\">"
    };
*/

function g(el){
    function f(){
            document.getElementById("base_text").innerHTML = el.getElementsByClassName("text")[0].innerHTML;
    };
    return f;
}


function main(){
    let y = document.getElementsByClassName('u');
    for(let i=0; i < y.length; i++){
        y[i].onclick = g(y[i]);
    };

}

document.addEventListener("DOMContentLoaded", main);


