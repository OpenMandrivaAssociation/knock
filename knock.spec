Summary:	Open connection through firewall on specified signal
Name:		knock
Version:	0.5
Release:	%mkrel 8
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

