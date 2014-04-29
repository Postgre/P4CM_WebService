from logging import getLogger
import os
import tempfile

from django.conf import settings

from fabric.context_managers import shell_env, settings as fab_settings, prefix, cd
from fabric.operations import local


__author__ = 'ericqu'


class BaseP4Command(object):
    def __init__(self, env):
        self.env = env
        self.executable = settings.P4_EXECUTABLE
        self.logger = getLogger(__name__)

    def run(self, command, capture=True):
        self.logger.debug(command)
        with fab_settings(warn_only=True):
            with shell_env(**self.env.dict()):
                result = local(command, capture=capture)

                if not result.succeeded:
                    self.logger.error(result.stderr)
                    print result.stderr

                return result


class P4Login(BaseP4Command):
    def login_status(self):
        command = "{p4exec} login -s"

        result = self.run(command.format(p4exec=self.executable))

        return result.succeeded


class P4Client(BaseP4Command):

    def create_temp_workspace(self):
        pre_workspace = "%s_%s_" % (self.env.user, "P4CM_WEB_TEMP")

        tmp_workspace_path = tempfile.mkdtemp(suffix="", prefix=pre_workspace)
        self.create_p4config_file(tmp_workspace_path)

        return tmp_workspace_path

    def delete_temp_workspace(self, workspace):
        if os.path.isabs(workspace):
            client_name = os.path.basename(workspace)
            root = workspace
        else:
            client_name = workspace
            root = os.path.join(tempfile.gettempdir(), workspace)
        with cd(root):
            self.delete_client(client_name)

        if os.path.exists(root):
            self.run('rm -rf %s' % root)

    def create_p4config_file(self, workspace):
        with open(os.path.join(workspace, self.env.p4config), 'w') as f:
            f.write("P4PORT=%s\n" % self.env.port)
            f.write("P4USER=%s\n" % self.env.user)
            f.write("P4CHARSET=%s\n" % self.env.charset)

            if self.env.workspace:
                f.write("P4CLIENT=%s\n" % self.env.workspace)

    def unlock_client(self, name):
        if not self.client_exists(name):
            return False

        command = "{p4exec} client -o {name}"
        result = self.run(command.format(p4exec=self.executable, name=name))

        spec = result.stdout
        if spec.count('unlocked') == 0:
            new_spec = spec.replace('Description:', 'Description: TO_DELETE')
            new_spec = new_spec.replace('locked', 'unlocked')
            result = self.run('echo "%s" | p4 client -i' % new_spec)

        return result.succeeded

    def client_exists(self, name):
        command = "{p4exec} clients -e {name}"
        result = self.run(command.format(p4exec=self.executable, name=name))

        return result.succeeded and result.stdout and result.stdout.count(name) > 0

    def delete_client(self, name):
        if not self.client_exists(name):
            return True

        self.unlock_client(name)
        command = "{p4exec} client -d {name}"
        result = self.run(command.format(p4exec=self.executable, name=name))

        return result.succeeded

    def clone_client(self, name, template, root):
        command = "{p4exec} client -o -t {template} {name}"

        with prefix("cd %s" % root):
            result = self.run(command.format(p4exec=self.executable, template=template, name=name))
            spec = str(result.stdout)
            new_spec = spec.replace('Created by', 'TO_DELETE')
            new_spec = new_spec.replace('locked', 'unlocked')
            result = self.run('echo "%s" | p4 client -i' % new_spec)

        return result.succeeded




