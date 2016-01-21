Summary:            Opensource Licenses
Name:               zimbra-osl
Version:            1.0.3
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

%changelog
* Mon Jan 11 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.3
- Update MariaDB to 10.1.10
- Update Selenium to 2.49.0
- Update jquery to 1.11.0
- Add converse.js 0.9.4
* Thu Jan 07 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.2
- Add oauth, guice
* Thu Dec 17 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Update for ZCS 8.7.0 release.

%install
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/docs
cp ../../open_source_licenses.txt ${RPM_BUILD_ROOT}/opt/zimbra/docs

%files
/opt/zimbra/docs/open_source_licenses.txt
