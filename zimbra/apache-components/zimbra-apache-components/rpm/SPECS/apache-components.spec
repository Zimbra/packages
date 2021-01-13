Summary:            Zimbra components for apache package
Name:               zimbra-apache-components
Version:            2.0.1
Release:            1zimbra8.8b1ZAPPEND 
License:            GPL-2
Requires:           zimbra-apache-base, zimbra-httpd >= 2.4.46-1zimbra8.7b1ZAPPEND, zimbra-php >= 7.3.25-1zimbra8.7b3ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra apache components pulls in all the packages used by
zimbra-apache

%changelog
* Fri Jan 08 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.1
- Updated PHP to 7.3.25, Updated HTTPD to 2.4.46
* Mon Mar 25 2019  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.0
- Updated PHP package.

%files
