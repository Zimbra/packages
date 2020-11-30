Summary:            Zimbra's Unbound build
Name:               zimbra-unbound
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            BSD
Source:             %{name}-%{version}.tar.gz
Patch0:             log-facility.patch
BuildRequires:      expat-devel, zimbra-openssl-devel >= 1.1.1h-1zimbra8.7b3ZAPPEND
Requires:           expat, zimbra-openssl-libs >= 1.1.1h-1zimbra8.7b3ZAPPEND
Requires:           zimbra-unbound-libs = %{version}-%{release}
AutoReqProv:        no
URL:                https://www.unbound.net/

%description
The Zimbra Unbound build

%define debug_package %{nil}

%changelog
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-ITERATIONZAPPEND
- Upgraded to 1.110 and updated dependency openssl to 1.1.1h

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
