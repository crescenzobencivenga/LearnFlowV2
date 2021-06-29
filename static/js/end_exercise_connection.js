
function response(){

    let pnt = getCookie('pnt');

    let pnt_done = getCookie('pnt_done')
    document.getElementById("put_score_done_1").innerHTML = pnt_done.toString();
    document.getElementById("put_score_done_2").innerHTML = pnt_done.toString();


    // prendere questi elementi dal json
    let pnt_min = null
    let pnt_max = null

    document.getElementById("put_min_score").innerHTML = pnt_min.toString();
    document.getElementById("put_max_score").innerHTML = pnt_max.toString();


    if(pnt_done<pnt_min){
        document.getElementById("pass_no").style.visibility = "block";
        document.getElementById("pass_yes").style.visibility = "none";

    }else{
        document.getElementById("pass_yes").style.visibility = "block";
        document.getElementById("pass_no").style.visibility = "none";
    }

}