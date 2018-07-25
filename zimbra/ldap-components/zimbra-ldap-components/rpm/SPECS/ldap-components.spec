Summary:            Zimbra components for ldap package
Name:               zimbra-ldap-components
Version:            1.0.1
Release:            ITERATIONZAPPEND
License:            GPL-2
Requires:           zimbra-ldap-base, zimbra-lmdb (>= 2.4.46-1zimbra8.7b2ZAPPEND), zimbra-openldap-server (>= 2.4.46-1zimbra8.7b2ZAPPEND)
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra ldap components pulls in all the packages used by
zimbra-ldap

%changelog
* Wen Jul 25 2018  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Updated Updated openldap 2.4.46
* Wed Sep 09 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.0
- Initial Release

%files
