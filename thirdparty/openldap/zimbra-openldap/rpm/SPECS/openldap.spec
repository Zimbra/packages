Summary:            Zimbra's openldap build
Name:               zimbra-openldap
Version:            VERSION
Release:            1zimbra8.8b1ZAPPEND
License:            BSD
Source:             %{name}-%{version}.tgz
Patch0:             liblmdb-soname.patch
Patch1:             liblmdb-keysize.patch
BuildRequires:      zimbra-openssl-devel >= 1.1.1h-1zimbra8.7b3ZAPPEND
BuildRequires:      zimbra-cyrus-sasl-devel >= 2.1.26-1zimbra8.7b3ZAPPEND
BuildRequires:      zimbra-libltdl-devel, zimbra-curl-devel, zimbra-heimdal-devel, zimbra-libxml2-devel
AutoReqProv:        no
URL:                http://www.openldap.org

%description
The Zimbra openldap build

%define debug_package %{nil}

%changelog
* Mon Dec 12 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
- Upgraded openldap to 2.5.13
* Wed Jul 07 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b5ZAPPEND
- Add fix for OpenLDAP ITS#9608
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b4ZAPPEND
- Upgraded openssl to 1.1.1h and updated cyrus-sasl
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b3ZAPPEND
- Upgraded openssl to 1.1.1g and updated cyrus-sasl
* Tue Jun 09 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b2ZAPPEND
- Fix for ZBUG-1441
* Mon Feb 10 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
- Update for OpenLDAP 2.4.49

%prep
%setup -n openldap-%{version}
%patch0 -p1
%patch1 -p1

%build
# Alternate Makeargs: DEFINES="-DCHECK_CSN -DSLAP_SCHEMA_EXPOSE -DMDB_DEBUG=3"
LDFLAGS="-L/opt/zimbra/common/lib -Wl,-rpath,/opt/zimbra/common/lib"; export LDFLAGS;
CFLAGS="-O0 -g -D_REENTRANT"; export CFLAGS;
CPPFLAGS="-I/opt/zimbra/common/include"; export CPPFLAGS;
PATH=/opt/zimbra/common/bin:$PATH; export PATH;
./configure --prefix=/opt/zimbra/common \
  --with-cyrus-sasl \
  --with-tls=openssl \
  --enable-dynamic \
  --enable-slapd \
  --enable-modules \
  --enable-backends=mod \
    --disable-sql \
    --disable-ndb \
    --disable-perl \
    --disable-wt \
  --enable-overlays=mod \
  --enable-debug \
  --enable-spasswd \
  --localstatedir=/opt/zimbra/data/ldap/state \
  --enable-crypt
LD_RUN_PATH=/opt/zimbra/common/lib make depend
LD_RUN_PATH=/opt/zimbra/common/lib make DEFINES="-DCHECK_CSN -DSLAP_SCHEMA_EXPOSE"
make -C libraries/liblmdb prefix=/opt/zimbra/common
make -C contrib/slapd-modules/noopsrch prefix=/opt/zimbra/common
make -C contrib/slapd-modules/passwd/sha2 prefix=/opt/zimbra/common

%install
make install DESTDIR=${RPM_BUILD_ROOT} STRIP=""
make -C libraries/liblmdb install prefix=/opt/zimbra/common DESTDIR=${RPM_BUILD_ROOT} STRIP=""
make -C contrib/slapd-modules/noopsrch install prefix=/opt/zimbra/common DESTDIR=${RPM_BUILD_ROOT} STRIP=""
make -C contrib/slapd-modules/passwd/sha2 install prefix=/opt/zimbra/common DESTDIR=${RPM_BUILD_ROOT} STRIP=""
rm -rf ${RPM_BUILD_ROOT}/opt/zimbra/data
rm -f ${RPM_BUILD_ROOT}/opt/zimbra/common/libexec/openldap/noopsrch.a
rm -f ${RPM_BUILD_ROOT}/opt/zimbra/common/libexec/openldap/pw-sha2.a
rm -f ${RPM_BUILD_ROOT}/opt/zimbra/common/etc/openldap/DB_CONFIG.example
rm -f ${RPM_BUILD_ROOT}/opt/zimbra/common/lib/pkgconfig/lber.pc
rm -f ${RPM_BUILD_ROOT}/opt/zimbra/common/lib/pkgconfig/ldap.pc
chmod 755 ${RPM_BUILD_ROOT}/opt/zimbra/common/libexec/openldap/pw-sha2.la ${RPM_BUILD_ROOT}/opt/zimbra/common/libexec/openldap/noopsrch.la
chmod 755 ${RPM_BUILD_ROOT}/opt/zimbra/common/lib/libldap* ${RPM_BUILD_ROOT}/opt/zimbra/common/lib/liblber*

%package libs
Summary:        openldap Libaries
Requires: zimbra-openssl-libs, zimbra-cyrus-sasl-libs, zimbra-base
AutoReqProv:        no

%description libs
The zimbra-openldap-libs package contains the openldap libraries

%package devel
Summary:        openldap Development
Requires: zimbra-openldap-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-openldap-devel package contains the linking libraries and include files

%package server
Summary:        openldap server binaries
Requires: zimbra-openldap-libs = %{version}-%{release}, zimbra-cyrus-sasl-libs
Requires: zimbra-libltdl-libs, zimbra-ldap-base
AutoReqProv:        no

%description server
The zimbra-openldap-server package contains slapd and its modules

%package client
Summary:        openldap client binaries
Requires: zimbra-openldap-libs = %{version}-%{release}, zimbra-cyrus-sasl-libs
AutoReqProv:        no

%description client
The zimbra-openldap-client package contains client tools such as ldapsearch

%package -n zimbra-lmdb
Summary:        LMDB binaries
Requires:       zimbra-ldap-base
AutoReqProv:        no

%description -n zimbra-lmdb
The zimbra-lmdb package contains the lmdb binary commands

%package -n zimbra-lmdb-libs
Summary:        LMDB libraries
Requires:       zimbra-base
AutoReqProv:        no

%description -n zimbra-lmdb-libs
The zimbra-lmdb-libs package contains the lmdb library

%package -n zimbra-lmdb-devel
Summary:        LMDB Development
Requires: zimbra-lmdb-libs = %{version}-%{release}
AutoReqProv:        no

%description -n zimbra-lmdb-devel
The zimbra-lmdb-devel package contains the linking libraries and include files

%files libs
%defattr(-,root,root)
/opt/zimbra/common/lib/*.so.*
%exclude /opt/zimbra/common/lib/liblmdb.so.0
%exclude /opt/zimbra/common/lib/liblmdb.so.0.0.0

%files devel
%defattr(-,root,root)
/opt/zimbra/common/include
/opt/zimbra/common/lib/*.a
/opt/zimbra/common/lib/*.la
/opt/zimbra/common/lib/*.so
%exclude /opt/zimbra/common/include/lmdb.h
%exclude /opt/zimbra/common/lib/liblmdb.a
%exclude /opt/zimbra/common/lib/liblmdb.so

%files server
%defattr(-,root,root)
/opt/zimbra/common/sbin
/opt/zimbra/common/etc
/opt/zimbra/common/libexec
/opt/zimbra/common/share/man
%attr(644, root, root) /opt/zimbra/common/etc/openldap/slapd.conf
%attr(644, root, root) /opt/zimbra/common/etc/openldap/slapd.conf.default
%attr(644, root, root) /opt/zimbra/common/etc/openldap/slapd.ldif
%attr(644, root, root) /opt/zimbra/common/etc/openldap/slapd.ldif.default
%exclude /opt/zimbra/common/etc/openldap/ldap.conf
%exclude /opt/zimbra/common/etc/openldap/ldap.conf.default
%exclude /opt/zimbra/common/share/man/man1
%exclude /opt/zimbra/common/share/man/man5/ldap.conf.5
%exclude /opt/zimbra/common/share/man/man5/ldif.5

%files client
%defattr(-,root,root)
/opt/zimbra/common/bin
/opt/zimbra/common/etc/openldap/ldap.conf
/opt/zimbra/common/etc/openldap/ldap.conf.default
/opt/zimbra/common/share/man/man1
/opt/zimbra/common/share/man/man5/ldap.conf.5
/opt/zimbra/common/share/man/man5/ldif.5
%exclude /opt/zimbra/common/bin/mdb_copy
%exclude /opt/zimbra/common/bin/mdb_dump
%exclude /opt/zimbra/common/bin/mdb_load
%exclude /opt/zimbra/common/bin/mdb_stat
%exclude /opt/zimbra/common/share/man/man1/mdb_copy.1
%exclude /opt/zimbra/common/share/man/man1/mdb_dump.1
%exclude /opt/zimbra/common/share/man/man1/mdb_load.1
%exclude /opt/zimbra/common/share/man/man1/mdb_stat.1

%files -n zimbra-lmdb
%defattr(-,root,root)
/opt/zimbra/common/bin/mdb_copy
/opt/zimbra/common/bin/mdb_dump
/opt/zimbra/common/bin/mdb_load
/opt/zimbra/common/bin/mdb_stat
/opt/zimbra/common/share/man/man1/mdb_copy.1
/opt/zimbra/common/share/man/man1/mdb_dump.1
/opt/zimbra/common/share/man/man1/mdb_load.1
/opt/zimbra/common/share/man/man1/mdb_stat.1

%files -n zimbra-lmdb-libs
%defattr(-,root,root)
/opt/zimbra/common/lib/liblmdb.so.*

%files -n zimbra-lmdb-devel
%defattr(-,root,root)
/opt/zimbra/common/include/lmdb.h
/opt/zimbra/common/lib/liblmdb.a
/opt/zimbra/common/lib/liblmdb.so

%post -p /bin/bash -n zimbra-openldap-server
if [ -x /opt/zimbra/common/libexec/slapd ]; then
  setcap CAP_NET_BIND_SERVICE=+ep /opt/zimbra/common/libexec/slapd
fi
