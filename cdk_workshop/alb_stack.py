import os
from aws_cdk import (
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elb,
    core
)


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
