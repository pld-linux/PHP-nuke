# TODO:
# - SECURITY: http://securitytracker.com/alerts/2004/Jul/1010734.html
# - SECURITY: http://securitytracker.com/alerts/2004/Jul/1010722.html
# - SECURITY: http://securitytracker.com/alerts/2004/Jun/1010571.html
Summary:	Slashdot-like webnews site written in php, easy to install and use
Summary(pl):	Serwis nowinek WWW w stylu Slashdota napisany w PHP, ³atwy w instalacji i u¿ywaniu
Name:		PHP-nuke
Version:	7.3
Release:	1
License:	GPL
Group:		Applications/Databases/Interfaces
Source0:	http://phpnuke.org/files/PHP-Nuke-%{version}.zip
# Source0-md5:	b6bdea4d54e0693e85b96bb405e2c874
Source1:	PHP-Nuke.README.first
#Icon:		phpnuke.gif
URL:		http://phpnuke.org/
Requires:	php-mysql
Requires:	php-pcre
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		nukeroot	/home/services/httpd/html/nuke

%description
Web-portal writen in php. Very powerful, yet easy to install and use:
see documentation in %{_docdir}/%{name}-%{version} for details.

You only have to run: mysqladmin create nuke mysql nuke < \
%{_docdir}/%{name}-%{version}/nuke.sql

(read %{_docdir}/%{name}-%{version}/README.first for further
information)

%description -l pl
Portal WWW napisany w PHP. Ma du¿e mo¿liwo¶ci, jest ³atwy w instalacji
u u¿ywaniu. Szczegó³y w dokumentacji w %{_docdir}/%{name}-%{version}.

Wystarczy zrobiæ jedno: mysqladmin create nuke mysql nuke < \
%{_docdir}/%{name}-%{version}/nuke.sql

(wiêcej informacji w %{_docdir}/%{name}-%{version}/README.first)

%prep
%setup -q -c %{name}-%{version}

install %{SOURCE1} README.first

# (TV): workaround for bad tarball
find -type d -exec chmod 755 '{}' \;
find -type f -exec chmod 644 '{}' \;
find -type f -empty |xargs rm -f
chmod 755 */*/*/

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{nukeroot}

cp -ar html/* $RPM_BUILD_ROOT%{nukeroot}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Addons* Blocks* Changes* Credits* Install* README* Readme*
%doc Support* Upgrade* sql/nuke.sql upgrades
%dir %{nukeroot}
%config(noreplace) %attr(640,http,http) %{nukeroot}/config.php
%{nukeroot}/[^c]*
# more needed?
