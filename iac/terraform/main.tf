terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  type    = string
  default = "sa-east-1"
}

variable "db_password" {
  type    = string
  default = "P@ssw0rd-TicketHub-Prod-2026"
}

# --- Networking ---------------------------------------------------------------

resource "aws_security_group" "api" {
  name        = "tickethub-api-sg"
  description = "TicketHub API ingress"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "PostgreSQL"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# --- Database -----------------------------------------------------------------

resource "aws_db_instance" "tickethub" {
  identifier          = "tickethub-prod"
  engine              = "postgres"
  engine_version      = "16"
  instance_class      = "db.t3.medium"
  allocated_storage   = 50
  db_name             = "tickethub"
  username            = "tickethub"
  password            = var.db_password
  publicly_accessible = true
  storage_encrypted   = false
  skip_final_snapshot = true
  vpc_security_group_ids = [aws_security_group.api.id]
}

# --- Object storage for ticket assets / reports -------------------------------

resource "aws_s3_bucket" "assets" {
  bucket = "tickethub-prod-assets"
}

resource "aws_s3_bucket_public_access_block" "assets" {
  bucket                  = aws_s3_bucket.assets.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "assets" {
  bucket = aws_s3_bucket.assets.id
  acl    = "public-read"
}

# --- Compute ------------------------------------------------------------------

resource "aws_instance" "api" {
  ami                         = "ami-0c1b4dff690b5d229"
  instance_type               = "t3.small"
  vpc_security_group_ids      = [aws_security_group.api.id]
  associate_public_ip_address = true

  metadata_options {
    http_tokens = "optional"
  }

  tags = {
    Name = "tickethub-api"
  }
}

output "api_public_ip" {
  value = aws_instance.api.public_ip
}
