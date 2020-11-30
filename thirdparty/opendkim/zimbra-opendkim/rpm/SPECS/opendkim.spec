Summary:            Zimbra's OpenDKIM build
Name:               zimbra-opendkim
Version:            VERSION
Release:            1zimbra8.7b3ZAPPEND
License:            OpenDKIM
Source:             %{name}-%{version}.tar.gz
Patch0:             ticket226.patch
BuildRequires:      zlib-devel
BuildRequires:      zimbra-openssl-devel >= 1.1.1h-1zimbra8.7b3ZAPPEND
BuildRequires:      zimbra-libbsd-devel
BuildRequires:      zimbra-openldap-devel >= 2.4.49-1zimbra8.8b3ZAPPEND 
BuildRequires:      zimbra-libmilter-devel
BuildRequires:      zimbra-cyrus-sasl-devel >= 2.1.26-1zimbra8.7b2ZAPPEND
Requires:           zlib, zimbra-opendkim-libs = %{version}-%{release}
Requires:           zimbra-openssl-libs >= 1.1.1h-1zimbra8.7b3ZAPPEND
Requires:           zimbra-libbsd-libs
Requires:           zimbra-openldap-libs >= 2.4.49-1zimbra8.8b3ZAPPEND
AutoReqProv:        no
URL:                http://www.opendkim.org/

%description
The Zimbra OpenDKIM build

%define debug_package %{nil}

%changelog
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Upgraded openssl to 1.1.1h and updated cyrus-sasl, openldap
* Mon May 02 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Add patch for ticket 226

%prep
%setup -n opendkim-%{version}
%patch0 -p1

%build
LDFLAGS="-LOZCL -Wl,-rpath,OZCL"; export LDFLAGS;
CFLAGS="-g -O0"; export CFLAGS;
CPPFLAGS="-IOZCI"; export CPPFLAGS;
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
  --with-openssl=OZCL \
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
