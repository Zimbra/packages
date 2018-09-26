Summary:            libwww - The World-Wide Web library for Perl
Name:               zimbra-perl-libwww
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-encode-locale, zimbra-perl-file-listing
BuildRequires:      zimbra-perl-http-cookies, zimbra-perl-http-daemon, zimbra-perl-http-date
BuildRequires:      zimbra-perl-http-negotiate, zimbra-perl-http-message, zimbra-perl-lwp-mediatypes
BuildRequires:      zimbra-perl-uri, zimbra-perl-net-http, zimbra-perl-www-robotrules, zimbra-perl-html-parser
Requires:            zimbra-perl-base, zimbra-perl-encode-locale, zimbra-perl-file-listing
Requires:            zimbra-perl-http-cookies, zimbra-perl-http-daemon, zimbra-perl-http-date
Requires:            zimbra-perl-http-negotiate, zimbra-perl-http-message, zimbra-perl-lwp-mediatypes
Requires:            zimbra-perl-uri, zimbra-perl-net-http, zimbra-perl-www-robotrules, zimbra-perl-html-parser
AutoReqProv:        no
URL:                https://metacpan.org/release/libwww-perl

%description
The libwww-perl collection is a set of Perl modules which provides a
simple and consistent application programming interface to the
World-Wide Web.  The main focus of the library is to provide classes
and functions that allow you to write WWW clients. The library also
contain modules that are of more general use and even classes that
help you implement simple HTTP servers.

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
