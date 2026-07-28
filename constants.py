# constants.py

from datetime import datetime

LOG_FILE_ENROLLMENT = datetime.now().strftime("%Y-%m-%d") + "_enrollment.txt"
LOG_FILE_EVENT = datetime.now().strftime("%Y-%m-%d") + "_event.txt"
LOG_FILE_DATA_VALUE_SET = datetime.now().strftime("%Y-%m-%d") + "_dataValueSet.txt"

LOG_FILE_DATA_VALUE_SET_DATA_SET_ATTRIBUTE = datetime.now().strftime("%Y-%m-%d") + "_dataValueSet_dataSetAttribute.txt"

LOG_FILE_DATA_VALUE_SET_DELETE = datetime.now().strftime("%Y-%m-%d") + "_dataValueSetDelete.txt"


LOG_FILE_DATA_VALUE_SET_LAST_SYNC = datetime.now().strftime("%Y-%m-%d") + "_dataValueSet_last_sync.txt"
LOG_FILE_EVENT_DATA_VALUE_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_updateEventDataValue.txt"

LOG_FILE_EVENT_DATE_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_updateEventDate.txt"
LOG_FILE_EVENT_ORGUNIT_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_updateEventOrgUnit.txt"
LOG_FILE_ENROLLMENT_DATE_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_updateEnrollmentDate.txt"

LOG_FILE_EVENT_ERROR_LOG = datetime.now().strftime("%Y-%m-%d") + "_event_error_log.txt"
LOG_FILE_EVENT_ERROR_LOG_XLSX = datetime.now().strftime("%Y-%m-%d") + "_event_error_log_xlsx.txt"

LOG_FILE_ENROLLMENT_ERROR_LOG_XLSX = datetime.now().strftime("%Y-%m-%d") + "_enrollment_error_log_xlsx.txt"
LOG_FILE_ENROLLMENT_POST_XLSX = datetime.now().strftime("%Y-%m-%d") + "_enrollment_post_xlsx.txt"


LOG_FILE_DELETE_TEI_ERROR_LOG_XLSX = datetime.now().strftime("%Y-%m-%d") + "_tei_delete_error_log_xlsx.txt"
LOG_FILE_DELETE_TEI_XLSX = datetime.now().strftime("%Y-%m-%d") + "_tei_delete_xlsx.txt"

LOG_FILE_DELETE_EVENT_ERROR_LOG_XLSX = datetime.now().strftime("%Y-%m-%d") + "_tei_delete_error_log_xlsx.txt"
LOG_FILE_DELETE_EVENT_XLSX = datetime.now().strftime("%Y-%m-%d") + "_event_delete_xlsx.txt"



LOG_FILE_DELETE_ENROLLMENT_ERROR_LOG_XLSX = datetime.now().strftime("%Y-%m-%d") + "_enrollment_delete_error_log_xlsx.txt"
LOG_FILE_DELETE_ENROLLMENT_XLSX = datetime.now().strftime("%Y-%m-%d") + "_enrollment_delete_xlsx.txt"

LOG_FILE_DELETE_PROGRAM_RULE_XLSX = datetime.now().strftime("%Y-%m-%d") + "_program_rule_delete_xlsx.txt"
LOG_FILE_DELETE_PROGRAM_RULE_ERROR_LOG_XLSX = datetime.now().strftime("%Y-%m-%d") + "_program_rule_delete_error_log_xlsx.txt"


LOG_FILE_EVENT_POST = datetime.now().strftime("%Y-%m-%d") + "_event_post.txt"
LOG_FILE_EVENT_TO_EVENT_POST = datetime.now().strftime("%Y-%m-%d") + "_event_to_event_post.txt"
LOG_FILE_EVENT_POST_XLSX = datetime.now().strftime("%Y-%m-%d") + "_event_post_xlsx.txt"
#LOG_FILE_ORGUNIT_POST = datetime.now().strftime("%Y-%m-%d") + "_organisationUnits_post.txt"

LOG_FILE_ORGUNIT_POST = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + "_organisationUnits_post.log"

LOG_FILE_ORGUNIT_UPDATE = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + "_organisationUnits_update.log"

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
LOG_FILE_OPTIONS_DELETE = datetime.now().strftime("%Y-%m-%d") + "_options_delete.txt"
LOG_FILE_OPTION_GRP_MEMBERS_PUT = datetime.now().strftime("%Y-%m-%d") + "_option_grp_member_put.txt"

LOG_FILE_OPTIONS_TRANSLATION_POST = datetime.now().strftime("%Y-%m-%d") + "_options_translation_post.txt"

LOG_FILE_PROGRAM_INDICATORS_POST = datetime.now().strftime("%Y-%m-%d") + "_program_indicators_post.txt"

LOG_FILE_TEI_ATTRIBUTE_VALUE_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_updateTEIAttributeValue.txt"
LOG_FILE_TEI_ATTRIBUTE_VALUE_ERROR_LOG = datetime.now().strftime("%Y-%m-%d") + "_tei_update_error_log.txt"

LOG_FILE_TEI_TETYPE_VALUE_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_update_tei_trackedentityType.txt"
LOG_FILE_TEI_TETYPE_VALUE_ERROR_LOG = datetime.now().strftime("%Y-%m-%d") + "_tei_update_trackedentityType_error_log.txt"


LOG_FILE_NEW_TABLE_CREATION_POSTGRES = datetime.now().strftime("%Y-%m-%d") + "_new_table_creation_postgres.txt"

LOG_FILE_USERS_POST = datetime.now().strftime("%Y-%m-%d") + "_users_post.txt"
LOG_FILE_USERS_GROUP_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_users_group_update.txt"

LOG_FILE_USERS_DISABLED_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_users_disabled_update.txt"

LOG_FILE_EVENT_DATAVALUE_MULTIPLE_DE = datetime.now().strftime("%Y-%m-%d") + "_event_update_multiple_dataelement.txt"

LOG_FILE_USERS_ORG_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_users_org_update.txt"
LOG_FILE_USERS_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_users_update.txt"
LOG_FILE_USERS_DELETE = datetime.now().strftime("%Y-%m-%d") + "_users_delete.txt"

LOG_FILE_TRANSLATION_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_translation_update.txt"
LOG_FILE_OPTIONSET_SHATING_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_optionset_sharing_update.txt"
LOG_FILE_DATAELEMENT_PUBLIC_ACCESS_UPDATE = datetime.now().strftime("%Y-%m-%d") + "_dataElement_public_access_update.txt"



