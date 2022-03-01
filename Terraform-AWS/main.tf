resource "aws_instance" "aws_instance_test" {
  ami           = "${var.ami}"
  instance_type = "${var.instance_type}"
  key_name = "${var.key_name}"
  security_groups = [aws_security_group.terraform_ec2_security_group.name]
  tags = {
    Name = "${var.instance_name}"
  }
}

resource "aws_security_group_rule" "rule_1" {
  type              = "ingress"
  from_port         = 0
  to_port           = 26
  protocol          = "tcp"
  cidr_blocks       = ["10.0.0.0/8"]
  security_group_id = aws_security_group.terraform_ec2_security_group.id
}

resource "aws_security_group_rule" "rule_2" {
  type              = "ingress"
  from_port         = 0
  to_port           = 28
  protocol          = "tcp"
  cidr_blocks       = ["172.0.0.0/8"]
  security_group_id = aws_security_group.terraform_ec2_security_group.id
}


resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}