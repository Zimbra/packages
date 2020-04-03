Summary:            Zimbra components for core package
Name:               zimbra-core-components
Version:            1.0.5
Release:            1zimbra8.8b1ZAPPEND
License:            GPL-2
Requires:           zimbra-base, zimbra-os-requirements, zimbra-perl, zimbra-pflogsumm
Requires:           zimbra-openssl >= 1.0.2l-1zimbra8.7b1ZAPPEND,zimbra-curl, zimbra-cyrus-sasl, zimbra-rsync
Requires:           zimbra-mariadb-libs >= 10.1.25-1zimbra8.7b1ZAPPEND, zimbra-openldap-client, zimbra-osl
Requires:           zimbra-prepflog, zimbra-tcmalloc-libs, zimbra-perl-innotop
Requires:           zimbra-openjdk >= 13.0.1-1zimbra8.8b1ZAPPEND, zimbra-openjdk-cacerts, zimbra-amavis-logwatch
Requires:           zimbra-postfix-logwatch, zimbra-rrdtool
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%changelog
* Wed Mar 18 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.5
- Updated zimbra-openjdk package 
* Fri May 18 2018 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.4
- Updated zimbra-openjdk package
* Fri Jul 28 2017 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.3
- Updated zimbra-openjdk package
* Fri Jul 28 2017 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.2
- Updated zimbra-openssl package
* Mon Jul 24 2017  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Updated zimbra-mariadb package
* Wed Sep 09 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.0
- Initial Release

%description
Zimbra core components pulls in all the packages used by
zimbra-core

%files
