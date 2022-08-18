Summary:	Zimbra's erlang
Name:		zimbra-erlang
Version:	VERSION
Release:	1zimbra8.8b1ZAPPEND
License:	ASL 2.0
URL:		https://www.erlang.org
Source:         %{name}-%{version}.tar.gz
Packager:       Zimbra Packaging Services <packaging-devel@zimbra.com>
Patch1:         otp-0001-Do-not-format-man-pages-and-do-not-install-miscellan.patch
Patch2:         otp-0002-Do-not-install-C-sources.patch
Patch3:         otp-0003-Do-not-install-erlang-sources.patch
BuildRequires:	ncurses-devel, zlib-devel
BuildRequires:	zimbra-openssl-devel >= 1.1.1q-1zimbra8.7b4ZAPPEND
Requires:       zimbra-openssl-libs >= 1.1.1q-1zimbra8.7b4ZAPPEND
AutoReqProv:    no

%description
The Zimbra erlang build

%define debug_package %{nil}

%prep
%setup -n otp-OTP-%{version}
%patch1 -p1 -b .Do_not_format_man_pages_and_do_not_install_miscellan
%patch2 -p1 -b .Do_not_install_C_sources
%patch3 -p1 -F2 -b .Do_not_install_erlang_sources

chmod 644 lib/kernel/examples/uds_dist/c_src/Makefile
chmod 644 lib/kernel/examples/uds_dist/src/Makefile
chmod 644 lib/ssl/examples/certs/Makefile
chmod 644 lib/ssl/examples/src/Makefile


%build
LDFLAGS="-Wl,-rpath,OZCL:OZCL"; export LDFLAGS; \
./configure --prefix=OZC \
 --without-javac \
 --with-ssl=/opt/zimbra/common \
 --with-ssl-incl=OZC \
 --enable-m64-build \
 --with-ssl-rpath=OZCL \
 --with-ssl-lib-subdir=OZCL
make clean
touch lib/common_test/SKIP
touch lib/debugger/SKIP
touch lib/dialyzer/SKIP
touch lib/diameter/SKIP
touch lib/edoc/SKIP
touch lib/et/SKIP
touch lib/erl_docgen/SKIP
touch lib/ftp/SKIP
touch lib/jinterface/SKIP
touch lib/megaco/SKIP
touch lib/observer/SKIP
touch lib/odbc/SKIP
touch lib/ssh/SKIP
touch lib/tftp/SKIP
touch lib/wx/SKIP
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
# Do not install info files - they are almost empty and useless
find %{buildroot}OZCL/erlang -type f -name info -exec rm -f {} \;
chmod 0755 %{buildroot}OZCL/erlang/bin
rm -f %{buildroot}OZCL/erlang/man/man1/erlsrv.*
rm -f %{buildroot}OZCL/erlang/man/man1/werl.*
rm -f %{buildroot}OZCL/erlang/man/man3/win32reg.*
rm -r %{buildroot}OZCL/erlang/erts-*/man
rm -f %{buildroot}OZCL/erlang/Install
rm -rf %{buildroot}OZCB/ct_run
rm -rf %{buildroot}OZCB/dialyzer
rm -rf %{buildroot}OZCB/run_test
rm -rf %{buildroot}OZCB/typer
rm -rf %{buildroot}OZCL/erlang/bin/ct_run
rm -rf %{buildroot}OZCL/erlang/bin/erl_call
rm -rf %{buildroot}OZCL/erlang/bin/dialyzer
rm -rf %{buildroot}OZCL/erlang/bin/run_test
rm -rf %{buildroot}OZCL/erlang/bin/typer
rm -rf %{buildroot}OZCL/erlang/erts-*/bin/ct_run
rm -rf %{buildroot}OZCL/erlang/erts-*/bin/erl_call
rm -rf %{buildroot}OZCL/erlang/erts-*/bin/dialyzer
rm -rf %{buildroot}OZCL/erlang/erts-*/bin/typer
rm -rf %{buildroot}OZCL/erlang/erts-*/bin/yielding_c_fun
rm -rf %{buildroot}OZCL/erlang/lib/*/examples

%files
%defattr(-,root,root)

%dir OZCL/erlang/lib/asn1-*/
OZCL/erlang/lib/asn1-*/ebin
OZCL/erlang/lib/asn1-*/priv
OZCL/erlang/lib/asn1-*/src
OZCL/erlang/lib/compiler-*/
OZCL/erlang/lib/crypto-*/

%dir OZCL/erlang/lib/eldap-*/
OZCL/erlang/lib/eldap-*/asn1
OZCL/erlang/lib/eldap-*/ebin
OZCL/erlang/lib/eldap-*/include
OZCL/erlang/lib/eldap-*/src
OZCL/erlang/lib/eunit-*/
OZCL/erlang/lib/erl_interface-*/

%dir OZCL/erlang/
%dir OZCL/erlang/bin/
%dir OZCL/erlang/lib/
%dir OZCL/erlang/releases/
OZCB/epmd
OZCB/erl
OZCB/erlc
OZCB/escript
OZCB/run_erl
OZCB/to_erl
OZCL/erlang/bin/epmd
OZCL/erlang/bin/erl
OZCL/erlang/bin/erlc
OZCL/erlang/bin/escript
OZCL/erlang/bin/no_dot_erlang.boot
OZCL/erlang/bin/run_erl
OZCL/erlang/bin/start
OZCL/erlang/bin/start.boot
OZCL/erlang/bin/start.script
OZCL/erlang/bin/start_clean.boot
OZCL/erlang/bin/start_erl
OZCL/erlang/bin/start_sasl.boot
OZCL/erlang/bin/to_erl
%dir OZCL/erlang/erts-*/bin
OZCL/erlang/erts-*/bin/beam.smp
OZCL/erlang/erts-*/bin/erl_child_setup
OZCL/erlang/erts-*/bin/dyn_erl
OZCL/erlang/erts-*/bin/epmd
OZCL/erlang/erts-*/bin/erl
OZCL/erlang/erts-*/bin/erl.src
OZCL/erlang/erts-*/bin/erlc
OZCL/erlang/erts-*/bin/erlexec
OZCL/erlang/erts-*/bin/escript
OZCL/erlang/erts-*/bin/heart
OZCL/erlang/erts-*/bin/inet_gethost
OZCL/erlang/erts-*/bin/run_erl
OZCL/erlang/erts-*/bin/start
OZCL/erlang/erts-*/bin/start.src
OZCL/erlang/erts-*/bin/start_erl.src
OZCL/erlang/erts-*/bin/to_erl
OZCL/erlang/erts-*/include
OZCL/erlang/erts-*/lib
OZCL/erlang/erts-*/src
OZCL/erlang/lib/erts-*/
OZCL/erlang/releases/*
OZCL/erlang/usr/

%dir OZCL/erlang/lib/inets-*/
OZCL/erlang/lib/inets-*/ebin
OZCL/erlang/lib/inets-*/include
OZCL/erlang/lib/inets-*/priv
OZCL/erlang/lib/inets-*/src

%dir OZCL/erlang/lib/kernel-*/
OZCL/erlang/lib/kernel-*/ebin
OZCL/erlang/lib/kernel-*/include
OZCL/erlang/lib/kernel-*/src

%dir OZCL/erlang/lib/mnesia-*/
OZCL/erlang/lib/mnesia-*/ebin
OZCL/erlang/lib/mnesia-*/include
OZCL/erlang/lib/mnesia-*/src
OZCL/erlang/lib/os_mon-*/
OZCL/erlang/lib/parsetools-*/
OZCL/erlang/lib/public_key-*/

%dir OZCL/erlang/lib/reltool-*/
OZCL/erlang/lib/reltool-*/ebin
OZCL/erlang/lib/reltool-*/src

%dir OZCL/erlang/lib/syntax_tools-*/
OZCL/erlang/lib/syntax_tools-*/ebin
OZCL/erlang/lib/syntax_tools-*/include
OZCL/erlang/lib/runtime_tools-*/

%dir OZCL/erlang/lib/sasl-*/
OZCL/erlang/lib/sasl-*/ebin
OZCL/erlang/lib/sasl-*/src

%dir OZCL/erlang/lib/snmp-*/
OZCL/erlang/lib/snmp-*/bin
OZCL/erlang/lib/snmp-*/ebin
OZCL/erlang/lib/snmp-*/include
OZCL/erlang/lib/snmp-*/mibs
OZCL/erlang/lib/snmp-*/priv
OZCL/erlang/lib/snmp-*/src

%dir OZCL/erlang/lib/ssl-*/
OZCL/erlang/lib/ssl-*/ebin
OZCL/erlang/lib/ssl-*/src

%dir OZCL/erlang/lib/stdlib-*/
OZCL/erlang/lib/stdlib-*/ebin
OZCL/erlang/lib/stdlib-*/include
OZCL/erlang/lib/stdlib-*/src
OZCL/erlang/lib/tools-*/
OZCL/erlang/lib/xmerl-*/

%changelog
* Mon Aug 08 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
- Initial Release.
