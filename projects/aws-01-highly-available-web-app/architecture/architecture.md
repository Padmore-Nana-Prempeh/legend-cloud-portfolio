```text
                    Internet
                        |
                        v
            Application Load Balancer
                        |
                  Target Group
             /                    \
            v                      v
      EC2 Instance A          EC2 Instance B
            \                      /
             \                    /
              Auto Scaling Group
                        |
                Launch Template
                        |
                  Custom AMI
                        |
                 Amazon CloudWatch
```