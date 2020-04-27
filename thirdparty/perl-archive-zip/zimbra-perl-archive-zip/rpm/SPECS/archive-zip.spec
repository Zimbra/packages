Summary:            Archive::Zip - Provide an interface to ZIP archive files
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-compress-raw-zlib >= 2.093-1zimbra8.7b1ZAPPEND
Requires:           zimbra-perl-base, zimbra-perl-compress-raw-zlib >= 2.093-1zimbra8.7b1ZAPPEND
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
Perl interface to Zip archive files

%changelog
* Sat Apr 25 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated dependency zimbra-perl-compress-raw-zlib

%define debug_package %{nil}

%prep
%setup -n MODNAME-%{version}

%build
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 INSTALLMAN3DIR=OZCS/man/man1 INSTALLVENDORMAN3DIR=OZCS/man/man1 \
 INSTALLMAN3DIR=OZCS/man/man3 INSTALLVENDORMAN3DIR=OZCS/man/man3 \
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
