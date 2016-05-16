Summary:            Zimbra's ant build
Name:               zimbra-ant
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            Apache-2.0
Source:             %{name}-%{version}.tar.bz2
AutoReqProv:        no
URL:                https://ant.apache.org/

%define debug_package %{nil}

%description
The Zimbra ant build tool

%prep
%setup -n apache-ant-%{version}

%build

%install
mkdir -p ${RPM_BUILD_ROOT}OZCB
mkdir -p ${RPM_BUILD_ROOT}OZCL
mkdir -p ${RPM_BUILD_ROOT}OZCE
cp -f bin/* ${RPM_BUILD_ROOT}OZCB
cp -f lib/* ${RPM_BUILD_ROOT}OZCL
cp -rf etc/* ${RPM_BUILD_ROOT}OZCE

%files
%defattr(-,root,root)
OZCB
OZCL
OZCE
