async function create_cur_for_rub (){
    let decision_date = document.getElementById("decision_date").value;
    let value_cur = await eel.convert_date_py(decision_date)();

    document.getElementById("result").innerHTML = value_cur;
}

document.getElementById("btn-sum").onclick = create_cur_for_rub;