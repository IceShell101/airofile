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
        a.style.display = "inline";
    }else{
        a.style.display = "none";
    }
}

function media_view(path , type){
    var a = document.getElementById("media_monitor");
    var exitbutton = `<p id="media_view_closebutton" onclick="media_view('0','0')">X</p>`;
    if (a.style.display === "none"){
       a.style.display = "block";
       if (type === "img"){
       a.innerHTML = exitbutton+ "<img " + ' src="'+path+'">';
       }
       else{
         a.innerHTML =exitbutton + "<video "+' src="'+path+'" controls autoplay muted></video>';
       }
    }
    else{
      var animate ;
      function animation(){
      a.style.filter= "opacity(0." - 1  + ")";
     animate = setTimeout(animation,200);
     }
     animation();
      a.style.display = "none";
      a.style.filter= "opacity(1)";
      a.innerHTML = "";
    }
}


function delete_file(name , current_path , file_path){
  var delete_form = document.getElementById("delete_submit");
  var delete_form_html=`<p>Are You Sure You Want To Delete? <br>${name}</p>
           <form action="/" method="POST">
           <button class="delete_choise">
                <p>Yes</p>
                <input type="hidden" value="${file_path}" name="path">
                <input type="hidden" value="${current_path}" name="file_path">
                <input type="hidden" value="delete_request" name="request">
            </button>
            <button onclick="delete_file(0,0,0)" class="delete_choise"><p>No</p></button>
       </form>`;
  if (delete_form.style.display === "none"){
      delete_form.style.display = "block";
      delete_form.innerHTML = delete_form_html;
  }else{
      delete_form.style.display = "none";
      delete_form.innerHTML = "";
  }
 
}
