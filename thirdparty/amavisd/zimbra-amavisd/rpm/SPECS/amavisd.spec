Summary:            Zimbra's amavisd build
Name:               zimbra-amavisd
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tar.bz2
Patch0:             amavisd.patch
Patch1:             amavis-mc.patch
Patch2:             perl-path.patch
Patch3:             socketpath.patch
Patch4:             zmq-sock.patch
Patch5:             amavis-pm.patch
Patch6:             rfc2821_2822_Tools.patch
Requires:           perl, zimbra-mta-base
AutoReqProv:        no
URL:                https://gitlab.com/amavis/amavis

%description
The Zimbra amavisd build

%define debug_package %{nil}

%prep
%setup -n amavis-v%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build

%install
mkdir -p ${RPM_BUILD_ROOT}OZC/sbin
cp bin/amavisd ${RPM_BUILD_ROOT}OZC/sbin
cp bin/amavisd-release ${RPM_BUILD_ROOT}OZC/sbin
cp bin/amavis-mc ${RPM_BUILD_ROOT}OZC/sbin
cp bin/amavis-services ${RPM_BUILD_ROOT}OZC/sbin
cp bin/amavisd-status ${RPM_BUILD_ROOT}OZC/sbin
cp bin/amavisd-snmp-subagent-zmq ${RPM_BUILD_ROOT}OZC/sbin
mkdir -p ${RPM_BUILD_ROOT}OZCL/perl5/
cp -r lib/* ${RPM_BUILD_ROOT}OZCL/perl5/

%files
%defattr(-,root,root)
OZC/sbin
OZCL

%changelog
* Fri Mar 10 2023  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- ZBUG-3025: Upgrade amavis to 2.13.0
* Mon Aug 22 2022  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Fix ZBUG-1457
