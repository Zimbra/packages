Summary:            Zimbra components for spell package
Name:               zimbra-spell-components
Version:            1.0.0
Release:            ITERATIONZAPPEND
License:            GPL-2
Requires:           zimbra-spell-base, zimbra-aspell-ar, zimbra-aspell-da, zimbra-aspell-de
Requires:           zimbra-aspell-en, zimbra-aspell-es, zimbra-aspell-fr, zimbra-aspell-hi
Requires:           zimbra-aspell-hu, zimbra-aspell-it, zimbra-aspell-nl, zimbra-aspell-pl
Requires:           zimbra-aspell-pt-br, zimbra-aspell-ru, zimbra-aspell-sv, zimbra-httpd,
Requires:           zimbra-php, zimbra-aspell-zimbra
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra spell components pulls in all the packages used by
zimbra-spell

%files
