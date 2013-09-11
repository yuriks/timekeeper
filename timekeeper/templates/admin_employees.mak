<%!
	import timekeeper.template_helpers as helpers
	page_title = u"Admin - Employees"
%>
<%inherit file="admin.mak"/>
<%block name="content">
	<table>
		<thead><tr>
			<td>Id</td>
			<td>Login</td>
			<td>Name</td>
			<td>Hourly Rate</td>
			<td>Active</td>
			<td>Admin</td>
		</tr></thead>
		% for e in employees:
			<tr>
				<td>${e.id}</td>
				<td>${e.login | h}</td>
				<td>${e.name | h}</td>
				<td>${'{:0.2f}'.format(e.hourly_rate)}</td>
				<td>${helpers.yesno(e.active)}</td>
				<td>${helpers.yesno(e.admin)}</td>
				<td><a href="${req.route_url('admin.employees.edit', employee_id=e.id)}">Edit</a></td>
			</tr>
		% endfor
	</table>
</%block>
