<%!
	import timekeeper.template_helpers as helpers
%>
<%def name="form_value(key, blank=None)">
	% if employee is None:
		% if blank is None:
			value=""
		% else:
			value="${blank}" disabled="disabled"
		% endif
	% else:
		value="${getattr(employee, key)}
	% endif
</%def>
<%inherit file="admin_employees.mak"/>
<%block name="content">
	<form action="${req.route_url('admin.employees.edit', employee_id=employee.id)}" method="POST">
		<label>Id: <input type="text" name="e_id" ${form_value('id', 'new')}></label>
		<label>Login: <input type="text" name="e_login" ${form_value('login', 'new')}></label>
		<br>
		<label>Name: <input type="text" name="e_name" value="${employee.name}"></label>
	</form>
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
