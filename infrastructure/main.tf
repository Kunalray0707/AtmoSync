# AtmoSync Terraform Infrastructure Definition (AWS Cloud)

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  default = "us-east-1"
}

resource "aws_vpc" "atmosync_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "AtmoSync-VPC"
  }
}

resource "aws_msk_cluster" "atmosync_kafka" {
  cluster_name           = "atmosync-kafka-cluster"
  kafka_version          = "3.4.0"
  number_of_broker_nodes = 3

  broker_node_group_info {
    instance_type = "kafka.m5.large"
    client_subnets = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id]
    security_groups = [aws_security_group.kafka_sg.id]
  }

  tags = {
    Environment = "Production"
  }
}

resource "aws_subnet" "subnet_a" {
  vpc_id            = aws_vpc.atmosync_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "subnet_b" {
  vpc_id            = aws_vpc.atmosync_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"
}

resource "aws_security_group" "kafka_sg" {
  name   = "atmosync-kafka-sg"
  vpc_id = aws_vpc.atmosync_vpc.id

  ingress {
    from_port   = 9092
    to_port     = 9092
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
}
