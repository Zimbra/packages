echo -n "host name: "
read develbox

echo -n "devel domain: "
read develdomain

echo -n "ip address 1: "
read proxyip1

echo -n "ip address 2: "
read proxyip2

echo "zmprov ms ${develbox} zimbraImapCleartextLoginEnabled TRUE"
zmprov ms ${develbox} zimbraImapCleartextLoginEnabled TRUE
echo "zmprov ms ${develbox} zimbraImapBindPort 7143"
zmprov ms ${develbox} zimbraImapBindPort 7143
echo "zmprov ms ${develbox} zimbraImapSSLBindPort 7993"
zmprov ms ${develbox} zimbraImapSSLBindPort 7993
echo "zmprov ms ${develbox} zimbraImapProxyBindPort 143"
zmprov ms ${develbox} zimbraImapProxyBindPort 143
echo "zmprov ms ${develbox} zimbraImapSSLProxyBindPort 993"
zmprov ms ${develbox} zimbraImapSSLProxyBindPort 993
echo "zmprov ms ${develbox} zimbraImapSSLServerEnabled TRUE"
zmprov ms ${develbox} zimbraImapSSLServerEnabled TRUE
echo "zmprov ms ${develbox} zimbraPop3CleartextLoginEnabled TRUE"
zmprov ms ${develbox} zimbraPop3CleartextLoginEnabled TRUE
echo "zmprov ms ${develbox} zimbraPop3BindPort 7110"
zmprov ms ${develbox} zimbraPop3BindPort 7110
echo "zmprov ms ${develbox} zimbraPop3SSLBindPort 7995"
zmprov ms ${develbox} zimbraPop3SSLBindPort 7995
echo "zmprov ms ${develbox} zimbraPop3ProxyBindPort 110"
zmprov ms ${develbox} zimbraPop3ProxyBindPort 110
echo "zmprov ms ${develbox} zimbraPop3SSLProxyBindPort 995"
zmprov ms ${develbox} zimbraPop3SSLProxyBindPort 995
echo "zmprov ms ${develbox} zimbraPop3SSLServerEnabled TRUE"
zmprov ms ${develbox} zimbraPop3SSLServerEnabled TRUE
echo "zmprov ms ${develbox} zimbraMemcachedBindPort 11211"
zmprov ms ${develbox} zimbraMemcachedBindPort 11211
echo "zmprov ms ${develbox} zimbraReverseProxyMailEnabled TRUE"
zmprov ms ${develbox} zimbraReverseProxyMailEnabled TRUE
echo "zmprov ms ${develbox} zimbraReverseProxyLookupTarget TRUE"
zmprov ms ${develbox} zimbraReverseProxyLookupTarget TRUE
echo "zmprov ms ${develbox} +zimbraServiceEnabled proxy"
zmprov ms ${develbox} +zimbraServiceEnabled proxy
echo "zmprov ms ${develbox} zimbraReverseProxyImapSaslGssapiEnabled TRUE"
zmprov ms ${develbox} zimbraReverseProxyImapSaslGssapiEnabled TRUE
echo "zmprov ms ${develbox} zimbraReverseProxyPop3SaslGssapiEnabled TRUE"
zmprov ms ${develbox} zimbraReverseProxyPop3SaslGssapiEnabled TRUE
echo "zmprov ms ${develbox} zimbraReverseProxyDefaultRealm EXAMPLE.COM"
zmprov ms ${develbox} zimbraReverseProxyDefaultRealm EXAMPLE.COM
echo "zmprov ms ${develbox} zimbraReverseProxyImapStartTlsMode on"
zmprov ms ${develbox} zimbraReverseProxyImapStartTlsMode on
echo "zmprov ms ${develbox} zimbraReverseProxyPop3StartTlsMode on"
zmprov ms ${develbox} zimbraReverseProxyPop3StartTlsMode on

if [ -n "${proxyip1}" ]; then
  echo "zmprov mcf +zimbraReverseProxyAdminIPAddress ${proxyip1}"
  zmprov mcf +zimbraReverseProxyAdminIPAddress ${proxyip1}
fi

if [ -n "${proxyip2}" ]; then
  echo "zmprov mcf +zimbraReverseProxyAdminIPAddress ${proxyip2}"
  zmprov mcf +zimbraReverseProxyAdminIPAddress ${proxyip2}
fi

if [ -n "${proxyip1}" ]; then
  echo "zmprov md ${develdomain} +zimbraVirtualIPAddress ${proxyip1}"
  zmprov md ${develdomain} +zimbraVirtualIPAddress ${proxyip1}
fi

if [ -n "${proxyip2}" ]; then
  echo "zmprov md ${develdomain} +zimbraVirtualIPAddress ${proxyip2}"
  zmprov md ${develdomain} +zimbraVirtualIPAddress ${proxyip2}
fi

echo "zmprov ms ${develbox} zimbraMailMode http"
zmprov ms ${develbox} zimbraMailMode http
echo "zmprov ms ${develbox} zimbraReverseProxyMailMode mixed"
zmprov ms ${develbox} zimbraReverseProxyMailMode mixed
echo "zmprov ms ${develbox} zimbraMailReferMode reverse-proxied"
zmprov ms ${develbox} zimbraMailReferMode reverse-proxied
echo "zmprov ms ${develbox} zimbraMailPort 7070"
zmprov ms ${develbox} zimbraMailPort 7070
echo "zmprov ms ${develbox} zimbraMailProxyPort 80"
zmprov ms ${develbox} zimbraMailProxyPort 80
echo "zmprov ms ${develbox} zimbraMailSSLPort 7443"
zmprov ms ${develbox} zimbraMailSSLPort 7443
echo "zmprov ms ${develbox} zimbraMailSSLProxyPort 443"
zmprov ms ${develbox} zimbraMailSSLProxyPort 443
echo "zmprov ms ${develbox} zimbraReverseProxyHttpEnabled TRUE"
zmprov ms ${develbox} zimbraReverseProxyHttpEnabled TRUE

if [ -n "${proxyip1}" ]; then
  echo "zmprov md ${develdomain} +zimbraVirtualHostname ${proxyip1}"
  zmprov md ${develdomain} +zimbraVirtualHostname ${proxyip1}
fi

if [ -n "${proxyip2}" ]; then
  echo "zmprov md ${develdomain} +zimbraVirtualHostname ${proxyip2}"
  zmprov md ${develdomain} +zimbraVirtualHostname ${proxyip2}
fi

