Summary:            Zimbra's OpenJDK build
Name:               zimbra-openjdk
Version:            VERSION
Release:            1zimbra8.8b1ZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tgz
BuildRequires:      zip, libX11-devel, libXau-devel, libXext-devel, libXfixes-devel
Requires:           zimbra-base
AutoReqProv:        no
URL:                http://openjdk.java.net/

%description
The Zimbra OpenJDK build

%changelog
* Mon Jul 22 2024 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
-- Upgrade Openjdk to 17.0.12
* Tue Sep 05 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
-- Update version to 17.0.8
* Thu Feb 17 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
-- Update version to 17.0.2
* Sat Apr 25 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
-- Update version to 13
* Tue Mar 19 2019 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
-- Update version to 11 update 2 build 01
%prep

%build

%install
mkdir -p ${RPM_BUILD_ROOT}/jvm
tar -xvzf ${RPM_BUILD_ROOT}/../../../../openjdk*.tgz -C ${RPM_BUILD_ROOT}/jvm
rm -rf ${RPM_BUILD_ROOT}/bin
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/common/bin
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/common/lib
mv ${RPM_BUILD_ROOT}/jvm ${RPM_BUILD_ROOT}/opt/zimbra/common/lib/
cd ${RPM_BUILD_ROOT}/opt/zimbra/common/lib/jvm
ln -s openjdk* java
rm -rf java/demo
rm -rf java/sample
rm -f java/lib/security/cacerts
chmod 644 java/lib/ct.sym
cd java/lib/security
ln -s /opt/zimbra/common/etc/java/cacerts cacerts
cd ${RPM_BUILD_ROOT}/opt/zimbra/common/bin
ln -s ../lib/jvm/java/bin/jar
ln -s ../lib/jvm/java/bin/java
ln -s ../lib/jvm/java/bin/javac
ln -s ../lib/jvm/java/bin/javap
ln -s ../lib/jvm/java/bin/jhat
ln -s ../lib/jvm/java/bin/jmap
ln -s ../lib/jvm/java/bin/jps
ln -s ../lib/jvm/java/bin/jstack
ln -s ../lib/jvm/java/bin/jstat
ln -s ../lib/jvm/java/bin/keytool

%files
%defattr(-,root,root)
/opt/zimbra/common/bin
/opt/zimbra/common/lib
