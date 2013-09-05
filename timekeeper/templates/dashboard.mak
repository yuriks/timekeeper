<!DOCTYPE html>
<html>
	<head>
		<title>TimeKeeper</title>
	</head>
	<body>
		<h1>TimeKeeper</h1>
		<span>${message}</span>
		<p>Welcome ${user.name}. Current clocked in project: ${current_project_name}.</p>
		<ul>
			% for project in projects:
			<li><a href="${request.route_url('project_clockin', projectname=project.name)}">${project.name}</a></li>
			% endfor
			<li><a href="${''}">Clock Out</a></li>
		</ul>
		<p>
			<a href="${request.route_url('logout')}">Logout</a> -
			<a href="${request.route_url('admin')}">Admin</a>
		</p>
	</body>
</html>