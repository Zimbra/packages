Summary:            Zimbra components for core package
Name:               zimbra-core-components
Version:            10.1.0
Release:            1zimbra10.0b1ZAPPEND
License:            GPL-2
Requires:           zimbra-base, zimbra-os-requirements >= 1.0.3-1zimbra8.7b1ZAPPEND, zimbra-perl >= 1.0.9-1zimbra8.7b1ZAPPEND
Requires:           zimbra-pflogsumm
Requires:           zimbra-openssl >= 3.0.9-1zimbra8.8b1ZAPPEND,zimbra-curl >= 7.49.1-1zimbra8.7b4ZAPPEND
Requires:           zimbra-cyrus-sasl >= 2.1.28-1zimbra8.7b4ZAPPEND
Requires:           zimbra-rsync
Requires:           zimbra-mariadb-libs >= 10.1.25-1zimbra8.7b3ZAPPEND, zimbra-openldap-client >= 2.5.17-1zimbra10.0b1ZAPPEND
Requires:           zimbra-osl >= 3.0.0-1zimbra10.0b1ZAPPEND
Requires:           zimbra-prepflog, zimbra-tcmalloc-libs, zimbra-perl-innotop >= 1.9.1-1zimbra8.7b4ZAPPEND
Requires:           zimbra-openjdk >= 17.0.12-1zimbra8.8b1ZAPPEND, zimbra-openjdk-cacerts >= 1.0.11-1zimbra8.7b1ZAPPEND
Requires:           zimbra-amavis-logwatch
Requires:           zimbra-postfix-logwatch >= 1.40.03-1zimbra8.7b1ZAPPEND, zimbra-rrdtool
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%changelog
* Mon Jul 22 2024 Zimbra Packaging Services <packaging-devel@zimbra.com> - 10.1.0
- Bumped-up version to differentiate from ZCS 10
* Mon Jul 22 2024 Zimbra Packaging Services <packaging-devel@zimbra.com> - 4.0.4
- Upgrade Openjdk to 17.0.12
* Mon Mar 04 2024 Zimbra Packaging Services <packaging-devel@zimbra.com> - 4.0.3
- Updated openldap, perl
* Wed Nov 29 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 4.0.2
- ZBUG-3696, Updated core-components for openjdk, openjdk-cacerts
* Mon Jul 17 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 4.0.1
- ZBUG-2931, Updated os-requirements
* Fri Jul 07 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 4.0.0
- ZBUG-3355, Updated OpenSSL License and other 3rd party open source licenses
* Tue Jun 13 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.19
- ZBUG-3355, Upgraded OpenSSL to 3.0.9 and Updated core-components to 3.0.19
* Fri Feb 10 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.18
- Fix ZBUG-3278, upgraded OpenSSL to 1.1.1t and updated core-components to 3.0.18
* Tue Feb 07 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.17
- Upgraded Date-Manip to 6.90, Updated core-components to 3.0.17
* Thu Jan 19 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.16
- Upgraded Compress::Raw::Zlib to 2.103, Updated core-components to 3.0.16
* Mon Sep 12 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.15
- Fix ZBUG-3017, Updated core-components to 3.0.15
* Mon Jul 11 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.14
- Fix for ZCS-11689, Upgraded OpenSSL to 1.1.1q
* Thu Jul 07 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.13
- ZBUG-2676, Upgraded Cyrus SASL to 2.1.28
* Fri Jun 03 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.12
- ZCS-11116, Upgraded JDK to 17.0.2
* Fri May 20 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.11
- Fix for ZBUG-2713, Upgraded OpenSSL to 1.1.1n
* Thu Sep 30 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.10
- Fix for ZBUG-2389, Upgraded OpenSSL to 1.1.1l
* Thu Sep 02 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.9
- Updated openjdk-cacerts to 1.0.8 and updated openldap
* Thu Sep 02 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.8
- Updated openjdk-cacerts, fix ZBUG-2400
* Tue Aug 24 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.7
- Updated openjdk-cacerts
* Tue Aug 17 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.6
- Upgraded openldap to 2.4.59
* Thu Apr 15 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.5
- Updated openssl to 1.1.1k
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 3.0.4
- Updated openssl
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.8
- Updated openssl
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.7
- Updated zimbra-postfix-logwatch to 1.40.03
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.6
- Updated openssl,curl,perl,perl-innotop,cyrus-sasl,mariadb
* Thu Sep 10 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.5
- Updated openssl,curl,perl,perl-innotop,cyrus-sasl,mariadb
* Tue Apr 07 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.3
- Update zimbra osl
* Tue Mar 31 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.2
* Wed Dec 11 2019  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.1
* Wed Mar 20 2019  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.0
- Initial Release

%description
Zimbra core components pulls in all the packages used by
zimbra-core

%files
