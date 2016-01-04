Summary:            Zimbra components for core package
Name:               zimbra-core-components
Version:            1.0.0
Release:            ITERATIONZAPPEND
License:            GPL-2
Requires:           zimbra-base, zimbra-os-requirements, zimbra-perl, zimbra-pflogsumm
Requires:           zimbra-openssl,zimbra-curl, zimbra-cyrus-sasl, zimbra-rsync
Requires:           zimbra-mariadb-libs, zimbra-openldap-client, zimbra-osl
Requires:           zimbra-prepflog, zimbra-tcmalloc-libs, zimbra-perl-innotop
Requires:           zimbra-openjdk, zimbra-openjdk-cacerts, zimbra-amavis-logwatch
Requires:           zimbra-postfix-logwatch, zimbra-rrdtool
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra core components pulls in all the packages used by
zimbra-core

%files
