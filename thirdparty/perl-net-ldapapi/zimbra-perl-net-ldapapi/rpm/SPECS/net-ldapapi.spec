Summary:            Net::LDAPapi - Perl5 Module Supporting LDAP API
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-openldap-devel >= 2.4.59-1zimbra8.8b6ZAPPEND, zimbra-cyrus-sasl-devel >= 2.1.28-1zimbra8.7b4ZAPPEND
BuildRequires:      zimbra-perl-convert-asn1
Requires:           zimbra-perl-base, zimbra-openldap-libs >= 2.4.59-1zimbra8.8b6ZAPPEND, zimbra-perl-convert-asn1
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
This module allows Perl programmers to access and manipulate an LDAP
based Directory.

%define debug_package %{nil}
%changelog
* Tue Jun 13 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated openldap, cyrus-sasl

%prep
%setup -n MODNAME-%{version}

%build
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 INSTALLMAN3DIR=OZCS/man/man1 INSTALLVENDORMAN3DIR=OZCS/man/man1 \
 INSTALLMAN3DIR=OZCS/man/man3 INSTALLVENDORMAN3DIR=OZCS/man/man3 \
 LIB=OZCL/perl5 -sdk openldap -lib_path OZCL -include_path OZCI \
 -sasl_include_path OZCL

# remove .packlist and perllocal.pod
#  $(DESTINSTALLSITEARCH)/auto/$(FULLEXT)/.packlist
#  $(DESTINSTALLSITEARCH)/perllocal.pod
%define perl_archname %(perl -MConfig -e 'print $Config{archname}')
%install
LD_RUN_PATH=OZCL make DESTDIR=${RPM_BUILD_ROOT} install
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/perllocal.pod
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/auto/*/*/.packlist

%files
%defattr(-,root,root)
OZCL
OZCS/man
