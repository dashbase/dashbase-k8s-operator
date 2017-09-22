import click
from click import UsageError
from pyformatter import Formatter, FormatType

from dashops.common.utils import execute_command, export_env, export_common_envs
from dashops.main import root
from dashops.parameters import ClusterNameParamType
from dashops.services import S3Service, KopsService


@root.command('create')
@click.argument('cluster-name', type=ClusterNameParamType(), nargs=1, expose_value=True)
@click.option('--s3-bucket', type=click.STRING,
              help='Specify the bucket to store cluster state.\nDefaults to cluster-name.')
@click.option('--machine-type', type=click.STRING, default='r4.xlarge', show_default=True,
              help='Specify the machine type to use in the cluster.')
@click.option('--num-nodes', type=click.IntRange(min=2), default=3, show_default=True,
              help='Specify number of nodes to start in the cluster.')
@click.option('--zone', type=click.STRING, default='us-west-1b', show_default=True, help='Specify the zone to use.')
@click.option('--region', type=click.STRING, default='us-west-1', show_default=True, help='Specify the region to use.')
@click.option('--vpc-id', type=click.STRING, help='Specify the vpc to use.')
@click.option('--network-cidr', type=click.STRING,
              help='Specify the network cidr of vpc.\nShould match the cidr of specified vpc.')
@click.option('--subnet-id', type=click.STRING, help='Specify the subnet-id to use.')
@click.option('--subnet-cidr', type=click.STRING, help='Specify the subnet cidr to create.')
@click.option('--edit', is_flag=True, help='If to edit the information before apply on aws.')
@click.pass_context
def create(ctx, cluster_name, s3_bucket, machine_type, num_nodes, zone, region, vpc_id, network_cidr, subnet_id,
           subnet_cidr, edit):
    """
    Create a cluster.
    """
    # validate input
    if not s3_bucket:
        s3_bucket = cluster_name
        ctx.param['s3_bucket'] = s3_bucket
    if region not in zone:
        raise UsageError('"zone" not in "region"!')
    if vpc_id and not network_cidr:
        raise UsageError('"network-cidr" should be specified if "vpc-id" is specified.')

    _validate_s3(s3_bucket, region)
    _create_cluster(cluster_name, s3_bucket, machine_type, num_nodes, zone, region, vpc_id, network_cidr, subnet_id,
                    subnet_cidr, edit)


def _validate_s3(s3_bucket, region):
    if s3_bucket not in S3Service.list_bucket(region_name=region):
        S3Service.create_bucket(s3_bucket, region_name=region)


def _create_cluster(cluster_name, s3_bucket, machine_type, num_nodes, zone, region, vpc_id, network_cidr, subnet_id,
                    subnet_cidr, edit):
    def _modify_subnet(key):
        formatter = Formatter(FormatType.YAML, S3Service.download(s3_bucket, key, region_name=region), human=True)
        if subnet_cidr:
            formatter.data['spec']['subnets'][0]['cidr'] = subnet_cidr
        if subnet_id:
            formatter.data['spec']['subnets'][0]['id'] = subnet_id
        S3Service.upload(s3_bucket, key, formatter.get_formatted_output(FormatType.YAML), region_name=region)

    # export necessary env
    export_common_envs(cluster_name, s3_bucket)
    if vpc_id is not None:
        export_env('VPC_ID', vpc_id)
        export_env('NETWORK_CIDR', network_cidr)

    # create cluster config
    execute_command(KopsService.get_create_command(cloud='aws', zones=zone, name=cluster_name, num_nodes=num_nodes,
                                                   machine_type=machine_type, vpc=vpc_id))
    if subnet_id or subnet_cidr:
        # modify config
        key = '/{}/config'.format(cluster_name)
        _modify_subnet(key)

        # modify cluster.spec
        key = '/{}/cluster.spec'.format(cluster_name)
        _modify_subnet(key)

    if edit:
        execute_command(KopsService.get_edit_command(cluster_name))
    execute_command(KopsService.get_update_command(cluster_name, yes=True))
