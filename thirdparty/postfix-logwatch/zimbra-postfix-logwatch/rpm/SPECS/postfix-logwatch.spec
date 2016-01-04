Summary:            Zimbra's postfix-logwatch build
Name:               zimbra-postfix-logwatch
Version:            1.40.01
Release:            1zimbra9.0b1
License:            MIT
Source:             %{name}-%{version}.tgz
Requires:           zimbra-base
AutoReqProv:        no
URL:                http://www.logwatch.org/

%description
The Zimbra postfix-logwatch build

%define debug_package %{nil}

%prep
%setup -n postfix-logwatch-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
make

%install
mkdir -p ${RPM_BUILD_ROOT}OZCB
mkdir -p ${RPM_BUILD_ROOT}OZCE
mkdir -p ${RPM_BUILD_ROOT}OZCS/man/man1
make install DESTDIR=${RPM_BUILD_ROOT}
cp -f postfix-logwatch ${RPM_BUILD_ROOT}OZCB
cp -f postfix-logwatch.conf ${RPM_BUILD_ROOT}OZCE
cp -f postfix-logwatch.1 ${RPM_BUILD_ROOT}OZCS/man/man1
sed -i -e 's|/usr/local/etc|OZCE|' ${RPM_BUILD_ROOT}OZCB/postfix-logwatch
sed -i -e 's|/usr/local/etc|OZCE|' -e 's|/usr/local/bin|OZCB|' ${RPM_BUILD_ROOT}OZCS/man/man1/postfix-logwatch.1
chmod 755 ${RPM_BUILD_ROOT}OZCB/postfix-logwatch

%files
%defattr(-,root,root)
OZCB
OZCE
OZCS
