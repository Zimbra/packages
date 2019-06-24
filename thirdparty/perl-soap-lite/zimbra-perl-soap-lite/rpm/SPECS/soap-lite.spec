Summary:            SOAP::Lite - Perl's Web Services Toolkit
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-class-inspector, zimbra-perl-io-compress
BuildRequires:      zimbra-perl-io-sessiondata, zimbra-perl-io-socket-ssl
BuildRequires:      zimbra-perl-lwp-protocol-https, zimbra-perl-libwww
BuildRequires:      zimbra-perl-task-weaken, zimbra-perl-uri, zimbra-perl-xml-parser
BuildRequires:      zimbra-perl-mime-tools, zimbra-perl-xml-parser-lite
Requires:            zimbra-perl-base, zimbra-perl-class-inspector, zimbra-perl-io-compress
Requires:            zimbra-perl-io-sessiondata, zimbra-perl-io-socket-ssl
Requires:            zimbra-perl-lwp-protocol-https, zimbra-perl-libwww
Requires:            zimbra-perl-task-weaken, zimbra-perl-uri, zimbra-perl-xml-parser
Requires:            zimbra-perl-mime-tools, zimbra-perl-xml-parser-lite
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
SOAP::Lite is a collection of Perl modules which provides a simple and
lightweight interface to the Simple Object Access Protocol (SOAP) both
on client and server side.

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
