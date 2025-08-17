#!/usr/bin/env python3
"""
Initialize MinIO bucket for MLflow
"""
import boto3
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_minio_bucket():
    """Initialize MinIO bucket for MLflow"""
    try:
        # Create S3 client for MinIO
        s3_client = boto3.client(
            's3',
            endpoint_url='http://localhost:9000',
            aws_access_key_id='minioadmin',
            aws_secret_access_key='minioadmin',
            region_name='us-east-1'
        )
        
        # Check if bucket exists
        try:
            s3_client.head_bucket(Bucket='mlflow')
            logger.info("✅ MLflow bucket already exists")
            return True
        except:
            # Create bucket if it doesn't exist
            s3_client.create_bucket(Bucket='mlflow')
            logger.info("✅ Created MLflow bucket in MinIO")
            return True
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize MinIO bucket: {e}")
        return False

def wait_for_minio():
    """Wait for MinIO to be ready"""
    logger.info("⏳ Waiting for MinIO to be ready...")
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            s3_client = boto3.client(
                's3',
                endpoint_url='http://localhost:9000',
                aws_access_key_id='minioadmin',
                aws_secret_access_key='minioadmin',
                region_name='us-east-1'
            )
            
            # Try to list buckets
            s3_client.list_buckets()
            logger.info("✅ MinIO is ready!")
            return True
            
        except Exception as e:
            attempt += 1
            logger.info(f"⏳ MinIO not ready yet (attempt {attempt}/{max_attempts})")
            time.sleep(2)
    
    logger.error("❌ MinIO failed to start within expected time")
    return False

if __name__ == "__main__":
    if wait_for_minio():
        init_minio_bucket()
    else:
        logger.error("Failed to initialize MinIO")
