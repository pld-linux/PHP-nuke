Summary:	Slashdot-like webnews site written in php, easy to install and use
Summary(pl):	Serwis nowinek WWW w stylu Slashdota napisany w PHP, ³atwy w instalacji i u¿ywaniu
Name:		PHP-nuke
Version:	7.8
Release:	2
License:	GPL
Group:		Applications/WWW
Source0:	http://phpnuke.org/files/PHP-Nuke-%{version}.zip
# Source0-md5:	0f60b9e5c67827192d4b36fc7b06b267
Source1:	PHP-Nuke.README.first
Source2:	%{name}.conf
URL:		http://phpnuke.org/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed > 4.0
BuildRequires:	unzip
Requires:	php-common >= 3:4.2.0
Requires:	php-pcre
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		phpnuke
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Content Management and Portal solution featuring web-based
administration, surveys, customizable blocks, modules and themes with
multilanguage support.

%description -l pl
Portal WWW napisany w PHP. Ma du¿e mo¿liwo¶ci, jest ³atwy w instalacji
u u¿ywaniu.

%prep
%setup -q -c
# undos the source
find . -type f -print0 | xargs -0 sed -i -e 's,\r$,,'
cp -p %{SOURCE1} README.first

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -a html/* $RPM_BUILD_ROOT%{_appdir}
mv $RPM_BUILD_ROOT%{_appdir}/config.php $RPM_BUILD_ROOT%{_sysconfdir}
ln -s %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/config.php
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
%banner -e %{name} <<EOF
If this is your first PHP Nuke install, then You should create the
MySQL database:
mysqladmin create nuke
zcat %{_docdir}/%{name}-%{version}/nuke.sql | mysql nuke

Read %{_docdir}/%{name}-%{version}/README.first.gz for further
information.
EOF
fi

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache >= 2.0.0
%webapp_register httpd %{_webapp}

%triggerun -- apache >= 2.0.0
%webapp_unregister httpd %{_webapp}

%triggerpostun -- %{name} < 7.8-1.4
# old 7.4-2 trigger
if [ -s /home/services/httpd/html/nuke/config.php ]; then
	mv -f /home/services/httpd/html/nuke/config.php %{_appdir}
fi

# nuke very-old config location (this mostly for Ra)
if [ -f /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*%{name}.conf/d" /etc/httpd/httpd.conf
fi

# migrate from httpd (apache2) config dir
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_sysconfdir}/httpd.conf
fi

rm -f /etc/httpd/httpd.conf/phpnuke.conf
/usr/sbin/webapp register httpd %{_webapp}
%service -q httpd reload

%files
%defattr(644,root,root,755)
%doc Addons* Blocks* Changes* Credits* Install* README* Readme*
%doc Support* Upgrade* sql/nuke.sql upgrades
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
