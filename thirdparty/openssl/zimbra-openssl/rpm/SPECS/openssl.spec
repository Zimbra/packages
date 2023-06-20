Summary:            Zimbra's Secure Socket Layer build
Name:               zimbra-openssl
Version:            VERSION
Release:            1zimbra8.8b1ZAPPEND
License:            OpenSSL
Source:             %{name}-%{version}.tar.gz
Source1:            openssl-fips.cnf
Requires:           zimbra-openssl-libs = %{version}-%{release}, perl, perl-core
AutoReqProv:        no
URL:                https://www.openssl.org/source

%description
The Zimbra OpenSSL build allows for secure communication between various processes.

%define debug_package %{nil}

%changelog
* Mon Jun 12 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
- ZBUG-3355, Upgraded OpenSSL to 3.0.9
* Fri Feb 10 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Fix ZBUG-3278, Upgraded OpenSSL to 1.1.1t
* Mon Jul 11 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Fix for ZCS-11689, Upgraded OpenSSL to 1.1.1q
* Mon Apr 11 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Fix for ZBUG-2713, Upgraded OpenSSL to 1.1.1n
* Thu Sep 30 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Fix for ZBUG-2389, Upgraded OpenSSL to 1.1.1l
* Wed Apr 14 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Fix for ZBUG-2198, Upgraded OpenSSL to 1.1.1k
* Fri Apr 02 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Fix for ZBUG-2184
* Fri Dec 04 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Upgraded openssl to 1.1.1h
* Fri Aug 28 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Upgraded openssl to 1.1.1g
* Fri Jul 28 2017  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Bug 106869: Updated openssl.
* Fri May 01 2015 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b1ZAPPEND
- Initial Release.

%prep
%setup -n openssl-%{version}
%build
./Configure enable-fips no-idea enable-ec_nistp_64_gcc_128 no-mdc2 no-rc5 \
  --prefix=OZC --with-rand-seed=devrandom,rdcpu,os,getrandom --libdir=lib --openssldir=OZCE/ssl \
  shared linux-x86_64 -g -O2 -DOPENSSL_NO_HEARTBEATS
LD_RUN_PATH=OZCL make depend
LD_RUN_PATH=OZCL make all


%install
LD_RUN_PATH=OZCL make DESTDIR=${RPM_BUILD_ROOT} MANDIR="OZCS/man" LIBS="" install
chmod u+w ${RPM_BUILD_ROOT}OZCL/lib* ${RPM_BUILD_ROOT}OZCL/engines-3/*.so
cp %{buildroot}/opt/zimbra/common/etc/ssl/openssl.cnf %{buildroot}/opt/zimbra/common/etc/ssl/openssl-source.cnf
cp -af %{SOURCE1} %{buildroot}/opt/zimbra/common/etc/ssl/openssl-fips.cnf

%package libs
Summary:	SSL Libaries
Requires: zimbra-base
AutoReqProv:        no

%description libs
The zimbra-openssl-libs package contains the openssl libraries

%package devel
Summary:	SSL Development
Requires: zimbra-openssl-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-openssl-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
OZCE
OZCS

%files libs
%defattr(-,root,root)
%dir /opt/zimbra
%dir OZC
%dir OZCL
%dir OZCL/engines-3
%dir OZCL/ossl-modules
%attr(555,-,-) OZCL/libssl.so.*
%attr(555,-,-) OZCL/libcrypto.so.*
%attr(555,-,-) OZCL/engines-3/*.so
%attr(555,-,-) OZCL/ossl-modules/*.so
%attr(555,-,-) OZCL/libcrypto.a
%attr(555,-,-) OZCL/libssl.a

%files devel
%defattr(-,root,root)
OZCL/*.so
OZCI
OZCL/pkgconfig

%post -p /bin/bash
/opt/zimbra/common/bin/openssl fipsinstall -quiet -out /opt/zimbra/common/etc/ssl/fipsmodule.cnf -module /opt/zimbra/common/lib/ossl-modules/fips.so
cp -af /opt/zimbra/common/etc/ssl/openssl-fips.cnf /opt/zimbra/common/etc/ssl/openssl.cnf
