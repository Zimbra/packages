Summary:            PostSRSd provides Sender Rewriting Scheme Support for Postfix
Name:               zimbra-postsrsd
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Requires:           zimbra-base
AutoReqProv:        no
URL:                https://github.com/roehling/postsrsd

%description
PostSRSd provides the Sender Rewriting Scheme (SRS) via TCP-based
lookup tables for Postfix. SRS is needed if your mail server acts
as forwarder.

%changelog
- Upgraded postsrsd from 1.3 to 1.11
* Wed Mar 02 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND

%prep
%setup -n postsrsd-%{version}

%build
mkdir build && \
cd build && \
/usr/bin/cmake .. \
  -DCMAKE_INSTALL_PREFIX="OZC" \
  -DCMAKE_INSTALL_RPATH="OZCL" \
  -DCMAKE_PREFIX_PATH="OZC" \
  -DINIT_FLAVOR=none \
  -DGENERATE_SRS_SECRET="/opt/zimbra/common/etc/postsrsd.secret" \
  -DSYSCONF_DIR=OZCE
make all

%install
make DESTDIR=${RPM_BUILD_ROOT} install
rm -rf ${RPM_BUILD_ROOT}/OZC/share

%files
%defattr(-,root,root)
OZCE
OZCL/postsrsd
OZC/sbin
