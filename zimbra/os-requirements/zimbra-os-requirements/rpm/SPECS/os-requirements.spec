Summary:            Zimbra OS Requirements
Name:               zimbra-os-requirements
Version:            1.0.2
Release:            1zimbra8.7b1ZAPPEND
License:            GPL-2
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
Requires:           coreutils, expat, file, gmp, libaio, libidn, libstdc++, pcre
Requires:           perl, perl-core, sudo, sysstat, unzip, zimbra-base
Requires:           perl-Socket6, OSDEPS
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra OS requirements is used as a simple method to pull in all
OS required core packages

%changelog
* Mon Sep 12 2022  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b1ZAPPEND
- Fix ZBUG-3017

%files
