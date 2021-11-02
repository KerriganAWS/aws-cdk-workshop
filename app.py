#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core
from cdk_workshop.ec2_in_default_vpc_stack import EC2InDefaultVPCStack
from cdk_workshop.bastion_ec2_stack import BastionEC2Stack
from cdk_workshop.vpc_stack import VPCStack
from cdk_workshop.alb_stack import ALBStack
from cdk_workshop.asg_stack import ASGStack

localEnv = core.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"])

app = core.App()
vpcStack = VPCStack(app, "vpc-stack", env=localEnv)
ec2InDefaultVPCStack = EC2InDefaultVPCStack(app, "ec2-in-default-vpc-stack", env=localEnv)
asgStack = ASGStack(app, "asg-stack", vpc=vpcStack.vpc, env=localEnv)
albStack = ALBStack(app, "alb-stack", asg=asgStack, env=localEnv)
core.Tags.of(vpcStack).of(asgStack).of(albStack).add("env", "workshop")
app.synth()
