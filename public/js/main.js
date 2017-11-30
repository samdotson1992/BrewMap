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

function get_user(typ) {
    $.ajax({
        url: "users/" + typ,
        type: 'GET',
        dataType: 'json',
        success(response) {
            console.log(response);
            var data = JSON.parse(response);
            console.log(data);
        },
        error(jqXHR, status, errorThrown) {
            console.log(status);
            console.log("No response from get_user");
            console.log(errorThrown);
        }
    });
}

function users(typ) {
    console.log("users is running")
    if (typ == 'signIn') {
        var data = JSON.stringify({
            'username': document.getElementById('username_login').value,
            'email': document.getElementById('email_login').value,
            'passwrd': document.getElementById('password_login').value
        })
    } else if (typ = 'signUp') {
        var username = document.getElementById('username_signup').value
        var email = document.getElementById('email_signup').value
        var passwrd = document.getElementById('password_signup').value
        var re_password_signup = document.getElementById('re_password_signup').value
    
    if (re_password_signup !== passwrd) {
        window.alert("Passwords don't match")
    } else {
        data = JSON.stringify({
            "username": username,
            "email": email,
            "passwrd": passwrd
        });
    }
    }
 else {
    window.alert("He's dead Jim")
}

console.log(data)

$.ajax({
    type: "POST",
    url: "users/" + typ,
    data: data,
    contentType: 'application/json',
    dataType: 'json',
    error: function (request, status, error) {
        console.log(request.responseText);
    },
    success: function () {
        console.log("success");
        get_user(typ)
    }
});
}