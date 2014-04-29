import logging
import os
import tempfile
from cmd_runner.runners import CommandsRunner
from django.conf import settings
from common.p4commands import P4Client
from fabric.context_managers import prefix
from fabric.operations import local

__author__ = 'ericqu'

logger = logging.getLogger('p4cm_web')


class P4CommandsRunner(CommandsRunner):
    workspace = None

    def __init__(self, environ, **kwargs):
        super(P4CommandsRunner, self).__init__(environ, **kwargs)
        self.agent = P4Client(environ)
        self.workspace_managed = environ.workspace is None

    def executable(self):
        return settings.P4_EXECUTABLE

    def extra_path(self):
        return "/usr/local/bin:/usr/local/sbin:~/bin"

    def pre_action(self):
        if self.workspace_managed:
            self.workspace = self.agent.create_temp_workspace()
            if self.env.client:
                self.agent.clone_client(os.path.basename(self.workspace), self.env.client, self.workspace)
        else:
            self.workspace = self.env.workspace

        return super(P4CommandsRunner, self).pre_action()

    def post_action(self, result):
        if self.workspace_managed and self.workspace:
            self.agent.delete_temp_workspace(self.workspace)

        return super(P4CommandsRunner, self).post_action(result)

    def run_command(self):
        with prefix("cd %s" % self.workspace):
            result = super(P4CommandsRunner, self).run_command()

            return result


class P4ClientRunner(P4CommandsRunner):

    def compose_command(self, **kwargs):
        if "list" in kwargs:
            return "%s %s" % (self.executable(), "clients")
        elif "clone_to_temp" in kwargs:
            p4client = P4Client(self.env)
            root = p4client.create_temp_workspace()
            p4client.clone_client(os.path.basename(root), self.env.client, root)

        else:
            return "%s %s -o %s" % (self.executable(), "client", kwargs['pk'])


