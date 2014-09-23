Summary:	Open connection through firewall on specified signal
Name:		knock
Version:	0.5
Release:	12
Source0:	http://www.zeroflux.org/knock/files/%{name}-%{version}.tar.bz2
Source1:	knockd.service
Source2:	knockd.logrotate
Patch0:   knock-0.5-limits.h.fix.diff
License:	GPLv2+
Group:		Networking/Other
URL:		http://www.zeroflux.org/knock/
BuildRequires:	libpcap-devel

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
%makeinstall_std

mkdir -p %{buildroot}%{_unitdir}
install -m0644 -D %{SOURCE1} %{buildroot}%{_unitdir}/%{name}d.service

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}d

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat > %{buildroot}%{_sysconfdir}/sysconfig/%{name} <<EOF
# Options to pass to %{name}d
OPTIONS=""
EOF

%post
%systemd_post %{name}d

%preun
%systemd_preun %{name}d

%clean

%files
%doc ChangeLog README TODO
%config(noreplace) %{_sysconfdir}/%{name}d.conf
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0644,root,root) %{_unitdir}/%{name}d.service
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}d
%{_bindir}/%{name}
%{_sbindir}/%{name}d
%{_mandir}/man1/*
