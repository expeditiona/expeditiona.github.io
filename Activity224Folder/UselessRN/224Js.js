<html>

<head>

<style>


</style>


<script>
	function validateForm()
	{
		var x=document.forms["login"]["username"].value;
		if (x==null || x=="")
  	{
  		alert("Please fill out the username");
  		return false;
  	}
}

</script>
</head>

<body>
<section class="loginform cf">
<form name="login" action="index_submit" method="get" accept-charset="utf-8">
    <ul>
        <li><label for="usermail">Email</label>
        <input type="email" name="usermail" placeholder="yourname@email.com" required></li>
        <li><label for="password">Password</label>
        <input type="password" name="password" placeholder="password" required></li>
        <li>
        <input type="submit" value="Login"></li>
    </ul>
</form>
</section>
</body>

</html>

