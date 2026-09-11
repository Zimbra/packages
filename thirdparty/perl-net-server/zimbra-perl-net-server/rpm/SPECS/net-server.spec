Summary:            an extensible, generic Perl server engine
Name:               zimbra-perl-net-server
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Patch0:             Net-Server-2.009-RT132245.patch
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base
Requires:           zimbra-perl-base
AutoReqProv:        no
URL:                https://metacpan.org/release/Net-Server

%description
Net::Server attempts to be a generic server as in Net::Daemon and
NetServer::Generic. It includes with it the ability to run as an
inetd process (Net::Server::INET), a single connection server
(Net::Server or Net::Server::Single), a forking server
(Net::Server::Fork), a preforking server which maintains a constant
number of preforked children (Net::Server::PreForkSimple), or as a
managed preforking server which maintains the number of children
based on server load (Net::Server::PreFork).

%define debug_package %{nil}

%changelog
* Tue Aug 10 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-ITERATIONZAPPEND
- Upgraded Net-Server to 2.009

%prep
%setup -n Net-Server-%{version}
%patch0 -p1

%build
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 LIB=OZCL/perl5
make test

# remove .packlist and perllocal.pod
#  $(DESTINSTALLSITEARCH)/auto/$(FULLEXT)/.packlist
#  $(DESTINSTALLSITEARCH)/perllocal.pod
#  also remove .../bin/net-server and associated man page
%define perl_archname %(perl -MConfig -e 'print $Config{archname}')
%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -rf %{buildroot}OZCL/perl5/%{perl_archname}
rm -rf %{buildroot}OZC/bin
rm -rf %{buildroot}OZCS/man/man1

%files
%defattr(-,root,root)
OZCL
OZCS/man
