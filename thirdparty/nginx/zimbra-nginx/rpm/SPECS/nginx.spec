Summary:            Zimbra's nginx build
Name:               zimbra-nginx
Version:            VERSION
Release:            1zimbra8.8b4ZAPPEND
License:            MIT
Source:             %{name}-%{version}.tar.gz
Patch0: 			nginx_auto_cc.patch
Patch1: 			nginx_auto_lib.patch
Patch2: 			nginx_auto_modules.patch
Patch3: 			nginx_auto_options.patch
Patch4: 			nginx_auto_sources.patch
Patch5: 			nginx_README.patch
Patch6: 			nginx_src_core.patch
Patch7: 			nginx_src_event.patch
Patch8: 			nginx_src_http.patch
Patch9: 			nginx_src_mail_ngx_mail.patch
Patch10: 			nginx_src_mail_ngx_mail_auth_http_module.patch
Patch11: 			nginx_src_mail_ngx_mail_core_module.patch
Patch12: 			nginx_src_mail_ngx_mail_handler.patch
Patch13: 			nginx_src_mail_ngx_mail_imap_handler.patch
Patch14: 			nginx_src_mail_ngx_mail_imap_module_c.patch
Patch15: 			nginx_src_mail_ngx_mail_imap_module_h.patch
Patch16: 			nginx_src_mail_ngx_mail_parse.patch
Patch17: 			nginx_src_mail_ngx_mail_pop3_handler.patch
Patch18: 			nginx_src_mail_ngx_mail_pop3_module_c.patch
Patch19: 			nginx_src_mail_ngx_mail_pop3_module_h.patch
Patch20: 			nginx_src_mail_ngx_mail_proxy_module.patch
Patch21: 			nginx_src_mail_ngx_mail_smtp_module.patch
Patch22: 			nginx_docs.patch

BuildRequires:      pcre-devel, zlib-devel
BuildRequires:      zimbra-openssl-devel >= 3.0.9-1zimbra8.8b1ZAPPEND
BuildRequires:      zimbra-cyrus-sasl-devel >= 2.1.28-1zimbra8.7b4ZAPPEND
Requires:           pcre, zlib
Requires:           zimbra-openssl-libs >= 3.0.9-1zimbra8.8b1ZAPPEND
Requires:           zimbra-cyrus-sasl-libs >= 2.1.28-1zimbra8.7b4ZAPPEND, zimbra-proxy-base
AutoReqProv:        no
URL:                http://nginx.org

%description
The Zimbra nginx build

%changelog
* Tue Jun 13 2023  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b4ZAPPEND
- ZBUG-3355, Upgraded OpenSSL to 3.0.9
* Fri May 06 2022  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b3ZAPPEND
- Fix ZBUG-2738
* Wed Jul 07 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b2ZAPPEND
- Fix ZBUG-2299
* Tue Jun 08 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
- Upgraded nginx to 1.20.0
* Wed Dec 02 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b3ZAPPEND
- Fix ZBUG-2098
* Wed Dec 02 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
- Upgraded nginx to 1.19.0
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1

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
  --with-http_v2_module \
  --with-pcre \
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
  --add-module=zmmodules/http/sso \
  --add-module=zmmodules/http/upstreamzmauth \
  --add-module=zmmodules/mail/zmauth \
  --add-module=zmmodules/mail/throttle
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
