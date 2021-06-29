Summary:            Zimbra components for ldap package
Name:               zimbra-ldap-components
Version:            1.0.8
Release:            ITERATIONZAPPEND
License:            GPL-2
Requires:           zimbra-ldap-base, zimbra-lmdb >= 2.4.49-1zimbra8.8b4ZAPPEND
Requires:           zimbra-openldap-server >= 2.4.49-1zimbra8.8b4ZAPPEND
Requires:           zimbra-openssl >= 1.1.1h-1zimbra8.7b4ZAPPEND, zimbra-openssl-libs >= 1.1.1h-1zimbra8.7b4ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra ldap components pulls in all the packages used by
zimbra-ldap

%changelog
* Fri Apr 02 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.8
- Updated openssl
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.7
- Updated openldap with openssl 1.1.h
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.6
- Updated openldap with openssl 1.1.h
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.5
- Updated openldap with openssl 1.1.1g
* Tue Jun 09 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.4
- Fixed ZBUG-1441 in openldap
* Tue Mar 17 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.3
- Updated openldap to 2.4.49
* Tue Sep 18 2018  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.2
- Updated Updated openldap 2.4.47
* Wed Jul 25 2018  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Updated Updated openldap 2.4.46
* Wed Sep 09 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.0
- Initial Release

%files
