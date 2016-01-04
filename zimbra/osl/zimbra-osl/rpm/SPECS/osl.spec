Summary:            Opensource Licenses
Name:               zimbra-osl
Version:            1.0.0
Release:            ITERATIONZAPPEND
License:            GPL-2
Requires:           zimbra-base
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
This file contains the licenses for the open source 3rd party
software used by Zimbra

%install
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/docs
cp ../../open_source_licenses.txt ${RPM_BUILD_ROOT}/opt/zimbra/docs

%files
/opt/zimbra/docs/open_source_licenses.txt
