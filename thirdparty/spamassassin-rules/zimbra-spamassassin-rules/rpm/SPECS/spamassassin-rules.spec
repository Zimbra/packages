Summary:            Default ruleset for SpamAssassin
Name:               zimbra-spamassassin-rules
Version:            1.0.0
Release:            1zimbra8.8b3ZAPPEND
License:            Apache-2.0
Requires:           zimbra-mta-base, zimbra-perl-mail-spamassassin >= 3.4.4-1zimbra8.8b3ZAPPEND
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Default ruleset for SpamAssassin

%changelog
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.0-1zimbra8.8b3ZAPPEND
- Updated zimbra-perl-mail-spamassassin
* Mon Apr 27 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.0-1zimbra8.8b2ZAPPEND
-Updated dependency zimbra-perl-mail-spamassassin
* Wed Apr 1 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.0-1zimbra8.8b1ZAPPEND
-Upgraded spamAssasin to 3.4.4

%install
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/data/spamassassin/rules
cp ../../../rules/updates_spamassassin_org/* ${RPM_BUILD_ROOT}/opt/zimbra/data/spamassassin/rules/
rm -rf ${RPM_BUILD_ROOT}/opt/zimbra/data/spamassassin/rules/user_prefs.template

%files
%defattr(-,zimbra,zimbra)
/opt/zimbra/data/spamassassin/rules
