import os
import sys
from collections import defaultdict

def get_cmd_arg(name):
    d = defaultdict(list)
    for cmd_args in sys.argv[1:]:
        cmd_arg = cmd_args.split('=')
        if len(cmd_arg) == 2:
            d[cmd_arg[0].lstrip('-')].append(cmd_arg[1])

    if name in d:
        return d[name][0]
    else:
        print('Unknown command line arg requested: {}'.format(name))

def get_env_var(name):
    if name in os.environ:
        return os.environ[name]
    else:
        print('Unknown environment variable requested: {}'.format(name))
            
def get_rabbitmq_binder():
    return get_env_var('SPRING_RABBITMQ_HOST')

def get_rabbitmq_binder_username():
    return get_env_var('SPRING_RABBITMQ_USERNAME')

def get_rabbitmq_binder_password():
    return get_env_var('SPRING_RABBITMQ_PASSWORD')

def get_input_queue():
    return get_cmd_arg("spring.cloud.stream.bindings.input.destination") +"."+ get_cmd_arg("spring.cloud.stream.bindings.input.group")

def get_output_queue():
    return get_cmd_arg("spring.cloud.stream.bindings.output.destination") +"."+ get_cmd_arg("spring.cloud.stream.bindings.input.group")

def get_reverse_string():
    return get_cmd_arg("reversestring")

def get_healthcheck_port():
    return get_cmd_arg("server.port")