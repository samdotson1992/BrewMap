function openTab(evt, TabName) {
     var i, x, tablinks;
     x = document.getElementsByClassName("Tab");
     for (i = 0; i < x.length; i++) {
         x[i].style.display = "none";
     }
     tablinks = document.getElementsByClassName("tablink");
     for (i = 0; i < x.length; i++) {
         tablinks[i].className = tablinks[i].className.replace(" w3-red", "");
     }
     document.getElementById(TabName).style.display = "block";
     evt.currentTarget.className += " w3-red";
 }

 function users(typ) {
     console.log("users is running")    
     if (typ=='signIn') {
       var data = JSON.stringify({
         'username': document.getElementById('username_login').value,
         'email': document.getElementById('email_login').value,
         'passwrd': document.getElementById('password_login').value
       })
       console.log(data)
    }
    else if(typ='signUp'){
         var obj = {
         'username': document.getElementById('username_signup').value,
         'email': document.getElementById('email_signup').value,
         'passwrd': document.getElementById('password_signup').value,
         're_password_signup': document.getElementById('re_password_signup').value
     }
    if (obj.re_password_signup!==obj.passwrd){
        window.alert("Passwords don't match")
    }
    else {data= JSON.stringify({"username":obj.username,"email":obj.email,"passwrd":obj.passwrd});}
 
    }
    else {
        window.alert("He's dead Jim")
}

     $.ajax({
         type: "POST",
         url: "users/"+typ,
         data: data,
         contentType: 'application/json',
         dataType: 'json',
         error: function (request, status, error) {
             console.log(request.responseText);
         },
         success: function () {
             console.log("success");
         }
     });
 }
