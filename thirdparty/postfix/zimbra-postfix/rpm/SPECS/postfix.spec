Summary:            Zimbra's Postfix build
Name:               zimbra-postfix
Version:            VERSION
Release:            1zimbra8.7b6ZAPPEND
License:            IPL-1.0
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zimbra-openldap-devel >= 2.5.17-1zimbra10.0b1ZAPPEND
BuildRequires:      zimbra-cyrus-sasl-devel >= 2.1.28-1zimbra8.7b4ZAPPEND
BuildRequires:      zimbra-openssl-devel >= 3.0.9-1zimbra8.8b1ZAPPEND
BuildRequires:      zimbra-mariadb-devel
BuildRequires:      zimbra-lmdb-devel >= 2.5.17-1zimbra10.0b1ZAPPEND
BuildRequires:      pcre-devel, libicu-devel
Requires:           pcre, libicu
Requires:           zimbra-openldap-libs >= 2.5.17-1zimbra10.0b1ZAPPEND, zimbra-mta-base
Requires:           zimbra-cyrus-sasl >= 2.1.28-1zimbra8.7b4ZAPPEND, zimbra-mariadb
Requires:           zimbra-lmdb-libs >= 2.5.17-1zimbra10.0b1ZAPPEND, zimbra-openssl-libs >= 3.0.9-1zimbra8.8b1ZAPPEND
Patch0:             postfix-main-cf-zimbra.patch
Patch1:             stop-warning.patch
Patch2:             postfix-ldap.patch
Patch3:             lmdb-default.patch
AutoReqProv:        no
URL:                https://www.postfix.org/

%description
The Zimbra Postfix build

%define debug_package %{nil}

%changelog
* Fri Sep 13 2024 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b6ZAPPEND
- Enable EAI support
* Sat May 11 2024 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b5ZAPPEND
- Updated postfix for openldap-2.5.17
* Fri Jan 26 2024 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Upgraded postfix to 3.6.14
* Mon Jun 12 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- ZBUG-3355, Upgraded OpenSSL to 3.0.9 and updated openldap, cyrus-sasl, lmdb
* Wed Jun 30 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Upgraded postfix to 3.6.1
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Updated openldap, cyrus-sasl, openssl, lmdb
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Upgraded postfix to 3.5.6

%prep
%setup -n postfix-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
#%patch4 -p1

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O0 -g"; export CFLAGS; \
make makefiles \
  OPT="-O2" \
  DEBUG="-g" \
  CCARGS='-DDEF_COMMAND_DIR=\"OZC/sbin\" \
  -DDEF_DAEMON_DIR=\"OZCLE\" \
  -DDEF_CONFIG_DIR=\"OZC/conf\" \
  -DDEF_QUEUE_DIR=\"/opt/zimbra/data/postfix/spool\" \
  -DDEF_SENDMAIL_PATH=\"OZC/sbin/sendmail\" \
  -DDEF_NEWALIAS_PATH=\"OZC/sbin/newaliases\" \
  -DDEF_MAILQ_PATH=\"OZC/sbin/mailq\" \
  -DDEF_MANPAGE_DIR=\"OZCS/man\" \
  -DDEF_HTML_DIR=\"no\" \
  -DDEF_README_DIR=\"no\" \
  -DDEF_DB_TYPE=\"lmdb\" \
  -DDEF_DATA_DIR=\"/opt/zimbra/data/postfix/data\" \
  -DUSE_SASL_AUTH -DUSE_CYRUS_SASL \
  -DHAS_LMDB -DNO_DB \
  -DHAS_LDAP -DHAS_MYSQL -DUSE_TLS -DHAS_PCRE -I/usr/include/pcre \
  -DUSE_LDAP_SASL \
  -IOZCI \
  -IOZCI/mysql \
  -IOZCI/sasl \
  -I/usr/include' \
  AUXLIBS='-LOZCL \
  -lpcre -lldap -llber -llmdb -lmysqlclient -lsasl2 -lssl -lcrypto \
  -L/usr/lib -lz -lm -lpthread'
LD_RUN_PATH=OZCL make

%install
make non-interactive-package install_root=${RPM_BUILD_ROOT}
sed  -e 's|postconf|OZC/sbin/postconf|' auxiliary/qshape/qshape.pl > ${RPM_BUILD_ROOT}OZC/sbin/qshape.pl
chmod a+rx ${RPM_BUILD_ROOT}OZC/sbin/qshape.pl
cd ${RPM_BUILD_ROOT}OZC/sbin
rm -f newaliases
rm -f mailq
ln -s sendmail mailq
ln -s sendmail newaliases
mkdir -p ${RPM_BUILD_ROOT}OZC/lib
cp -r /opt/zimbra/common/lib/libmariadb.so.3 ${RPM_BUILD_ROOT}OZC/lib/

%files
%defattr(-,root,root)
%attr(775, root, zimbra) OZC/conf
OZCLE
OZC/sbin
OZCS
OZC/lib

%post -p /bin/bash
/bin/chgrp postdrop /opt/zimbra/common/sbin/postdrop
/bin/chgrp postdrop /opt/zimbra/common/sbin/postqueue
/bin/chmod 2755 /opt/zimbra/common/sbin/postqueue
/bin/chmod 2755 /opt/zimbra/common/sbin/postdrop
/bin/chown -f zimbra:zimbra /opt/zimbra/common/conf/master.cf
/bin/chown -f zimbra:zimbra /opt/zimbra/common/conf/main.cf
if [ "$1" -ge "2" ]; then
 USER=$(whoami)
 if [ "$USER" = "zimbra" ]; then
    /opt/zimbra/libexec/configrewrite mta
 else
   su - zimbra -c "/opt/zimbra/libexec/configrewrite mta"
 fi
fi
