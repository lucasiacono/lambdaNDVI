import json
import boto3
import botocore
import os


def lambda_handler(event, context):
    
    
    for record in event['Records']:
        BUCKET_NAME = 'lucasiacono'  # replace with your bucket name

        KEY3 = 'main'
        s3 = boto3.resource('s3')
        KEY1 = record['s3']['object']['key']

        print("El archivo es:", KEY1)

        try:
            KEY1_P = KEY1.split ("NIR_")
            print ("Split es:", KEY1_P[1])
            KEY2 = "INPUT/RED/RED_"+ KEY1_P[1]

            print ("key 2 es:", KEY2)
            s3.Bucket(BUCKET_NAME).download_file(KEY1, '/tmp/Part0_0_NIR.tif')
            print("Se bajo NIR")
            s3.Bucket(BUCKET_NAME).download_file(KEY2, '/tmp/Part0_0_RED.tif')
            print("Se bajo RED")
            out1 = os.system('ls /tmp/main > /tmp/repipo2.txt')
            testear = open ( "/tmp/repipo2.txt", "r")
            linea = testear.readlines()
            os.system('date\n > /tmp/repipo.txt')
            try:
	            print ("No bajo:", linea[0])
	            os.system('echo NoBajo >> /tmp/repipo.txt')
            except:
	            print ("Bajo")
	            s3.Bucket(BUCKET_NAME).download_file(KEY3, '/tmp/main')
	            os.system('echo Bajo\n >> /tmp/repipo.txt')
                
            out = os.system("cd /tmp/"+ "\n"+"chmod 777 main"+"\n"+"./main")
            print("Ejecuto script")
            #out = os.system("python --version")
            #out = os.system("cat /etc/os-release")
            #out = os.system('stat /tmp/main')
             
            s3.Bucket(BUCKET_NAME).upload_file('/tmp/Part0_0_NDVI.tif','NDVI/NDVI_'+ KEY1_P[1])
            os.system('date > /tmp/repipo.txt')
            s3.Bucket(BUCKET_NAME).upload_file('/tmp/repipo.txt','Log/log'+ KEY1_P[1]+'.txt')
            #s3.Bucket(BUCKET_NAME).upload_file('/tmp/repipo.txt','NDVI/log.txt')
            print("Subio info")
            
            
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
