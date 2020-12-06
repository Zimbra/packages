Summary:            libwww - The World-Wide Web library for Perl
Name:               zimbra-perl-libwww
Version:            VERSION
Release:            1zimbra8.7b4ZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-encode-locale, zimbra-perl-file-listing
BuildRequires:      zimbra-perl-http-cookies >= 6.01-1zimbra8.7b2ZAPPEND, zimbra-perl-http-daemon >= 6.01-1zimbra8.7b2ZAPPEND, zimbra-perl-http-date
BuildRequires:      zimbra-perl-http-negotiate >= 6.01-1zimbra8.7b2ZAPPEND, zimbra-perl-http-message >= 6.11-1zimbra8.7b2ZAPPEND, zimbra-perl-lwp-mediatypes
BuildRequires:      zimbra-perl-uri, zimbra-perl-net-http >= 6.09-1zimbra8.7b4ZAPPEND, zimbra-perl-www-robotrules, zimbra-perl-html-parser
Requires:           zimbra-perl-base, zimbra-perl-encode-locale, zimbra-perl-file-listing
Requires:           zimbra-perl-http-cookies >= 6.01-1zimbra8.7b2ZAPPEND, zimbra-perl-http-daemon >= 6.01-1zimbra8.7b2ZAPPEND, zimbra-perl-http-date
Requires:           zimbra-perl-http-negotiate >= 6.01-1zimbra8.7b2ZAPPEND, zimbra-perl-http-message >= 6.11-1zimbra8.7b2ZAPPEND, zimbra-perl-lwp-mediatypes
Requires:           zimbra-perl-uri, zimbra-perl-net-http >= 6.09-1zimbra8.7b4ZAPPEND, zimbra-perl-www-robotrules, zimbra-perl-html-parser
AutoReqProv:        no
URL:                https://metacpan.org/release/libwww-perl

%description
The libwww-perl collection is a set of Perl modules which provides a
simple and consistent application programming interface to the
World-Wide Web.  The main focus of the library is to provide classes
and functions that allow you to write WWW clients. The library also
contain modules that are of more general use and even classes that
help you implement simple HTTP servers.

%changelog
* Sat Dec 05 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Updated dependency zimbra-perl-net-http
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Updated dependency zimbra-perl-net-http
* Sat Apr 25 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated dependencies zimbra-perl-http-cookies,zimbra-perl-http-daemon,zimbra-perl-http-negotiate,zimbra-perl-http-message,zimbra-perl-net-http

%define debug_package %{nil}

%prep
%setup -n libwww-perl-%{version}

%build
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 INSTALLMAN1DIR=OZCS/man/man1 INSTALLVENDORMAN1DIR=OZCS/man/man1 \
 INSTALLMAN3DIR=OZCS/man/man3 INSTALLVENDORMAN3DIR=OZCS/man/man3 \
 LIB=OZCL/perl5 --no-programs
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
