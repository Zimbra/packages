Summary:            ClueBringer Policy Daemon
Name:               zimbra-cluebringer
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tgz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Requires:            zimbra-mta-base, zimbra-perl-base, zimbra-perl-cache-fastmmap
Requires:            zimbra-perl-config-inifiles, zimbra-perl-dbi, zimbra-perl-dbd-sqlite
Requires:            zimbra-perl-mail-spf, zimbra-perl-net-cidr, zimbra-perl-net-dns
Requires:            zimbra-perl-net-server, zimbra-perl-timedate
AutoReqProv:        no
URL:                http://wiki.policyd.org/

%description
PolicyD v2 (codenamed "cluebringer") is a multi-platform policy server for popular
MTAs. This policy daemon is designed mostly for large scale mail hosting environments.
The main goal is to implement as many spam combating and email compliance features as
possible while at the same time maintaining the portability, stability and performance
required for mission critical email hosting of today. Most of the ideas and methods
implemented in PolicyD v2 stem from PolicyD v1 as well as the authors' long time
involvement in large scale mail hosting industry.

%define debug_package %{nil}

%prep
%setup -n cluebringer-%{version}

%build

%install
mkdir -p ${RPM_BUILD_ROOT}OZCB
cp cbpadmin ${RPM_BUILD_ROOT}/OZCB
sed -i -e 's|/usr/local/lib/cbpolicyd-2.1|/opt/zimbra/common/lib/policyd-2.1|' \
       -e 's|/usr/lib/cbpolicyd-2.1|/opt/zimbra/common/lib/perl5|' \
       -e 's|/etc/cbpolicyd/cluebringer.conf|/opt/zimbra/conf/cbpolicyd.conf|' \
       -e "s|'/usr/lib64/cbpolicyd-2.1',||" \
       ${RPM_BUILD_ROOT}/OZCB/cbpadmin
cp cbpolicyd ${RPM_BUILD_ROOT}/OZCB
sed -i -e 's|/usr/local/lib/cbpolicyd-2.1|/opt/zimbra/common/lib/policyd-2.1|' \
       -e 's|/usr/lib/cbpolicyd-2.1|/opt/zimbra/common/lib/perl5|' \
       -e 's|/etc/cbpolicyd/cluebringer.conf|/opt/zimbra/conf/cbpolicyd.conf|' \
       -e 's|/var/run/cbpolicyd/cbpolicyd.pid|/opt/zimbra/log/cbpolicyd.pid|' \
       -e 's|/var/log/cbpolicyd/cbpolicyd.log|/opt/zimbra/log/cbpolicyd.log|' \
       -e "s|'/usr/lib64/cbpolicyd-2.1',||" \
       ${RPM_BUILD_ROOT}/OZCB/cbpolicyd
mkdir -p ${RPM_BUILD_ROOT}/OZCL/policyd-2.1
cp -r cbp ${RPM_BUILD_ROOT}/OZCL/policyd-2.1
cp -r awitpt ${RPM_BUILD_ROOT}/OZCL/policyd-2.1
mkdir -p  ${RPM_BUILD_ROOT}OZCS
cp -r contrib ${RPM_BUILD_ROOT}/OZCS/
cp -r docs ${RPM_BUILD_ROOT}/OZCS/
cp -r database ${RPM_BUILD_ROOT}/OZCS/
cp -r webui ${RPM_BUILD_ROOT}/OZCS/

%files
%defattr(-,root,root)
OZCB
OZCL/policyd-2.1
OZCS
