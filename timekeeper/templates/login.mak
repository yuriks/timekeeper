<!DOCTYPE html>
<html>
	<head>
		<title>TimeKeeper - Login</title>
	</head>
	<body>
		<h1>Login</h1>
		<span>${message}</span>
		<form action="${url}" method="post">
			Login: <input type="text" name="login", value="${login}"><br>
			Password: <input type="password" name="password"><br>
			<input type="submit" value="Login">
		</form>
	</body>
</html>
