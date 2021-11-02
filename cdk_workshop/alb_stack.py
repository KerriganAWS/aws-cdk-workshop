import os
from aws_cdk import (
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elb,
    core
)
# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
# vpc = ec2.Vpc.from_lookup(self, "vpc", vpc_id=vpcID)


class ALBStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, asg, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        alb = elb.ApplicationLoadBalancer(self, "workshopALB",
                                          vpc=asg.vpc,
                                          internet_facing=True,
                                          load_balancer_name="workshopALB"
                                          )

        alb.connections.allow_from_any_ipv4(ec2.Port.tcp(80), "Internet access ALB 80")
        listener = alb.add_listener("httpPort",
                                    port=80,
                                    open=True)
        listener.add_targets("addTargetGroup",
                             port=80,
                             targets=[asg.asg])
