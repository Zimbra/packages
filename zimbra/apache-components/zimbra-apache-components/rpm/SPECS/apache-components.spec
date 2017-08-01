Summary:            Zimbra components for apache package
Name:               zimbra-apache-components
Version:            1.0.1
Release:            1zimbra8.7b1ZAPPEND 
License:            GPL-2
Requires:           zimbra-apache-base, zimbra-httpd, zimbra-php >= 5.6.31-1zimbra8.7b2ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra apache components pulls in all the packages used by
zimbra-apache

%changelog
* Fri Jul 28 2017  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Updated PHP package.
* Wed Sep 09 2015 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.0
- Inital release

%files
