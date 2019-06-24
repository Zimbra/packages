Summary:            a client LDAP services API
Name:               zimbra-perl-net-ldap
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            Artistic 2.0
Source:             %{name}-%{version}.tar.gz
Patch0:             net-ldap-keepalive.patch
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-convert-asn1, zimbra-perl-socket-linux
Requires:            zimbra-perl-base, zimbra-perl-convert-asn1, zimbra-perl-socket-linux
AutoReqProv:        no
URL:                https://metacpan.org/release/perl-ldap

%description
Net::LDAP is a collection of modules that implements a LDAP services
API for Perl programs. The module may be used to search directories or
perform maintenance functions such as adding, deleting or modifying
entries.

%define debug_package %{nil}

%prep
%setup -n perl-ldap-%{version}
%patch0 -p1

%build
# Notes/Workarounds:
# * avoid prompt about network tests by setting PERL_MM_USE_DEFAULT=1
# * set PERL5LIB so tests find other custom modules
PERL_MM_USE_DEFAULT=1 perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 LIB=OZCL/perl5
PERL5LIB=OZCL/perl5 make test

%define perl_archname %(perl -MConfig -e 'print $Config{archname}')
%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -rf %{buildroot}OZCL/perl5/%{perl_archname}

%files
%defattr(-,root,root)
OZCL
OZCS/man
