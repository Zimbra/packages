Summary:            Zimbra's MariaDB build
Name:               zimbra-mariadb
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            GPLv2
Source:             %{name}-%{version}.tar.gz
BuildRequires:      libaio-devel
BuildRequires:      ncurses-devel
BuildRequires:      zimbra-openssl-devel
Requires:           libaio, zimbra-openssl-libs, zimbra-base
Requires:           zimbra-mariadb-libs = %{version}-%{release}, ncurses-libs, perl
AutoReqProv:        no
URL:                https://www.mariadb.org/

%description
The Zimbra MariaDB build for SQL database storage

%prep
%setup -n mariadb-%{version}

%define debug_package %{nil}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O3 -fno-omit-frame-pointer -pipe -Wall -Wno-uninitialized -DNDEBUG"; export CFLAGS; \
/usr/bin/cmake . \
  -DBUILD_TYPE=mysql_release \
  -DPLUGIN_AUTH_PAM=NO \
  -DPLUGIN_AUTH_PAM_V1=NO \
  -DCOMPILATION_COMMENT="Zimbra MariaDB binary distribution" \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=FALSE  \
  -DCMAKE_INSTALL_PREFIX="OZC" \
  -DCMAKE_INSTALL_RPATH="OZCL" \
  -DCMAKE_PREFIX_PATH="OZC" \
  -DCMAKE_SKIP_BUILD_RPATH=FALSE \
  -DINSTALL_SYSCONFDIR=/opt/zimbra/conf \
  -DINSTALL_MANDIR=share/man \
  -DWITH_EMBEDDED_SERVER=OFF \
  -DWITH_FAST_MUTEXES=ON \
  -DWITH_JEMALLOC=no \
  -DWITH_SAFEMALLOC=OFF \
  -DWITH_SSL=yes \
  -DPLUGIN_ARCHIVE=NO \
  -DPLUGIN_ARIA=NO \
  -DPLUGIN_BLACKHOLE=NO \
  -DPLUGIN_CONNECT=NO \
  -DPLUGIN_EXAMPLE=NO \
  -DPLUGIN_FEDERATED=NO \
  -DPLUGIN_FEDERATEDX=NO \
  -DPLUGIN_MROONGA=NO \
  -DPLUGIN_SPHINX=NO \
  -DPLUGIN_SPIDER=NO \
  -DPLUGIN_TOKUDB=NO \
  -DINSTALL_DOCDIR=share/mysql/docs \
  -DINSTALL_DOCREADMEDIR=share/mysql/docs \
  -DINSTALL_INFODIR=share/mysql/docs \
  -DINSTALL_MYSQLSHAREDIR=share/mysql \
  -DINSTALL_SHAREDIR=share/mysql \
  -DINSTALL_SBINDIR=sbin \
  -DINSTALL_SCRIPTDIR=share/mysql/scripts \
  -DINSTALL_UNIX_ADDRDIR=/opt/zimbra/data/tmp/mysqldata/mysql.sock
make depend
make all

%install
make DESTDIR=${RPM_BUILD_ROOT} install
rm -rf ${RPM_BUILD_ROOT}/opt/zimbra/conf
rm -rf ${RPM_BUILD_ROOT}OZC/data
rm -rf ${RPM_BUILD_ROOT}OZC/mysql-test
rm -rf ${RPM_BUILD_ROOT}OZC/sql-bench
rm -rf ${RPM_BUILD_ROOT}OZC/support-files
rm -f ${RPM_BUILD_ROOT}OZC/sbin/rcmysql
rm -f ${RPM_BUILD_ROOT}OZCL/libmysqlclient_r.so.18
rm -f ${RPM_BUILD_ROOT}OZCL/libmysqlclient_r.so.18.0.0
cd ${RPM_BUILD_ROOT}OZCL && \
ln -s libmysqlclient.so.18.0.0 libmysqlclient_r.so.18.0.0 && \
ln -s libmysqlclient.so.18 libmysqlclient_r.so.18

%package libs
Summary:        MariaDB Libaries
Requires: libaio, zimbra-openssl-libs, zimbra-base
AutoReqProv:        no

%description libs
The zimbra-mariadb-libs package contains the mariadb libraries

%package devel
Summary:        MariaDB Development
Requires: zimbra-mariadb-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-mariadb-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
OZC/sbin
OZCS
%exclude OZCB/mysql_config
%exclude OZCS/man/man1/mysql_config.1

%files libs
%defattr(-,root,root)
OZCL/*.so.*
OZCL/plugin
OZCL/pkgconfig/libmariadb.pc
OZCL/pkgconfig/mariadb.pc

%files devel
%defattr(-,root,root)
OZCB/mysql_config
OZCL/*.a
OZCL/*.so
OZCI
OZCS/man/man1/mysql_config.1

%changelog
* Thu Sep 17 2020 Zimbra Packaging Services <packaging-devel@zimbra.com>
- Upgraded dependency openssl to 1.1.1g
* Wed May 20 2015 Zimbra Packaging Services <packaging-devel@zimbra.com>
- initial packaging
