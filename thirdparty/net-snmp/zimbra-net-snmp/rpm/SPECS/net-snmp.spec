Summary:            Zimbra's NetSNMP build
Name:               zimbra-net-snmp
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            BSD
Source:             %{name}-%{version}.tar.gz
Patch0:             rpm.patch
Patch1:             0001-CHANGES-BUG-2712-Fix-Perl-module-compilation.patch
Patch2:             0001-Remove-U64-typedef.patch
BuildRequires:      zimbra-openssl-devel
BuildRequires:      perl-devel
Requires:           perl, perl-core
Requires:           zimbra-net-snmp-libs = %{version}-%{release}
AutoReqProv:        no
URL:                http://www.net-snmp.org/

%description
The Zimbra NetSNMP build

%prep
%setup -n net-snmp-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g -DHAVE_HEADERGET"; export CFLAGS; \
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
