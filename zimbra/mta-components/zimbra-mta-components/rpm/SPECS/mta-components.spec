Summary:            Zimbra components for MTA package
Name:               zimbra-mta-components
Version:            1.0.1
Release:            ITERATIONZAPPEND
License:            GPL-2
Requires:           sqlite, zimbra-mta-base, zimbra-altermime, zimbra-amavisd
Requires:           zimbra-clamav, zimbra-cluebringer, zimbra-mariadb
Requires:           zimbra-opendkim, zimbra-perl-mail-spamassassin, zimbra-postfix
Requires:           zimbra-spamassassin-rules
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra mta components pulls in all the packages used by
zimbra-mta

%changelog
* Fri Dec 14 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Add Spamassassin default ruleset

%files
