resource "aws_security_group" "terraform_ec2_security_group" {
  name        = "${var.security_group_name}"
  description = "Allow TLS inbound traffic"
  vpc_id="${aws_default_vpc.default.id}"

  tags={
    Name="terraform_sg"
  }
}

