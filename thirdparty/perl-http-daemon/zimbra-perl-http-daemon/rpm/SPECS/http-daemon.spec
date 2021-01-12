Summary:            HTTP::Daemon - a simple http server class
Name:               zimbra-perl-http-daemon
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-http-date, zimbra-perl-http-message >= 6.11-1zimbra8.7b2ZAPPEND, zimbra-perl-lwp-mediatypes
Requires:           zimbra-perl-base, zimbra-perl-http-date, zimbra-perl-http-message >= 6.11-1zimbra8.7b2ZAPPEND, zimbra-perl-lwp-mediatypes
AutoReqProv:        no
URL:                https://metacpan.org/release/HTTP-Daemon

%description
Instances of the HTTP::Daemon class are HTTP/1.1 servers that listen
on a socket for incoming requests. The HTTP::Daemon is a subclass of
IO::Socket::INET, so you can perform socket operations directly on it
too.

%changelog
* Sat Apr 25 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated dependency zimbra-perl-http-message

%define debug_package %{nil}

%prep
%setup -n HTTP-Daemon-%{version}

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
