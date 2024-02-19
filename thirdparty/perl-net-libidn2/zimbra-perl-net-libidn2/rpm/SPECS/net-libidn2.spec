Summary:            Net::LibIDN2 - Perl bindings for GNU Libidn2
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            1zimbra10.0b1ZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, libidn2-devel
Requires:           zimbra-perl-base, libidn2
Obsoletes:          zimbra-perl-net-libidn
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
Provides bindings for GNU Libidn2, a C library for handling internationalized domain names based on IDNA 2008, Punycode and TR46.

%define debug_package %{nil}

%prep
%setup -n MODNAME-%{version}

%build
perl -I OZCL/perl5 Build.PL install_base=OZC --install_path libdoc=OZCS/man/man3 --install_path bindoc=OZCS/man/man1
PERL5LIB=OZCL/perl5 ./Build test

%define perl_archname %(perl -MConfig -e 'print $Config{archname}')
%install
./Build install destdir=${RPM_BUILD_ROOT}
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/auto/*/*/.packlist

%files
%defattr(-,root,root)
OZCL
OZCS/man
