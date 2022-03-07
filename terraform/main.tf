terraform {
  backend "s3" {
    bucket = "logora-terraform"
    key = "logora-nlp/terraform.state"
    region = "eu-west-3"
  }
}

provider "aws" {
  region = "eu-west-3"
}

variable "project_name" {
  type = string
  default = "nlp"
}

module "ecs-cluster" {  
  source  = "hboisgibault/ecs-cluster/aws"
  version = "1.2.5"

  vpc_id = "vpc-d7ded3be"
  ami_id = "ami-0bce8e5f8fd912af2"
  alb_arn = "arn:aws:elasticloadbalancing:eu-west-3:812844034365:loadbalancer/app/logora-main/b07504f433dc2038"
  alb_security_group_id = "sg-034c9a669c9a97438"
  alb_listener_arn = "arn:aws:elasticloadbalancing:eu-west-3:812844034365:listener/app/logora-main/b07504f433dc2038/76e41df49624512a"
  subnet_ids = ["subnet-8ff4dce6"]
  ingress_security_groups = ["monitoring-production"]
  application_name = "${var.project_name}-${terraform.workspace}"
  environment_name = terraform.workspace
  application_host = terraform.workspace == "production" ? "nlp.logora.fr" : "${var.project_name}-${terraform.workspace}.logora.fr"
  instance_type = terraform.workspace == "production" ? "t3.small" : "t3a.small"
  target_capacity = terraform.workspace == "production" ? 1 : 1
  container_port = 8000
  alb_listener_rule_priority = terraform.workspace == "production" ? 35 : 105
}