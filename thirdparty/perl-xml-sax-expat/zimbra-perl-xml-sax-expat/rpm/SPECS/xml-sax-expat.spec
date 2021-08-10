Summary:            XML::SAX::Expat - SAX2 Driver for Expat (XML::Parser)
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            1zimbra8.7b4ZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-xml-sax, zimbra-perl-xml-parser >= 2.44-1zimbra8.7b4ZAPPEND
Requires:           zimbra-perl-base, zimbra-perl-xml-sax, zimbra-perl-xml-parser >= 2.44-1zimbra8.7b4ZAPPEND
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
This is an implementation of a SAX2 driver sitting on top of
Expat (XML::Parser)

%define debug_package %{nil}

%changelog
* Tue Aug 10 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Updated dependency zimbra-perl-xml-parser
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Updated dependency zimbra-perl-xml-parser
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated dependency zimbra-perl-xml-parser

%prep
%setup -n MODNAME-%{version}

%build
export SKIP_SAX_INSTALL=1
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 INSTALLMAN3DIR=OZCS/man/man1 INSTALLVENDORMAN3DIR=OZCS/man/man1 \
 INSTALLMAN3DIR=OZCS/man/man3 INSTALLVENDORMAN3DIR=OZCS/man/man3
 LIB=OZCL/perl5
PERL5LIB=OZCL/perl5 make test

# remove .packlist and perllocal.pod
#  $(DESTINSTALLSITEARCH)/auto/$(FULLEXT)/.packlist
#  $(DESTINSTALLSITEARCH)/perllocal.pod
%define perl_archname %(perl -MConfig -e 'print $Config{archname}')
%install
PERL5LIB=OZCL/perl5:%{buildroot}OZCL/perl5 make install DESTDIR=${RPM_BUILD_ROOT}
rm -rf %{buildroot}OZCL/perl5/%{perl_archname}

%files
%defattr(-,root,root)
OZCL
OZCS/man

%post
/usr/bin/perl -I/opt/zimbra/common/lib/perl5 -MXML::SAX -e "XML::SAX->add_parser(q(XML::SAX::Expat))->save_parsers()"
