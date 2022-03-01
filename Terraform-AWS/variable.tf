variable "ami"{
    default ="ami-087c17d1fe0178315"
}
variable "instance_type"{
    default = "t2.micro"
}
variable "key_name"{
    default = "aws_key"
}
variable "instance_name"{
    default = "myAWS_Instance"
}
variable "vpc_name"{
    default="Default VPC"
}
variable "security_group_name"{
    default="terraform_sg"
}
variable "http_port"{
    default = 80
}
variable "ssh_port"{
    default = 22
}
variable "https_port"{
    default = 443
}
variable "egress_port"{
    default = 0
}
variable "destination_port"{
    default = "0.0.0.0/0"
}