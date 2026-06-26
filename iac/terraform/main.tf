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

# Restrict administrative/database access to a known corporate CIDR.
variable "admin_cidr" {
  type        = string
  description = "CIDR allowed to reach SSH/Postgres (e.g. the VPN egress range)."
  default     = "10.0.0.0/16"
}

# --- Networking ---------------------------------------------------------------

resource "aws_security_group" "api" {
  name        = "tickethub-api-sg"
  description = "TicketHub API ingress"

  ingress {
    description = "HTTP from the load balancer subnet"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  ingress {
    description = "PostgreSQL from the application subnet"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  egress {
    description = "HTTPS egress only"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# --- Database -----------------------------------------------------------------

resource "aws_db_instance" "tickethub" {
  identifier                  = "tickethub-prod"
  engine                      = "postgres"
  engine_version              = "16"
  instance_class              = "db.t3.medium"
  allocated_storage           = 50
  db_name                     = "tickethub"
  username                    = "tickethub"
  manage_master_user_password = true # password managed in AWS Secrets Manager
  publicly_accessible         = false
  storage_encrypted           = true
  deletion_protection         = true
  auto_minor_version_upgrade  = true
  performance_insights_enabled = true
  backup_retention_period     = 14
  skip_final_snapshot         = false
  final_snapshot_identifier   = "tickethub-prod-final"
  vpc_security_group_ids      = [aws_security_group.api.id]
}

# --- Object storage for ticket assets / reports -------------------------------

resource "aws_s3_bucket" "assets" {
  bucket = "tickethub-prod-assets"
}

resource "aws_s3_bucket_public_access_block" "assets" {
  bucket                  = aws_s3_bucket.assets.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "assets" {
  bucket = aws_s3_bucket.assets.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_versioning" "assets" {
  bucket = aws_s3_bucket.assets.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_logging" "assets" {
  bucket        = aws_s3_bucket.assets.id
  target_bucket = aws_s3_bucket.assets.id
  target_prefix = "access-logs/"
}

# --- Compute ------------------------------------------------------------------

resource "aws_instance" "api" {
  ami                         = "ami-0c1b4dff690b5d229"
  instance_type               = "t3.small"
  vpc_security_group_ids      = [aws_security_group.api.id]
  associate_public_ip_address = false

  metadata_options {
    http_tokens   = "required" # enforce IMDSv2
    http_endpoint = "enabled"
  }

  root_block_device {
    encrypted = true
  }

  tags = {
    Name = "tickethub-api"
  }
}

output "db_endpoint" {
  value = aws_db_instance.tickethub.endpoint
}
