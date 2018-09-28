import pandas as pd
import libs.analytics.logpreprocessor as lp
import time
import numpy as numpy
import json
import YouSearch.settings as settings
import os
import libs.utilities.pathtools as pt
# Create your views here.

COMMON_ERROR_KEYS = [
     'exception',
     'warn',
     'error',
     'fail',
     'unauthorized',
     'timeout',
     'refused',
     'NoSuchPageException',
     '404 ',
     '401 ',
     '505 '
]


def error_analytics(dataframe):
     """ Return a JSON object contains insight
     about the errors of this log file"""
     frames = []
     res_dict = {}
     for k in COMMON_ERROR_KEYS:
          frames.append(dataframe[dataframe.message.str.contains(pat=k, case=False) == True])     
     result = pd.concat(frames)
     res_dict['total_entries'] = len(dataframe.index)
     res_dict['num_error'] = len(result.index)
     res_dict['error_rate'] = res_dict['num_error'] / res_dict['total_entries']
     res_dict['error_by_keywords'] = count_error_occurences(result)
     res_dict['error_by_dates'] = result.groupby('date').date.size().to_dict()
     return json.dumps(res_dict, cls=encoder, indent=4, sort_keys=True)


def user_analytics(user):
     """ Return JSON contains user information"""
     res_dict = {}
     res_dict['username'] = user.username
     res_dict['num_log_limit'] = settings.NUM_LOG_LIMIT
     res_dict['num_log'] = user.logfile_set.count()
     res_dict['storage_limit'] = settings.STORAGE_LIMIT
     res_dict['storage_used'] = pt.get_user_dir_size(user.username)
     return json.dumps(res_dict, indent=4, sort_keys=True)
     

def count_error_occurences(dataframe):
     error_dict = {}
     for key in COMMON_ERROR_KEYS:
          for row in dataframe[(dataframe.message.str.contains(key))].count():
               error_dict[key] = row
     return error_dict


class encoder(json.JSONEncoder):
     """ Customized encoder to encode numpy types"""
     def default(self, obj):
          if isinstance(obj, numpy.integer):
               return int(obj)
          elif isinstance(obj, numpy.floating):
               return float(obj)
          elif isinstance(obj, numpy.ndarray):
               return obj.tolist()
          else:
               return super(encoder, self).default(obj)


# start_time = time.process_time()
# log = lp.read_log("ly-admin", "syslogClassShare.5")
# elapsed_time = time.process_time() - start_time
# error_analytics(log)
# elapsed_time1 = time.process_time() - elapsed_time
# print("read speed: " + str(elapsed_time))
# print("processing speed: " + str(elapsed_time1))

