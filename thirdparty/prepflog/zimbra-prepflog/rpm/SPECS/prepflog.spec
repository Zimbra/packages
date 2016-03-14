Summary:            prepflog.pl - Pre-processor for pflogsumm
Name:               zimbra-prepflog
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Requires:           zimbra-base, zimbra-perl-base, zimbra-perl-date-calc
AutoReqProv:        no
URL:                http://www.voipsupport.it/pmwiki/pmwiki.php?n=Linux.PrePflog

%description
The script sanitizes mail log files that are to be passed to pflogsumm or awstats
disregarding the lines relating to the re-injection of messages into postfix. I
use it with amavisd-new configured as a postfix after queue content filter which
does anti spam checks through spamassassin and antivirus checks through a third
party virus checker. If your postfix setup requires additional content filters
resulting in 3 or more passages of the same message through postfix, this script
will not work for you.

%define debug_package %{nil}

%prep
%setup -n prepflog-%{version}

%build

%install
mkdir -p ${RPM_BUILD_ROOT}OZCB
cp -f prepflog.pl ${RPM_BUILD_ROOT}OZCB
sed -i -e '/=pod/ i use lib qw(/opt/zimbra/common/lib/perl5);' ${RPM_BUILD_ROOT}OZCB/prepflog.pl

%files
%defattr(-,root,root)
OZCB
