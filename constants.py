import os

LOCAL_WORKING_DIR = '/Users/davidasfaha/Documents/coding/twitter-location-working'
REMOTE_DOWNLOAD = '/home/me/twitter-location'
#REMOTE_DOWNLOAD = '/home/me/misc' # testing
RAW_FILE_NAME = 'brickLaneStream.log'
#RAW_FILE_NAME = 'test.json' # testing
SCP_SERVER_TEMPLATE = '' #Add scp connection string
file_name, _ = os.path.splitext(RAW_FILE_NAME)
remote_path = os.path.join(REMOTE_DOWNLOAD,RAW_FILE_NAME)
local_path = os.path.join(LOCAL_WORKING_DIR, RAW_FILE_NAME)

pandas_path = os.path.join(LOCAL_WORKING_DIR, file_name + '.pandas')