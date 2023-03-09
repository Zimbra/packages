Summary:            Zimbra components for ldap package
Name:               zimbra-ldap-components
Version:            2.0.12
Release:            ITERATIONZAPPEND
License:            GPL-2
Requires:           zimbra-ldap-base, zimbra-lmdb >= 2.4.59-1zimbra8.8b5ZAPPEND
Requires:           zimbra-openldap-server >= 2.4.59-1zimbra8.8b5ZAPPEND
Requires:           zimbra-openssl >= 1.1.1t-1zimbra8.7b4ZAPPEND, zimbra-openssl-libs >= 1.1.1t-1zimbra8.7b4ZAPPEND
Requires:           zimbra-core-components >= 3.0.18-1zimbra8.8b1ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra ldap components pulls in all the packages used by
zimbra-ldap

%changelog
* Fri Feb 10 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.12
- Fix ZBUG-3278, upgraded OpenSSL to 1.1.1t and updated core-components to 3.0.18
* Tue Feb 07 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.11
- Upgraded Date-Manip to 6.90, Updated core-components to 3.0.17
* Thu Jan 19 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.10
- Upgraded Compress::Raw::Zlib to 2.103, Updated core-components to 3.0.16
* Mon Sep 12 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.9
- Fix ZBUG-3017, Updated core-components to 3.0.15
* Mon Jul 11 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.8
- Fix for ZCS-11689, Upgraded OpenSSL to 1.1.1q and core-components to 3.0.14
* Thu Jul 07 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.7
- ZBUG-2676, Upgraded Cyrus SASL to 2.1.28 and core-components to 3.0.13
* Fri Jun 03 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.6
- ZCS-11116, Upgraded JDK to 17.0.2 and core-components to 3.0.12
* Fri May 20 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.5
- Updated openssl to 1.1.1n and core-components to 3.0.11
* Thu Sep 30 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.4
- Updated openssl to 1.1.1l and core-components to 3.0.10
* Thu Sep 02 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.3
- Updated openldap and core-components to 3.0.9
* Thu Sep 02 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.2
- Updated core-components to 3.0.8
* Tue Aug 24 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.1
- Added dependency core-components
* Tue Aug 24 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.13
- Updated openldap and core-components to 2.0.13
* Tue Aug 24 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.12
- Updated core-components to 2.0.12
* Tue Aug 24 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.11
- Added dependency core-components
* Tue Aug 17 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.10
- Upgraded openldap to 2.4.59
* Thu Apr 15 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.9
- Updated openssl to 1.1.1k
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
