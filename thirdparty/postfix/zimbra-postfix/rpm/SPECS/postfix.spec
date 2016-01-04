Summary:            Zimbra's Postfix build
Name:               zimbra-postfix
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            IPL-1.0
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zimbra-openldap-devel
BuildRequires:      zimbra-cyrus-sasl-devel
BuildRequires:      zimbra-openssl-devel
BuildRequires:      zimbra-mariadb-devel
BuildRequires:      zimbra-lmdb-devel
BuildRequires:      pcre-devel
Requires:           pcre
Requires:           zimbra-openldap-libs, zimbra-mta-base
Requires:           zimbra-cyrus-sasl, zimbra-mariadb
Requires:           zimbra-lmdb-libs, zimbra-openssl-libs
Patch0:             fallback.patch
Patch1:             postfix-main-cf-zimbra.patch
Patch2:             stop-warning.patch
Patch3:             postfix-ldap.patch
Patch4:             lmdb-default.patch
Patch5:             pass-ip-address.patch
AutoReqProv:        no
URL:                https://www.postfix.org/

%description
The Zimbra Postfix build

%prep
%setup -n postfix-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

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

%files
%defattr(-,root,root)
%attr(775, root, zimbra) OZC/conf
OZCLE
OZC/sbin
OZCS

%post -p /bin/bash
/bin/chgrp postdrop /opt/zimbra/common/sbin/postdrop
/bin/chgrp postdrop /opt/zimbra/common/sbin/postqueue
/bin/chmod 2755 /opt/zimbra/common/sbin/postqueue
/bin/chmod 2755 /opt/zimbra/common/sbin/postdrop
/bin/chown -f zimbra:zimbra /opt/zimbra/common/conf/master.cf
/bin/chown -f zimbra:zimbra /opt/zimbra/common/conf/main.cf
if [ "$1" -ge "2" ]; then
 /opt/zimbra/libexec/configrewrite mta
fi
