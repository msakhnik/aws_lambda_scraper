# Default VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "Main"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.0.0/24"

  tags = {
    Name = "PublicSubnet"
  }
}

resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.main.id

  route = []

  tags = {
    Name = "example"
  }
}


resource "aws_subnet" "private_subnet_1" {

  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.16.0/24"
  availability_zone = "${data.aws_availability_zones.available.names[0]}"
  tags = {
    Name = "PrivateSubnet1"
  }
}

resource "aws_route_table_association" "private_1" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_route_table_association" "private_2" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_rt.id
}
resource "aws_subnet" "private_subnet_2" {

  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.32.0/24"
  availability_zone = "${data.aws_availability_zones.available.names[1]}"
  tags = {
    Name = "PrivateSubnet2"
  }

}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "Main"
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

# Default security group
resource "aws_default_security_group" "default" {
  vpc_id     = aws_vpc.main.id

  ingress {
    protocol  = -1
    self      = true
    from_port = 0
    to_port   = 0
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "Main"
  }
}

# EFS file system
resource "aws_efs_file_system" "efs_for_lambda" {
  tags = {
    Name = "Main"
  }
}

# Two mount targets connect the file system to the subnets
resource "aws_efs_mount_target" "mount_target_az1" {
  file_system_id  = "${aws_efs_file_system.efs_for_lambda.id}"
  subnet_id       = "${aws_subnet.private_subnet_1.id}"
  security_groups = ["${aws_default_security_group.default.id}"]
}

resource "aws_efs_mount_target" "mount_target_az2" {
  file_system_id  = "${aws_efs_file_system.efs_for_lambda.id}"
  subnet_id       = "${aws_subnet.private_subnet_2.id}"
  security_groups = ["${aws_default_security_group.default.id}"]
}

# EFS access point used by lambda file system
resource "aws_efs_access_point" "access_point_lambda" {
  file_system_id = "${aws_efs_file_system.efs_for_lambda.id}"

  root_directory {
    path = "/efs"
    creation_info {
      owner_gid   = 1000
      owner_uid   = 1000
      permissions = "777"
    }
  }

  posix_user {
    gid = 1000
    uid = 1000
  }
}

