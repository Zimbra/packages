Summary:            Perl extension for using OpenSSL
Name:               zimbra-perl-net-ssleay
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            Artistic 2.0
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-openssl-devel >= 1.1.1h-1zimbra8.7b3ZAPPEND
Requires:           zimbra-perl-base, zimbra-openssl-libs >= 1.1.1h-1zimbra8.7b3ZAPPEND
AutoReqProv:        no
URL:                https://metacpan.org/release/Net-SSLeay

%define perl_archname %(eval "`perl -V:archname`"; echo $archname)

%description
The Net::SSLeay module basically comprises:
- High level functions for accessing web servers (by using HTTP/HTTPS)
- Low level API (mostly mapped 1:1 to openssl's C functions)
- Convenience functions (related to low level API but with more perl friendly interface)

%define debug_package %{nil}

%changelog
* Fri Dec 02 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Upgraded dependency openssl to 1.1.1h
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-ITERATIONZAPPEND
- Upgraded to 1.88 and updated dependency openssl to 1.1.1g

%prep
%setup -n Net-SSLeay-%{version}

%build
# Notes/Workarounds:
# * avoid prompt about network tests by setting PERL_MM_USE_DEFAULT=1
# * LIBS not working as expected due to a MakeMaker bug:
#     https://github.com/Perl-Toolchain-Gang/ExtUtils-MakeMaker/pull/240
#   - use NBSP instead of space in LIBS as workaround
#     (avoids Unrecognized argument in LIBS ignored...)
#   - (RHEL) use -LOZCL in LDLOADLIBS since -L is not preserved
PERL_MM_USE_DEFAULT=1 OPENSSL_PREFIX=OZC perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 LIB=OZCL/perl5 LIBS="-LOZCL -lssl" INC="-IOZCI"
LD_RUN_PATH=OZCL make test LDLOADLIBS="-LOZCL -lssl"

%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/perllocal.pod
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/auto/*/*/.packlist

%files
%defattr(-,root,root)
OZCL
OZCS/man
