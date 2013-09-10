<!DOCTYPE html>
<html>
	<head>
		<title>TimeKeeper</title>
	</head>
	<body>
		<h1>TimeKeeper</h1>
		<span>${message}</span>
		<p>Welcome ${user.name}. Current clocked in project:
			% if current_session is not None:
				${current_session.project.name}, since
				${h.format_localtime(req, current_session.start_time)}.
			% else:
				None.
			% endif
			</p>
		<form action="${request.route_url('clock_in')}" method="POST">
			<ul>
				% for project in projects:
				<li><input type="submit" name="projectname" value="${project.name}"></li>
				% endfor
				<li><input type="submit" value="Clock Out"></li>
				<li>Override time: <input type="text" name="time_override"></li>
			</ul>
		</form>
		<p>
			<a href="${request.route_url('logout')}">Logout</a>
			% if user.admin:
				- <a href="${request.route_url('admin')}">Admin</a>
			% endif
		</p>
	</body>
</html>
