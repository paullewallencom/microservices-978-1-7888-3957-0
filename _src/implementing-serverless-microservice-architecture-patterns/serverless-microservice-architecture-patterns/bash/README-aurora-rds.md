## RDS MySQL, RDS Aurora, and Aurora Serverless Setup

### Setting up an AWS VPC and subnets

RDS and Aurora are best launched in a custom VPC for being invoked from a Lambda function.

1. Create VPC
    * Name tag: wolf-vpc
    * IPv4 CIDR block*: 10.0.0.0/16
    * No IPv6 CIDR Block
    
2. Create Subnet in AZ A:
    * Name tag: pub-subnet-a
    * Select the VPC above wolf-vpc
    * Availability Zone: eu-west-1a (or your region + AZ)
    * IPv4 CIDR Block: 10.0.0.0/20

3. Create Subnet in AZ B:
    * Name tag: pub-subnet-b
    * Select the VPC above wolf-vpc
    * Availability Zone: eu-west-1b (or your region + AZ)
    * IPv4 CIDR Block: 10.0.16.0/20

4. Internet Gateway > Create internet gateway
    * Name tag: wolf-ig
    * Actions > attach to VPC > Select wolf-vpc

5. Egress Only Internet Gateways

6. Add your IPV4 to Route Tables, e.g. https://checkip.amazonaws.com if your external IP is 90.100.50.155 then enter 90.100.50.155/32
    * If you use 0.0.0.0/0, you enable all IPv4 addresses to access

7. Add Subnet Associations to Route Tables

8. VPC > Actions
    * Edit DNS resolution > Yes
    * Edit Hostnames > Yes

9. (Optional) Setup a VPC Security Group and DB Subnet Group or let AWS Create them when you launch RDS or Aurora

10. Deleting a Lambda VPC Stack,
 
> If you get a "CloudFormation is waiting for NetworkInterfaces associated with the Lambda Function to be cleaned up" when deleting stack then it's a know bug, I've seen it take up to 30min.


#### Additional more details are here: 
* [USER_VPC.Scenarios](https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/vpc-subnets-commands-example.html)
* [USER_VPC.Scenarios](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.Scenarios.html#USER_VPC.Scenario4)
* [WebServerDB.CreateVP](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateVPC.html)
* [WorkingWithRDSInstanceinaVPC](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html)
* [Lambda Deleting ENI delay Issues](https://stackoverflow.com/questions/41299662/aws-lambda-created-eni-not-deleting-while-deletion-of-stack)
* [Lambda ENI workaround - not tested!](http://websitenotebook.blogspot.co.uk/2017/07/cloudformation-wont-delete-lambda-or.html)

### Lambda SAM Template 
You need to modify the `lambda yaml` SAM template file to match you configuration. Replace the following

* Role with accountId
* SecurityGroupIds
* SubnetIds

### Creating the IAM credentials for Passwordless Access

Connect to the server with mySQL command line (e.g. `sudo apt-get install  mysql-server`) or MySQL Workbench. This will allow you to use the IAM credentials rather than need a password.

```
CREATE USER 'lambda' IDENTIFIED WITH AWSAuthenticationPlugin as 'RDS';
GRANT ALL PRIVILEGES ON dev.* TO 'lambda'@'%';
FLUSH PRIVILEGES;

CREATE USER 'lambda'@'localhost' IDENTIFIED WITH AWSAuthenticationPlugin as 'RDS';
GRANT ALL PRIVILEGES ON dev.* TO 'lambda'@'localhost';
FLUSH PRIVILEGES;

```

Ensure that the following policy is attached to the lambda VPC Role
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "rds-db:connect",
      "Resource": "arn:aws:rds-db:<REGION>:<AWS_ACCOUNT_ID>:dbuser:<DB_RESOURCE_ID>/lambda"
    }
  ]
}
```
<DB_RESOURCE_ID>=* can be used as provided but less secure as access to all DBs, but less config. You can find the DB_RESOURCE_ID for each cluster under the RDS Management console.

If you get something like "Access denied for user Access denied for user 'lambda'@'172.31.25.181' or 'lambda'@'10.0.7.102' (using password: YES)". One hack is to open up more internal IP ranges within the VPC. You can reduce the IP range by changing the values depending on the VPC CIDR.
```
CREATE USER 'lambda'@'0.0.0.0/0.0.0.0' IDENTIFIED WITH AWSAuthenticationPlugin as 'RDS';
GRANT ALL PRIVILEGES ON dev.* TO 'lambda'@'localhost';
FLUSH PRIVILEGES;
```
If you get a message `you must restart it without this switch for this grant to work`, you can do this via the AWS CLI or using the AWS Management Console.

* Aurora > Instance Action > Reboot > Reboot


### Secure your Instance 

Once IAM Authentication is setup with the admin user/pass, you can disable the cluster to be Public accessibility

* In AWS Management Console >  Modify
* Public accessibility > No
* Continue > Modify Cluster


### Troubleshooting Aurora and Lambda VPC connectivity

If you are having issues with your custom VPC then you can try to get it to work with the default VPC, make sure in either case that the the Lambda is in the same VPC. For testing you can use the AWS Management Console > Lambda screen to change the Lamabda VPC and Aurora endpoints under `aurora_config.py` or `aurora_config_iam.py`.
