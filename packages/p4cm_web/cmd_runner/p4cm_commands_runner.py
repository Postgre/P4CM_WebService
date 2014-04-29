from django.conf import settings
from cmd_runner.p4_commands_runner import P4CommandsRunner

__author__ = 'ericqu'


class P4CMCommandsRunner(P4CommandsRunner):
    label = ''
    supported_params = []

    def executable(self):
        return getattr(settings, "P4CM_EXECUTABLE", "p4cm")

    # def extra_path(self):
    #     path = super(P4CMCommandsRunner, self).extra_path()
    #     return "%s:%s" % (path, "/Users/ericqu/Workspace/equ_CM_P4CM_main_dev_mac")

    def compose_command(self, cmd='p4cm', **kwargs):
        if not self.label:
            raise KeyError("label must have a value")
        command = [self.executable(), self.label]
        for opt in self.supported_params:
            if opt in kwargs:
                command.append('--%s' % opt.replace('_', '-'))
                if kwargs[opt] and not kwargs[opt] == 'True':
                    command.append(kwargs[opt])

        return " ".join(command)

    def run(self):
        result = super(P4CMCommandsRunner, self).run()

        data = {
            'succeeded': result.succeeded,
            'message': result.stdout,
            'error': result.stderr,
        }

        return data


class P4CMInfoRunner(P4CMCommandsRunner):
    label = 'info'
    supported_params = ['codeline']


class P4CMConfigRunner(P4CMCommandsRunner):
    label = 'config'
    supported_params = ['codeline',
                        'output',
                        'fail_on_overlap',
                        'include_pretag',
                        'ignore_codeline_missing',
                        'batch',
                        ]

