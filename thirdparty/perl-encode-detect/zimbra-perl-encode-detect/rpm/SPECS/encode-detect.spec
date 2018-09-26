Summary:            Encode::Detect - An Encode::Encoding subclass that detects the encoding of data 
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            MPL-1.1, GPL-2, LGPL-2.1
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base
Requires:            zimbra-perl-base
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
This Perl module is an Encode::Encoding subclass that uses Encode::Detect::Detector
to determine the charset of the input data and then decodes it using the encoder of
the detected charset.

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
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/perllocal.pod
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/auto/*/*/.packlist
mkdir -p %{buildroot}OZCS/man/man3
cp %{buildroot}OZC/man/man3/* %{buildroot}OZCS/man/man3
rm -rf %{buildroot}OZC/man

%files
%defattr(-,root,root)
OZCL
OZCS/man
