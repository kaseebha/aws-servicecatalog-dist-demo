import json, boto3, logging, sys
import rds_config
import pymysql

rds_host  = "disti-bundle-rds.cbsat73ywhuo.ap-south-1.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
    
logger = logging.getLogger()
logger.setLevel(logging.INFO)
    
    
try:
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

def lambda_handler(event, context):
    # TODO implement
#     print(event['Records'][0]['Sns']['Message'])
#     {
#     "Data": 120,
#     "bundle_name": "aws_waf_lite_bundle_v1",
#     "aws_distributor_name": "Redington",
#     "timestamp": "{\"created_at\": \"2022-11-25 11:24:26.638482\"}",
#     "account_id": "122679783945"
# }
    bundle_name = event['Records'][0]['Sns']['Message']['bundle_name']
    aws_distributor_name = event['Records'][0]['Sns']['Message']['aws_distributor_name']
    deploy_time = event['Records'][0]['Sns']['Message']['timestamp']
    account_id = event['Records'][0]['Sns']['Message']['account_id']
    
    #INSERT INTO metrics_table (bundle_name, aws_distributor_name, deploy_time, account_id) 
    #VALUES ('aws_waf_lite_bundle_v1','Redington','2022-11-25 09:49:04.451908','122679783945');
    
    """
    This function fetches content from MySQL RDS instance
    """

    item_count = 0

    with conn.cursor() as cur:
        #cur.execute('insert into metrics (bundle_name, aws_distributor_name, deploy_time, account_id) values("aws_waf_lite_bundle_v1","Redington","2022-11-25 09:49:04.451908","122679783945")')
        cur.execute('insert into metrics (bundle_name, aws_distributor_name, deploy_time, account_id) values(bundle_name,aws_distributor_name,deploy_time,account_id)')

        conn.commit()
    
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
