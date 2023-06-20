Summary:            Mail::DKIM - Signs/verifies Internet mail with DKIM/DomainKey signatures
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            1zimbra8.7b4ZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Patch0:             public_key.patch
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-crypt-openssl-rsa >= 0.33-1zimbra8.8b1ZAPPEND, zimbra-perl-digest-sha1
BuildRequires:      zimbra-perl-net-dns zimbra-perl-mailtools
Requires:           zimbra-perl-base, zimbra-perl-crypt-openssl-rsa >= 0.33-1zimbra8.8b1ZAPPEND, zimbra-perl-digest-sha1
Requires:           zimbra-perl-net-dns zimbra-perl-mailtools
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
This module implements the various components of the DKIM and DomainKeys
message-signing and verifying standards for Internet mail. It currently
tries to implement these specifications:
RFC4871, for DKIM
RFC4870, for DomainKeys

%define debug_package %{nil}

%changelog
* Tue Jun 13 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Updated dependency zimbra-perl-crypt-openssl-rsa
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Updated dependency zimbra-perl-crypt-openssl-rsa
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated dependency zimbra-perl-crypt-openssl-rsa

%prep
%setup -n MODNAME-%{version}
%patch0 -p1

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
