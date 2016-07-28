Summary:            Zimbra's openldap build
Name:               zimbra-openldap
Version:            VERSION
Release:            1zimbra8.8b8ZAPPEND
License:            BSD
Source:             %{name}-%{version}.tgz
Patch0:             ITS5037.patch
Patch1:             writers.patch
Patch2:             ITS7683.patch
Patch3:             ITS8054.patch
Patch4:             threadpool.patch
Patch5:             liblmdb-soname.patch
Patch6:             ITS7506.patch
Patch7:             ITS8413.patch
Patch8:             ITS8432.patch
BuildRequires:      zimbra-openssl-devel
BuildRequires:      zimbra-cyrus-sasl-devel
BuildRequires:      zimbra-libltdl-devel
AutoReqProv:        no
URL:                http://www.openldap.org

%description
The Zimbra openldap build

%changelog
* Thu Jul 29 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b8ZAPPEND
- Import fix from upstream for ITS#8448, ITS#8460, ITS#8462.
* Thu Jun 9 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b7ZAPPEND
- Finalized patch for ITS#8432
* Thu Jun 9 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b6ZAPPEND
- syncrepl patch for ITS#8432
* Thu Jun 9 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b5ZAPPEND
- syncprov patch for ITS#8432
* Thu Jun 9 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b4ZAPPEND
- Add debug logging for ITS#8432
* Wed Apr 27 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b3ZAPPEND
- Add patch for ITS#8413
* Thu Feb 11 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b2ZAPPEND
- Add patch for ITS#7506

%prep
%setup -n openldap-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
# Alternate Makeargs: DEFINES="-DCHECK_CSN -DSLAP_SCHEMA_EXPOSE -DMDB_DEBUG=3"
LDFLAGS="-LOZCL -Wl,-rpath,OZCL"; export LDFLAGS;
CFLAGS="-O0 -g -D_REENTRANT"; export CFLAGS;
CPPFLAGS="-IOZCI"; export CPPFLAGS;
PATH=OZCB:$PATH; export PATH;
./configure --prefix=OZC \
  --with-cyrus-sasl \
  --with-tls=openssl \
  --enable-dynamic \
  --enable-slapd \
  --enable-modules \
  --enable-backends=mod \
    --disable-shell \
    --disable-sql \
    --disable-bdb \
    --disable-hdb \
    --disable-ndb \
    --disable-perl \
  --enable-overlays=mod \
  --enable-debug \
  --enable-spasswd \
  --localstatedir=/opt/zimbra/data/ldap/state \
  --enable-crypt
LD_RUN_PATH=OZCL make depend
LD_RUN_PATH=OZCL make DEFINES="-DCHECK_CSN -DSLAP_SCHEMA_EXPOSE"
make -C libraries/liblmdb prefix=OZC
make -C contrib/slapd-modules/noopsrch prefix=OZC
make -C contrib/slapd-modules/passwd/sha2 prefix=OZC

%install
make install DESTDIR=${RPM_BUILD_ROOT} STRIP=""
make -C libraries/liblmdb install prefix=OZC DESTDIR=${RPM_BUILD_ROOT} STRIP=""
make -C contrib/slapd-modules/noopsrch install prefix=OZC DESTDIR=${RPM_BUILD_ROOT} STRIP=""
make -C contrib/slapd-modules/passwd/sha2 install prefix=OZC DESTDIR=${RPM_BUILD_ROOT} STRIP=""
rm -rf ${RPM_BUILD_ROOT}/opt/zimbra/data
rm -f ${RPM_BUILD_ROOT}OZCLE/openldap/noopsrch.a
rm -f ${RPM_BUILD_ROOT}OZCLE/openldap/pw-sha2.a
rm -f ${RPM_BUILD_ROOT}OZCE/openldap/DB_CONFIG.example
chmod 755 ${RPM_BUILD_ROOT}OZCLE/openldap/pw-sha2.la ${RPM_BUILD_ROOT}OZCLE/openldap/noopsrch.la
chmod 755 ${RPM_BUILD_ROOT}OZCL/libldap* ${RPM_BUILD_ROOT}OZCL/liblber*

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
OZCL/*.so.*
%exclude OZCL/liblmdb.so.0
%exclude OZCL/liblmdb.so.0.0.0

%files devel
%defattr(-,root,root)
OZCI
OZCL/*.a
OZCL/*.la
OZCL/*.so
%exclude OZCI/lmdb.h
%exclude OZCL/liblmdb.a
%exclude OZCL/liblmdb.so

%files server
%defattr(-,root,root)
/opt/zimbra/common/sbin
OZCE
OZCLE
OZCS/man
%exclude OZCE/openldap/ldap.conf
%exclude OZCE/openldap/ldap.conf.default
%exclude OZCS/man/man1
%exclude OZCS/man/man5/ldap.conf.5
%exclude OZCS/man/man5/ldif.5

%files client
%defattr(-,root,root)
OZCB
OZCE/openldap/ldap.conf
OZCE/openldap/ldap.conf.default
OZCS/man/man1
OZCS/man/man5/ldap.conf.5
OZCS/man/man5/ldif.5
%exclude OZCB/mdb_copy
%exclude OZCB/mdb_dump
%exclude OZCB/mdb_load
%exclude OZCB/mdb_stat
%exclude OZCS/man/man1/mdb_copy.1
%exclude OZCS/man/man1/mdb_dump.1
%exclude OZCS/man/man1/mdb_load.1
%exclude OZCS/man/man1/mdb_stat.1

%files -n zimbra-lmdb
%defattr(-,root,root)
OZCB/mdb_copy
OZCB/mdb_dump
OZCB/mdb_load
OZCB/mdb_stat
OZCS/man/man1/mdb_copy.1
OZCS/man/man1/mdb_dump.1
OZCS/man/man1/mdb_load.1
OZCS/man/man1/mdb_stat.1

%files -n zimbra-lmdb-libs
%defattr(-,root,root)
OZCL/liblmdb.so.*

%files -n zimbra-lmdb-devel
%defattr(-,root,root)
OZCI/lmdb.h
OZCL/liblmdb.a
OZCL/liblmdb.so
