
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
