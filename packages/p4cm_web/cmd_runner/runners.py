import os
from fabric.context_managers import shell_env, settings, path
from fabric.api import local
from fabric.state import env

__author__ = 'ericqu'


class CommandsRunner(object):
    required_keys = []
    args = None

    def __init__(self, environ, **kwargs):
        self.validate(**kwargs)
        self.args = kwargs
        self.env = environ
        self.command = self.compose_command(**kwargs)

    def executable(self):
        raise NotImplementedError("Must provide a executable command")

    def run(self):
        with settings(warn_only=True):
            if self.extra_path() != "":
                with path(self.extra_path()):
                    with shell_env(**self.shell_env()):
                        self.pre_action()
                        result = self.run_command()
                        self.post_action(result)
            else:
                with shell_env(**self.env):
                    self.pre_action()
                    result = self.run_command()
                    self.post_action(result)

        return result

    def extra_path(self):
        return ""

    def shell_env(self):
        return self.env.dict()

    def compose_command(self, **kwargs):
        raise NotImplementedError

    def run_command(self):
        return local(self.command, capture=True)

    def validate(self, **kwargs):
        for k in self.required_keys:
            if not k in kwargs:
                raise ValueError("%s is required" % k)

    def pre_action(self):
        pass

    def post_action(self, result):
        pass
