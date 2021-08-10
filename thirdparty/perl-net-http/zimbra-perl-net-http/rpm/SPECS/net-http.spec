Summary:            Net::HTTP - Low-level HTTP connection (client)
Name:               zimbra-perl-net-http
Version:            VERSION
Release:            1zimbra8.7b4ZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-uri, zimbra-perl-io-socket-ssl >= 2.068-1zimbra8.7b3ZAPPEND
Requires:           zimbra-perl-base, zimbra-perl-uri, zimbra-perl-io-socket-ssl >= 2.068-1zimbra8.7b3ZAPPEND
AutoReqProv:        no
URL:                https://metacpan.org/release/Net-HTTP

%description
The Net::HTTP class is a low-level HTTP client. An instance of the
Net::HTTP class represents a connection to an HTTP server. The HTTP
protocol is described in RFC 2616. The Net::HTTP class supports
HTTP/1.0 and HTTP/1.1

%define debug_package %{nil}

%changelog
* Tue Aug 10 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Updated dependency perl-io-socket-ssl for perl-net-http
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated dependency perl-io-socket-ssl for perl-net-http

%prep
%setup -n Net-HTTP-%{version}

%build
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 LIB=OZCL/perl5
PERL5LIB=OZCL/perl5 make

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
