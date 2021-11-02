from aws_cdk import (
    aws_ec2 as ec2,
    core
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
# vpc = ec2.Vpc.from_lookup(self, "vpc", vpc_id=vpcID)

instanceName = "workshop-ec2-instance"
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )


class EC2InDefaultVPCStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)
        ec2.Instance(self,
                     "ec2-instance",
                     instance_name=instanceName,
                     instance_type=ec2.InstanceType("t2.micro"),
                     machine_image=linux_ami,
                     vpc=vpc)
