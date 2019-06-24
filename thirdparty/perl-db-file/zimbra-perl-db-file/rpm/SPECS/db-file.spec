Summary:            DB_File - Perl5 access to Berkeley DB version 1.x
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-bdb-devel
Requires:            zimbra-perl-base, zimbra-bdb-libs
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
DB_File is a module which allows Perl programs to make use of the facilities
provided by Berkeley DB version 1.x (if you have a newer version of DB, see
"Using DB_File with Berkeley DB version 2 or greater"). It is assumed that you
have a copy of the Berkeley DB manual pages at hand when reading this documentation.
The interface defined here mirrors the Berkeley DB interface closely.

%define debug_package %{nil}

%prep
%setup -n MODNAME-%{version}

%build
export DB_FILE_LIB=OZCL; \
export DB_FILE_INCLUDE=OZCI; \
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 INSTALLMAN3DIR=OZCS/man/man1 INSTALLVENDORMAN3DIR=OZCS/man/man1 \
 INSTALLMAN3DIR=OZCS/man/man3 INSTALLVENDORMAN3DIR=OZCS/man/man3 \
 LIB=OZCL/perl5
LD_RUN_PATH=OZCL PERL5LIB=OZCL/perl5 make test

# remove .packlist and perllocal.pod
#  $(DESTINSTALLSITEARCH)/auto/$(FULLEXT)/.packlist
#  $(DESTINSTALLSITEARCH)/perllocal.pod
%define perl_archname %(perl -MConfig -e 'print $Config{archname}')
%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/perllocal.pod
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/auto/*/.packlist

%files
%defattr(-,root,root)
OZCL
OZCS/man
