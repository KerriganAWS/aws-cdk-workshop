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
