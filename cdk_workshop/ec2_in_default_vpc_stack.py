from aws_cdk import (
    aws_ec2 as ec2,
    core
)
from aws_cdk.aws_autoscaling import BlockDevice


instanceName = "workshop-ec2-instance"
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )
# A couple of ways that you can use to look up existing AWS VPC are below.
# 1. ec2.Vpc.from_lookup(self, "vpc", vpc_name="vpc-stack/workshop_VPC")
# 2. ec2.Vpc.from_lookup(self, "vpc", tags={"Name": "vpc-stack/workshop_VPC"})
# 3. ec2.Vpc.from_lookup(self, "vpc", vpc_id="vpc-12345678") // It's not recommendation. VPC id always changes after rebuilding.
# https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/README.html


class EC2InDefaultVPCStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)
        host = ec2.Instance(self,
                            "ec2-instance",
                            instance_name=instanceName,
                            instance_type=ec2.InstanceType("t2.micro"),
                            machine_image=linux_ami,
                            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                            block_devices=[ec2.BlockDevice(
                                device_name="/dev/xvda", volume=ec2.BlockDeviceVolume.ebs(20))],
                            vpc=vpc)
        host.connections.allow_from_any_ipv4(ec2.Port.tcp(22), "Allow ssh from internet")
        host.connections.allow_from_any_ipv4(ec2.Port.tcp(80), "Allow http from internet")
        core.CfnOutput(self, "Output", value=host.instance_public_ip)
