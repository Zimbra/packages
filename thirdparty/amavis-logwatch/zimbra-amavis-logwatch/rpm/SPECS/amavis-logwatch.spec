Summary:            Zimbra's amavis-logwatch build
Name:               zimbra-amavis-logwatch
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            MIT
Source:             %{name}-%{version}.tgz
Requires:           zimbra-base
AutoReqProv:        no
URL:                http://www.logwatch.org/

%description
The Zimbra amavis-logwatch build

%define debug_package %{nil}

%prep
%setup -n amavis-logwatch-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
make

%install
mkdir -p ${RPM_BUILD_ROOT}OZCB
mkdir -p ${RPM_BUILD_ROOT}OZCE
mkdir -p ${RPM_BUILD_ROOT}OZCS/man/man1
cp -f amavis-logwatch ${RPM_BUILD_ROOT}OZCB
cp -f amavis-logwatch.conf ${RPM_BUILD_ROOT}OZCE
cp -f amavis-logwatch.1 ${RPM_BUILD_ROOT}OZCS/man/man1
sed -i -e 's|/usr/local/etc|OZCE|' ${RPM_BUILD_ROOT}OZCB/amavis-logwatch
sed -i -e 's|/usr/local/etc|OZCE|' -e 's|/usr/local/bin|OZCB|' ${RPM_BUILD_ROOT}OZCS/man/man1/amavis-logwatch.1
chmod 755 ${RPM_BUILD_ROOT}OZCB/amavis-logwatch

%files
%defattr(-,root,root)
OZCB
OZCE
OZCS
