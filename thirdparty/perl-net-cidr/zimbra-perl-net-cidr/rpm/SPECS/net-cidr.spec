Summary:            Zimbra's Net::CIDR build
Name:               zimbra-perl-net-cidr
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zimbra-perl-base
Requires:           zimbra-perl-base
AutoReqProv:        no
URL:                http://search.cpan.org/dist/Net-CIDR/

%define perl_archname %(eval "`perl -V:archname`"; echo $archname)

%description
The Zimbra Net::CIDR Build

%define debug_package %{nil}

%prep
%setup -n Net-CIDR-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC LIB=OZCL/perl5 \
  INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -rf %{buildroot}OZCL/perl5/%{perl_archname}

%files
%defattr(-,root,root)
OZCL
OZCS/man
