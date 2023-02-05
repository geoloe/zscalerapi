// Toggler for SLCC File Download
function toggleText() {
    var text = document.getElementById("mes");
    if (text.style.display === "none") {
    text.style.display = "block";
    } else {
    text.style.display = "block";
    }
}

// Toggler for Loading Spinner
function toggleLoad() {
    var text = document.getElementById("load");
    if (text.style.display === "none") {
    text.style.display = "block";
    } else {
    text.style.display = "block";
    }
}

function modalOn(value){
    document.getElementById(value).className += " is-active";
}
function modalOff(value){
    document.getElementById(value).className =
    document.getElementById(value).className.replace
    ( /(?:^|\s)modal is-active(?!\S)/g , 'modal' )
}
 

function activate4(id, kundenname, api, cloud, domain, users, test2){
    var id = id;
    var test = document.getElementById("edit-id");
    test.value = id;

    var kundenname = kundenname;
    var cu = document.getElementById("placeholder-kundenname");
    cu.value = kundenname;

    var api = api;
    var key = document.getElementById("placeholder-apikey");
    key.value = api;

    var domain = domain;
    var dm = document.getElementById("placeholder-domain");
    dm.value = domain;

    var cloud = cloud;
    var cd = document.getElementById("option6");
    cd.value = cloud;

    //Length fixer
    for(var i=0; i<test2.length; i++){
        for(var j=0; j<users.length; j++){
            if(test2[i] == users[j]){
                createCheckboxes(i+1+'_'+test2[i], test2[i], 'checkbox-field2');
            }
        }
    }
    document.getElementById("question4").className += " is-active";
}



function activate5(id, email){
    var id = id;
    var test = document.getElementById("ad-id");
    test.value = id;

    var email = email;
    var e = document.getElementById("email-loeschen");
    e.innerHTML = "Den Admin mit der LoginID: '" + email + "' löschen?";

    document.getElementById("question5").className += " is-active";
}

 // cookie policy
 //Fix Function

$(document).on('ready', function() {
    alert('I hate tomatoes.');
if (document.cookie.indexOf("accepted_cookies=") < 0) {
    $('.cookie-overlay').removeClass('d-none').addClass('d-block');
}

$('#allow-cookie').on('click', function() {
    document.cookie = "accepted_cookies=yes;"
    alert('I hate tomatoes.');
    $('.cookie-overlay').removeClass('d-block').addClass('d-none');
})

$('.close-cookies').on('click', function() {
    $('.cookie-overlay').removeClass('d-block').addClass('d-none');
    })
})


$(document).ready(function() {
    var table = $('#data2').DataTable( {
      lengthChange: false,
      responsive: true,
      buttons: [ 'copy', 'pdf', 'colvis',
      {
        text: 'Admin hinzufügen',
        action: function ( e, dt, node, config ) {
            modalOn('add-admin');
            }
        }
    ]
} );

table.buttons().container()
    .appendTo( $('div.column.is-half', table.table().container()).eq(0) );
} );

$(document).ready(function() {
    var table = $('#data').DataTable( {  
        lengthChange: false,
        responsive: true,
        buttons: [ 'copy', 'pdf', 'colvis',
            {
                text: 'Kunden hinzufügen',
                action: function ( e, dt, node, config ) {
                    modalOn('add-customer');
                }
            },
    ],
    } );

// Insert at the top left of the table
table.buttons().container()
  .appendTo( $('div.column.is-half', table.table().container()).eq(0) );
} );



function apiTab(evt, apiTab) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" is-active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(apiTab).style.display = "block";
    document.getElementById(apiTab).style.visibility = "visible";
    evt.currentTarget.className += " is-active";
} 

function pageloader(value) {
    document.getElementById(value).className += " is-active";
}

function quickview(value) {
    var quickview = document.getElementById(value);
    if(quickview.className == "quickview"){
        quickview.className += " is-active";
    }
    else{
        quickview.className = "quickview";
    }
}

function accordion(value) {
    var accordion= document.getElementById(value);
    if(accordion.className == "accordion"){
        accordion.className += " is-active";
    }
    else{
        accordion.className = "accordion";
    }
}

function message(value){
    var message = document.getElementById(value);
    message.style.display = "none";
}

//Global array for currrently assigned customers
let nodes = [];
let all_customers = [];

function userHandler(value, target, customers){
    //console.log(value);

    // target is username
    document.getElementById(target).setAttribute("value", value);
    document.getElementById(target).innerHTML = value;

    var hiddenUserID = document.createElement("input");
    hiddenUserID.setAttribute("name", value);
    hiddenUserID.setAttribute("type", "hidden");
    insertAfter(hiddenUserID, document.getElementById(target));

    //console.log(document.querySelectorAll('.meinekunden'));
    var all = document.querySelectorAll('.meinekunden');

    console.log(all)
    for(var i = 0; i<all.length; i++) {
        if(String(all[i].id).includes(value)){
        //console.log(all[i].innerHTML); 
        nodes.push(all[i].innerHTML);         
        }
    }

    //send all customer values and check already assigned ones
    all_customers = customers;

    for(var i = 0; i<all_customers.length; i++) {
        const li = document.createElement("li");
        const div = document.createElement("div");

        div.setAttribute("class", "field");
        div.setAttribute("onClick", "assignHandler('"+all_customers[i]+"')");
        li.appendChild(div);
        const input = document.createElement("input");
        input.setAttribute("class", "is-checkradio is-small is-primary");
        input.setAttribute("type", "radio");
        input.setAttribute("id", all_customers[i]);
        input.setAttribute("name", i+1+"_"+all_customers[i]);
            for(var p = 0; p<nodes.length; p++) {        
                if(nodes[p] == all_customers[i]){
                    input.setAttribute("checked", true);
                }
            }
        div.appendChild(input);
        const label = document.createElement("label");
        label.innerHTML = all_customers[i];
        div.appendChild(label);
        document.getElementById("used").appendChild(li);
    }
}

function insertAfter(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}

function createInput(value){
    const input = document.createElement("input");
    console.log(input)
    input.setAttribute("value", value);
    input.setAttribute("type", "hidden");
    input.setAttribute("class", "text");
    input.setAttribute("name", value);
    document.getElementById(value).appendChild(input);
    console.log("create!");
}
function deleteInput(e){
    //Delete child elements from element        
    //e.firstElementChild can be used.
    var child = e.lastElementChild; 
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
    console.log("delete!");
}

function assignHandler(value){
    var checkbox = document.getElementById(value);

    if(checkbox.checked){
        checkbox.checked = false;
    }
    else{
        checkbox.checked = true;
    }
}

function checkboxHandler(value, name, ulValue){
    var checkbox = document.getElementById(value);
    var option = document.createElement("input");
    var label = document.createElement("label");
    label.innerHTML = name;
    var li = document.createElement("li");
    li.setAttribute("id", name + value);
    var ul = document.getElementById(ulValue);
    option.setAttribute("class", "is-checkradio is-small is-primary");
    option.setAttribute("type", "radio");
    option.setAttribute("id", value);
    option.checked = true;
    option.disabled = true;

    //console.log(checkbox.id);
    if(checkbox == undefined){
        ul.appendChild(li);
        li.appendChild(option);
        insertAfter(label, option);
        createInput(value);
    }
    else{ 
        var e = document.getElementById(name + value);
        e.remove();
    }
}

function undoList(value){
    //Delete child elements from element
    var e = document.querySelector(value);
        
    //e.firstElementChild can be used.
    var child = e.lastElementChild; 
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
    nodes = [];
}


//Tags control

document.addEventListener('DOMContentLoaded', function () {
    var tagsinput = bulmaTagsinput.attach('[type="tags"]');
    console.log(tagsinput);
})

function setColor(value){
    var optionItem = document.getElementById(value); 
    //console.log(optionItem);   
    optionItem.setAttribute("selected", true);
    if(optionItem.selected == true){
        console.log(optionItem.id);
        optionItem.selected = false;
    }
    else if(optionItem.selected == false){
        optionItem.setAttribute("style", "");
    }
}

$(function () {
    $("#option1").select2();
    $("#option2").select2();
    $("#option3").select2();
    $("#option4").select2();
    $("#option7").select2();
});



function find(search, array) {
    return function check(search, value, ...rest) {
        return search === value || rest.length && check(search, ... rest) || false;
    }(search, ...array);
}

///// Search Logic /////
///// Get Domains from data.html and programmatically check on text typing if input includes domains array
var element = document.getElementById('searchable');
var domains = document.getElementsByClassName('get-domain');
var domainIDs = document.getElementsByClassName('get-id');
var domainNames = document.getElementsByClassName('get-name');
var e = document.getElementById('admin-submit');
var div = document.getElementById('my-feedback');
var text = document.createElement("p");
var option = document.createElement("option");
var selector = document.getElementById("option5");

if(element != null){
    //Customer Search
    element.addEventListener('input', function() {
        console.log('The value is now ' + element.value);
        insertAfter(text, div);
        for (var i = 0; i<domains.length; i++){
            //var reg = "^/[a-zA-Z.]"
            console.log(domains[i]);
            //Regex
            var regex = new RegExp('[a-z.]@\\b' + domains[i].innerHTML + '\\b', 'g');
            if(!element.value.match(regex)){     
                e.disabled = true;
                //Button Feedback
                e.setAttribute("class", "button is-outlined has-tooltip-bottom");
                e.setAttribute("data-tooltip", "Sorry, die Domain ist nicht registriert :(");
                //Input Feedback
                element.setAttribute("class", "input is-danger");
                text.setAttribute("class", "help is-danger");
                text.innerHTML = "Sorry, die Domain ist nicht registriert :(";
            }
            else{
                console.log("its a match!");
                //Button Feedback
                e.setAttribute("class", "button is-outlined has-tooltip-bottom");
                e.setAttribute("data-tooltip", "Domain '" + domains[i].innerHTML + "' existiert!");
                //Input Feedback
                element.setAttribute("class", "input is-success");
                text.setAttribute("class", "help is-success");
                text.innerHTML = "Domain '" + domains[i].innerHTML + "' existiert!";
                e.disabled = false;
                //Option Feeback
                console.log(domainIDs[i].className);
                option.setAttribute("value", domainIDs[i].value);
                option.innerHTML = domainNames[i].innerHTML;
                option.selected = true;
                deleteInput(selector);
                selector.appendChild(option);
                break;
            }                 
        }
    });
}

function isNum(val){
    return !isNaN(val)
  }


function reload(val) {
    console.log("clicking");   
    alert("Edit options loaded... Please close and click again the edit button");
    return true;
}


function createCheckboxes(value, name, ulValue){
    var option = document.createElement("input");
    var label = document.createElement("label");
    label.innerHTML = name;
    var li = document.createElement("li");
    li.setAttribute("id", name + value);
    var ul = document.getElementById(ulValue);
    option.setAttribute("class", "is-checkradio is-small is-primary");
    option.setAttribute("type", "radio");
    option.setAttribute("id", value);
    option.checked = true;
    option.disabled = true;

    ul.appendChild(li);
    li.appendChild(option);
    insertAfter(label, option);
    createInput(value);
}


$('#file').change(function(e){
    var filename = e.target.files[0].name;
    displayfilename(filename);
  });
  function displayfilename(filename) {
    var name = document.getElementById('filename-selector');
    name.innerHTML = filename;
  }

function steps(marker, segment){
    var m = document.getElementById(marker);
    var s = document.getElementById(segment);
    var last = document.getElementById('last-one');
    if(s.className == "steps-segment has-gaps"){
        s.className += " is-active";
        last.className = "steps-segment";
    }
    else{
        s.className = "steps-segment has-gaps";
    }
    if(m.className == "steps-marker is-white"){
        m.className = "steps-marker is-primary";
    }
    else{
        m.className = "steps-marker is-white";
    }

}


//Search bar
function searchfunc() {
    // Declare variables
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('searchbar');
    filter = input.value.toUpperCase();
    ul = document.getElementById("menu-nav");
    li = ul.getElementsByTagName('li');
  
    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
      a = li[i].getElementsByTagName("a")[0];
      txtValue = a.textContent || a.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        li[i].style.display = "";
      } else {
        li[i].style.display = "none";
      }
    }
  }

  function httpTab(evt, httpTab) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByName("httptab");
    for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByName("httplinks");
    for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace("is-active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(httpTab).style.display = "block";
    document.getElementById(httpTab).style.visibility = "visible";
    evt.currentTarget.className += " is-active";
}