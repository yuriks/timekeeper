<%!
	import timekeeper.template_helpers as helpers
%>
<%inherit file="base.mak"/>
<%block name="content">
	<p>Welcome ${user.name | h}. Current clocked in project:
		% if current_session is not None:
			${current_session.project.name | h}, since
			${helpers.format_localtime(req, current_session.start_time)}.
		% else:
			None.
		% endif
	</p>
	<form action="${request.route_url('clock_in')}" method="POST">
		<ul>
			% for project in projects:
			<li><input type="submit" name="projectname" value="${project.name | h}"></li>
			% endfor
			<li><input type="submit" value="Clock Out"></li>
			<li>Override time: <input type="text" name="time_override"></li>
		</ul>
	</form>
</%block>
