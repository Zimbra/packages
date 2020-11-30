Summary:            Zimbra's NetSNMP build
Name:               zimbra-net-snmp
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            BSD
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zimbra-openssl-devel >= 1.1.1h-1zimbra8.7b3ZAPPEND
BuildRequires:      perl-devel
Requires:           perl, perl-core
Requires:           zimbra-net-snmp-libs = %{version}-%{release}
AutoReqProv:        no
URL:                http://www.net-snmp.org/

%description
The Zimbra NetSNMP build

%define debug_package %{nil}

%changelog
* Thu Sep 10 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated zimbra-openssl
* Tue Apr 24 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-ITERATIONZAPPEND
- Upgraded net-snmp to 5.8

%prep
%setup -n net-snmp-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC \
  --with-default-snmp-version=3 --with-sys-contact="admin" \
  --with-sys-location="unknown" --with-logfile="/opt/zimbra/log/snmpd.log" \
  --with-openssl=OZC \
  --disable-embedded-perl \
  --with-perl-modules="INSTALL_BASE=OZC LIB=OZCL/perl5 INSTALLSITEMAN3DIR=OZCS/man/man3" \
  --with-persistent-directory="/opt/zimbra/data/snmp/persist" \
  --localstatedir="/opt/zimbra/data/snmp/state"
make

%define perl_archname %(perl -MConfig -e 'print $Config{archname}')
%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/perllocal.pod
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/auto/*/*/.packlist

%package libs
Summary:            NetSNMP Libaries
Requires:           zimbra-openssl-libs, zimbra-snmp-base
AutoReqProv:        no

%description libs
The zimbra-net-snmp-libs package contains the net-snmp libraries

%package devel
Summary:        NetSNMP Development
Requires:       zimbra-net-snmp-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-net-snmp-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
OZCS
%exclude OZC/sbin

%files libs
%defattr(-,root,root)
OZCL/*.so.*
OZCL/perl5

%files devel
%defattr(-,root,root)
OZCI
OZCL/*.a
OZCL/*.la
OZCL/*.so
