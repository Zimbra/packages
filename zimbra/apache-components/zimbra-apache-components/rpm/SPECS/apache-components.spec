Summary:            Zimbra components for apache package
Name:               zimbra-apache-components
Version:            2.0.6
Release:            1zimbra8.8b1ZAPPEND 
License:            GPL-2
Requires:           zimbra-apache-base, zimbra-httpd >= 2.4.51-1zimbra8.7b3ZAPPEND, zimbra-php >= 7.3.25-1zimbra8.7b3ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra apache components pulls in all the packages used by
zimbra-apache

%changelog
* Mon 14 Feb 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.6
- Fix ZBUG-2498, Upgraded PHP to 7.4.27
* Tue Oct 19 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.5
- Fix ZBUG-2362, Upgraded Apache to 2.4.51
* Tue Mar 16 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.4
- Updated zimbra-httpd and zimbra-php
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.3
- Updated zimbra-httpd
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.2
- Updated zimbra-httpd
* Mon Mar 25 2019  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.0
- Updated PHP package.

%files
