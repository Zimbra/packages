Summary:            Zimbra's postfix-logwatch build
Name:               zimbra-postfix-logwatch
Version:            VERSION
Release:            1zimbra8.7b1ZAPPEND
License:            MIT
Source:             %{name}-%{version}.tgz
Patch0:             postfix-logwatch.patch
Requires:           zimbra-base
AutoReqProv:        no
URL:                http://www.logwatch.org/

%description
The Zimbra postfix-logwatch build

%define debug_package %{nil}

%changelog
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b1ZAPPEND
- Upgraded postfix-logwatch to 1.40.03

%prep
%setup -n postfix-logwatch-%{version}
%patch0 -p1

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
