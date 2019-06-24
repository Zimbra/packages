Summary:            Postfix Log Entry Summarizer
Name:               zimbra-pflogsumm
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Requires:            zimbra-base, zimbra-perl-base, zimbra-perl-date-calc
AutoReqProv:        no
URL:                http://jimsun.linxnet.com/postfix_contrib.html

%description
pflogsumm.pl is designed to provide an over-view of postfix
activity, with just enough detail to give the administrator
a "heads up" for potential trouble spots.

%define debug_package %{nil}

%prep
%setup -n pflogsumm-%{version}

%build

%install
mkdir -p ${RPM_BUILD_ROOT}OZCB
mkdir -p ${RPM_BUILD_ROOT}OZCS/man/man1
cp -f pflogsumm.pl ${RPM_BUILD_ROOT}OZCB
cp -f pflogsumm.1 ${RPM_BUILD_ROOT}OZCS/man/man1
sed -i -e '/=head1 NAME/ i use lib qw(/opt/zimbra/common/lib/perl5);' ${RPM_BUILD_ROOT}OZCB/pflogsumm.pl

%files
%defattr(-,root,root)
OZCB
OZCS
