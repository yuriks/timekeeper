<%!
	page_title = None
%>
<%def name="title()">
	TimeKeeper
	% if self.attr.page_title:
		- ${self.attr.page_title}
	% endif
</%def>
<!DOCTYPE html>
<html>
	<head>
		<title>${title()}</title>
	</head>
	<body>
		<%block name="header">
			<h1>${title()}</h1>
		</%block>
		<%block name="content">
		</%block>
		<%block name="footer">
			<p>
				<a href="${request.route_url('logout')}">Logout</a>
				% if user.admin:
					- <a href="${request.route_url('admin')}">Admin</a>
				% endif
			</p>
		</%block>
	</body>
</html>
