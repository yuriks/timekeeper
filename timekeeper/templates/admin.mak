<%!
	page_title = u"Admin"
%>
<%inherit file="base.mak"/>
<%block name="content">
	<ul>
		<li><a href="${req.route_url('admin.employees')}">Manage Employees</a></li>
		<li><a href="${req.route_url('admin.projects')}">Manage Projects</a></li>
		<li><a href="${req.route_url('admin.periods')}">Manage Billing Periods</a></li>
	</ul>
</%block>
<%block name="footer">
	<p>
		<a href="${req.route_url('logout')}">Logout</a> -
		<a href="${req.route_url('dashboard')}">Dashboard</a>
	</p>
</%block>
