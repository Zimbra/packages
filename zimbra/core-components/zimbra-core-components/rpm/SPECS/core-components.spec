Summary:            Zimbra components for core package
Name:               zimbra-core-components
Version:            1.0.1
Release:            1zimbra8.7b1ZAPPEND
License:            GPL-2
Requires:           zimbra-base, zimbra-os-requirements, zimbra-perl, zimbra-pflogsumm
Requires:           zimbra-openssl,zimbra-curl, zimbra-cyrus-sasl, zimbra-rsync
Requires:           zimbra-mariadb-libs >= 10.1.25-1zimbra8.7b1ZAPPEND, zimbra-openldap-client, zimbra-osl
Requires:           zimbra-prepflog, zimbra-tcmalloc-libs, zimbra-perl-innotop
Requires:           zimbra-openjdk, zimbra-openjdk-cacerts, zimbra-amavis-logwatch
Requires:           zimbra-postfix-logwatch, zimbra-rrdtool
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%changelog
* Mon Jul 24 2017  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Updated zimbra-mariadb package
* Wed Sep 09 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.0
- Initial Release

%description
Zimbra core components pulls in all the packages used by
zimbra-core

%files
