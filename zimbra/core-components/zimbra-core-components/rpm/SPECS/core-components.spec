Summary:            Zimbra components for core package
Name:               zimbra-core-components
Version:            2.0.5
Release:            1zimbra8.8b1ZAPPEND
License:            GPL-2
Requires:           zimbra-base, zimbra-os-requirements, zimbra-perl >= 1.0.4-1zimbra8.7b1ZAPPEND, zimbra-pflogsumm
Requires:           zimbra-openssl >= 1.1.1g-1zimbra8.7b3ZAPPEND,zimbra-curl >= 7.49.1-1zimbra8.7b2ZAPPEND, zimbra-cyrus-sasl >= 2.1.26-1zimbra8.7b2ZAPPEND
Requires:           zimbra-rsync
Requires:           zimbra-mariadb-libs >= 10.1.25-1zimbra8.7b1ZAPPEND, zimbra-openldap-client >= 2.4.49-1zimbra8.8b3ZAPPEND
Requires:           zimbra-osl >= 1.0.9-1zimbra8.7b1ZAPPEND
Requires:           zimbra-prepflog, zimbra-tcmalloc-libs, zimbra-perl-innotop >= 1.9.1-1zimbra8.7b2ZAPPEND
Requires:           zimbra-openjdk >= 13.0.1-1zimbra8.8b1ZAPPEND, zimbra-openjdk-cacerts, zimbra-amavis-logwatch
Requires:           zimbra-postfix-logwatch, zimbra-rrdtool
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%changelog
* Thu Sep 10 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.5
- Updated openssl,curl,perl,perl-innotop,cyrus-sasl
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
