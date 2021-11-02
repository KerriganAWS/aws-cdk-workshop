import os
from aws_cdk import (
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    core
)

ec2_type = "t2.micro"
key_name = "id_rsa"
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )
with open("./user_data/user_data.sh") as f:
    user_data = f.read()


class ASGNestedStack(core.NestedStack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = vpc
        self.asg = autoscaling.AutoScalingGroup(self, "acerASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
                                                instance_type=ec2.InstanceType.of(
                                                    ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
                                                machine_image=linux_ami,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2
                                                )
