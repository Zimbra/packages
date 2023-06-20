Summary:            Zimbra's Unbound build
Name:               zimbra-unbound
Version:            VERSION
Release:            1zimbra8.8b1ZAPPEND
License:            BSD
Source:             %{name}-%{version}.tar.gz
Patch0:             log-facility.patch
BuildRequires:      expat-devel, zimbra-openssl-devel >= 3.0.9-1zimbra8.8b1ZAPPEND
Requires:           expat, zimbra-openssl-libs >= 3.0.9-1zimbra8.8b1ZAPPEND
Requires:           zimbra-unbound-libs = %{version}-%{release}
AutoReqProv:        no
URL:                https://www.unbound.net/

%description
The Zimbra Unbound build

%define debug_package %{nil}

%changelog
* Mon Jun 12 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
- ZBUG-3355, Upgraded OpenSSL to 3.0.9 and upgraded unbound to 1.17.1
* Sat Aug 20 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Fix ZCS-11941, remove anchor key generation
* Tue Apr 12 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Fix ZBUG-2723, Generate anchor key required for DNSSEC
* Fri Dec 02 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Upgraded dependency openssl to 1.1.1h
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-ITERATIONZAPPEND
- Upgraded to 1.110 and updated dependency openssl to 1.1.1g

%prep
%setup -n unbound-%{version}
%patch0 -p1

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC \
  --with-ssl=OZC \
  --with-username=zimbra \
  --with-conf-file=/opt/zimbra/conf/unbound.conf \
  --with-pidfile=/opt/zimbra/log/unbound.pid \
  --with-chroot-dir=/opt/zimbra
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        Unbound Libaries
Requires:       zimbra-openssl-libs, zimbra-dnscache-base
AutoReqProv:        no

%description libs
The zimbra-unbound-libs package contains the unbound libraries

%package devel
Summary:        Unbound Development
Requires: zimbra-unbound-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-unbound-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZC/sbin
OZCS
%exclude /opt/zimbra/conf

%files libs
%defattr(-,root,root)
OZCL/*.so.*
OZC/lib/pkgconfig/libunbound.pc

%files devel
%defattr(-,root,root)
OZCI
OZCL/*.a
OZCL/*.la
OZCL/*.so
