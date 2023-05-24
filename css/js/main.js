
document.getElementById('login-btn').addEventListener('click', function() {
    alert('Login realizado com sucesso!');
        });

function checkInp()
{
    var x=document.forms["myForm"]["age"].value;
    var regex=/^[0-9]+$/;
    if (x.match(regex))
    {
        alert("Must input numbers");
        return false;
    }
}

function mostrarInput() {
    
    var Mbway= document.querySelector("#MBWay");
    var numtel= document.querySelector("#numtel");

    if (Mbway.checked==true) {
        numtel.style.display = "block";
        numtel.style.animation = "Mbway 1s ease-in-out infinite";
        numtel.style.background = "#f2f2f2";
        numtel.style.border = "1px solid #ccc";
    } else {
        numtel.style.display = "none";
    }
}
   
    