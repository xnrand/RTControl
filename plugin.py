###
# 2017, grumble
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

from RTControl.util import *
import sys

if sys.hexversion < 0x03040000:
    # Raising this as SyntaxError so that it is shown to whoever tries to load the module
    raise SyntaxError('Python <3.4 does not provide easily secure means of opening HTTPS connections. This plugin will not work with Python <3.4.')

import http.client, urllib.parse, ssl, base64

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization("RTControl")
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class RTControl(callbacks.Plugin):
    """Send REST requests to RT"""

    @cmd("int")
    def spam(self, irc, msg, args, ticketnum):
        """<ticket ID>

        Moves the ticket in question to the spam queue"""

        assertThat(ticketnum >= self.registryValue("minID"), "Your Ticket ID is too small")
        assertThat(ticketnum <= self.registryValue("maxID"), "Your Ticket ID is too big")

        self.log.info("Moving %s to spam queue as per %s's request" % (ticketnum, msg.prefix))

        connection = self.connect_to_rt()
        reply = self.request_rt(connection, "ticket/" + str(ticketnum), "Queue: Spam")
        reply = reply.replace("\n","  ")

        assertThat(len(reply.strip()) > 0, "No changes were made")

        irc.reply(reply)

    def connect_to_rt(self):
        host = self.registryValue('host')
        port = self.registryValue('port')
        ciphers = self.registryValue('ciphers')

        if self.registryValue('ssl'):
            context = ssl.create_default_context() # new in python 3.4: uses system trust store
            context.options |= ssl.OP_NO_SSLv2
            context.options |= ssl.OP_NO_SSLv3
            context.options |= ssl.OP_NO_TLSv1
            context.options |= ssl.OP_NO_TLSv1_1
            context.set_ciphers(ciphers)

            return http.client.HTTPSConnection(host, port=port, context=context)
        else:
            return http.client.HTTPConnection(host, port=port)

    def headers(self):
        username = self.registryValue('httpUser')
        password = self.registryValue('httpPassword')

        return {
            "Connection": "keep-alive",
            "Accept": "text/plain",
            "Authorization": "Basic %s" % base64.b64encode(
                ('%s:%s' % (username, password)).encode('utf8')
            ).decode('utf8')
        }

    def request_rt(self, connection, path, content=None):
        apipath = self.registryValue("path")

        if content:
            method = "POST"
            body = urllib.parse.urlencode({'content': content})
        else:
            method = "GET"
            body = None

        connection.request(method, apipath+path, body=body, headers=self.headers())
        resp = connection.getresponse()

        assertThat(resp.status // 100 == 2, "HTTP Request failed with %s %s" %
            (resp.status, resp.reason))

        return resp.read().decode('utf8', 'replace')

Class = RTControl
