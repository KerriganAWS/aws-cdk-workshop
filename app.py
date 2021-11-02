#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core
from cdk_workshop.ec2_in_default_vpc_stack import EC2InDefaultVPCStack
from cdk_workshop.bastion_ec2_nested_stack import BastionEC2NestedStack
from cdk_workshop.vpc_stack import VPCStack
from cdk_workshop.alb_nested_stack import ALBNestedStack
from cdk_workshop.asg_nested_stack import ASGNestedStack

localEnv = core.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"])

app = core.App()
vpcStack = VPCStack(app, "vpc-stack", env=localEnv)
ec2Stack = BastionEC2NestedStack(vpcStack, "bastion-ec2-nested-stack", vpc=vpcStack.vpc)
asgStack = ASGNestedStack(vpcStack, "asg-nested-stack", vpc=vpcStack.vpc)
albStack = ALBNestedStack(vpcStack, "alb-nested-stack", asg=asgStack)
ec2InDefaultVPCStack = EC2InDefaultVPCStack(app, "ec2-in-default-vpc-stack", env=localEnv)
app.synth()
