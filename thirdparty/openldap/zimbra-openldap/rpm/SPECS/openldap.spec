Summary:            Zimbra's openldap build
Name:               zimbra-openldap
Version:            VERSION
Release:            1zimbra8.7b3ZAPPEND
License:            BSD
Source:             %{name}-%{version}.tgz
Patch0:             ITS5037.patch
Patch1:             writers.patch
Patch2:             ITS7683.patch
Patch3:             ITS8054.patch
Patch4:             ITS8843.patch
Patch5:             liblmdb-soname.patch
Patch6:             multival.patch
Patch7:             liblmdb-keysize.patch
Patch8:             index-delete.patch
BuildRequires:      zimbra-openssl-devel
BuildRequires:      zimbra-cyrus-sasl-devel
BuildRequires:      zimbra-libltdl-devel
AutoReqProv:        no
URL:                http://www.openldap.org

%description
The Zimbra openldap build

%changelog
* Fri Aug 31 2018  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Update multival for new syntax that allows the capability to work around LDMB 0.9 limitations
- Update liblmdb library to have a larger max keysize
* Wed Jul 18 2018  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Update multival patch to make sure a->a_numvals matches id2v counts
* Tue Apr 24 2018  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b1ZAPPEND
- Initial package for OpenLDAP 2.4.46
- Includes multival support
- Includes upstream fix for ITS#8843

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
chmod 755 ${RPM_BUILD_ROOT}/opt/zimbra/common/libexec/openldap/pw-sha2.la ${RPM_BUILD_ROOT}/opt/zimbra/common/libexec/openldap/noopsrch.la
chmod 755 ${RPM_BUILD_ROOT}/opt/zimbra/common/lib/libldap* ${RPM_BUILD_ROOT}/opt/zimbra/common/lib/liblber*

%package libs
Summary:        openldap Libaries
Requires:  zimbra-openssl-libs, zimbra-cyrus-sasl-libs, zimbra-base
AutoReqProv:        no

%description libs
The zimbra-openldap-libs package contains the openldap libraries

%package devel
Summary:        openldap Development
Requires:  zimbra-openldap-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-openldap-devel package contains the linking libraries and include files

%package server
Summary:        openldap server binaries
Requires:  zimbra-openldap-libs = %{version}-%{release}, zimbra-cyrus-sasl-libs
Requires:  zimbra-libltdl-libs, zimbra-ldap-base
AutoReqProv:        no

%description server
The zimbra-openldap-server package contains slapd and its modules

%package client
Summary:        openldap client binaries
Requires:  zimbra-openldap-libs = %{version}-%{release}, zimbra-cyrus-sasl-libs
AutoReqProv:        no

%description client
The zimbra-openldap-client package contains client tools such as ldapsearch

%package -n zimbra-lmdb
Summary:        LMDB binaries
Requires:        zimbra-ldap-base
AutoReqProv:        no

%description -n zimbra-lmdb
The zimbra-lmdb package contains the lmdb binary commands

%package -n zimbra-lmdb-libs
Summary:        LMDB libraries
Requires:        zimbra-base
AutoReqProv:        no

%description -n zimbra-lmdb-libs
The zimbra-lmdb-libs package contains the lmdb library

%package -n zimbra-lmdb-devel
Summary:        LMDB Development
Requires:  zimbra-lmdb-libs = %{version}-%{release}
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
