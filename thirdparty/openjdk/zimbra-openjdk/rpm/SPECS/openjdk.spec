Summary:            Zimbra's OpenJDK build
Name:               zimbra-openjdk
Version:            VERSION
Release:            1zimbra8.7b4ZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tgz
BuildRequires:      zip, libX11-devel, libXau-devel, libXext-devel, libXfixes-devel
BuildRequires:      libXtst-devel, libXi-devel, libxcb-devel, xorg-x11-proto-devel
BuildRequires:      libICE-devel, libSM-devel, libXt, libXt-devel, libXrender-devel
BuildRequires:      keyutils-libs-devel, krb5-devel, libcom_err-devel, libselinux-devel
BuildRequires:      libsepol-devel, openssl-devel, cups-devel, freetype-devel
BuildRequires:      alsa-lib-devel, java-1.7.0-openjdk-devel
Requires:           libX11, libXext, libXi, libXrender, libXtst, alsa-lib, freetype
Requires:           zimbra-base
AutoReqProv:        no
URL:                http://openjdk.java.net/

%description
The Zimbra OpenJDK build

%changelog
* Fri Jul 28 2016 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Update version to 1.8 update 144 build 01
* Mon Mar 28 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Update version to 1.8 update 77 build 03
* Thu Feb 11 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Fix cacerts handling to avoid conflicts

%prep
%setup -n openjdk-%{version}

%build
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC \
--enable-unlimited-crypto \
--with-update-version=JDK_UPDATE \
--with-build-number=JDK_BUILD \
--with-milestone=zimbra
make

%install
make install INSTALL_PREFIX=${RPM_BUILD_ROOT}
rm -rf ${RPM_BUILD_ROOT}/bin
mkdir -p ${RPM_BUILD_ROOT}OZCB
mkdir -p ${RPM_BUILD_ROOT}OZCL
mv ${RPM_BUILD_ROOT}/jvm ${RPM_BUILD_ROOT}OZCL/
cd ${RPM_BUILD_ROOT}OZCL/jvm
ln -s openjdk* java
rm -rf java/demo
rm -rf java/sample
rm -f java/jre/lib/security/cacerts
chmod 644 java/lib/ct.sym
cd java/jre/lib/security
ln -s OZCE/java/cacerts cacerts
cd ${RPM_BUILD_ROOT}OZCB
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
OZCB
OZCL
