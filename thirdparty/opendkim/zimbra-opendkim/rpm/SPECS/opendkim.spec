Summary:            Zimbra's OpenDKIM build
Name:               zimbra-opendkim
Version:            VERSION
Release:            1zimbra9.0b2ZAPPEND
License:            OpenDKIM
Source:             %{name}-%{version}.tar.gz
Patch0:             ticket226.patch
BuildRequires:      zlib-devel
BuildRequires:      zimbra-openssl-devel
BuildRequires:      zimbra-libbsd-devel
BuildRequires:      zimbra-openldap-devel
BuildRequires:      zimbra-libmilter-devel
BuildRequires:      zimbra-cyrus-sasl-devel
Requires:           zlib, zimbra-opendkim-libs = %{version}-%{release}
Requires:           zimbra-openssl-libs
Requires:           zimbra-libbsd-libs
Requires:           zimbra-openldap-libs
AutoReqProv:        no
URL:                http://www.opendkim.org/

%description
The Zimbra OpenDKIM build

%changelog
* Mon May 02 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra9.0b2ZAPPEND
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
