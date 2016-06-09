Summary:            Default ruleset for SpamAssassin
Name:               zimbra-spamassasin-rules
Version:            1.0.0
Release:            ITERATIONZAPPEND
License:            Apache-2.0
Requires:           zimbra-mta-base, zimbra-perl-mail-spamassassin
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Default ruleset for SpamAssassin

%install
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/data/spamassassin/rules
cp ../../../rules/updates_spamassassin_org/* ${RPM_BUILD_ROOT}/opt/zimbra/data/spamassassin/rules/

%files
%defattr(-,zimbra,zimbra)
/opt/zimbra/data/spamassassin/rules
