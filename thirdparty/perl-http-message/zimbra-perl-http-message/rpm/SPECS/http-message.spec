Summary:            HTTP-Message
Name:               zimbra-perl-http-message
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-io-compress >= 2.093-1zimbra8.7b1ZAPPEND, zimbra-perl-uri
BuildRequires:      zimbra-perl-http-date, zimbra-perl-io-html
BuildRequires:      zimbra-perl-encode-locale, zimbra-perl-lwp-mediatypes
Requires:           zimbra-perl-base, zimbra-perl-io-compress >= 2.093-1zimbra8.7b1ZAPPEND, zimbra-perl-uri
Requires:           zimbra-perl-http-date, zimbra-perl-io-html
Requires:           zimbra-perl-encode-locale, zimbra-perl-lwp-mediatypes
AutoReqProv:        no
URL:                https://metacpan.org/release/HTTP-Message

%description
The HTTP-Message distribution contains classes useful for representing the
messages passed in HTTP style communication.  These are classes representing
requests, responses and the headers contained within them.

%changelog
* Tue Aug 10 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated dependency zimbra-perl-io-compress

%define debug_package %{nil}

%prep
%setup -n HTTP-Message-%{version}

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
