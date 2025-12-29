# constants.py

from datetime import datetime

LOG_FILE_ENROLLMENT = datetime.now().strftime("%Y-%m-%d") + "_enrollment.txt"
LOG_FILE_EVENT = datetime.now().strftime("%Y-%m-%d") + "_event.txt"
LOG_FILE_DATA_VALUE_SET = datetime.now().strftime("%Y-%m-%d") + "_dataValueSet.txt"
LOG_FILE_DATA_VALUE_SET_LAST_SYNC = datetime.now().strftime("%Y-%m-%d") + "_dataValueSet_last_sync.txt"
LOG_FILE_EVENT_DATA_VALUE_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_updateEventDataValue.txt"
LOG_FILE_EVENT_ERROR_LOG = datetime.now().strftime("%Y-%m-%d") + "_event_error_log.txt"
LOG_FILE_EVENT_ERROR_LOG_XLSX = datetime.now().strftime("%Y-%m-%d") + "_event_error_log_xlsx.txt"

LOG_FILE_ENROLLMENT_ERROR_LOG_XLSX = datetime.now().strftime("%Y-%m-%d") + "_enrollment_error_log_xlsx.txt"
LOG_FILE_ENROLLMENT_POST_XLSX = datetime.now().strftime("%Y-%m-%d") + "_enrollment_post_xlsx.txt"


LOG_FILE_DELETE_TEI_ERROR_LOG_XLSX = datetime.now().strftime("%Y-%m-%d") + "_tei_delete_error_log_xlsx.txt"
LOG_FILE_DELETE_TEI_XLSX = datetime.now().strftime("%Y-%m-%d") + "_tei_delete_xlsx.txt"

LOG_FILE_DELETE_EVENT_ERROR_LOG_XLSX = datetime.now().strftime("%Y-%m-%d") + "_tei_delete_error_log_xlsx.txt"
LOG_FILE_DELETE_EVENT_XLSX = datetime.now().strftime("%Y-%m-%d") + "_tei_delete_xlsx.txt"

LOG_FILE_EVENT_POST = datetime.now().strftime("%Y-%m-%d") + "_event_post.txt"
LOG_FILE_EVENT_POST_XLSX = datetime.now().strftime("%Y-%m-%d") + "_event_post_xlsx.txt"
#LOG_FILE_ORGUNIT_POST = datetime.now().strftime("%Y-%m-%d") + "_organisationUnits_post.txt"

LOG_FILE_ORGUNIT_POST = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + "_organisationUnits_post.log"

LOG_FILE_TEI_ERROR_LOG = datetime.now().strftime("%Y-%m-%d") + "_tei_error_log.txt"
LOG_FILE_TEI_POST = datetime.now().strftime("%Y-%m-%d") + "_tei_post.txt"
LOG_FILE_TEI_ENROLLMENT_POST = datetime.now().strftime("%Y-%m-%d") + "_tei_enrollment_post.txt"
LOG_FILE_TEI_ATTRIBUTE_ENROLLMENT_POST = datetime.now().strftime("%Y-%m-%d") + "_tei_attribute_enrollment_post.txt"

LOG_FILE_PROGRAMRULE_POST = datetime.now().strftime("%Y-%m-%d") + "_programrule_post.txt"
LOG_FILE_PROGRAMRULE_ERROR_LOG = datetime.now().strftime("%Y-%m-%d") + "_programrule_error_log.txt"

LOG_FILE_PROGRAMRULE_VARIABLE_POST = datetime.now().strftime("%Y-%m-%d") + "_programrule_variable_post.txt"
LOG_FILE_PROGRAMRULE_VARIABLE_ERROR_LOG = datetime.now().strftime("%Y-%m-%d") + "_programrule_variable_error_log.txt"


LOG_FILE_PROGRAMRULE_ACTION_POST = datetime.now().strftime("%Y-%m-%d") + "_programrule_action_post.txt"
LOG_FILE_PROGRAMRULE_ACTION_ERROR_LOG = datetime.now().strftime("%Y-%m-%d") + "_programrule_action_error_log.txt"

LOG_FILE_OPTIONS_POST = datetime.now().strftime("%Y-%m-%d") + "_options_post.txt"
LOG_FILE_OPTION_GRP_MEMBERS_PUT = datetime.now().strftime("%Y-%m-%d") + "_option_grp_member_put.txt"



