
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

    var cartao= document.querySelector("#card");
    var nomecartao= document.querySelector("#nomecartao");
    var numcartao= document.querySelector("#numcartao");
    var validade= document.querySelector("#datacartao");
    var cvv= document.querySelector("#cartaocvv");
    if (Mbway.checked) {
        numtel.style.animation = "cair 0.3s ease-in-out ";
        numtel.style.display = "block";
        
        nomecartao.style.animation = "subir 0.3s ease-in-out ";
        nomecartao.style.display = "none";
        
        numcartao.style.animation = "subir 0.3s ease-in-out ";
        numcartao.style.display = "none";
        
        validade.style.animation = "subir 0.3s ease-in-out ";
        validade.style.display = "none";
        
        cvv.style.animation = "subir 0.3s ease-in-out ";
        cvv.style.display = "none";
        
    } else if (cartao.checked) {
        numtel.style.display = "none";
        numtel.style.animation = "subir 0.3s ease-in-out ";

        nomecartao.style.display = "block";
        nomecartao.style.animation = "cair 0.3s ease-in-out ";


        numcartao.style.display = "block";
        numcartao.style.animation = "cair 0.3s ease-in-out ";

        validade.style.display = "block";
        validade.style.animation = "cair 0.3s ease-in-out ";

        cvv.style.display = "block";
        cvv.style.animation = "cair 0.3s ease-in-out ";

    }else{
        numtel.style.animation = "subir 0.3s ease-in-out ";
        numtel.style.display = "none";
        

        nomecartao.style.display = "none";
        numcartao.style.display = "none";
        validade.style.display = "none";
        cvv.style.display = "none";
    }
}
   
    