Summary:            Zimbra's Cyrus-SASL build
Name:               zimbra-cyrus-sasl
Version:            VERSION
Release:            1zimbra8.7b3ZAPPEND
License:            MIT
Source:             %{name}-%{version}.tar.gz
Patch0:             sasl-auth-zimbra-2.1.28.patch
Patch1:             saslauthd-conf-2.1.28.patch
Patch2:             auxprop.patch
Patch3:             testsaslauthd.c.patch
BuildRequires:      zlib-devel
BuildRequires:      zimbra-openssl-devel >= 1.1.1h-1zimbra8.7b3ZAPPEND
BuildRequires:      zimbra-heimdal-devel >= 1.5.3-1zimbra8.7b3ZAPPEND
BuildRequires:      zimbra-libxml2-devel
BuildRequires:      zimbra-curl-devel >= 7.49.1-1zimbra8.7b3ZAPPEND
Requires:           zlib, zimbra-cyrus-sasl-libs = %{version}-%{release}, zimbra-openssl-libs >= 1.1.1h-1zimbra8.7b3ZAPPEND, zimbra-heimdal-libs >= 1.5.3-1zimbra8.7b3ZAPPEND
Requires:           zimbra-libxml2-libs, zimbra-curl-libs >= 7.49.1-1zimbra8.7b3ZAPPEND
AutoReqProv:        no
URL:                https://cyrusimap.org/

%description
The Zimbra Cyrus-SASL build

%define debug_package %{nil}

%changelog
* Tue Jun 21 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Upgraded cyrus-sasl to 2.1.28
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Upgraded dependency openssl to 1.1.1h
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Upgraded dependency openssl to 1.1.1g and updated heimdal,curl

%prep
%setup -n cyrus-sasl-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS;
CFLAGS="-O2 -g -D_REENTRANT"; export CFLAGS;
PATH=OZCB:$PATH; export PATH;
rm -f config/ltconfig config/libtool.m4
libtoolize -f -c
aclocal -I config -I m4
automake -a -c -f
autoheader
autoconf -f
sed -i.bak 's/-lRSAglue //' configure
./configure --prefix=OZC \
  --with-saslauthd=/opt/zimbra/data/sasl2/state \
  --with-plugindir=OZCL/sasl2 \
  --with-dblib=no \
  --with-devrandom=/dev/urandom \
  --with-gss_impl=heimdal \
  --with-lib-subdir=lib \
  --with-openssl=OZC \
  --with-configdir=/opt/zimbra/conf/sasl2 \
  --enable-gssapi=OZC \
  --enable-login \
  --enable-shared=yes --enable-static=no --without-python
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        Cyrus-SASL Libaries
Requires: zimbra-openssl-libs, zimbra-heimdal-libs, zimbra-base
AutoReqProv:        no

%description libs
The zimbra-cyrus-sasl-libs package contains the curl libraries

%package devel
Summary:        Cyrus-SASL Development
Requires: zimbra-cyrus-sasl-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-cyrus-sasl-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZC/sbin
OZCS

%files libs
%defattr(-,root,root)
%dir OZCL/sasl2
OZCL/*.so.*
OZCL/sasl2

%files devel
%defattr(-,root,root)
OZCI
OZCL/*.la
OZCL/*.so
OZCL/pkgconfig
