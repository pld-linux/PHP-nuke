Summary:	Slashdot-like webnews site written in php, easy to install and use
Summary(pl):	Serwis nowinek WWW w stylu Slashdota napisany w PHP, �atwy w instalacji i u�ywaniu
Name:		PHP-nuke
Version:	6.8
Release:	0.1
License:	GPL
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/phpnuke/PHP-Nuke-%{version}.tar.gz
# Source0-md5:	cd5a164f5094edc4e182d6ec8c00700e
Source1:	PHP-Nuke.README.first
Icon:		phpnuke.gif
URL:		http://phpnuke.org/
Requires:	php-mysql
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
Portal WWW napisany w PHP. Ma du�e mo�liwo�ci, jest �atwy w instalacji
u u�ywaniu. Szczeg�y w dokumentacji w %{_docdir}/%{name}-%{version}.

Wystarczy zrobi� jedno: mysqladmin create nuke mysql nuke < \
%{_docdir}/%{name}-%{version}/nuke.sql

(wi�cej informacji w %{_docdir}/%{name}-%{version}/README.first)

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
%doc ADDONS-MODULES BLOCKS CHANGES CREDITS INSTALL README*
%doc SUPPORT TODO UPGRADE sql/nuke.sql upgrades
%dir %{nukeroot}
%config(noreplace) %attr(640,http,http) %{nukeroot}/config.php
%{nukeroot}/[^c]*
# more needed?
