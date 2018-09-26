Summary:            Zimbra Perl Base
Name:               zimbra-perl-base
Version:            1.0.0
Release:            ITERATIONZAPPEND
License:            GPL-2
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      perl, perl-core
Requires:  zimbra-base
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra Perl Base is used as a simple method to allow removing
all the zimbra specific perl modules.  It in itself has no
actual contents.

%files
