Summary:            Zimbra's RabbitMQ server
Name:               zimbra-rabbitmq-server
Version:            VERSION
Release:            1zimbra8.8b1ZAPPEND
License:            MPLv2.0 and MIT and ASL 2.0 and BSD
Source:             %{name}-%{version}.tar.xz
Source1:            rabbitmq-env.conf
Patch0:             rabbitmq-script-wrapper.patch
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
AutoReqProv:        no
URL:                https://github.com/rabbitmq/rabbitmq-server
BuildRequires:      zimbra-erlang >= 25.0.3-1zimbra8.8b1ZAPPEND
BuildRequires:      zimbra-openssl-devel >= 1.1.1q-1zimbra8.7b4ZAPPEND, zimbra-openssl-libs >= 1.1.1q-1zimbra8.7b4ZAPPEND
BuildRequires:      gzip, sed, zip, rsync
Requires:           zimbra-erlang >= 25.0.3-1zimbra8.8b1ZAPPEND


%description
The Zimbra's RabbitMQ server

%define _rabbit_erllibdir OZCL/rabbitmq/lib/rabbitmq_server-%{version}
%define debug_package %{nil}

%changelog
* Mon Aug 08 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
- Initial Release.

%prep
%setup -n rabbitmq-server-%{version}
%patch0 -p1

%build
env -u DEPS_DIR make dist manpages

%install
rm -rf %{buildroot}
env -u DEPS_DIR make install install-bin install-man DESTDIR=${RPM_BUILD_ROOT} PREFIX=/opt/zimbra RMQ_ROOTDIR="OZCL/rabbitmq" RMQ_ERLAPP_DIR=%{_rabbit_erllibdir} MANDIR="OZCS/man"
rm -rf %{buildroot}%{_rabbit_erllibdir}/LICENSE*
rm -rf %{buildroot}%{_rabbit_erllibdir}/INSTALL
rm -rf %{buildroot}%{_rabbit_erllibdir}/plugins/README
mkdir -p %{buildroot}/opt/zimbra/common/sbin/
mkdir -p %{buildroot}/opt/zimbra/conf
cp -a scripts/rabbitmq-script-wrapper %{buildroot}/opt/zimbra/common/sbin/rabbitmqctl
chmod 0755 %{buildroot}/opt/zimbra/common/sbin/rabbitmqctl
for script in rabbitmq-server rabbitmq-plugins rabbitmq-diagnostics rabbitmq-queues rabbitmq-upgrade rabbitmq-streams; do \
	cp -a %{buildroot}/opt/zimbra/common/sbin/rabbitmqctl \
	 %{buildroot}/opt/zimbra/common/sbin/$script; \
done
cp -a %{SOURCE1} %{buildroot}/opt/zimbra/conf/rabbitmq-env.conf

%files
%defattr(-,root,root)
OZCL/rabbitmq
OZC/sbin
OZCS
/opt/zimbra/conf/rabbitmq-env.conf

%post -p /bin/bash
mkdir -p /opt/zimbra/data/rabbitmq/mnesia
/bin/chown -R zimbra:zimbra /opt/zimbra/common/lib/rabbitmq
/bin/chown -R zimbra:zimbra /opt/zimbra/data/rabbitmq
if [ -f /opt/zimbra/conf/rabbitmq-env.conf ]; then
   /bin/chown zimbra:zimbra /opt/zimbra/conf/rabbitmq-env.conf
fi
