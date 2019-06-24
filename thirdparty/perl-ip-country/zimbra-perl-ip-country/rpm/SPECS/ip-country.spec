Summary:            IP::Country - fast lookup of country codes from IP addresses
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-geography-countries
Requires:            zimbra-perl-base, zimbra-perl-geography-countries
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
This module comes bundled with a database of countries where various IP addresses
have been assigned. Although the country of assignment will probably be the
country associated with a large ISP rather than the client herself, this is
probably good enough for most log analysis applications, and under test has
proved to be as accurate as reverse-DNS and WHOIS lookup.

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
