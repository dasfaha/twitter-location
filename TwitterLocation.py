#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import pandas as pd
import json
import dateutil
import constants as var

class Downloader():

	def run(self): 
		"""Downloads and processes the file"""

		pth = self.download_file(var.remote_path, var.local_path)
		if not pth:
			raise Exception("Could not download file from server")

		data, exceptions = self.tweets_to_df(pth)

		data, dict_cols = self.expand_all_cols(data)
		#datetimes are string need to turn into datetime
		#Wed Jul 31 23:15:02 +0000 2013
		data['created_at'] = [dateutil.parser.parse(x) for x in data['created_at']]
		data['user_created_at'] = [dateutil.parser.parse(x) for x in data['user_created_at']]

		data.to_pickle(var.pandas_path)

	def download_file(self, remote_path, local_path):
	    """Download from server"""
	    scp_server =  var.SCP_SERVER_TEMPLATE.format(remote_path)
	    scp_out = subprocess.call(['scp', scp_server, local_path])
	    return local_path if not scp_out else ''

	def tweets_to_df(self, local_path):
	    """Turn json into data frame"""
	    f = open(local_path, 'r')
	    tweets = []
	    exceptions  = {} 
	    for number, line in enumerate(f.readlines()):
	        if line:
	            try:
	                data = json.loads(line)
	                tweets.append(data)
	            except ValueError as e:
	                exceptions[number] = str(e) + '\n' #TODO - Exceptions are garbage
	    return pd.DataFrame(tweets), exceptions            

	def get_dict_cols(self, data):
	    """ Return the columns that are dictionaries"""
	    dict_cols = []
	    counter = 0
	    for c in data.columns:
	        if hasattr(data[c][1], 'keys'):
	            counter += 1
	            dict_cols.append(c)
	    return dict_cols


	def expand_col(self, df, field, debug=True):  
	    """
	    Transform a columns which is an object, turn into columns and add
	    to the data frame
        """  
	    counter = 0
	    dict_field = []
	    #TODO - test that these error conditions work.
	    if not field in df.columns:
	        raise Exception('Field is not in DF')
	    elif not isinstance(df[field][0], dict):
	        raise Exception('Columns {0} is not a dictionary.'.format(field)) 
	    for row in df.iterrows():
	        #Pandas iterrows returns each row as a tuple, second element is the dictionary
	        r =  row[1][field]
	        #if field's dictionary is empty add an empty dict, which will be turned into NAN in pandas
	        if r:
	            #append the field name to prevent key clashes
	            rf = { field + '_' + k : v  for k, v in r.iteritems() }
	            dict_field.append(rf)
	        else:
	            dict_field.append({})
	        counter += 1    
	        if debug and counter == 10: break
	    f = pd.DataFrame(dict_field)
	    combi = pd.merge(df, f, left_index=True, right_index=True)        
	    #Expanded column, in its dictionary form, is no longer needed
	    del combi[field]
	    return combi          

	def expand_all_cols(self,  data):
	    """ Turn all columns with objects into columns """
	    dict_cols = self.get_dict_cols(data)
	    for dc in dict_cols:
	        data = self.expand_col(data, dc, False)
	    return data, dict_cols




