Summary:            Zimbra's Apache Portable Runtime Utilities build
Name:               zimbra-apr-util
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            Apache-2.0
Source:             %{name}-%{version}.tar.bz2
BuildRequires:      zimbra-apr-devel, expat-devel
BuildRequires:      zimbra-openssl-devel >= 1.1.1h-1zimbra8.7b3ZAPPEND
Requires:           zimbra-apr-util-libs = %{version}-%{release}
AutoReqProv:        no
URL:                https://apr.apache.org/

%description
The Zimbra Apache Portable Runtime Utilities build

%define debug_package %{nil}

%changelog
* Fri Dec 02 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Upgraded dependency openssl to 1.1.1h
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-ITERATIONZAPPEND
- Upgraded to 1.6.1 and updated dependency openssl to 1.1.1g

%prep
%setup -n apr-util-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC \
 --with-apr=OZCB/apr-1-config \
 --with-crypto \
 --with-openssl=OZC
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        Apache Portable Runtime Utilities Libaries
Requires:	zimbra-apr-libs, expat, zimbra-apache-base
Requires:       zimbra-openssl-libs
AutoReqProv:        no

%description libs
The zimbra-apr-util-libs package contains the apr utilities libraries

%package devel
Summary:        Apache Portable Runtime Utilities Development
Requires: zimbra-apr-util-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-apr-util-devel package contains the linking libraries and include files

%files libs
%defattr(-,root,root)
OZCL/*.so.*
OZCL/apr-util-1/*.so

%files devel
%defattr(-,root,root)
OZCB/apu-1-config
OZCI
OZCL/*.a
OZCL/*.la
OZCL/*.so
OZCL/apr-util-1/*.la
OZCL/apr-util-1/*.a
OZCL/aprutil.exp
OZCL/pkgconfig
