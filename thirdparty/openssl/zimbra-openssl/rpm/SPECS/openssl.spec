Summary:            Zimbra's Secure Socket Layer build
Name:               zimbra-openssl
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            OpenSSL
Source:             %{name}-%{version}.tar.gz
Patch:              ipv6.patch
Requires:           zimbra-openssl-libs = %{version}-%{release}, perl, perl-core
AutoReqProv:        no
URL:                https://www.openssl.org/source

%description
The Zimbra OpenSSL build allows for secure communication between various processes.

%changelog
* Fri Jul 28 2017  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Bug 106869: Updated openssl.
* Fri May 01 2015 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b1ZAPPEND
- Initial Release.

%prep
%setup -n openssl-%{version}
%patch -p1

%build
./Configure no-idea enable-ec_nistp_64_gcc_128 no-mdc2 no-rc5 no-ssl2 \
  no-hw --prefix=OZC --libdir=lib --openssldir=OZCE/ssl \
  shared linux-x86_64 -g -O2 -DOPENSSL_NO_HEARTBEATS -DOPENSSL_NO_BUF_FREELISTS
LD_RUN_PATH=OZCL make depend
LD_RUN_PATH=OZCL make all

%install
LD_RUN_PATH=OZCL make INSTALL_PREFIX=${RPM_BUILD_ROOT} MANDIR="OZCS/man" LIBS="" install
chmod u+w ${RPM_BUILD_ROOT}OZCL/lib* ${RPM_BUILD_ROOT}OZCL/engines/*.so

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
%dir OZCL/engines
%attr(555,-,-) OZCL/libssl.so.*
%attr(555,-,-) OZCL/libcrypto.so.*
%attr(555,-,-) OZCL/engines/*.so

%files devel
%defattr(-,root,root)
OZCL/*.so
OZCI
OZCL/pkgconfig

%changelog
* Wed May 20 2015 Zimbra Packaging Services <packaging-devel@zimbra.com>
- initial packaging
