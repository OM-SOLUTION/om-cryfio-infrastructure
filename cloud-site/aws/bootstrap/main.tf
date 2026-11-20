# Creates the S3 bucket that stores Terraform's state for the AWS stack, with locking so two
# people cannot apply at the same time. Run once, before the main AWS stack.
