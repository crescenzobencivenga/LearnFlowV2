let lvl = 0;

function get_level() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    lvl = urlParams.get('level')
    return lvl
}

function pick_json(){
    // il file json si chiamerà jt+x con x=1..N esempio, json teoria lvl1 = jt1
    let path_json_t = "./LVL"+lvl+"/jt"+lvl
    //-> fai le oprazioni adeguate per parserizzare il json
}



// per accedere alla teoria
function go_to_exercise(lvl){
    window.location.href = './Exercise.html?level=' + lvl;
}


function exit_user_2(){
    deleteAllCookies()
    window.location.href='../../../login.html'
}


// impostare le giuste variabili alla
function assign_page_2(){
    let user = getCookie('username');
    if (user==null){
        window.location.href='../../../login.html'
    }
    let pnt = getCookie('pnt');
    let lvl = getCookie('lvl');
    document.getElementById("put_username").innerHTML = user.toString();
    document.getElementById("put_pnt2").innerHTML = pnt.toString();
}