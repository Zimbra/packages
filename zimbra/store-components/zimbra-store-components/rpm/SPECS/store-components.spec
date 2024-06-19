Summary:            Zimbra components for store package
Name:               zimbra-store-components
Version:            1.0.4
Release:            1zimbra8.7b1ZAPPEND
License:            GPL-2
Requires:           zimbra-store-base, zimbra-mariadb >= 11.4.2-1zimbra10.0b1ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra store components pulls in all the packages used by
zimbra-store

%changelog
* Fri Jun 14 2024 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.4
- Upgraded mariadb to 11.4.2
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.3
- Updated zimbra-mariadb package
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.2
- Updated zimbra-mariadb package
* Mon Jul 24 2017  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Updated zimbra-mariadb package
* Wed Sep 09 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.0
- Initial Release

%files
