import os
import subprocess

from dashops.common.errors import CliRuntimeError


def execute_command(cmd):
    ret = subprocess.call(cmd, shell=True, env=os.environ)
    if ret != 0:
        raise CliRuntimeError('Executing {} failed!'.format(cmd))


def export_env(key, value):
    os.environ[key] = value


def export_common_envs(cluster_name, s3_bucket):
    export_env('CLUSTER_NAME', cluster_name)
    export_env('KOPS_STATE_STORE', 's3://{}'.format(s3_bucket))
