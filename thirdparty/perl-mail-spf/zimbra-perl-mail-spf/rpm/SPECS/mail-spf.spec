Summary:            Mail::SPF - An object-oriented implementation of Sender Policy Framework
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            MIT
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-error, zimbra-perl-netaddr-ip
BuildRequires:      zimbra-perl-net-dns, zimbra-perl-net-dns-resolver-programmable
Requires:            zimbra-perl-base, zimbra-perl-error, zimbra-perl-netaddr-ip
Requires:            zimbra-perl-net-dns, zimbra-perl-net-dns-resolver-programmable
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
Mail::SPF is an object-oriented implementation of Sender Policy Framework (SPF).
See http://www.openspf.org for more information about SPF.
This class collection aims to fully conform to the SPF specification (RFC 4408)
so as to serve both as a production quality SPF implementation and as a reference
for other developers of SPF implementations.

%define debug_package %{nil}

%prep
%setup -n MODNAME-v%{version}

%build
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 INSTALLMAN3DIR=OZCS/man/man1 INSTALLVENDORMAN3DIR=OZCS/man/man1 \
 INSTALLMAN3DIR=OZCS/man/man3 INSTALLVENDORMAN3DIR=OZCS/man/man3 \
 LIB=OZCL/perl5
PERL5LIB=OZCL/perl5 make

# remove .packlist and perllocal.pod
#  $(DESTINSTALLSITEARCH)/auto/$(FULLEXT)/.packlist
#  $(DESTINSTALLSITEARCH)/perllocal.pod
%define perl_archname %(perl -MConfig -e 'print $Config{archname}')
%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -rf %{buildroot}OZCL/perl5/%{perl_archname}
rm -rf %{buildroot}OZCB
rm -rf %{buildroot}/usr/sbin
mkdir -p %{buildroot}OZCS/man/man3
mv %{buildroot}/OZC/man/man3/* %{buildroot}OZCS/man/man3
rm -rf %{buildroot}/OZC/man

%files
%defattr(-,root,root)
OZCL
OZCS/man
