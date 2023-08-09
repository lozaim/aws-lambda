#
# Source from https://github.com/prabhath 
#
# https://gist.github.com/prabhath/b15484538aec506c096e6c4facc6f4fd
#
import urllib3
import boto3
sns= boto3.client('sns')
http = urllib3.PoolManager()

urls = [
        'https://google.com'
]
topic_arn='arn:aws:sns:us-east-1:041027301676:DevOps-Email'

def lambda_handler(event, context):
    do_health_check()

def do_health_check():
    failures = list()
    for url in urls:
        try:
            response = http.request('GET', url)
            if response.status != 200:
                error = dict()
                temp=url.split('://')
                error['url'] = '('+temp[0]+') '+temp[1]
                error['status'] = response.status
                error['response'] = response.data
                failures.append(error)
        except Exception as e:
            error = dict()
            temp=url.split('://')
            error['url'] = '('+temp[0]+') '+temp[1]
            error['status'] = 'xxx'
            error['response'] = str(e)
            failures.append(error)
            message = "Error occurred for url: " + error['url']+ ". Error: " + str(e)
            print(message)
            
    if len(failures) > 0:
        message = "Health check failures in following. \n\n"
        for failure in failures:
            message += repr(failure) + '\n'
        print('Sending message:'+ message)
        # Publish to topic
        sns.publish(TopicArn=topic_arn,
                    Message=message,
                    Subject="Health check failures in cloud component(s)")
