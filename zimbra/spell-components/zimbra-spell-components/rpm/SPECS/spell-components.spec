Summary:            Zimbra components for spell package
Name:               zimbra-spell-components
Version:            2.0.14
Release:            1zimbra8.8b1ZAPPEND
License:            GPL-2
Requires:           zimbra-spell-base, zimbra-aspell-ar, zimbra-aspell-ca, zimbra-aspell-da, zimbra-aspell-de
Requires:           zimbra-aspell-en, zimbra-aspell-es, zimbra-aspell-fr, zimbra-aspell-hi
Requires:           zimbra-aspell-hu, zimbra-aspell-it, zimbra-aspell-nl, zimbra-aspell-pl
Requires:           zimbra-aspell-pt-br, zimbra-aspell-ru, zimbra-aspell-sv, zimbra-httpd >= 2.4.62-1zimbra8.7b5ZAPPEND
Requires:           zimbra-php >= 8.3.0-1zimbra8.7b3ZAPPEND, zimbra-aspell-zimbra
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra spell components pulls in all the packages used by
zimbra-spell

%changelog
* Fri Aug 23 2024 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.14
- ZCS-15706, Upgraded Apache to 2.4.62
* Fri Dec 15 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.13
- Upgraded PHP to 8.3.0  (ZBUG-3082)
* Tue Jun 13 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.12
- Updated zimbra-httpd
* Mon Apr 17 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.11
- ZBUG-3354, Upgraded Apache to 2.4.57
* Wed Nov 23 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.10
- Fix ZBUG-3126
* Tue Oct 18 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.9
- Fix ZBUG-2819, Upgraded Apache to 2.4.54
* Tue Mar 15 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.8
- Fix ZCS-11149, Upgraded Apache to 2.4.53
* Mon Feb 14 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.7
- Fix ZBUG-2498, Update PHP to 7.4.27
* Tue Jan 24 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.6
- Fix ZBUG-2145, Added Catalan dictionary
* Tue Oct 19 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.5
- Fix ZBUG-2362, Upgraded Apache to 2.4.51
* Tue Mar 16 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.4
- Updated dependency zimbra-httpd and zimbra-php
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.3
- Updated dependency zimbra-httpd
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.2
- Updated dependency zimbra-httpd
* Mon Mar 25 2019  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.0
- Updated PHP package.

%files
