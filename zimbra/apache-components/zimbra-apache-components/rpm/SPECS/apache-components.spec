Summary:            Zimbra components for apache package
Name:               zimbra-apache-components
Version:            2.0.3
Release:            1zimbra8.8b1ZAPPEND
License:            GPL-2
Requires:           zimbra-apache-base, zimbra-httpd >= 2.4.38-1zimbra8.7b3ZAPPEND, zimbra-php >= 7.3.1-1zimbra8.7b6ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra apache components pulls in all the packages used by
zimbra-apache

%changelog
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.3
- Updated zimbra-httpd and zimbra-php
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.2
- Updated zimbra-httpd
* Sat Apr 25 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.1
- Updated dependency zimbra-php
* Mon Mar 25 2019  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.0
- Updated PHP package.

%files
