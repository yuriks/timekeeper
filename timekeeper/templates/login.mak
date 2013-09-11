<%!
	page_title = u"Login"
%>
<%inherit file="base.mak"/>
<%block name="content">
	<form action="${url}" method="post">
		Login: <input type="text" name="login", value="${login | h}"><br>
		Password: <input type="password" name="password"><br>
		<input type="submit" value="Login">
	</form>
</%block>
<%block name="footer"></%block>
