Summary:            LWP::Protocol::https - Provide https support for LWP::UserAgent 
Name:               zimbra-perl-lwp-protocol-https
Version:            VERSION
Release:            1zimbra8.7b4ZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-libwww >= 6.13-1zimbra8.7b5ZAPPEND, zimbra-perl-net-http >= 6.09-1zimbra8.7b5ZAPPEND
BuildRequires:      zimbra-perl-io-socket-ssl >= 2.083-1zimbra8.7b4ZAPPEND, zimbra-perl-mozilla-ca
Requires:           zimbra-perl-base, zimbra-perl-libwww >= 6.13-1zimbra8.7b5ZAPPEND, zimbra-perl-net-http >= 6.09-1zimbra8.7b5ZAPPEND
Requires:           zimbra-perl-io-socket-ssl >= 2.083-1zimbra8.7b4ZAPPEND, zimbra-perl-mozilla-ca
AutoReqProv:        no
URL:                https://metacpan.org/release/LWP-Protocol-https

%description
The LWP::Protocol::https module provides support for using https schemed
URLs with LWP. This module is a plug-in to the LWP protocol handling, so
you don't use it directly. Once the module is installed LWP is able to
access sites using HTTP over SSL/TLS.

%define debug_package %{nil}

%changelog
* Tue Jun 13 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Updated dependencies zimbra-perl-libwww,zimbra-perl-net-http,zimbra-perl-io-socket-ssl and upgraded LWP::Protocol::https to 6.10
* Tue Aug 10 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Updated dependencies zimbra-perl-libwww,zimbra-perl-net-http,zimbra-perl-io-socket-ssl
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Updated dependencies zimbra-perl-libwww,zimbra-perl-net-http,zimbra-perl-io-socket-ssl
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated dependencies zimbra-perl-libwww,zimbra-perl-net-http,zimbra-perl-io-socket-ssl


%prep
%setup -n LWP-Protocol-https-%{version}

%build
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 INSTALLMAN1DIR=OZCS/man/man1 INSTALLVENDORMAN1DIR=OZCS/man/man1 \
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

%files
%defattr(-,root,root)
OZCL
OZCS/man
