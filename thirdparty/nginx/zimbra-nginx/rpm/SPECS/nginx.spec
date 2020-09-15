Summary:            Zimbra's nginx build
Name:               zimbra-nginx
Version:            VERSION
Release:            1zimbra8.8b1ZAPPEND
License:            MIT
Source:             %{name}-%{version}.tar.gz
BuildRequires:      pcre-devel, zlib-devel
BuildRequires:      zimbra-openssl-devel
BuildRequires:      zimbra-cyrus-sasl-devel
Requires:           pcre, zlib
Requires:           zimbra-openssl-libs
Requires:           zimbra-cyrus-sasl-libs, zimbra-proxy-base
AutoReqProv:        no
URL:                http://nginx.org

%description
The Zimbra nginx build

%changelog
* Fri Mar 13 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
- Patch for nginx bug Bug 109101
* Thu Feb 12 2019  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b12ZAPPEND
- Patch for nginx bug ZBUG-838
- Patch for nginx for drive issue
* Thu Feb 07 2019  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b11ZAPPEND
- Patch for nginx bug ZBUG-838
- Tue Nov 06 2018  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b10ZAPPEND
- Patch for nginx bug ZESC-821
- Patch for nginx bug ZBUG-172
* Thu Aug 30 2018  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b9ZAPPEND
- ZCS-4021 for JWT support.
* Fri Aug 24 2018  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b8ZAPPEND
- Patch for nginx Bug 107566
* Wed May 10 2017  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b7ZAPPEND
- Patch for nginx Bug 107438 (and 106918, 106876)
- Patch for nginx Bug 106948.
- IMAP/POP3 throttling, whitelisting (ZMS-55, ZMS-59).
* Tue Jun 14 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b6ZAPPEND
- Backport upstream patch for CVE-2016-4450
* Wed Mar 23 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b5ZAPPEND
- Backport upstream patch for nginx ticket 901
* Mon Mar 14 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Build with OpenSSL 1.0.2
* Tue Feb 09 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Turn off compiler optimization.  Was breaking lookup extension.
* Wed Feb 03 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Patch nginx for CVE-2016-0742
- Patch nginx for CVE-2016-0746
- Patch nginx for CVE-2016-0747

%prep
%setup -n nginx-%{version}-zimbra

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-g -O0"; export CFLAGS; \
./configure --prefix=OZC \
  --with-cc-opt="-g -IOZCI" \
  --with-ld-opt="-Wl,-rpath,OZCL -LOZCL" \
  --with-debug \
  --with-ipv6 \
  --with-http_ssl_module \
  --with-http_stub_status_module \
  --with-pcre \
  --with-http_upstream_zmauth_module \
  --with-http_zm_sso_module \
  --with-http_spdy_module \
  --with-mail \
  --with-mail-sasl \
  --with-mail_ssl_module \
  --error-log-path=/opt/zimbra/log/nginx.log \
  --http-log-path=/opt/zimbra/log/nginx.access.log \
  --http-client-body-temp-path=/opt/zimbra/data/tmp/nginx/client \
  --http-proxy-temp-path=/opt/zimbra/data/tmp/nginx/proxy \
  --http-fastcgi-temp-path=/opt/zimbra/data/tmp/nginx/fastcgi \
  --without-http_scgi_module \
  --without-http_uwsgi_module \
  --add-module=modules/nviennot-nginx-tcp-keepalive \
  --add-module=modules/nginx-module-txid120
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/data/nginx
mv ${RPM_BUILD_ROOT}OZC/html ${RPM_BUILD_ROOT}/opt/zimbra/data/nginx/

%files
%defattr(-,root,root)
OZC/sbin
/opt/zimbra/data/nginx
%exclude OZC/conf
