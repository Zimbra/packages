Summary:            Zimbra components for snmp package
Name:               zimbra-snmp-components
Version:            1.0.1
Release:            ITERATIONZAPPEND
License:            GPL-2
Requires:           zimbra-snmp-base, zimbra-net-snmp >= 5.8-1zimbra8.7b1ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra snmp components pulls in all the packages used by
zimbra-snmp

%changelog
* Sat Apr 25 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Updated zimbra-net-snmp

%files
