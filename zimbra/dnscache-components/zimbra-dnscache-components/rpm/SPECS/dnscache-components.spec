Summary:            Zimbra components for dnscache package
Name:               zimbra-dnscache-components
Version:            1.0.2
Release:            1zimbra8.7b1ZAPPEND
License:            GPL-2
Requires:           zimbra-dnscache-base, zimbra-unbound >= 1.11.0-1zimbra8.7b2ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%changelog
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.2
- Updated zimbra-unbound
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Updated zimbra-unbound

%description
Zimbra dnscache components pulls in all the packages used by
zimbra-dnscache

%files
