%define nukeroot /var/www/html/nuke

Summary:	Slashdot-like webnews site written in php. Easy to install and use
Name:		PHP-nuke
Version:	6.0
Release:	1mdk
Source0:	http://belnet.dl.sourceforge.net/sourceforge/phpnuke/PHP-Nuke-%version.tar.bz2
Source1:	PHP-Nuke-README.first.bz2
License:	GPL
Url:		http://phpnuke.org
Icon:		phpnuke.gif
Group:		System/Servers
Requires:	webserver mysqlserver php-common mod_php php-mysql
BuildRoot:	%_tmppath/%name-%{version}-buildroot
BuildArch:	noarch
Prefix:		%{nukeroot}

%description
Web-portal writen in php. 
Very powerful, yet easy to install and use: see documentation in 
%{_docdir}/%{name}-%{version} for details. 

You only have to run :
	mysqladmin create nuke
	mysql nuke < %{_docdir}/%{name}-%{version}/nuke.sql
	
[read %{_docdir}/%{name}-%{version}/README.first
 for further information .-)]

%prep

# Create Build Subdirectory and Unpack the Tar Ball
%setup -q -c %{name}-%{version}

cp %{SOURCE1} %{_builddir}/%{name}-%{version}/README.first.bz2
bunzip2 %{_builddir}/%{name}-%{version}/*.bz2

# (TV): workaround for bad tarball
find -type d -exec chmod 755 '{}' \;
find -type f -exec chmod 644 '{}' \;
find -type f -empty |xargs rm -f
chmod 755 */*/*/

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# Make the Necessary Directories
install -m755 -d %{buildroot}%{nukeroot}
install -m755 -d %{buildroot}%{_docdir}/%{name}-%{version}

cp -ar html/* %{buildroot}/%{nukeroot}/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc ADDONS-MODULES BLOCKS CHANGES CREDITS INSTALL README*
%doc SUPPORT TODO TRANSLATIONS UPGRADE sql/nuke.sql upgrades
%config(noreplace) %attr(644,apache,apache) %{nukeroot}/config.php
%{nukeroot}

%changelog
* Mon Sep 23 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 6.0-1mdk
- new version
- new relocatable Prefix: %%{nukeroot} (defaults to /var/www/html/nuke)
 
* Wed Sep 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 5.6-5mdk
- do not require non existant php extensions

* Thu Aug 22 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.6-4mdk
- never output text in %%post

* Tue Aug  6 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 5.6-3mdk
- remove useradd/delete in %%pre %%postun
- added some instructions in %%post

* Mon Jul 22 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.6-2mdk
- build release

* Fri Jun  7 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 5.6-1mdk
- new version
- misc spec file fixes

* Wed May 22 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.5-1mdk
- new release

* Thu Nov 22 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.3-2mdk
- rpmlint fixes

* Thu Nov 08 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.3-1mdk
- new release

* Fri Oct 05 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.2-2mdk
- explain how to create the nuke db

* Wed Oct 03 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.2-1mdk
- new release

* Thu Aug 16 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.1-1mdk
- new release

* Mon Aug 06 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.0.1-1mdk
- don't overwirte config file
- let apache alter it
- clean spec file
- readd url int source0
- explain the only remaining step to do in description (one-liner)

* Thu Jul 19 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.0.1-1mdk
- new release
- spec cleaning (empty {%%post,%%preun}, s,Copyright!License, ...)
- fix '%%changelog not in decending chronological order' from denis

* Tue  Jan  26 2001 Denis Havlik <deno@mandrakesoft.com> 4.3-1mdk
- update to version 4.3, add php-mysql and mod-php to 'requires' 

* Thu  Jan 11 2001 Denis Havlik <deno@mandrakesoft.com> 3.6-1mdk
- version 3.6, rebuild for php4 

* Sat Sep  2 2000 Denis Havlik <deno@mandrakesoft.com> 3.0-1mdk
- first RPM of PHP-nuke-3.0
