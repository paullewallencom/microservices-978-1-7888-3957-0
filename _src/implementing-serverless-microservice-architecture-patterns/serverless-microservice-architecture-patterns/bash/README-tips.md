

## Additional Bash Tips

### DynamoDB Errors

* If you get `Unknown options: --sse-specification, Enabled=true` then you are probably on an older version of the AWS CLI. The tested version here is 

```
$ aws --version
aws-cli/1.14.63 Python/2.7.12 Linux/4.4.0-43-Microsoft botocore/1.9.16
```

### Windows Carriage Returns

You might get errors in the bash scripts on windows this is due to the `\r` or `CR`  characters added at the end of each line, use nano, vi, Windows apps like notepad++ or run recursive command to remove them so that you can run the shell scripts:

```
find ./ -type f -exec sed -i '' -e 's/\r//' {} \;
```