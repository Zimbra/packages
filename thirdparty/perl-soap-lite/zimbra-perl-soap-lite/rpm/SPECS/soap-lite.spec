Summary:            SOAP::Lite - Perl's Web Services Toolkit
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-class-inspector, zimbra-perl-io-compress >= 2.093-1zimbra8.7b1ZAPPEND
BuildRequires:      zimbra-perl-io-sessiondata, zimbra-perl-io-socket-ssl >= 2.068-1zimbra8.7b1ZAPPEND
BuildRequires:      zimbra-perl-lwp-protocol-https >= 6.06-1zimbra8.7b2ZAPPEND, zimbra-perl-libwww >= 6.13-1zimbra8.7b2ZAPPEND
BuildRequires:      zimbra-perl-task-weaken, zimbra-perl-uri, zimbra-perl-xml-parser >= 2.44-1zimbra8.7b2ZAPPEND
BuildRequires:      zimbra-perl-mime-tools, zimbra-perl-xml-parser-lite
Requires:           zimbra-perl-base, zimbra-perl-class-inspector, zimbra-perl-io-compress >= 2.093-1zimbra8.7b1ZAPPEND
Requires:           zimbra-perl-io-sessiondata, zimbra-perl-io-socket-ssl >= 2.068-1zimbra8.7b1ZAPPEND
Requires:           zimbra-perl-lwp-protocol-https >= 6.06-1zimbra8.7b2ZAPPEND, zimbra-perl-libwww >= 6.13-1zimbra8.7b2ZAPPEND
Requires:           zimbra-perl-task-weaken, zimbra-perl-uri, zimbra-perl-xml-parser >= 2.44-1zimbra8.7b2ZAPPEND
Requires:           zimbra-perl-mime-tools, zimbra-perl-xml-parser-lite
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
SOAP::Lite is a collection of Perl modules which provides a simple and
lightweight interface to the Simple Object Access Protocol (SOAP) both
on client and server side.

%changelog
* Sat Apr 25 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated dependencies zimbra-perl-io-compress,zimbra-perl-io-socket-ssl,zimbra-perl-lwp-protocol-https,zimbra-perl-libwww,zimbra-perl-xml-parser

%define debug_package %{nil}

%prep
%setup -n MODNAME-%{version}

%build
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
make install DESTDIR=${RPM_BUILD_ROOT}
rm -rf %{buildroot}OZCL/perl5/%{perl_archname}
rm -rf %{buildroot}OZCB

%files
%defattr(-,root,root)
OZCL
OZCS/man
