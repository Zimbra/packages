Summary:            Mail::SpamAssassin - Spam detector and markup engine
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            1zimbra8.8b2ZAPPEND
License:            Apache-2.0
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-digest-sha1, zimbra-perl-net-dns
BuildRequires:      zimbra-perl-html-parser, zimbra-perl-io-compress >= 2.093-1zimbra8.7b1ZAPPEND, zimbra-perl-mail-spf
BuildRequires:      zimbra-perl-mail-dkim, zimbra-perl-netaddr-ip, zimbra-perl-net-cidr-lite
BuildRequires:      zimbra-perl-encode-detect
Requires:           zimbra-perl-base, zimbra-perl-digest-sha1, zimbra-perl-net-dns
Requires:           zimbra-perl-html-parser, zimbra-perl-io-compress >= 2.093-1zimbra8.7b1ZAPPEND, zimbra-perl-mail-spf
Requires:           zimbra-perl-mail-dkim, zimbra-perl-netaddr-ip, zimbra-perl-net-cidr-lite
Requires:           zimbra-perl-encode-detect, zimbra-mta-base
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
Mail::SpamAssassin is a module to identify spam using several methods
including text analysis, internet-based realtime blacklists, statistical
analysis, and internet-based hashing algorithms.

%changelog
* Sat Apr 25 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b2ZAPPEND
- Updated dependency zimbra-perl-io-compress
* Mon Mar 16 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
-Upgraded to 3.4.4
* Fri Jul 7 2017 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
-Added patch for spamAssasin bug-5561.
-Miscellaneous patch including bugs 7223,7265.

%define debug_package %{nil}

%prep
%setup -n MODNAME-%{version}

%build
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 INSTALLMAN3DIR=OZCS/man/man1 INSTALLVENDORMAN3DIR=OZCS/man/man1 \
 INSTALLMAN3DIR=OZCS/man/man3 INSTALLVENDORMAN3DIR=OZCS/man/man3 \
 LIB=OZCL/perl5 DATADIR=/opt/zimbra/data/spamassassin/rules \
 CONFDIR=/opt/zimbra/data/spamassassin/localrules \
 LOCALSTATEDIR=/opt/zimbra/data/spamassassin/state \
 CONTACT_ADDRESS=""
PERL5LIB=OZCL/perl5 make

# remove .packlist and perllocal.pod
#  $(DESTINSTALLSITEARCH)/auto/$(FULLEXT)/.packlist
#  $(DESTINSTALLSITEARCH)/perllocal.pod
%define perl_archname %(perl -MConfig -e 'print $Config{archname}')
%install
PERL5LIB=OZCL/perl5 make install DESTDIR=${RPM_BUILD_ROOT}
rm -rf %{buildroot}OZCL/perl5/%{perl_archname}
rm -rf %{buildroot}/opt/zimbra/common/data/spamassassin/rules
sed -i -e 's/^#loadplugin Mail::SpamAssassin::Plugin::DCC/loadplugin Mail::SpamAssassin::Plugin::DCC/' \
 %{buildroot}/opt/zimbra/data/spamassassin/localrules/v310.pre
sed -i -e 's/^# loadplugin Mail::SpamAssassin::Plugin::Rule2XSBody/loadplugin Mail::SpamAssassin::Plugin::Rule2XSBody/' \
 %{buildroot}/opt/zimbra/data/spamassassin/localrules/v320.pre

%files
%defattr(-,root,root)
OZCL
OZCS/man
OZCB
%attr(-,zimbra,zimbra) /opt/zimbra/data/spamassassin

%post
chown -R zimbra:zimbra /opt/zimbra/data/spamassassin
