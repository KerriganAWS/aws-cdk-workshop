import os
from aws_cdk import (
    aws_ec2 as ec2,
    core
)

instanceName = "workshop-ec2-instance"
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )

# A couple of ways that you can use to look up existing AWS VPC are below.
# 1. ec2.Vpc.from_lookup(self, "vpc", vpc_name="vpc-stack/workshop_VPC")
# 2. ec2.Vpc.from_lookup(self, "vpc", tags={"Name": "vpc-stack/workshop_VPC"})
# 3. ec2.Vpc.from_lookup(self, "vpc", vpc_id="12345678") // It's not recommendation. VPC id always changes after re-building.


class BastionEC2Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "vpc", vpc_name="default_vpc")

        bastion = ec2.BastionHostLinux(self, "bastion-host-instance",
                                       vpc=vpc,
                                       subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                       instance_name="bastion-host-instance",
                                       instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"))

        bastion.connections.allow_from_any_ipv4(ec2.Port.tcp(22), "Internet access SSH")
