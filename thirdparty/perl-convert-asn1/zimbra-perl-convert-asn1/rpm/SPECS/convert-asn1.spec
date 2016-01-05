Summary:            Zimbra's Convert::ASN1 build
Name:               zimbra-perl-convert-asn1
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zimbra-perl-base, perl-Test-Simple, zimbra-perl-math-bigint
Requires:           zimbra-perl-base, zimbra-perl-math-bigint
AutoReqProv:        no
URL:                https://metacpan.org/release/Convert-ASN1/

%define perl_archname %(eval "`perl -V:archname`"; echo $archname)

%description
ASN.1 Encode/Decode library

%define debug_package %{nil}

%prep
%setup -n Convert-ASN1-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC LIB=OZCL/perl5 \
  INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
  INSTALLMAN1DIR=OZCS/man/man1 INSTALLVENDORMAN1DIR=OZCS/man/man1 \
  INSTALLMAN3DIR=OZCS/man/man3 INSTALLVENDORMAN3DIR=OZCS/man/man3
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -rf %{buildroot}OZCL/perl5/%{perl_archname}

%files
%defattr(-,root,root)
OZCL
OZCS/man
