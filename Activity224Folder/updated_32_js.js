//Checks if the input is numerical (valid)
function NumCheck() 
{

//value in the input box
var my_string=document.getElementById("tbox").value;

if(isNaN(my_string))
{
	//not a number
    alert("You did not enter a number.");
}

else if (document.getElementById('tbox').value === "")
{
	//nothing inputted
    alert("You did not enter anything.");
}

else
{
	//Valid grade (number) inputted
    alert("Grade entered.");
}

}