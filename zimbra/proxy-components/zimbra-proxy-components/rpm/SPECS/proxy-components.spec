Summary:            Zimbra components for proxy package
Name:               zimbra-proxy-components
Version:            1.0.4
Release:            1zimbra8.8b1ZAPPEND
License:            GPL-2
Requires:           zimbra-proxy-base, zimbra-nginx >= 1.7.1-1zimbra8.8b1ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%changelog
* Tue Mar 17 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.4
- Updated zimbra-nginx package
* Tue Feb 12 2019  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.3
- Updated zimbra-nginx package
* Tue Sep 5 2018  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.2
- Updated zimbra-nginx package
* Tue Jul 18 2017  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Updated zimbra-nginx package
* Wed Sep 09 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.0
- Initial Release

%description
Zimbra proxy components pulls in all the packages used by
zimbra-proxy

%files
