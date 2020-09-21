Summary:            Zimbra components for snmp package
Name:               zimbra-snmp-components
Version:            1.0.2
Release:            ITERATIONZAPPEND
License:            GPL-2
Requires:           zimbra-snmp-base, zimbra-net-snmp >= 5.8-1zimbra8.7b2ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra snmp components pulls in all the packages used by
zimbra-snmp

%changelog
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.2
- Updated zimbra-net-snmp
* Sat Apr 25 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Updated zimbra-net-snmp

%files
