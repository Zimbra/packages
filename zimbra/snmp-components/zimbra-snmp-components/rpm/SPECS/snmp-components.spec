Summary:            Zimbra components for snmp package
Name:               zimbra-snmp-components
Version:            1.0.4
Release:            1zimbra8.7b1ZAPPEND
License:            GPL-2
Requires:           zimbra-snmp-base, zimbra-net-snmp >= 5.8-1zimbra8.7b3ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%changelog
* Tue Jun 13 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.4
- Updated zimbra-net-snmp
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.3
- Updated zimbra-net-snmp
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.2
- Updated zimbra-net-snmp

%description
Zimbra snmp components pulls in all the packages used by
zimbra-snmp

%files
