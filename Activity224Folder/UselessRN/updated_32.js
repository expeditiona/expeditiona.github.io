function NumCheck() 
{

var my_string=document.getElementById("tbox").value;

if(isNaN(my_string))
{
    alert("You did not enter a number.");
}

else if (document.getElementById('tbox').value === "")
{
     alert("You did not enter anything.");
}

else
{
    alert("Grade entered.");
}

}