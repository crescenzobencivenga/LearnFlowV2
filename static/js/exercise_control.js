let lvl = 0;

function get_level() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    lvl = urlParams.get('level')
    return lvl
}

function pick_json(){
    // il file json si chiamerà je+x con x=1..N esempio, json esercizi lvl1 = je1
    let path_json_t = "./LVL"+lvl+"/je"+lvl
    //-> fai le oprazioni adeguate per parserizzare il json
}


// per accedere alla teoria
function go_back_theory(lvl){
    window.location.href = './Theory.html?level=' + lvl;
}

