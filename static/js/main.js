function upload_form(){
    var myform = document.getElementById("upload_form_container")
    if (myform.style.display === "none"){
        myform.style.display = "block";
    }
    else{
        myform.style.display = "none";
    }

}


function options_menu(){
    var a = document.getElementById("controls_menu");
    if (a.style.display === "none"){
        a.style.display = "block";
    }else{
        a.style.display = "none";
    }
}
