Summary:	Open connection through firewall on specified signal
Name:		knock
Version:	0.5
Release:	%mkrel 9
Source0:	http://www.zeroflux.org/knock/files/%{name}-%{version}.tar.bz2
Source1:	knockd.initscript
Source2:	knockd.logrotate
Patch0:   knock-0.5-limits.h.fix.diff
License:	GPLv2+
Group:		Networking/Other
URL:		http://www.zeroflux.org/knock/
BuildRequires:	libpcap-devel
Requires(post):		rpm-helper
Requires(preun):	rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
knock is a server/client set that implements the idea known as port-
knocking. Port-knocking is a method of accessing a backdoor to your
firewall through a special sequence of port hits. This can be useful
for opening up temporary holes in a restrictive firewall for SSH
access or similar.

%prep
%setup -q
%patch0 -p0

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%_initrddir
install -m 744 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}d

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}d

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat > %{buildroot}%{_sysconfdir}/sysconfig/%{name} <<EOF
# Options to pass to %{name}d
OPTIONS=""
EOF

%post
%_post_service %{name}d

%preun
%_preun_service %{name}d

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog README TODO
%config(noreplace) %{_sysconfdir}/%{name}d.conf
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(755,root,root) %{_initrddir}/%{name}d
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}d
%{_bindir}/%{name}
%{_sbindir}/%{name}d
%{_mandir}/man1/*



%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5-9mdv2011.0
+ Revision: 619994
- the mass rebuild of 2010.0 packages

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.5-8mdv2010.0
+ Revision: 438134
- rebuild

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 0.5-7mdv2009.1
+ Revision: 298596
- fix build
- rebuilt against libpcap-1.0.0

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Adam Williamson <awilliamson@mandriva.org>
    - remove old sources

* Wed Feb 13 2008 Adam Williamson <awilliamson@mandriva.org> 0.5-4mdv2008.1
+ Revision: 166898
- add copytruncate to logrotate config file as knock does not re-initialize the logfile on a SIGHUP (#37666)
- add parallel init info to the initscript
- rewrap description
- bunzip2 additional sources
- better summary
- new license policy
- spec clean

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Oct 24 2007 Olivier Thauvin <nanardon@mandriva.org> 0.5-3mdv2008.1
+ Revision: 101909
- rebuild


* Wed Aug 09 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 08/09/06 17:55:38 (54965)
- prereq fix

* Wed Aug 09 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 08/09/06 17:53:18 (54963)
Import knock

* Mon Jul 25 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.5-1mdk
- New release 0.5

* Wed Jul 13 2005 Oden Eriksson <oeriksson@mandriva.com> 0.4-2mdk
- rebuilt against new libpcap-0.9.1 (aka. a "play safe" rebuild)

* Wed Jan 12 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.4-1mdk
- 0.4 ("Est-ce que ça vous chatouille ou est-ce que ça vous gratouille ?")

* Fri May 07 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.3-1mdk
- What's news, doc ? (a spec file :)

