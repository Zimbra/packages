Summary:            Zimbra components for store package
Name:               zimbra-store-components
Version:            1.0.1
Release:            1zimbra8.7b1ZAPPEND
License:            GPL-2
Requires:           zimbra-store-base, zimbra-mariadb >= 10.1.25-1zimbra8.7b1ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra store components pulls in all the packages used by
zimbra-store

%changelog
* Mon Jul 24 2017  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Updated zimbra-mariadb package
* Wed Sep 09 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.0
- Initial Release

%files
