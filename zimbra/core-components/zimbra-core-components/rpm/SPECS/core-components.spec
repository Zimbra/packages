Summary:            Zimbra components for core package
Name:               zimbra-core-components
Version:            2.0.6
Release:            1zimbra8.8b1ZAPPEND
License:            GPL-2
Requires:           zimbra-base, zimbra-os-requirements, zimbra-perl >= 1.0.6-1zimbra8.7b1ZAPPEND
Requires:           zimbra-pflogsumm >= 1.1.5-1zimbra8.7b2ZAPPEND
Requires:           zimbra-openssl >= 1.1.1h-1zimbra8.7b3ZAPPEND, zimbra-curl >= 7.49.1-1zimbra8.7b3ZAPPEND
Requires:           zimbra-cyrus-sasl >= 2.1.26-1zimbra8.7b3ZAPPEND, zimbra-rsync
Requires:           zimbra-mariadb-libs >= 10.1.25-1zimbra8.7b3ZAPPEND
Requires:           zimbra-openldap-client >= 2.4.49-1zimbra8.8b4ZAPPEND, zimbra-osl >= 1.0.9-1zimbra8.7b1ZAPPEND
Requires:           zimbra-prepflog >= 0.4.1-1zimbra8.7b2ZAPPEND, zimbra-tcmalloc-libs
Requires:           zimbra-perl-innotop >= 1.9.1-1zimbra8.7b4ZAPPEND
Requires:           zimbra-openjdk >= 13.0.1-1zimbra8.8b1ZAPPEND, zimbra-openjdk-cacerts, zimbra-amavis-logwatch
Requires:           zimbra-postfix-logwatch, zimbra-rrdtool
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%changelog
* Sun Dec 06 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.6
- Updated openssl,curl,perl,perl-innotop,cyrus-sasl,mariadb,openldap
* Thu Sep 10 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.5
- Updated openssl,curl,perl,perl-innotop,cyrus-sasl,mariadb,openldap
* Tue Apr 28 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.4
- Updated zimbra-perl,zimbra-pflogsumm,zimbra-prepflog and zimbra-perl-innotop
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
