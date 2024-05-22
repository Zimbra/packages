Summary:            Zimbra's OpenDKIM build
Name:               zimbra-opendkim
Version:            VERSION
Release:            1zimbra8.7b7ZAPPEND
License:            OpenDKIM
Source:             %{name}-%{version}.tar.gz
Patch0:             ticket226.patch
Patch1:             opendkim-2.10.3.patch
BuildRequires:      zlib-devel
BuildRequires:      zimbra-openssl-devel >= 3.0.9-1zimbra8.8b1ZAPPEND
BuildRequires:      zimbra-libbsd-devel
BuildRequires:      zimbra-openldap-devel >= 2.5.17-1zimbra10.0b1ZAPPEND
BuildRequires:      zimbra-libmilter-devel
BuildRequires:      zimbra-cyrus-sasl-devel >= 2.1.28-1zimbra8.7b4ZAPPEND
Requires:           zlib, zimbra-opendkim-libs = %{version}-%{release}
Requires:           zimbra-openssl-libs >= 3.0.9-1zimbra8.8b1ZAPPEND
Requires:           zimbra-libbsd-libs
Requires:           zimbra-openldap-libs >= 2.5.17-1zimbra10.0b1ZAPPEND
AutoReqProv:        no
URL:                http://www.opendkim.org/

%description
The Zimbra OpenDKIM build

%define debug_package %{nil}

%changelog
* Mon Mar 04 2024 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b7ZAPPEND
- Updated opendkim, Upgraded openldap to 2.5.17
* Mon Jun 12 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b6ZAPPEND
- ZBUG-3355, Upgraded OpenSSL to 3.0.9
* Tue Mar 16 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b5ZAPPEND
- add patch for ZBUG-2140
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Upgraded openssl to 1.1.1h and updated cyrus-sasl, openldap
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Upgraded openssl to 1.1.1g and updated cyrus-sasl, openldap
* Mon May 02 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Add patch for ticket 226

%prep
%setup -n opendkim-%{version}
%patch0 -p1
%patch1 -p1

%build
LDFLAGS="-LOZCL -Wl,-rpath,OZCL"; export LDFLAGS;
CFLAGS="-g -O0"; export CFLAGS;
CPPFLAGS="-IOZCI"; export CPPFLAGS;
autoreconf -fi configure.ac;
./configure --prefix=OZC \
  --enable-poll \
  --enable-adsp_lists \
  --enable-atps \
  --enable-rate_limit \
  --enable-replace_rules \
  --enable-resign \
  --enable-sender_macro \
  --enable-vbr \
  --enable-default_sender \
  --enable-rpath \
  --with-openssl=OZC \
  --with-milter=OZC \
  --with-openldap=OZC \
  --with-sasl=OZC \
  --without-db
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        OpenDKIM Libaries
Requires: zlib, zimbra-openssl-libs
Requires: zimbra-libbsd-libs, zimbra-mta-base
AutoReqProv:        no

%description libs
The zimbra-opendkim-libs package contains the opendkim libraries

%package devel
Summary:        OpenDKIM Development
Requires: zimbra-opendkim-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-opendkim-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZC/sbin
OZCS

%files libs
%defattr(-,root,root)
OZCL/*.so.*

%files devel
%defattr(-,root,root)
OZCL/*.a
OZCL/*.la
OZCL/*.so
OZCL/pkgconfig
OZCI
