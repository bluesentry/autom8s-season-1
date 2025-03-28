import json
import boto3 
import zipfile

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html
client = boto3.client('kinesis') 
print ('got client')

# Specify the path to your ZIP file
zip_file_path = '13724811047.zip'
print ('going to open %s' % zip_file_path)

# Open the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_contents = zip_ref.namelist()
    for file in zip_contents:
        print ('file: %s' % file)
        # Read a specific file from the ZIP archive
        with zip_ref.open(file) as file:
            partKey = file.name
            print ('partKey: %s' % partKey)
            content = file.read()
            # print ('content: %s' % content)
            for line in content.splitlines():
                # Split based on the first space
                try:
                    thetime, message = line.strip().decode('utf-8').split(' ', 1)
                    data = {
                        'timestamp': thetime,
                        'message': message
                    }
                    record = json.dumps(data)
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/put_records.html
        # https://docs.aws.amazon.com/code-library/latest/ug/python_3_kinesis_code_examples.html
                    response = client.put_record(
                        StreamName='mikeo-test',
                        PartitionKey=partKey,
                        Data=record
                    );
                    print ('response: %s' % response)
                except:
                    print ('error: %s' % line)
client.close()