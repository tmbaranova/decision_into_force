

async function create_cur_for_rub (){
    // получаем значение введенных рублей
    let decision_date = document.getElementById("decision_date").value;

        // теперь передает значение в Python для обработки
    let value_cur = await eel.convert_date_py(decision_date)();
        // выводим на экран полученное значение

    document.getElementById("result").innerHTML = value_cur;

}


document.getElementById("btn-sum").onclick = create_cur_for_rub;