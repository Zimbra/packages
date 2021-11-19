Summary:            Zimbra components for proxy package
Name:               zimbra-proxy-components
Version:            1.0.9
Release:            1zimbra8.8b1ZAPPEND
License:            GPL-2
Requires:           zimbra-proxy-base, zimbra-nginx >= 1.20.0-1zimbra8.8b2ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%changelog
* Sun Jul 25 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.9
- Updated zimbra-nginx to 1.20.0
* Thu Jan 21 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.8
- Updated zimbra-nginx
* Thu Jan 21 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.7
- Updated zimbra-nginx
* Sat Dec 05 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.6
- Updated zimbra-nginx package to 1.19.0
* Mon Oct 19 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.5
- Updated zimbra-nginx package
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
