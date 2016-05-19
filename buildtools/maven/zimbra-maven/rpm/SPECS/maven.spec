Summary:            Zimbra's maven build
Name:               zimbra-maven
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            Apache-2.0
Source:             %{name}-%{version}.tar.gz
AutoReqProv:        no
URL:                https://maven.apache.org/

%define debug_package %{nil}

%description
The Zimbra maven build

%prep
%setup -n apache-maven-%{version}

%build

%install
mkdir -p ${RPM_BUILD_ROOT}/OZCB
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/common/boot
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/common/conf
mkdir -p ${RPM_BUILD_ROOT}/OZCL
cp -f bin/* ${RPM_BUILD_ROOT}/OZCB
cp -f boot/* ${RPM_BUILD_ROOT}/opt/zimbra/common/boot
cp -rf conf/* ${RPM_BUILD_ROOT}/opt/zimbra/common/conf
cp -rf lib/* ${RPM_BUILD_ROOT}/OZCL

%files
%defattr(-,root,root)
OZCB
/opt/zimbra/common/boot
/opt/zimbra/common/conf
OZCL

