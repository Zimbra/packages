Summary:            Zimbra's ClamAV build
Name:               zimbra-clamav
Version:            VERSION
Release:            1zimbra8.8b4ZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tar.gz
Patch0:             clamav-fips.patch
BuildRequires:      zlib-devel
BuildRequires:      ncurses-devel
BuildRequires:      bzip2-devel, check-devel, json-c-devel, pcre2-devel
BuildRequires:      zimbra-openssl-devel >= 3.0.9-1zimbra8.8b1ZAPPEND
BuildRequires:      zimbra-libxml2-devel
BuildRequires:      zimbra-libmilter-devel
Requires:           zlib, ncurses-libs, zimbra-clamav-libs = %{version}-%{release}, zimbra-openssl-libs >= 3.0.9-1zimbra8.8b1ZAPPEND
Requires:           zimbra-libxml2-libs, pcre2, json-c, bzip2-libs
AutoReqProv:        no
URL:                http://www.clamav.net/

%description
The Zimbra ClamAV build

%define debug_package %{nil}

%changelog
* Mon Jul 29 2024  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b4ZAPPEND
- ZCS-15540, Upgraded ClamAV to 1.0.6
* Fri Jun 23 2023  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b4ZAPPEND
- ZCS-13605, Upgraded ClamAV to 1.0.1
* Mon Jun 12 2023  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b4ZAPPEND
- ZBUG-3355, Upgraded OpenSSL to 3.0.9
* Wed Feb 22 2023  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b3ZAPPEND
- Upgraded ClamAV to 0.105.2
* Wed Nov 02 2022  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b3ZAPPEND
- Upgraded ClamAV to 0.105.1-2
* Fri Oct 14 2022  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b3ZAPPEND
- Fix ZBUG-2817,Upgraded ClamAV to 0.105.1
* Mon Mar 28 2022  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b3ZAPPEND
- Fix ZCS-11150,Upgraded clamav to 0.103.3
* Thu Apr 15 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b3ZAPPEND
- Upgraded clamav to 0.103.2
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b3ZAPPEND
- Upgraded dependency openssl to 1.1.1h
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b2ZAPPEND
- Upgraded dependency openssl to 1.1.1g
* Sun Mar 15 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
- Upgraded clamav to 0.102.2

%prep
%setup -n clamav-%{version}
%patch0 -p1

%build
LDFLAGS="-LOZCL -Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
CPPFLAGS="-IOZCI"; export CPPFLAGS; \
cd cmake && cmake .. \
 -DCMAKE_BUILD_TYPE="Release" \
 -DCLAMAV_USER=zimbra \
 -DCLAMAV_GROUP=zimbra \
 -DOPENSSL_INCLUDE_DIR="OZCI" \
 -DOPENSSL_CRYPTO_LIBRARY="OZCL/libcrypto.so" \
 -DOPENSSL_SSL_LIBRARY="OZCL/libssl.so" \
 -DLIBXML2_INCLUDE_DIR="OZCI/libxml2" \
 -DLIBXML2_LIBRARY="OZCL/libxml2.so.2" \
 -DCMAKE_INSTALL_PREFIX="OZC" \
 -DCMAKE_INSTALL_LIBDIR="OZCL"

%install
cd cmake && make install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}OZCE/*.sample
rm -rf ${RPM_BUILD_ROOT}/usr/lib/systemd
rm -rf ${RPM_BUILD_ROOT}OZCS/doc

%package libs
Summary:        ClamAV Libaries
Requires: zlib, zimbra-openssl-libs, zimbra-libxml2-libs, zimbra-mta-base
AutoReqProv:        no

%description libs
The zimbra-clamav-libs package contains the clamav libraries

%package devel
Summary:        ClamAV Development
Requires: zimbra-clamav-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-clamav-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
OZC/sbin
OZCS
%exclude OZCB/clamav-config

%files libs
%defattr(-,root,root)
OZCL/*.so.*

%files devel
%defattr(-,root,root)
OZCB/clamav-config
OZCL/*.so
OZCL/pkgconfig
OZCI
