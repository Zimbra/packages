Summary:            HTML::Parser - HTML extraction tools
Name:               zimbra-perl-html-parser
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zimbra-perl-base
Requires:           zimbra-perl-base
AutoReqProv:        no
URL:                https://metacpan.org/release/HTML-Parser

%define perl_archname %(eval "`perl -V:archname`"; echo $archname)

%description
The HTML-Parser distribution is is a collection
of modules that parse and extract information
from HTML documents.

%define debug_package %{nil}

%prep
%setup -n HTML-Parser-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC LIB=OZCL/perl5 \
  INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
  INSTALLMAN1DIR=OZCS/man/man1 INSTALLVENDORMAN1DIR=OZCS/man/man1 \
  INSTALLMAN3DIR=OZCS/man/man3 INSTALLVENDORMAN3DIR=OZCS/man/man3
make
PERL5LIB=OZCL/perl5 make test

%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/perllocal.pod
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/auto/*/*/.packlist

%files
%defattr(-,root,root)
OZCL
OZCS/man
