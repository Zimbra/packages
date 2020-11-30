Summary:            Zimbra components for spell package
Name:               zimbra-spell-components
Version:            2.0.2
Release:            1zimbra8.8b1ZAPPEND
License:            GPL-2
Requires:           zimbra-spell-base, zimbra-aspell-ar >= 1.2.0-1zimbra8.7b2ZAPPEND, zimbra-aspell-da >= 1.4.42.1-1zimbra8.7b2ZAPPEND
Requires:           zimbra-aspell-de >= 20030222.1-1zimbra8.7b2ZAPPEND
Requires:           zimbra-aspell-en >= 7.1.0-1zimbra8.7b2ZAPPEND, zimbra-aspell-es >= 1.11.2-1zimbra8.7b2ZAPPEND, zimbra-aspell-fr >= 0.50.3-1zimbra8.7b2ZAPPEND
Requires:           zimbra-aspell-hi >= 0.02.0-1zimbra8.7b2ZAPPEND, zimbra-aspell-hu >= 0.99.4.2.0-1zimbra8.7b2ZAPPEND, zimbra-aspell-it >= 2.2.20050523.0-1zimbra8.7b2ZAPPEND
Requires:           zimbra-aspell-nl >= 0.50.2-1zimbra8.7b2ZAPPEND, zimbra-aspell-pl >= 6.0.20061121.0-1zimbra8.7b2ZAPPEND, zimbra-aspell-pt-br >= 20090702.0-1zimbra8.7b2ZAPPEND
Requires:           zimbra-aspell-ru >= 0.99f7.1-1zimbra8.7b2ZAPPEND, zimbra-aspell-sv >= 0.51.0-1zimbra8.7b2ZAPPEND
Requires:           zimbra-httpd >= 2.4.38-1zimbra8.7b2ZAPPEND
Requires:           zimbra-php >= 7.3.1-1zimbra8.7b5ZAPPEND, zimbra-aspell-zimbra >= 1.0.0-1zimbra8.7b2ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra spell components pulls in all the packages used by
zimbra-spell

%changelog
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.2
- Updated dependency zimbra-httpd and zimbra-php
* Sat Apr 25 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.1
- Updated zimbra-aspell and zimbra-php
* Mon Mar 25 2019  Zimbra Packaging Services <packaging-devel@zimbra.com> - 2.0.0
- Updated PHP package.

%files
