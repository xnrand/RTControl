###
# 2017, grumble
###

import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization("RTControl")
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin("RTControl", True)


RTControl = conf.registerPlugin("RTControl")
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(RTControl, "someConfigVariableName",
#     registry.Boolean(False, _("""Help for someConfigVariableName.""")))

conf.registerGlobalValue(RTControl, "ssl",
    registry.Boolean(True, _("Use SSL/TLS to connect to RT")))

conf.registerGlobalValue(RTControl, "ciphers",
    registry.String("ECDHE-ECDSA-AES256-GCM-SHA384:"+
        "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:"+
        "ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:"+
        "ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:"+
        "ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:"+
        "ECDHE-RSA-AES128-SHA256",
        _("OpenSSL ciphersuite to use for connecting to the server")))

conf.registerGlobalValue(RTControl, "host",
    registry.String("rt.example.com", _("Hostname of the RT REST interface")))

conf.registerGlobalValue(RTControl, "port",
    registry.PositiveInteger(443, _("Port of the RT REST interface")))

conf.registerGlobalValue(RTControl, "path",
    registry.String("/REST/1.0/", _("RT REST base URL, with leading and trailing slash!")))

conf.registerGlobalValue(RTControl, "httpUser",
    registry.String("", _("HTTP Basic Auth username"), private=True))

conf.registerGlobalValue(RTControl, "httpPassword",
    registry.String("", _("HTTP Basic Auth password"), private=True))

conf.registerGlobalValue(RTControl, "minID",
    registry.PositiveInteger(100000, _("Minimum RT ticket ID that will be available to edit.")))

conf.registerGlobalValue(RTControl, "maxID",
    registry.PositiveInteger(999999, _("Maximum RT ticket ID that will be available to edit.")))

conf.registerGlobalValue(RTControl, "timeout",
    registry.PositiveInteger(3, _("Connection timeout in seconds, large values can significantly slow down your bot")))
