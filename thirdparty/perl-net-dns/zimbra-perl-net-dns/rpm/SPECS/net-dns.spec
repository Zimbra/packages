Summary:            Net::DNS - Perl Interface to the Domain Name System
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            MIT
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-digest-hmac, zimbra-perl-digest-sha1
BuildRequires:      zimbra-perl-io-socket-inet6
Requires:           zimbra-perl-base, zimbra-perl-digest-hmac, zimbra-perl-digest-sha1
Requires:           zimbra-perl-io-socket-inet6
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
Net::DNS is a DNS resolver implemented in Perl. It allows the programmer
to perform nearly any type of DNS query from a Perl script. For details
and examples, please read the Net::DNS manual page.

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
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/perllocal.pod
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/auto/*/*/.packlist

%files
%defattr(-,root,root)
OZCL
OZCS/man
