
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


function signUp(){

    
var obj = {'username_signup': document.getElementById('username_signup').value, 'email_signup': document.getElementById('email_signup').value, 'password_signup': document.getElementById('password_signup').value, 're_password_signup': document.getElementById('re_password_signup').value}  

if (obj["3"]!=obj["2"]){
    alert("Passwords don't match!")
}
    else {
var data=JSON.stringify(obj)
console.log(data)}
    

$.ajax({
    type: "POST",
    url: "sign_up",
    data: data,
    contentType: 'application/json',
    dataType: 'json',
       error: function (request, status, error) {
        console.log(request.responseText);
    },
    success: function() {
        console.log("success");
    }
});

}

function signIn(){
    
var data =JSON.stringify({"username_login":(document.getElementById('username_login').value),"email_login":(document.getElementById('email_login').value),"password_login": document.getElementById('password_login').value}) 

console.log(data)
    
$.ajax({
    type: "POST",
    url: "sign_in",
    data: data,
    contentType: 'application/json',
    dataType: 'json',
    error: function() {
        console.log("error");
    },
    success: function() {
        console.log("success");
    }
});

}


/*
function processFormData(){
                  // code for IE7+, Firefox, Chrome, Opera, Safari
                  if(window.XMLHttpRequest)
                      xmlhttp=new XMLHttpRequest();
                  else// code for IE5
                      xmlhttp=new ActiveXObject('Microsoft.XMLHTTP');

                  xmlhttp.open("POST","/observe", true);
                  var json_list = JSON.stringify([(document.getElementById('username_login').value),(document.getElementById('email_login').value),document.getElementById('password_login').value]);
                  xmlhttp.setRequestHeader('Content-Type', 'application/json');
                  xmlhttp.send(json_list);
                  }
                  
        */          
              

/*
function processFormData() {
    var list = [(document.getElementById('username_login').value), (document.getElementById('email_login').value), document.getElementById('password_login').value]
    json_list = JSON.stringify(list)
    console.log(json_list)
    console.log("bananas!")

*/

/*

var xhr = new XMLHttpRequest();
var url = '/join';

var data= JSON.stringify({id: '200'});
xhr.responseType='json'
xhr.onreadystatechange=function(){
  if (xhr.readyState===XMLHttpRequest.DONE) { console.log(xhr.response)};
  
};

xhr.open('POST',url)
xhr.send(json_list)
};

*/