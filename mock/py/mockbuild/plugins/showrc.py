# -*- coding: utf-8 -*-
# vim:expandtab:autoindent:tabstop=4:shiftwidth=4:filetype=python:textwidth=0:
# License: GPL2 or later see COPYING

# python library imports
import codecs

# our imports
from mockbuild.trace_decorator import getLog, traceLog
import mockbuild.util

requires_api_version = "1.1"


# plugin entry point
@traceLog()
def init(plugins, conf, buildroot):
    ShowRC(plugins, conf, buildroot)


class ShowRC(object):
    # pylint: disable=too-few-public-methods
    """Get the runtime rpm --showrc"""
    @traceLog()
    def __init__(self, plugins, conf, buildroot):
        self.buildroot = buildroot
        self.showrc_opts = conf
        self.config = buildroot.config

        # actually run our plugin at this step
        plugins.add_hook("prebuild", self._PreBuildHook)

    # =============
    # 'Private' API
    # =============
    @traceLog()
    def _PreBuildHook(self):
        getLog().info("enabled ShowRC plugin")

        out_file = self.buildroot.resultdir + '/showrc.log'
        with codecs.open(out_file, 'w', 'utf-8', 'replace') as out:

            cmd = ["/usr/bin/rpm", "--showrc"]
            output = mockbuild.util.do(cmd, shell=False, returnOutput=True, raiseExc=False)
            out.write(output)

        self.buildroot.uid_manager.changeOwner(out_file, gid=self.config['chrootgid'])
