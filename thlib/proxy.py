# -*- coding: utf8 -*-

# Requires python-ntlm (http://code.google.com/p/python-ntlm/) package
from thlib.side.ntlm import HTTPNtlmAuthHandler
import xmlrpclib
import base64
import cookielib
from urllib import unquote, splittype, splithost
import urllib2
from thlib.environment import env_server


useAuthOnProxy = True

httpAuthName = "admin"
httpAuthPassword = "admin"
serverTopLevelURL = "http://my.server.com"


class UrllibTransport(xmlrpclib.Transport, object):
    def __init__(self):
        super(self.__class__, self).__init__(None)
        self.proxy = env_server.get_proxy()
        self.proxy_user = self.proxy['login']
        self.proxy_pass = self.proxy['pass']
        self.proxy_server = self.proxy['server']
        self.proxy_enabled = self.proxy['enabled']

    def update_proxy(self, proxy_dict=None):
        if proxy_dict:
            self.proxy = proxy_dict
        else:
            self.proxy = env_server.get_proxy()
        self.proxy_user = self.proxy['login']
        self.proxy_pass = self.proxy['pass']
        self.proxy_server = self.proxy['server']
        self.proxy_enabled = self.proxy['enabled']
        if not self.proxy_enabled:
            self.proxyurl = None

    def disable_proxy(self):
        self.proxy_enabled = False

    def enable_proxy(self):
        self.proxy_enabled = True

    def request(self, host, handler, request_body, verbose=0):
        self.verbose = verbose

        if self.proxy_enabled:
            if self.proxy_server.startswith('http://'):
                proxy_server = self.proxy_server[7:]
            else:
                proxy_server = self.proxy_server
            if useAuthOnProxy:
                self.proxyurl = 'http://{0}:{1}@{2}'.format(self.proxy_user, self.proxy_pass, proxy_server)
            else:
                self.proxyurl = proxy_server
        else:
            self.proxyurl = None

        puser_pass = None

        if self.proxyurl is not None:
            type, r_type = splittype(self.proxyurl)
            phost, XXX = splithost(r_type)

            if '@' in phost:
                user_pass, phost = phost.split('@', 1)
                if ':' in user_pass:
                    self.proxy_user, self.proxy_pass = user_pass.split(':', 1)
                    puser_pass = base64.encodestring(
                        '%s:%s' % (unquote(self.proxy_user), unquote(self.proxy_pass))).strip()

            proxies = {'http': 'http://%s' % phost, 'https': None}

        host = unquote(host)
        address = "http://%s%s" % (host, handler)

        request = urllib2.Request(address)
        request.add_data(request_body)
        request.add_header('User-agent', self.user_agent)
        request.add_header("Content-Type", "text/xml")

        # HTTP Auth
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        top_level_url = serverTopLevelURL
        password_mgr.add_password(None,
                                  top_level_url,
                                  httpAuthName,
                                  httpAuthPassword)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)

        # Cookies
        cj = cookielib.CookieJar()

        if puser_pass:
            # NTLM
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, serverTopLevelURL, self.proxy_user, self.proxy_pass)

            authNTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)
            request.add_header('Proxy-authorization', 'Basic ' + puser_pass)

            proxy_support = urllib2.ProxyHandler(proxies)

            opener = urllib2.build_opener(handler, proxy_support,
                                          urllib2.HTTPCookieProcessor(cj),
                                          authNTLM)
        elif self.proxyurl:
            # Proxy without auth
            proxy_support = urllib2.ProxyHandler(proxies)
            opener = urllib2.build_opener(proxy_support,
                                          handler,
                                          urllib2.HTTPCookieProcessor(cj))
        else:
            # Direct connection
            proxy_support = urllib2.ProxyHandler({})
            opener = urllib2.build_opener(proxy_support,
                                          handler,
                                          urllib2.HTTPCookieProcessor(cj))

        urllib2.install_opener(opener)

        response = urllib2.urlopen(request, timeout=env_server.get_timeout())
        return self.parse_response(response)
