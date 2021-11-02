import os
from aws_cdk import (
    aws_ec2 as ec2,
    core
)
# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
# vpc = ec2.Vpc.from_lookup(self, "vpc", vpc_id=vpcID)

instanceName = "acer-ec2-instance"
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )


class BastionEC2NestedStack(core.NestedStack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bastion = ec2.BastionHostLinux(self, "bastion-host-instance",
                                       vpc=vpc,
                                       subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                       instance_name="bastion-host-instance",
                                       instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"))

        bastion.connections.allow_from_any_ipv4(ec2.Port.tcp(22), "Internet access SSH")
