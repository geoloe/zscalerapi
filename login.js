function insertAfter(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}

var password = document.getElementById("verify_pass");
var first = document.getElementById("first");
var div = document.getElementById('feedback_div');
var text = document.createElement("p");
var registerButton = document.getElementById("register_btn");
    //Password Verification
if(password != null){
    password.addEventListener('input', function(){

        console.log(password.value);

        insertAfter(text, div);
        if(password.value != first.value){
            registerButton.disabled = true;

            //Input Feedback
            password.setAttribute("class", "input is-danger");
            first.setAttribute("class", "input is-danger");
            text.setAttribute("class", "help is-danger");
            text.innerHTML = "Sorry, Passwörter stimmen nicht überein :(";
        }
        else {
            registerButton.disabled = false;

            password.setAttribute("class", "input is-success");
            first.setAttribute("class", "input is-success");
            text.setAttribute("class", "help is-success");
            text.innerHTML = "Passwörter stimmen überein :)";
        }
    } );
}


var bar = document.createElement('progress');
var span = document.getElementById('password-security');
var text = document.createElement('p');

if (first != null){
    first.addEventListener('input', function(){
        //password security
        registerButton.disabled = true;
        span.appendChild(text);
        span.appendChild(bar);
        console.log(first.value.length);
        if(first.value.length < 5 && first.value.length > 0){
            bar.setAttribute('class', 'progress is-danger' );
            bar.setAttribute('value', '25' );
            bar.setAttribute('max', '100' );
            bar.innerHTML = '25%';
            text.setAttribute("class", "help is-danger");
            text.innerHTML = "schwaches Passwort";
        }
        else if (first.value.length < 8 && first.value.length >= 4) {
            bar.setAttribute('class', 'progress is-warning' );
            bar.setAttribute('value', '50' );
            bar.setAttribute('max', '100' );
            bar.innerHTML = '50%';
            text.setAttribute("class", "help is-warning");
            text.innerHTML = "akzeptables Passwort";

        }
        else if (first.value.length < 10 && first.value.length >= 7) {
            bar.setAttribute('class', 'progress is-info' );
            bar.setAttribute('value', '75' );
            bar.setAttribute('max', '100' );
            bar.innerHTML = '75%';
            text.setAttribute("class", "help is-info");
            text.innerHTML = "Gutes Passwort";
        }
        else{
            bar.setAttribute('class', 'progress is-success' );
            bar.setAttribute('value', '100' );
            bar.setAttribute('max', '100' );
            bar.innerHTML = '100%';
            text.setAttribute("class", "help is-success");
            text.innerHTML = "Sehr gutes Passwort";

            registerButton.disabled = false;
        }
    } );
}

function pageloader(value) {
    document.getElementById(value).className += " is-active";
}