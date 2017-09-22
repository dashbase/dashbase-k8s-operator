import os
import subprocess


def execute_command(cmd):
    subprocess.call(cmd, shell=True, env=os.environ)


def export_env(key, value):
    os.environ[key] = value


def export_common_envs(cluster_name, s3_bucket):
    export_env('CLUSTER_NAME', cluster_name)
    export_env('KOPS_STATE_STORE', 's3://{}'.format(s3_bucket))
