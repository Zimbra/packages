Summary:            Zimbra components for dnscache package
Name:               zimbra-dnscache-components
Version:            1.0.5
Release:            1zimbra8.7b1ZAPPEND
License:            GPL-2
Requires:           zimbra-dnscache-base, zimbra-unbound >= 1.17.1-1zimbra8.8b1ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%changelog
* Tue Jun 13 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.5
- ZBUG-3355, Upgraded zimbra-unbound to 1.17.1
* Sat Aug 20 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.4
- Fix ZCS-11941, Updated zimbra-unbound
* Fri May 20 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.3
- Fix for ZBUG-2723,Updated zimbra-unbound
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.2
- Updated zimbra-unbound
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Updated zimbra-unbound

%description
Zimbra dnscache components pulls in all the packages used by
zimbra-dnscache

%files
