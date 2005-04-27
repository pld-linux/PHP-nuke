# TODO:
# - SECURITY: http://securitytracker.com/alerts/2004/Jul/1010734.html
# - SECURITY: http://securitytracker.com/alerts/2004/Jul/1010722.html
# - SECURITY: http://securitytracker.com/alerts/2004/Jun/1010571.html
# - SECURITY: http://securitytracker.com/alerts/2004/Jun/1010477.html
# - SECURITY: http://securitytracker.com/alerts/2004/Aug/1010924.html
# - SECURITY: http://securitytracker.com/alerts/2004/Sep/1011160.html
Summary:	Slashdot-like webnews site written in php, easy to install and use
Summary(pl):	Serwis nowinek WWW w stylu Slashdota napisany w PHP, ³atwy w instalacji i u¿ywaniu
Name:		PHP-nuke
Version:	7.6
Release:	1
License:	GPL
Group:		Applications/Databases/Interfaces
Source0:	http://phpnuke.org/files/PHP-Nuke-%{version}.zip
# Source0-md5:	1996a21729c06dc2b975342ee945d7e1
Source1:	PHP-Nuke.README.first
Source2:	%{name}.conf
#Icon:		phpnuke.gif
URL:		http://phpnuke.org/
Requires:	php-mysql
Requires:	php-pcre
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_nukeroot	%{_datadir}/phpnuke

%description
Web-portal writen in php. Very powerful, yet easy to install and use:
see documentation in %{_docdir}/%{name}-%{version} for details.

You only have to run:
mysqladmin create nuke
mysql nuke < %{_docdir}/%{name}-%{version}/nuke.sql

(read %{_docdir}/%{name}-%{version}/README.first for further
information)

%description -l pl
Portal WWW napisany w PHP. Ma du¿e mo¿liwo¶ci, jest ³atwy w instalacji
u u¿ywaniu. Szczegó³y w dokumentacji w %{_docdir}/%{name}-%{version}.

Wystarczy zrobiæ jedno:
mysqladmin create nuke
mysql nuke < %{_docdir}/%{name}-%{version}/nuke.sql

(wiêcej informacji w %{_docdir}/%{name}-%{version}/README.first)

%prep
%setup -q -c

install %{SOURCE1} README.first

# (TV): workaround for bad tarball
find -type d -exec chmod 755 '{}' \;
find -type f -exec chmod 644 '{}' \;
find -type f -empty |xargs rm -f
chmod 755 */*/*/

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_nukeroot},/etc/httpd}

cp -ar html/* $RPM_BUILD_ROOT%{_nukeroot}

install %{SOURCE2} $RPM_BUILD_ROOT/etc/httpd/phpnuke.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- %{name} <= 7.4-2
if [ -s /home/services/httpd/html/nuke/config.php ]; then
	mv -f /home/services/httpd/html/nuke/config.php %{_nukeroot}
fi

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*phpnuke.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/phpnuke.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/phpnuke.conf /etc/httpd/httpd.conf/phpnuke.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_phpnuke.conf
	else
		grep -v "^Include.*phpnuke.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc Addons* Blocks* Changes* Credits* Install* README* Readme*
%doc Support* Upgrade* sql/nuke.sql upgrades
%config(noreplace) %verify(not size mtime md5) /etc/httpd/phpnuke.conf
%dir %{_nukeroot}
%config(noreplace) %attr(640,http,http) %{_nukeroot}/config.php
%{_nukeroot}/[!c]*
# more needed?
