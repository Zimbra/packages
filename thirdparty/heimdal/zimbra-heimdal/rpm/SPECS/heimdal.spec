Summary:            Zimbra's Heimdal Kerberos build
Name:               zimbra-heimdal
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            BSD
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zimbra-openssl-devel >= 1.1.1g-1zimbra8.7b3ZAPPEND
BuildRequires:      ncurses-devel
Requires:           zimbra-openssl-libs >= 1.1.1g-1zimbra8.7b3ZAPPEND, zimbra-heimdal-libs = %{version}-%{release}, ncurses-libs
AutoReqProv:        no
URL:                http://www.h5l.org/

%description
The Zimbra Heimdal Kerberos build for additional encryption services

%define debug_package %{nil}

%prep
%setup -n heimdal-%{version}

%build
LDFLAGS="-LOZCL -Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g -D_REENTRANT"; export CFLAGS; \
CPPFLAGS="-IOZCI"; export CPPFLAGS; \
./configure --prefix=OZC \
  --sysconfdir=/etc \
  --enable-shared \
  --enable-pthread-support \
  --disable-berkeley-db \
  --disable-ndbm-db \
  --disable-afs-support \
  --without-readline \
  --without-openldap \
  --without-hesiod \
  --enable-static=no
make -C include
make -C base
make -C lib/roken
make -C lib/vers
make -C lib/com_err
make -C lib/asn1
make -C lib/libedit
make -C lib/sl
make -C lib/hcrypto
make -C lib/wind
make -C lib/hx509
make -C lib/sqlite
make -C lib/ipc
make -C lib/krb5
make -C lib/ntlm
make -C lib/gssapi

%install
make -C include install DESTDIR=${RPM_BUILD_ROOT}
make -C base install DESTDIR=${RPM_BUILD_ROOT}
make -C lib/roken install DESTDIR=${RPM_BUILD_ROOT}
make -C lib/com_err install DESTDIR=${RPM_BUILD_ROOT}
make -C lib/asn1 install DESTDIR=${RPM_BUILD_ROOT}
make -C lib/libedit install DESTDIR=${RPM_BUILD_ROOT}
make -C lib/sl install DESTDIR=${RPM_BUILD_ROOT}
make -C lib/hcrypto install DESTDIR=${RPM_BUILD_ROOT}
make -C lib/wind install DESTDIR=${RPM_BUILD_ROOT}
make -C lib/hx509 install DESTDIR=${RPM_BUILD_ROOT}
make -C lib/sqlite install DESTDIR=${RPM_BUILD_ROOT}
make -C lib/ipc install DESTDIR=${RPM_BUILD_ROOT}
make -C lib/krb5 install DESTDIR=${RPM_BUILD_ROOT}
make -C lib/ntlm install DESTDIR=${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}OZCS/man/cat5/mech
mkdir -p ${RPM_BUILD_ROOT}OZCS/man/man5/mech
make -C lib/gssapi install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        Heimdal Libaries
Requires: zimbra-openssl-libs, ncurses-libs, zimbra-base
AutoReqProv:        no

%description libs
The zimbra-heimdal-libs package contains the heimdal libraries

%package devel
Summary:        Heimdal Development
Requires: zimbra-heimdal-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-heimdal-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
OZCLE
OZCS

%files libs
%defattr(-,root,root)
OZCL/*.so.*

%files devel
%defattr(-,root,root)
OZCL/*.la
OZCL/*.so
OZCI

%changelog
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Upgraded dependency openssl to 1.1.1g
* Wed May 20 2015 Zimbra Packaging Services <packaging-devel@zimbra.com>
- initial packaging
