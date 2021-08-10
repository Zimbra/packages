Summary:            HTTP::Negotiate - choose a variant to serve
Name:               zimbra-perl-http-negotiate
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-http-message >= 6.11-1zimbra8.7b2ZAPPEND
Requires:           zimbra-perl-base, zimbra-perl-http-message >= 6.11-1zimbra8.7b2ZAPPEND
AutoReqProv:        no
URL:                https://metacpan.org/release/HTTP-Negotiate

%description
This module provides a complete implementation of the HTTP content
negotiation algorithm specified in draft-ietf-http-v11-spec-00.ps
chapter 12. Content negotiation allows for the selection of a preferred
content representation based upon attributes of the negotiable variants
and the value of the various Accept* header fields in the request.

%changelog
* Tue Aug 10 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated dependency zimbra-perl-http-message
 
%define debug_package %{nil}

%prep
%setup -n HTTP-Negotiate-%{version}

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
