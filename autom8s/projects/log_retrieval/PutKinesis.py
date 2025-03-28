import json
import boto3 
import zipfile

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html
client = boto3.client('kinesis') 
print ('got client')

stream_name = 'mikeo-test'

# Specify the path to your ZIP file
workflow_id = '13724811047'
zip_file_path = f'{workflow_id}.zip'
print ('going to open %s' % zip_file_path)

# Open the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_contents = zip_ref.namelist()
    for file in zip_contents:
        print ('file: %s' % file)
        # Read a specific file from the ZIP archive
        with zip_ref.open(file) as file:
            partition_key = file.name
            content = file.read()
            for line in content.splitlines():
                # Split based on the first space
                try:
                    msg_time, message = line.strip().decode('utf-8').split(' ', 1)
                    data = {
                        "workflow_id": workflow_id,
                        'job_name': partition_key,
                        'msg_time': msg_time,
                        'msg': message
                    }
                    record = json.dumps(data)
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis/client/put_records.html
        # https://docs.aws.amazon.com/code-library/latest/ug/python_3_kinesis_code_examples.html
                    response = client.put_record(
                        StreamName=stream_name,
                        PartitionKey=partition_key,
                        Data=record
                    );
                    # print ('response: %s' % response)
                except:
                    print ('error: %s' % line)
            print ('finished processing file: %s' % file.name)
client.close()