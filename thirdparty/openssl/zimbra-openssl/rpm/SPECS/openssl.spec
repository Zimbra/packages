Summary:            Zimbra's Secure Socket Layer build
Name:               zimbra-openssl
Version:            VERSION
Release:            1zimbra8.7b4ZAPPEND
License:            OpenSSL
Source:             %{name}-%{version}.tar.gz
Patch0:             openssl-1.1.1-fips.patch
Patch1:             openssl-1.1.1-version-override.patch
Patch2:             openssl-1.1.1-seclevel.patch
Patch3:             openssl-1.1.1-fips-post-rand.patch
Patch4:             openssl-1.1.1-evp-kdf.patch
Patch5:             openssl-1.1.1-ssh-kdf.patch
Patch6:             openssl-1.1.1-krb5-kdf.patch
Patch7:             openssl-1.1.1-edk2-build.patch
patch8:             openssl-1.1.1-ec-curve.patch
Patch9:             openssl-1.1.1-fips-curves.patch
Patch10:            openssl-1.1.1-fips-drbg-selftest.patch
Patch11:            openssl-1.1.1-fips-dh.patch
Patch12:            openssl-1.1.1-kdf-selftest.patch
Patch13:            openssl-1.1.1-rewire-fips-drbg.patch
Patch14:            openssl-1.1.1-fips-crng-test.patch
Patch15:            openssl-1.1.1-linux-random.patch
Requires:           zimbra-openssl-libs = %{version}-%{release}, perl, perl-core
AutoReqProv:        no
URL:                https://www.openssl.org/source

%description
The Zimbra OpenSSL build allows for secure communication between various processes.

%define debug_package %{nil}

%changelog
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%build
./Configure no-idea enable-ec_nistp_64_gcc_128 no-mdc2 no-rc5 no-ssl2 \
  no-hw --prefix=OZC --with-rand-seed=devrandom,rdcpu,os,getrandom --libdir=lib --openssldir=OZCE/ssl \
  shared linux-x86_64 -g -O2 -DOPENSSL_NO_HEARTBEATS
LD_RUN_PATH=OZCL make depend
LD_RUN_PATH=OZCL make all

%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    export LD_LIBRARY_PATH="${RPM_BUILD_ROOT}OZCL" && crypto/fips/fips_standalone_hmac ${RPM_BUILD_ROOT}OZCL/libcrypto.so.1.1 >${RPM_BUILD_ROOT}OZCL/.libcrypto.so.1.1.hmac \
    export LD_LIBRARY_PATH="${RPM_BUILD_ROOT}OZCL" && crypto/fips/fips_standalone_hmac ${RPM_BUILD_ROOT}OZCL/libssl.so.1.1 >${RPM_BUILD_ROOT}OZCL/.libssl.so.1.1.hmac \
    unset LD_LIBRARY_PATH \
%{nil}

%install
LD_RUN_PATH=OZCL make DESTDIR=${RPM_BUILD_ROOT} MANDIR="OZCS/man" LIBS="" install
chmod u+w ${RPM_BUILD_ROOT}OZCL/lib* ${RPM_BUILD_ROOT}OZCL/engines-1.1/*.so

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
%dir OZCL/engines-1.1
%attr(555,-,-) OZCL/libssl.so.*
%attr(555,-,-) OZCL/libcrypto.so.*
%attr(555,-,-) OZCL/engines-1.1/*.so
%attr(555,-,-) OZCL/libcrypto.a
%attr(555,-,-) OZCL/libssl.a
%attr(0644,-,-) OZCL/.libcrypto.so.*.hmac
%attr(0644,-,-) OZCL/.libssl.so.*.hmac

%files devel
%defattr(-,root,root)
OZCL/*.so
OZCI
OZCL/pkgconfig
