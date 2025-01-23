from enum import Enum
from pydantic import BaseModel
from .api_service import APIService
from typing import Union, List

class Action(BaseModel):
    
    @staticmethod
    def get_random_action_by_api_service(api_service: APIService) -> str:
        """
        Get a random action for a given API service
        TODO: This is a workaround to get OAuth info for a given API service
        """
        actions = Action.from_api_service(api_service)
        return actions[0]
        
    @staticmethod
    def from_string(action_string: str) -> 'ActionType':
        """
        Resolve an Action enum instance from a string identifier.
        e.g. gmail_threads_list
        """
        # Get all enum classes defined within Action
        service_enums = [v for k, v in Action.__dict__.items() 
                        if isinstance(v, type) and issubclass(v, Enum)]
        
        # Try matching against each service's actions
        for service_enum in service_enums:
            try:
                return service_enum(action_string)
            except ValueError:
                continue
            
        raise ValueError(f"Unknown action: {action_string}")

    @staticmethod 
    def from_enum_name(enum_name: str) -> 'ActionType':
        """
        Resolve an Action enum instance from an enum name.
        e.g. Gmail.DRAFTS_LIST
        """
        try:
            service_name, action_name = enum_name.split('.')
            service_enum = getattr(Action, service_name)
            return getattr(service_enum, action_name)
        except (AttributeError, ValueError):
            raise ValueError(f"Invalid enum name format: {enum_name}. Expected format: Service.ACTION_NAME OR the specified enum is not found")
        
    @staticmethod
    def from_api_service(api_service: APIService) -> List[str]:
        """
        Get all actions for a given API service
        """
        actions = []
        for attr in Action.__dict__.values():
            if isinstance(attr, type) and issubclass(attr, Enum):
                actions.extend([action.value for action in attr if action.get_api_service() == api_service])
        return actions

    class GoogleCalendar(str, Enum):
        def get_api_service(self) -> APIService:
            return APIService.GOOGLE_CALENDAR
        
        ACL_DELETE = "google_calendar_acl_delete"
        """Acl delete."""
        
        ACL_GET = "google_calendar_acl_get"
        """Acl get."""
        
        ACL_INSERT = "google_calendar_acl_insert"
        """Acl insert."""
        
        ACL_LIST = "google_calendar_acl_list"
        """Acl list."""
        
        ACL_PATCH = "google_calendar_acl_patch"
        """Acl patch."""
        
        ACL_UPDATE = "google_calendar_acl_update"
        """Acl update."""
        
        ACL_WATCH = "google_calendar_acl_watch"
        """Acl watch."""
        
        CALENDARS_CLEAR = "google_calendar_calendars_clear"
        """Calendars clear."""
        
        CALENDARS_DELETE = "google_calendar_calendars_delete"
        """Calendars delete."""
        
        CALENDARS_GET = "google_calendar_calendars_get"
        """Calendars get."""
        
        CALENDARS_INSERT = "google_calendar_calendars_insert"
        """Calendars insert."""
        
        CALENDARS_PATCH = "google_calendar_calendars_patch"
        """Calendars patch."""
        
        CALENDARS_UPDATE = "google_calendar_calendars_update"
        """Calendars update."""
        
        CALENDAR_LIST_DELETE = "google_calendar_calendar_list_delete"
        """Calendar list delete."""
        
        CALENDAR_LIST_GET = "google_calendar_calendar_list_get"
        """Calendar list get."""
        
        CALENDAR_LIST_INSERT = "google_calendar_calendar_list_insert"
        """Calendar list insert."""
        
        CALENDAR_LIST_LIST = "google_calendar_calendar_list_list"
        """Calendar list list."""
        
        CALENDAR_LIST_PATCH = "google_calendar_calendar_list_patch"
        """Calendar list patch."""
        
        CALENDAR_LIST_UPDATE = "google_calendar_calendar_list_update"
        """Calendar list update."""
        
        CALENDAR_LIST_WATCH = "google_calendar_calendar_list_watch"
        """Calendar list watch."""
        
        CHANNELS_STOP = "google_calendar_channels_stop"
        """Channels stop."""
        
        COLORS_GET = "google_calendar_colors_get"
        """Colors get."""
        
        EVENTS_DELETE = "google_calendar_events_delete"
        """Events delete."""
        
        EVENTS_GET = "google_calendar_events_get"
        """Events get."""
        
        EVENTS_IMPORT = "google_calendar_events_import"
        """Events import."""
        
        EVENTS_INSERT = "google_calendar_events_insert"
        """Events insert."""
        
        EVENTS_INSTANCES = "google_calendar_events_instances"
        """Events instances."""
        
        EVENTS_LIST = "google_calendar_events_list"
        """Events list."""
        
        EVENTS_MOVE = "google_calendar_events_move"
        """Events move."""
        
        EVENTS_PATCH = "google_calendar_events_patch"
        """Events patch."""
        
        EVENTS_QUICK_ADD = "google_calendar_events_quick_add"
        """Events quick add."""
        
        EVENTS_UPDATE = "google_calendar_events_update"
        """Events update."""
        
        EVENTS_WATCH = "google_calendar_events_watch"
        """Events watch."""
        
        FREEBUSY_QUERY = "google_calendar_freebusy_query"
        """Freebusy query."""
        
        SETTINGS_GET = "google_calendar_settings_get"
        """Settings get."""
        
        SETTINGS_LIST = "google_calendar_settings_list"
        """Settings list."""
        
        SETTINGS_WATCH = "google_calendar_settings_watch"
        """Settings watch."""
        

    class Notion(str, Enum):
        def get_api_service(self) -> APIService:
            return APIService.NOTION
        
        APPEND_BLOCK_CHILDREN = "notion_append_block_children"
        """Block children."""
        
        DELETE_ABLOCK = "notion_delete_ablock"
        """Ablock."""
        
        QUERY_ADATABASE = "notion_query_adatabase"
        """Adatabase."""
        
        RETRIEVE_ABLOCK = "notion_retrieve_ablock"
        """Ablock."""
        
        RETRIEVE_ADATABASE = "notion_retrieve_adatabase"
        """Adatabase."""
        
        RETRIEVE_APAGE = "notion_retrieve_apage"
        """Apage."""
        
        RETRIEVE_APAGE_PROPERTY_ITEM = "notion_retrieve_apage_property_item"
        """Apage property item."""
        
        RETRIEVE_AUSER = "notion_retrieve_auser"
        """Auser."""
        
        RETRIEVE_BLOCK_CHILDREN = "notion_retrieve_block_children"
        """Block children."""
        
        RETRIEVE_COMMENTS = "notion_retrieve_comments"
        """Comments."""
        
        UPDATE_ABLOCK = "notion_update_ablock"
        """Ablock."""
        
        UPDATE_ADATABASE = "notion_update_adatabase"
        """Adatabase."""
        
        UPDATE_PAGE_PROPERTIES = "notion_update_page_properties"
        """Page properties."""
        

    class Nyt(str, Enum):
        def get_api_service(self) -> APIService:
            return APIService.NYT
        
        ARTICLE_SEARCH_JSON_GET = "nyt_article_search_json_get"
        """Search json get."""
        

    class Slack(str, Enum):
        def get_api_service(self) -> APIService:
            return APIService.SLACK
        
        ADMIN_APPS_APPROVE = "slack_web_api_admin_apps_approve"
        """Api admin apps approve."""
        
        ADMIN_APPS_APPROVED_LIST = "slack_web_api_admin_apps_approved_list"
        """Api admin apps approved list."""
        
        ADMIN_APPS_REQUESTS_LIST = "slack_web_api_admin_apps_requests_list"
        """Api admin apps requests list."""
        
        ADMIN_APPS_RESTRICT = "slack_web_api_admin_apps_restrict"
        """Api admin apps restrict."""
        
        ADMIN_APPS_RESTRICTED_LIST = "slack_web_api_admin_apps_restricted_list"
        """Api admin apps restricted list."""
        
        ADMIN_CONVERSATIONS_ARCHIVE = "slack_web_api_admin_conversations_archive"
        """Api admin conversations archive."""
        
        ADMIN_CONVERSATIONS_CONVERT_TO_PRIVATE = "slack_web_api_admin_conversations_convert_to_private"
        """Api admin conversations convert to private."""
        
        ADMIN_CONVERSATIONS_CREATE = "slack_web_api_admin_conversations_create"
        """Api admin conversations create."""
        
        ADMIN_CONVERSATIONS_DELETE = "slack_web_api_admin_conversations_delete"
        """Api admin conversations delete."""
        
        ADMIN_CONVERSATIONS_DISCONNECT_SHARED = "slack_web_api_admin_conversations_disconnect_shared"
        """Api admin conversations disconnect shared."""
        
        ADMIN_CONVERSATIONS_EKM_LIST_ORIGINAL_CONNECTED_CHANNEL_INFO = "slack_web_api_admin_conversations_ekm_list_original_connected_channel_info"
        """Api admin conversations ekm list original connected channel info."""
        
        ADMIN_CONVERSATIONS_GET_CONVERSATION_PREFS = "slack_web_api_admin_conversations_get_conversation_prefs"
        """Api admin conversations get conversation prefs."""
        
        ADMIN_CONVERSATIONS_GET_TEAMS = "slack_web_api_admin_conversations_get_teams"
        """Api admin conversations get teams."""
        
        ADMIN_CONVERSATIONS_INVITE = "slack_web_api_admin_conversations_invite"
        """Api admin conversations invite."""
        
        ADMIN_CONVERSATIONS_RENAME = "slack_web_api_admin_conversations_rename"
        """Api admin conversations rename."""
        
        ADMIN_CONVERSATIONS_RESTRICT_ACCESS_ADD_GROUP = "slack_web_api_admin_conversations_restrict_access_add_group"
        """Api admin conversations restrict access add group."""
        
        ADMIN_CONVERSATIONS_RESTRICT_ACCESS_LIST_GROUPS = "slack_web_api_admin_conversations_restrict_access_list_groups"
        """Api admin conversations restrict access list groups."""
        
        ADMIN_CONVERSATIONS_RESTRICT_ACCESS_REMOVE_GROUP = "slack_web_api_admin_conversations_restrict_access_remove_group"
        """Api admin conversations restrict access remove group."""
        
        ADMIN_CONVERSATIONS_SEARCH = "slack_web_api_admin_conversations_search"
        """Api admin conversations search."""
        
        ADMIN_CONVERSATIONS_SET_CONVERSATION_PREFS = "slack_web_api_admin_conversations_set_conversation_prefs"
        """Api admin conversations set conversation prefs."""
        
        ADMIN_CONVERSATIONS_SET_TEAMS = "slack_web_api_admin_conversations_set_teams"
        """Api admin conversations set teams."""
        
        ADMIN_CONVERSATIONS_UNARCHIVE = "slack_web_api_admin_conversations_unarchive"
        """Api admin conversations unarchive."""
        
        ADMIN_EMOJI_ADD = "slack_web_api_admin_emoji_add"
        """Api admin emoji add."""
        
        ADMIN_EMOJI_ADD_ALIAS = "slack_web_api_admin_emoji_add_alias"
        """Api admin emoji add alias."""
        
        ADMIN_EMOJI_LIST = "slack_web_api_admin_emoji_list"
        """Api admin emoji list."""
        
        ADMIN_EMOJI_REMOVE = "slack_web_api_admin_emoji_remove"
        """Api admin emoji remove."""
        
        ADMIN_EMOJI_RENAME = "slack_web_api_admin_emoji_rename"
        """Api admin emoji rename."""
        
        ADMIN_INVITE_REQUESTS_APPROVE = "slack_web_api_admin_invite_requests_approve"
        """Api admin invite requests approve."""
        
        ADMIN_INVITE_REQUESTS_APPROVED_LIST = "slack_web_api_admin_invite_requests_approved_list"
        """Api admin invite requests approved list."""
        
        ADMIN_INVITE_REQUESTS_DENIED_LIST = "slack_web_api_admin_invite_requests_denied_list"
        """Api admin invite requests denied list."""
        
        ADMIN_INVITE_REQUESTS_DENY = "slack_web_api_admin_invite_requests_deny"
        """Api admin invite requests deny."""
        
        ADMIN_INVITE_REQUESTS_LIST = "slack_web_api_admin_invite_requests_list"
        """Api admin invite requests list."""
        
        ADMIN_TEAMS_ADMINS_LIST = "slack_web_api_admin_teams_admins_list"
        """Api admin teams admins list."""
        
        ADMIN_TEAMS_CREATE = "slack_web_api_admin_teams_create"
        """Api admin teams create."""
        
        ADMIN_TEAMS_LIST = "slack_web_api_admin_teams_list"
        """Api admin teams list."""
        
        ADMIN_TEAMS_OWNERS_LIST = "slack_web_api_admin_teams_owners_list"
        """Api admin teams owners list."""
        
        ADMIN_TEAMS_SETTINGS_INFO = "slack_web_api_admin_teams_settings_info"
        """Api admin teams settings info."""
        
        ADMIN_TEAMS_SETTINGS_SET_DEFAULT_CHANNELS = "slack_web_api_admin_teams_settings_set_default_channels"
        """Api admin teams settings set default channels."""
        
        ADMIN_TEAMS_SETTINGS_SET_DESCRIPTION = "slack_web_api_admin_teams_settings_set_description"
        """Api admin teams settings set description."""
        
        ADMIN_TEAMS_SETTINGS_SET_DISCOVERABILITY = "slack_web_api_admin_teams_settings_set_discoverability"
        """Api admin teams settings set discoverability."""
        
        ADMIN_TEAMS_SETTINGS_SET_ICON = "slack_web_api_admin_teams_settings_set_icon"
        """Api admin teams settings set icon."""
        
        ADMIN_TEAMS_SETTINGS_SET_NAME = "slack_web_api_admin_teams_settings_set_name"
        """Api admin teams settings set name."""
        
        ADMIN_USERGROUPS_ADD_CHANNELS = "slack_web_api_admin_usergroups_add_channels"
        """Api admin usergroups add channels."""
        
        ADMIN_USERGROUPS_ADD_TEAMS = "slack_web_api_admin_usergroups_add_teams"
        """Api admin usergroups add teams."""
        
        ADMIN_USERGROUPS_LIST_CHANNELS = "slack_web_api_admin_usergroups_list_channels"
        """Api admin usergroups list channels."""
        
        ADMIN_USERGROUPS_REMOVE_CHANNELS = "slack_web_api_admin_usergroups_remove_channels"
        """Api admin usergroups remove channels."""
        
        ADMIN_USERS_ASSIGN = "slack_web_api_admin_users_assign"
        """Api admin users assign."""
        
        ADMIN_USERS_INVITE = "slack_web_api_admin_users_invite"
        """Api admin users invite."""
        
        ADMIN_USERS_LIST = "slack_web_api_admin_users_list"
        """Api admin users list."""
        
        ADMIN_USERS_REMOVE = "slack_web_api_admin_users_remove"
        """Api admin users remove."""
        
        ADMIN_USERS_SESSION_INVALIDATE = "slack_web_api_admin_users_session_invalidate"
        """Api admin users session invalidate."""
        
        ADMIN_USERS_SESSION_RESET = "slack_web_api_admin_users_session_reset"
        """Api admin users session reset."""
        
        ADMIN_USERS_SET_ADMIN = "slack_web_api_admin_users_set_admin"
        """Api admin users set admin."""
        
        ADMIN_USERS_SET_EXPIRATION = "slack_web_api_admin_users_set_expiration"
        """Api admin users set expiration."""
        
        ADMIN_USERS_SET_OWNER = "slack_web_api_admin_users_set_owner"
        """Api admin users set owner."""
        
        ADMIN_USERS_SET_REGULAR = "slack_web_api_admin_users_set_regular"
        """Api admin users set regular."""
        
        API_TEST = "slack_web_api_api_test"
        """Api api test."""
        
        APPS_EVENT_AUTHORIZATIONS_LIST = "slack_web_api_apps_event_authorizations_list"
        """Api apps event authorizations list."""
        
        APPS_PERMISSIONS_INFO = "slack_web_api_apps_permissions_info"
        """Api apps permissions info."""
        
        APPS_PERMISSIONS_REQUEST = "slack_web_api_apps_permissions_request"
        """Api apps permissions request."""
        
        APPS_PERMISSIONS_RESOURCES_LIST = "slack_web_api_apps_permissions_resources_list"
        """Api apps permissions resources list."""
        
        APPS_PERMISSIONS_SCOPES_LIST = "slack_web_api_apps_permissions_scopes_list"
        """Api apps permissions scopes list."""
        
        APPS_PERMISSIONS_USERS_LIST = "slack_web_api_apps_permissions_users_list"
        """Api apps permissions users list."""
        
        APPS_PERMISSIONS_USERS_REQUEST = "slack_web_api_apps_permissions_users_request"
        """Api apps permissions users request."""
        
        APPS_UNINSTALL = "slack_web_api_apps_uninstall"
        """Api apps uninstall."""
        
        AUTH_REVOKE = "slack_web_api_auth_revoke"
        """Api auth revoke."""
        
        AUTH_TEST = "slack_web_api_auth_test"
        """Api auth test."""
        
        BOTS_INFO = "slack_web_api_bots_info"
        """Api bots info."""
        
        CALLS_ADD = "slack_web_api_calls_add"
        """Api calls add."""
        
        CALLS_END = "slack_web_api_calls_end"
        """Api calls end."""
        
        CALLS_INFO = "slack_web_api_calls_info"
        """Api calls info."""
        
        CALLS_PARTICIPANTS_ADD = "slack_web_api_calls_participants_add"
        """Api calls participants add."""
        
        CALLS_PARTICIPANTS_REMOVE = "slack_web_api_calls_participants_remove"
        """Api calls participants remove."""
        
        CALLS_UPDATE = "slack_web_api_calls_update"
        """Api calls update."""
        
        CHAT_DELETE = "slack_web_api_chat_delete"
        """Api chat delete."""
        
        CHAT_DELETE_SCHEDULED_MESSAGE = "slack_web_api_chat_delete_scheduled_message"
        """Api chat delete scheduled message."""
        
        CHAT_GET_PERMALINK = "slack_web_api_chat_get_permalink"
        """Api chat get permalink."""
        
        CHAT_ME_MESSAGE = "slack_web_api_chat_me_message"
        """Api chat me message."""
        
        CHAT_POST_EPHEMERAL = "slack_web_api_chat_post_ephemeral"
        """Api chat post ephemeral."""
        
        CHAT_POST_MESSAGE = "slack_web_api_chat_post_message"
        """Api chat post message."""
        
        CHAT_SCHEDULED_MESSAGES_LIST = "slack_web_api_chat_scheduled_messages_list"
        """Api chat scheduled messages list."""
        
        CHAT_SCHEDULE_MESSAGE = "slack_web_api_chat_schedule_message"
        """Api chat schedule message."""
        
        CHAT_UNFURL = "slack_web_api_chat_unfurl"
        """Api chat unfurl."""
        
        CHAT_UPDATE = "slack_web_api_chat_update"
        """Api chat update."""
        
        CONVERSATIONS_ARCHIVE = "slack_web_api_conversations_archive"
        """Api conversations archive."""
        
        CONVERSATIONS_CLOSE = "slack_web_api_conversations_close"
        """Api conversations close."""
        
        CONVERSATIONS_CREATE = "slack_web_api_conversations_create"
        """Api conversations create."""
        
        CONVERSATIONS_HISTORY = "slack_web_api_conversations_history"
        """Api conversations history."""
        
        CONVERSATIONS_INFO = "slack_web_api_conversations_info"
        """Api conversations info."""
        
        CONVERSATIONS_INVITE = "slack_web_api_conversations_invite"
        """Api conversations invite."""
        
        CONVERSATIONS_JOIN = "slack_web_api_conversations_join"
        """Api conversations join."""
        
        CONVERSATIONS_KICK = "slack_web_api_conversations_kick"
        """Api conversations kick."""
        
        CONVERSATIONS_LEAVE = "slack_web_api_conversations_leave"
        """Api conversations leave."""
        
        CONVERSATIONS_LIST = "slack_web_api_conversations_list"
        """Api conversations list."""
        
        CONVERSATIONS_MARK = "slack_web_api_conversations_mark"
        """Api conversations mark."""
        
        CONVERSATIONS_MEMBERS = "slack_web_api_conversations_members"
        """Api conversations members."""
        
        CONVERSATIONS_OPEN = "slack_web_api_conversations_open"
        """Api conversations open."""
        
        CONVERSATIONS_RENAME = "slack_web_api_conversations_rename"
        """Api conversations rename."""
        
        CONVERSATIONS_REPLIES = "slack_web_api_conversations_replies"
        """Api conversations replies."""
        
        CONVERSATIONS_SET_PURPOSE = "slack_web_api_conversations_set_purpose"
        """Api conversations set purpose."""
        
        CONVERSATIONS_SET_TOPIC = "slack_web_api_conversations_set_topic"
        """Api conversations set topic."""
        
        CONVERSATIONS_UNARCHIVE = "slack_web_api_conversations_unarchive"
        """Api conversations unarchive."""
        
        DIALOG_OPEN = "slack_web_api_dialog_open"
        """Api dialog open."""
        
        DND_END_DND = "slack_web_api_dnd_end_dnd"
        """Api dnd end dnd."""
        
        DND_END_SNOOZE = "slack_web_api_dnd_end_snooze"
        """Api dnd end snooze."""
        
        DND_INFO = "slack_web_api_dnd_info"
        """Api dnd info."""
        
        DND_SET_SNOOZE = "slack_web_api_dnd_set_snooze"
        """Api dnd set snooze."""
        
        DND_TEAM_INFO = "slack_web_api_dnd_team_info"
        """Api dnd team info."""
        
        EMOJI_LIST = "slack_web_api_emoji_list"
        """Api emoji list."""
        
        FILES_COMMENTS_DELETE = "slack_web_api_files_comments_delete"
        """Api files comments delete."""
        
        FILES_DELETE = "slack_web_api_files_delete"
        """Api files delete."""
        
        FILES_INFO = "slack_web_api_files_info"
        """Api files info."""
        
        FILES_LIST = "slack_web_api_files_list"
        """Api files list."""
        
        FILES_REMOTE_ADD = "slack_web_api_files_remote_add"
        """Api files remote add."""
        
        FILES_REMOTE_INFO = "slack_web_api_files_remote_info"
        """Api files remote info."""
        
        FILES_REMOTE_LIST = "slack_web_api_files_remote_list"
        """Api files remote list."""
        
        FILES_REMOTE_REMOVE = "slack_web_api_files_remote_remove"
        """Api files remote remove."""
        
        FILES_REMOTE_SHARE = "slack_web_api_files_remote_share"
        """Api files remote share."""
        
        FILES_REMOTE_UPDATE = "slack_web_api_files_remote_update"
        """Api files remote update."""
        
        FILES_REVOKE_PUBLIC_URL = "slack_web_api_files_revoke_public_url"
        """Api files revoke public url."""
        
        FILES_SHARED_PUBLIC_URL = "slack_web_api_files_shared_public_url"
        """Api files shared public url."""
        
        FILES_UPLOAD = "slack_web_api_files_upload"
        """Api files upload."""
        
        MIGRATION_EXCHANGE = "slack_web_api_migration_exchange"
        """Api migration exchange."""
        
        OAUTH_ACCESS = "slack_web_api_oauth_access"
        """Api oauth access."""
        
        OAUTH_TOKEN = "slack_web_api_oauth_token"
        """Api oauth token."""
        
        OAUTH_V2_ACCESS = "slack_web_api_oauth_v2_access"
        """Api oauth v2 access."""
        
        PINS_ADD = "slack_web_api_pins_add"
        """Api pins add."""
        
        PINS_LIST = "slack_web_api_pins_list"
        """Api pins list."""
        
        PINS_REMOVE = "slack_web_api_pins_remove"
        """Api pins remove."""
        
        REACTIONS_ADD = "slack_web_api_reactions_add"
        """Api reactions add."""
        
        REACTIONS_GET = "slack_web_api_reactions_get"
        """Api reactions get."""
        
        REACTIONS_LIST = "slack_web_api_reactions_list"
        """Api reactions list."""
        
        REACTIONS_REMOVE = "slack_web_api_reactions_remove"
        """Api reactions remove."""
        
        REMINDERS_ADD = "slack_web_api_reminders_add"
        """Api reminders add."""
        
        REMINDERS_COMPLETE = "slack_web_api_reminders_complete"
        """Api reminders complete."""
        
        REMINDERS_DELETE = "slack_web_api_reminders_delete"
        """Api reminders delete."""
        
        REMINDERS_INFO = "slack_web_api_reminders_info"
        """Api reminders info."""
        
        REMINDERS_LIST = "slack_web_api_reminders_list"
        """Api reminders list."""
        
        RTM_CONNECT = "slack_web_api_rtm_connect"
        """Api rtm connect."""
        
        SEARCH_MESSAGES = "slack_web_api_search_messages"
        """Api search messages."""
        
        STARS_ADD = "slack_web_api_stars_add"
        """Api stars add."""
        
        STARS_LIST = "slack_web_api_stars_list"
        """Api stars list."""
        
        STARS_REMOVE = "slack_web_api_stars_remove"
        """Api stars remove."""
        
        TEAM_ACCESS_LOGS = "slack_web_api_team_access_logs"
        """Api team access logs."""
        
        TEAM_BILLABLE_INFO = "slack_web_api_team_billable_info"
        """Api team billable info."""
        
        TEAM_INFO = "slack_web_api_team_info"
        """Api team info."""
        
        TEAM_INTEGRATION_LOGS = "slack_web_api_team_integration_logs"
        """Api team integration logs."""
        
        TEAM_PROFILE_GET = "slack_web_api_team_profile_get"
        """Api team profile get."""
        
        USERGROUPS_CREATE = "slack_web_api_usergroups_create"
        """Api usergroups create."""
        
        USERGROUPS_DISABLE = "slack_web_api_usergroups_disable"
        """Api usergroups disable."""
        
        USERGROUPS_ENABLE = "slack_web_api_usergroups_enable"
        """Api usergroups enable."""
        
        USERGROUPS_LIST = "slack_web_api_usergroups_list"
        """Api usergroups list."""
        
        USERGROUPS_UPDATE = "slack_web_api_usergroups_update"
        """Api usergroups update."""
        
        USERGROUPS_USERS_LIST = "slack_web_api_usergroups_users_list"
        """Api usergroups users list."""
        
        USERGROUPS_USERS_UPDATE = "slack_web_api_usergroups_users_update"
        """Api usergroups users update."""
        
        USERS_CONVERSATIONS = "slack_web_api_users_conversations"
        """Api users conversations."""
        
        USERS_DELETE_PHOTO = "slack_web_api_users_delete_photo"
        """Api users delete photo."""
        
        USERS_GET_PRESENCE = "slack_web_api_users_get_presence"
        """Api users get presence."""
        
        USERS_IDENTITY = "slack_web_api_users_identity"
        """Api users identity."""
        
        USERS_INFO = "slack_web_api_users_info"
        """Api users info."""
        
        USERS_LIST = "slack_web_api_users_list"
        """Api users list."""
        
        USERS_LOOKUP_BY_EMAIL = "slack_web_api_users_lookup_by_email"
        """Api users lookup by email."""
        
        USERS_PROFILE_GET = "slack_web_api_users_profile_get"
        """Api users profile get."""
        
        USERS_PROFILE_SET = "slack_web_api_users_profile_set"
        """Api users profile set."""
        
        USERS_SET_ACTIVE = "slack_web_api_users_set_active"
        """Api users set active."""
        
        USERS_SET_PHOTO = "slack_web_api_users_set_photo"
        """Api users set photo."""
        
        USERS_SET_PRESENCE = "slack_web_api_users_set_presence"
        """Api users set presence."""
        
        VIEWS_OPEN = "slack_web_api_views_open"
        """Api views open."""
        
        VIEWS_PUBLISH = "slack_web_api_views_publish"
        """Api views publish."""
        
        VIEWS_PUSH = "slack_web_api_views_push"
        """Api views push."""
        
        VIEWS_UPDATE = "slack_web_api_views_update"
        """Api views update."""
        
        WORKFLOWS_STEP_COMPLETED = "slack_web_api_workflows_step_completed"
        """Api workflows step completed."""
        
        WORKFLOWS_STEP_FAILED = "slack_web_api_workflows_step_failed"
        """Api workflows step failed."""
        
        WORKFLOWS_UPDATE_STEP = "slack_web_api_workflows_update_step"
        """Api workflows update step."""
        

    class Stripe(str, Enum):
        def get_api_service(self) -> APIService:
            return APIService.STRIPE
        
        DELETE_ACCOUNTS_ACCOUNT = "stripe_delete_accounts_account"
        """Accounts account."""
        
        DELETE_ACCOUNTS_ACCOUNT_BANK_ACCOUNTS_ID = "stripe_delete_accounts_account_bank_accounts_id"
        """Accounts account bank accounts id."""
        
        DELETE_ACCOUNTS_ACCOUNT_EXTERNAL_ACCOUNTS_ID = "stripe_delete_accounts_account_external_accounts_id"
        """Accounts account external accounts id."""
        
        DELETE_ACCOUNTS_ACCOUNT_PEOPLE_PERSON = "stripe_delete_accounts_account_people_person"
        """Accounts account people person."""
        
        DELETE_ACCOUNTS_ACCOUNT_PERSONS_PERSON = "stripe_delete_accounts_account_persons_person"
        """Accounts account persons person."""
        
        DELETE_APPLE_PAY_DOMAINS_DOMAIN = "stripe_delete_apple_pay_domains_domain"
        """Apple pay domains domain."""
        
        DELETE_COUPONS_COUPON = "stripe_delete_coupons_coupon"
        """Coupons coupon."""
        
        DELETE_CUSTOMERS_CUSTOMER = "stripe_delete_customers_customer"
        """Customers customer."""
        
        DELETE_CUSTOMERS_CUSTOMER_BANK_ACCOUNTS_ID = "stripe_delete_customers_customer_bank_accounts_id"
        """Customers customer bank accounts id."""
        
        DELETE_CUSTOMERS_CUSTOMER_CARDS_ID = "stripe_delete_customers_customer_cards_id"
        """Customers customer cards id."""
        
        DELETE_CUSTOMERS_CUSTOMER_DISCOUNT = "stripe_delete_customers_customer_discount"
        """Customers customer discount."""
        
        DELETE_CUSTOMERS_CUSTOMER_SOURCES_ID = "stripe_delete_customers_customer_sources_id"
        """Customers customer sources id."""
        
        DELETE_CUSTOMERS_CUSTOMER_SUBSCRIPTIONS_SUBSCRIPTION_EXPOSED_ID = "stripe_delete_customers_customer_subscriptions_subscription_exposed_id"
        """Customers customer subscriptions subscription exposed id."""
        
        DELETE_CUSTOMERS_CUSTOMER_SUBSCRIPTIONS_SUBSCRIPTION_EXPOSED_ID_DISCOUNT = "stripe_delete_customers_customer_subscriptions_subscription_exposed_id_discount"
        """Customers customer subscriptions subscription exposed id discount."""
        
        DELETE_CUSTOMERS_CUSTOMER_TAX_IDS_ID = "stripe_delete_customers_customer_tax_ids_id"
        """Customers customer tax ids id."""
        
        DELETE_EPHEMERAL_KEYS_KEY = "stripe_delete_ephemeral_keys_key"
        """Ephemeral keys key."""
        
        DELETE_INVOICEITEMS_INVOICEITEM = "stripe_delete_invoiceitems_invoiceitem"
        """Invoiceitems invoiceitem."""
        
        DELETE_INVOICES_INVOICE = "stripe_delete_invoices_invoice"
        """Invoices invoice."""
        
        DELETE_PLANS_PLAN = "stripe_delete_plans_plan"
        """Plans plan."""
        
        DELETE_PRODUCTS_ID = "stripe_delete_products_id"
        """Products id."""
        
        DELETE_PRODUCTS_PRODUCT_FEATURES_ID = "stripe_delete_products_product_features_id"
        """Products product features id."""
        
        DELETE_RADAR_VALUE_LISTS_VALUE_LIST = "stripe_delete_radar_value_lists_value_list"
        """Radar value lists value list."""
        
        DELETE_RADAR_VALUE_LIST_ITEMS_ITEM = "stripe_delete_radar_value_list_items_item"
        """Radar value list items item."""
        
        DELETE_SUBSCRIPTIONS_SUBSCRIPTION_EXPOSED_ID = "stripe_delete_subscriptions_subscription_exposed_id"
        """Subscriptions subscription exposed id."""
        
        DELETE_SUBSCRIPTIONS_SUBSCRIPTION_EXPOSED_ID_DISCOUNT = "stripe_delete_subscriptions_subscription_exposed_id_discount"
        """Subscriptions subscription exposed id discount."""
        
        DELETE_SUBSCRIPTION_ITEMS_ITEM = "stripe_delete_subscription_items_item"
        """Subscription items item."""
        
        DELETE_TAX_IDS_ID = "stripe_delete_tax_ids_id"
        """Tax ids id."""
        
        DELETE_TERMINAL_CONFIGURATIONS_CONFIGURATION = "stripe_delete_terminal_configurations_configuration"
        """Terminal configurations configuration."""
        
        DELETE_TERMINAL_LOCATIONS_LOCATION = "stripe_delete_terminal_locations_location"
        """Terminal locations location."""
        
        DELETE_TERMINAL_READERS_READER = "stripe_delete_terminal_readers_reader"
        """Terminal readers reader."""
        
        DELETE_TEST_HELPERS_TEST_CLOCKS_TEST_CLOCK = "stripe_delete_test_helpers_test_clocks_test_clock"
        """Test helpers test clocks test clock."""
        
        DELETE_WEBHOOK_ENDPOINTS_WEBHOOK_ENDPOINT = "stripe_delete_webhook_endpoints_webhook_endpoint"
        """Webhook endpoints webhook endpoint."""
        
        GET_ACCOUNT = "stripe_get_account"
        """Account."""
        
        GET_ACCOUNTS = "stripe_get_accounts"
        """Accounts."""
        
        GET_ACCOUNTS_ACCOUNT = "stripe_get_accounts_account"
        """Accounts account."""
        
        GET_ACCOUNTS_ACCOUNT_BANK_ACCOUNTS_ID = "stripe_get_accounts_account_bank_accounts_id"
        """Accounts account bank accounts id."""
        
        GET_ACCOUNTS_ACCOUNT_CAPABILITIES = "stripe_get_accounts_account_capabilities"
        """Accounts account capabilities."""
        
        GET_ACCOUNTS_ACCOUNT_CAPABILITIES_CAPABILITY = "stripe_get_accounts_account_capabilities_capability"
        """Accounts account capabilities capability."""
        
        GET_ACCOUNTS_ACCOUNT_EXTERNAL_ACCOUNTS = "stripe_get_accounts_account_external_accounts"
        """Accounts account external accounts."""
        
        GET_ACCOUNTS_ACCOUNT_EXTERNAL_ACCOUNTS_ID = "stripe_get_accounts_account_external_accounts_id"
        """Accounts account external accounts id."""
        
        GET_ACCOUNTS_ACCOUNT_PEOPLE = "stripe_get_accounts_account_people"
        """Accounts account people."""
        
        GET_ACCOUNTS_ACCOUNT_PEOPLE_PERSON = "stripe_get_accounts_account_people_person"
        """Accounts account people person."""
        
        GET_ACCOUNTS_ACCOUNT_PERSONS = "stripe_get_accounts_account_persons"
        """Accounts account persons."""
        
        GET_ACCOUNTS_ACCOUNT_PERSONS_PERSON = "stripe_get_accounts_account_persons_person"
        """Accounts account persons person."""
        
        GET_APPLE_PAY_DOMAINS = "stripe_get_apple_pay_domains"
        """Apple pay domains."""
        
        GET_APPLE_PAY_DOMAINS_DOMAIN = "stripe_get_apple_pay_domains_domain"
        """Apple pay domains domain."""
        
        GET_APPLICATION_FEES = "stripe_get_application_fees"
        """Application fees."""
        
        GET_APPLICATION_FEES_FEE_REFUNDS_ID = "stripe_get_application_fees_fee_refunds_id"
        """Application fees fee refunds id."""
        
        GET_APPLICATION_FEES_ID = "stripe_get_application_fees_id"
        """Application fees id."""
        
        GET_APPLICATION_FEES_ID_REFUNDS = "stripe_get_application_fees_id_refunds"
        """Application fees id refunds."""
        
        GET_APPS_SECRETS = "stripe_get_apps_secrets"
        """Apps secrets."""
        
        GET_APPS_SECRETS_FIND = "stripe_get_apps_secrets_find"
        """Apps secrets find."""
        
        GET_BALANCE = "stripe_get_balance"
        """Balance."""
        
        GET_BALANCE_HISTORY = "stripe_get_balance_history"
        """Balance history."""
        
        GET_BALANCE_HISTORY_ID = "stripe_get_balance_history_id"
        """Balance history id."""
        
        GET_BALANCE_TRANSACTIONS = "stripe_get_balance_transactions"
        """Balance transactions."""
        
        GET_BALANCE_TRANSACTIONS_ID = "stripe_get_balance_transactions_id"
        """Balance transactions id."""
        
        GET_BILLING_ALERTS = "stripe_get_billing_alerts"
        """Billing alerts."""
        
        GET_BILLING_ALERTS_ID = "stripe_get_billing_alerts_id"
        """Billing alerts id."""
        
        GET_BILLING_CREDIT_BALANCE_SUMMARY = "stripe_get_billing_credit_balance_summary"
        """Billing credit balance summary."""
        
        GET_BILLING_CREDIT_BALANCE_TRANSACTIONS = "stripe_get_billing_credit_balance_transactions"
        """Billing credit balance transactions."""
        
        GET_BILLING_CREDIT_BALANCE_TRANSACTIONS_ID = "stripe_get_billing_credit_balance_transactions_id"
        """Billing credit balance transactions id."""
        
        GET_BILLING_CREDIT_GRANTS = "stripe_get_billing_credit_grants"
        """Billing credit grants."""
        
        GET_BILLING_CREDIT_GRANTS_ID = "stripe_get_billing_credit_grants_id"
        """Billing credit grants id."""
        
        GET_BILLING_METERS = "stripe_get_billing_meters"
        """Billing meters."""
        
        GET_BILLING_METERS_ID = "stripe_get_billing_meters_id"
        """Billing meters id."""
        
        GET_BILLING_METERS_ID_EVENT_SUMMARIES = "stripe_get_billing_meters_id_event_summaries"
        """Billing meters id event summaries."""
        
        GET_BILLING_PORTAL_CONFIGURATIONS = "stripe_get_billing_portal_configurations"
        """Billing portal configurations."""
        
        GET_BILLING_PORTAL_CONFIGURATIONS_CONFIGURATION = "stripe_get_billing_portal_configurations_configuration"
        """Billing portal configurations configuration."""
        
        GET_CHARGES = "stripe_get_charges"
        """Charges."""
        
        GET_CHARGES_CHARGE = "stripe_get_charges_charge"
        """Charges charge."""
        
        GET_CHARGES_CHARGE_DISPUTE = "stripe_get_charges_charge_dispute"
        """Charges charge dispute."""
        
        GET_CHARGES_CHARGE_REFUNDS = "stripe_get_charges_charge_refunds"
        """Charges charge refunds."""
        
        GET_CHARGES_CHARGE_REFUNDS_REFUND = "stripe_get_charges_charge_refunds_refund"
        """Charges charge refunds refund."""
        
        GET_CHARGES_SEARCH = "stripe_get_charges_search"
        """Charges search."""
        
        GET_CHECKOUT_SESSIONS = "stripe_get_checkout_sessions"
        """Checkout sessions."""
        
        GET_CHECKOUT_SESSIONS_SESSION = "stripe_get_checkout_sessions_session"
        """Checkout sessions session."""
        
        GET_CHECKOUT_SESSIONS_SESSION_LINE_ITEMS = "stripe_get_checkout_sessions_session_line_items"
        """Checkout sessions session line items."""
        
        GET_CLIMATE_ORDERS = "stripe_get_climate_orders"
        """Climate orders."""
        
        GET_CLIMATE_ORDERS_ORDER = "stripe_get_climate_orders_order"
        """Climate orders order."""
        
        GET_CLIMATE_PRODUCTS = "stripe_get_climate_products"
        """Climate products."""
        
        GET_CLIMATE_PRODUCTS_PRODUCT = "stripe_get_climate_products_product"
        """Climate products product."""
        
        GET_CLIMATE_SUPPLIERS = "stripe_get_climate_suppliers"
        """Climate suppliers."""
        
        GET_CLIMATE_SUPPLIERS_SUPPLIER = "stripe_get_climate_suppliers_supplier"
        """Climate suppliers supplier."""
        
        GET_CONFIRMATION_TOKENS_CONFIRMATION_TOKEN = "stripe_get_confirmation_tokens_confirmation_token"
        """Confirmation tokens confirmation token."""
        
        GET_COUNTRY_SPECS = "stripe_get_country_specs"
        """Country specs."""
        
        GET_COUNTRY_SPECS_COUNTRY = "stripe_get_country_specs_country"
        """Country specs country."""
        
        GET_COUPONS = "stripe_get_coupons"
        """Coupons."""
        
        GET_COUPONS_COUPON = "stripe_get_coupons_coupon"
        """Coupons coupon."""
        
        GET_CREDIT_NOTES = "stripe_get_credit_notes"
        """Credit notes."""
        
        GET_CREDIT_NOTES_CREDIT_NOTE_LINES = "stripe_get_credit_notes_credit_note_lines"
        """Credit notes credit note lines."""
        
        GET_CREDIT_NOTES_ID = "stripe_get_credit_notes_id"
        """Credit notes id."""
        
        GET_CREDIT_NOTES_PREVIEW = "stripe_get_credit_notes_preview"
        """Credit notes preview."""
        
        GET_CREDIT_NOTES_PREVIEW_LINES = "stripe_get_credit_notes_preview_lines"
        """Credit notes preview lines."""
        
        GET_CUSTOMERS = "stripe_get_customers"
        """Customers."""
        
        GET_CUSTOMERS_CUSTOMER = "stripe_get_customers_customer"
        """Customers customer."""
        
        GET_CUSTOMERS_CUSTOMER_BALANCE_TRANSACTIONS = "stripe_get_customers_customer_balance_transactions"
        """Customers customer balance transactions."""
        
        GET_CUSTOMERS_CUSTOMER_BALANCE_TRANSACTIONS_TRANSACTION = "stripe_get_customers_customer_balance_transactions_transaction"
        """Customers customer balance transactions transaction."""
        
        GET_CUSTOMERS_CUSTOMER_BANK_ACCOUNTS = "stripe_get_customers_customer_bank_accounts"
        """Customers customer bank accounts."""
        
        GET_CUSTOMERS_CUSTOMER_BANK_ACCOUNTS_ID = "stripe_get_customers_customer_bank_accounts_id"
        """Customers customer bank accounts id."""
        
        GET_CUSTOMERS_CUSTOMER_CARDS = "stripe_get_customers_customer_cards"
        """Customers customer cards."""
        
        GET_CUSTOMERS_CUSTOMER_CARDS_ID = "stripe_get_customers_customer_cards_id"
        """Customers customer cards id."""
        
        GET_CUSTOMERS_CUSTOMER_CASH_BALANCE = "stripe_get_customers_customer_cash_balance"
        """Customers customer cash balance."""
        
        GET_CUSTOMERS_CUSTOMER_CASH_BALANCE_TRANSACTIONS = "stripe_get_customers_customer_cash_balance_transactions"
        """Customers customer cash balance transactions."""
        
        GET_CUSTOMERS_CUSTOMER_CASH_BALANCE_TRANSACTIONS_TRANSACTION = "stripe_get_customers_customer_cash_balance_transactions_transaction"
        """Customers customer cash balance transactions transaction."""
        
        GET_CUSTOMERS_CUSTOMER_DISCOUNT = "stripe_get_customers_customer_discount"
        """Customers customer discount."""
        
        GET_CUSTOMERS_CUSTOMER_PAYMENT_METHODS = "stripe_get_customers_customer_payment_methods"
        """Customers customer payment methods."""
        
        GET_CUSTOMERS_CUSTOMER_PAYMENT_METHODS_PAYMENT_METHOD = "stripe_get_customers_customer_payment_methods_payment_method"
        """Customers customer payment methods payment method."""
        
        GET_CUSTOMERS_CUSTOMER_SOURCES = "stripe_get_customers_customer_sources"
        """Customers customer sources."""
        
        GET_CUSTOMERS_CUSTOMER_SOURCES_ID = "stripe_get_customers_customer_sources_id"
        """Customers customer sources id."""
        
        GET_CUSTOMERS_CUSTOMER_SUBSCRIPTIONS = "stripe_get_customers_customer_subscriptions"
        """Customers customer subscriptions."""
        
        GET_CUSTOMERS_CUSTOMER_SUBSCRIPTIONS_SUBSCRIPTION_EXPOSED_ID = "stripe_get_customers_customer_subscriptions_subscription_exposed_id"
        """Customers customer subscriptions subscription exposed id."""
        
        GET_CUSTOMERS_CUSTOMER_SUBSCRIPTIONS_SUBSCRIPTION_EXPOSED_ID_DISCOUNT = "stripe_get_customers_customer_subscriptions_subscription_exposed_id_discount"
        """Customers customer subscriptions subscription exposed id discount."""
        
        GET_CUSTOMERS_CUSTOMER_TAX_IDS = "stripe_get_customers_customer_tax_ids"
        """Customers customer tax ids."""
        
        GET_CUSTOMERS_CUSTOMER_TAX_IDS_ID = "stripe_get_customers_customer_tax_ids_id"
        """Customers customer tax ids id."""
        
        GET_CUSTOMERS_SEARCH = "stripe_get_customers_search"
        """Customers search."""
        
        GET_DISPUTES = "stripe_get_disputes"
        """Disputes."""
        
        GET_DISPUTES_DISPUTE = "stripe_get_disputes_dispute"
        """Disputes dispute."""
        
        GET_ENTITLEMENTS_ACTIVE_ENTITLEMENTS = "stripe_get_entitlements_active_entitlements"
        """Entitlements active entitlements."""
        
        GET_ENTITLEMENTS_ACTIVE_ENTITLEMENTS_ID = "stripe_get_entitlements_active_entitlements_id"
        """Entitlements active entitlements id."""
        
        GET_ENTITLEMENTS_FEATURES = "stripe_get_entitlements_features"
        """Entitlements features."""
        
        GET_ENTITLEMENTS_FEATURES_ID = "stripe_get_entitlements_features_id"
        """Entitlements features id."""
        
        GET_EVENTS = "stripe_get_events"
        """Events."""
        
        GET_EVENTS_ID = "stripe_get_events_id"
        """Events id."""
        
        GET_EXCHANGE_RATES = "stripe_get_exchange_rates"
        """Exchange rates."""
        
        GET_EXCHANGE_RATES_RATE_ID = "stripe_get_exchange_rates_rate_id"
        """Exchange rates rate id."""
        
        GET_FILES = "stripe_get_files"
        """Files."""
        
        GET_FILES_FILE = "stripe_get_files_file"
        """Files file."""
        
        GET_FILE_LINKS = "stripe_get_file_links"
        """File links."""
        
        GET_FILE_LINKS_LINK = "stripe_get_file_links_link"
        """File links link."""
        
        GET_FINANCIAL_CONNECTIONS_ACCOUNTS = "stripe_get_financial_connections_accounts"
        """Financial connections accounts."""
        
        GET_FINANCIAL_CONNECTIONS_ACCOUNTS_ACCOUNT = "stripe_get_financial_connections_accounts_account"
        """Financial connections accounts account."""
        
        GET_FINANCIAL_CONNECTIONS_ACCOUNTS_ACCOUNT_OWNERS = "stripe_get_financial_connections_accounts_account_owners"
        """Financial connections accounts account owners."""
        
        GET_FINANCIAL_CONNECTIONS_SESSIONS_SESSION = "stripe_get_financial_connections_sessions_session"
        """Financial connections sessions session."""
        
        GET_FINANCIAL_CONNECTIONS_TRANSACTIONS = "stripe_get_financial_connections_transactions"
        """Financial connections transactions."""
        
        GET_FINANCIAL_CONNECTIONS_TRANSACTIONS_TRANSACTION = "stripe_get_financial_connections_transactions_transaction"
        """Financial connections transactions transaction."""
        
        GET_FORWARDING_REQUESTS = "stripe_get_forwarding_requests"
        """Forwarding requests."""
        
        GET_FORWARDING_REQUESTS_ID = "stripe_get_forwarding_requests_id"
        """Forwarding requests id."""
        
        GET_IDENTITY_VERIFICATION_REPORTS = "stripe_get_identity_verification_reports"
        """Identity verification reports."""
        
        GET_IDENTITY_VERIFICATION_REPORTS_REPORT = "stripe_get_identity_verification_reports_report"
        """Identity verification reports report."""
        
        GET_IDENTITY_VERIFICATION_SESSIONS = "stripe_get_identity_verification_sessions"
        """Identity verification sessions."""
        
        GET_IDENTITY_VERIFICATION_SESSIONS_SESSION = "stripe_get_identity_verification_sessions_session"
        """Identity verification sessions session."""
        
        GET_INVOICEITEMS = "stripe_get_invoiceitems"
        """Invoiceitems."""
        
        GET_INVOICEITEMS_INVOICEITEM = "stripe_get_invoiceitems_invoiceitem"
        """Invoiceitems invoiceitem."""
        
        GET_INVOICES = "stripe_get_invoices"
        """Invoices."""
        
        GET_INVOICES_INVOICE = "stripe_get_invoices_invoice"
        """Invoices invoice."""
        
        GET_INVOICES_INVOICE_LINES = "stripe_get_invoices_invoice_lines"
        """Invoices invoice lines."""
        
        GET_INVOICES_SEARCH = "stripe_get_invoices_search"
        """Invoices search."""
        
        GET_INVOICES_UPCOMING = "stripe_get_invoices_upcoming"
        """Invoices upcoming."""
        
        GET_INVOICES_UPCOMING_LINES = "stripe_get_invoices_upcoming_lines"
        """Invoices upcoming lines."""
        
        GET_INVOICE_RENDERING_TEMPLATES = "stripe_get_invoice_rendering_templates"
        """Invoice rendering templates."""
        
        GET_INVOICE_RENDERING_TEMPLATES_TEMPLATE = "stripe_get_invoice_rendering_templates_template"
        """Invoice rendering templates template."""
        
        GET_ISSUING_AUTHORIZATIONS = "stripe_get_issuing_authorizations"
        """Issuing authorizations."""
        
        GET_ISSUING_AUTHORIZATIONS_AUTHORIZATION = "stripe_get_issuing_authorizations_authorization"
        """Issuing authorizations authorization."""
        
        GET_ISSUING_CARDHOLDERS = "stripe_get_issuing_cardholders"
        """Issuing cardholders."""
        
        GET_ISSUING_CARDHOLDERS_CARDHOLDER = "stripe_get_issuing_cardholders_cardholder"
        """Issuing cardholders cardholder."""
        
        GET_ISSUING_CARDS = "stripe_get_issuing_cards"
        """Issuing cards."""
        
        GET_ISSUING_CARDS_CARD = "stripe_get_issuing_cards_card"
        """Issuing cards card."""
        
        GET_ISSUING_DISPUTES = "stripe_get_issuing_disputes"
        """Issuing disputes."""
        
        GET_ISSUING_DISPUTES_DISPUTE = "stripe_get_issuing_disputes_dispute"
        """Issuing disputes dispute."""
        
        GET_ISSUING_PERSONALIZATION_DESIGNS = "stripe_get_issuing_personalization_designs"
        """Issuing personalization designs."""
        
        GET_ISSUING_PERSONALIZATION_DESIGNS_PERSONALIZATION_DESIGN = "stripe_get_issuing_personalization_designs_personalization_design"
        """Issuing personalization designs personalization design."""
        
        GET_ISSUING_PHYSICAL_BUNDLES = "stripe_get_issuing_physical_bundles"
        """Issuing physical bundles."""
        
        GET_ISSUING_PHYSICAL_BUNDLES_PHYSICAL_BUNDLE = "stripe_get_issuing_physical_bundles_physical_bundle"
        """Issuing physical bundles physical bundle."""
        
        GET_ISSUING_SETTLEMENTS_SETTLEMENT = "stripe_get_issuing_settlements_settlement"
        """Issuing settlements settlement."""
        
        GET_ISSUING_TOKENS = "stripe_get_issuing_tokens"
        """Issuing tokens."""
        
        GET_ISSUING_TOKENS_TOKEN = "stripe_get_issuing_tokens_token"
        """Issuing tokens token."""
        
        GET_ISSUING_TRANSACTIONS = "stripe_get_issuing_transactions"
        """Issuing transactions."""
        
        GET_ISSUING_TRANSACTIONS_TRANSACTION = "stripe_get_issuing_transactions_transaction"
        """Issuing transactions transaction."""
        
        GET_LINKED_ACCOUNTS = "stripe_get_linked_accounts"
        """Linked accounts."""
        
        GET_LINKED_ACCOUNTS_ACCOUNT = "stripe_get_linked_accounts_account"
        """Linked accounts account."""
        
        GET_LINKED_ACCOUNTS_ACCOUNT_OWNERS = "stripe_get_linked_accounts_account_owners"
        """Linked accounts account owners."""
        
        GET_LINK_ACCOUNT_SESSIONS_SESSION = "stripe_get_link_account_sessions_session"
        """Link account sessions session."""
        
        GET_MANDATES_MANDATE = "stripe_get_mandates_mandate"
        """Mandates mandate."""
        
        GET_PAYMENT_INTENTS = "stripe_get_payment_intents"
        """Payment intents."""
        
        GET_PAYMENT_INTENTS_INTENT = "stripe_get_payment_intents_intent"
        """Payment intents intent."""
        
        GET_PAYMENT_INTENTS_SEARCH = "stripe_get_payment_intents_search"
        """Payment intents search."""
        
        GET_PAYMENT_LINKS = "stripe_get_payment_links"
        """Payment links."""
        
        GET_PAYMENT_LINKS_PAYMENT_LINK = "stripe_get_payment_links_payment_link"
        """Payment links payment link."""
        
        GET_PAYMENT_LINKS_PAYMENT_LINK_LINE_ITEMS = "stripe_get_payment_links_payment_link_line_items"
        """Payment links payment link line items."""
        
        GET_PAYMENT_METHODS = "stripe_get_payment_methods"
        """Payment methods."""
        
        GET_PAYMENT_METHODS_PAYMENT_METHOD = "stripe_get_payment_methods_payment_method"
        """Payment methods payment method."""
        
        GET_PAYMENT_METHOD_CONFIGURATIONS = "stripe_get_payment_method_configurations"
        """Payment method configurations."""
        
        GET_PAYMENT_METHOD_CONFIGURATIONS_CONFIGURATION = "stripe_get_payment_method_configurations_configuration"
        """Payment method configurations configuration."""
        
        GET_PAYMENT_METHOD_DOMAINS = "stripe_get_payment_method_domains"
        """Payment method domains."""
        
        GET_PAYMENT_METHOD_DOMAINS_PAYMENT_METHOD_DOMAIN = "stripe_get_payment_method_domains_payment_method_domain"
        """Payment method domains payment method domain."""
        
        GET_PAYOUTS = "stripe_get_payouts"
        """Payouts."""
        
        GET_PAYOUTS_PAYOUT = "stripe_get_payouts_payout"
        """Payouts payout."""
        
        GET_PLANS = "stripe_get_plans"
        """Plans."""
        
        GET_PLANS_PLAN = "stripe_get_plans_plan"
        """Plans plan."""
        
        GET_PRICES = "stripe_get_prices"
        """Prices."""
        
        GET_PRICES_PRICE = "stripe_get_prices_price"
        """Prices price."""
        
        GET_PRICES_SEARCH = "stripe_get_prices_search"
        """Prices search."""
        
        GET_PRODUCTS = "stripe_get_products"
        """Products."""
        
        GET_PRODUCTS_ID = "stripe_get_products_id"
        """Products id."""
        
        GET_PRODUCTS_PRODUCT_FEATURES = "stripe_get_products_product_features"
        """Products product features."""
        
        GET_PRODUCTS_PRODUCT_FEATURES_ID = "stripe_get_products_product_features_id"
        """Products product features id."""
        
        GET_PRODUCTS_SEARCH = "stripe_get_products_search"
        """Products search."""
        
        GET_PROMOTION_CODES = "stripe_get_promotion_codes"
        """Promotion codes."""
        
        GET_PROMOTION_CODES_PROMOTION_CODE = "stripe_get_promotion_codes_promotion_code"
        """Promotion codes promotion code."""
        
        GET_QUOTES = "stripe_get_quotes"
        """Quotes."""
        
        GET_QUOTES_QUOTE = "stripe_get_quotes_quote"
        """Quotes quote."""
        
        GET_QUOTES_QUOTE_COMPUTED_UPFRONT_LINE_ITEMS = "stripe_get_quotes_quote_computed_upfront_line_items"
        """Quotes quote computed upfront line items."""
        
        GET_QUOTES_QUOTE_LINE_ITEMS = "stripe_get_quotes_quote_line_items"
        """Quotes quote line items."""
        
        GET_QUOTES_QUOTE_PDF = "stripe_get_quotes_quote_pdf"
        """Quotes quote pdf."""
        
        GET_RADAR_EARLY_FRAUD_WARNINGS = "stripe_get_radar_early_fraud_warnings"
        """Radar early fraud warnings."""
        
        GET_RADAR_EARLY_FRAUD_WARNINGS_EARLY_FRAUD_WARNING = "stripe_get_radar_early_fraud_warnings_early_fraud_warning"
        """Radar early fraud warnings early fraud warning."""
        
        GET_RADAR_VALUE_LISTS = "stripe_get_radar_value_lists"
        """Radar value lists."""
        
        GET_RADAR_VALUE_LISTS_VALUE_LIST = "stripe_get_radar_value_lists_value_list"
        """Radar value lists value list."""
        
        GET_RADAR_VALUE_LIST_ITEMS = "stripe_get_radar_value_list_items"
        """Radar value list items."""
        
        GET_RADAR_VALUE_LIST_ITEMS_ITEM = "stripe_get_radar_value_list_items_item"
        """Radar value list items item."""
        
        GET_REFUNDS = "stripe_get_refunds"
        """Refunds."""
        
        GET_REFUNDS_REFUND = "stripe_get_refunds_refund"
        """Refunds refund."""
        
        GET_REPORTING_REPORT_RUNS = "stripe_get_reporting_report_runs"
        """Reporting report runs."""
        
        GET_REPORTING_REPORT_RUNS_REPORT_RUN = "stripe_get_reporting_report_runs_report_run"
        """Reporting report runs report run."""
        
        GET_REPORTING_REPORT_TYPES = "stripe_get_reporting_report_types"
        """Reporting report types."""
        
        GET_REPORTING_REPORT_TYPES_REPORT_TYPE = "stripe_get_reporting_report_types_report_type"
        """Reporting report types report type."""
        
        GET_REVIEWS = "stripe_get_reviews"
        """Reviews."""
        
        GET_REVIEWS_REVIEW = "stripe_get_reviews_review"
        """Reviews review."""
        
        GET_SETUP_ATTEMPTS = "stripe_get_setup_attempts"
        """Setup attempts."""
        
        GET_SETUP_INTENTS = "stripe_get_setup_intents"
        """Setup intents."""
        
        GET_SETUP_INTENTS_INTENT = "stripe_get_setup_intents_intent"
        """Setup intents intent."""
        
        GET_SHIPPING_RATES = "stripe_get_shipping_rates"
        """Shipping rates."""
        
        GET_SHIPPING_RATES_SHIPPING_RATE_TOKEN = "stripe_get_shipping_rates_shipping_rate_token"
        """Shipping rates shipping rate token."""
        
        GET_SIGMA_SCHEDULED_QUERY_RUNS = "stripe_get_sigma_scheduled_query_runs"
        """Sigma scheduled query runs."""
        
        GET_SIGMA_SCHEDULED_QUERY_RUNS_SCHEDULED_QUERY_RUN = "stripe_get_sigma_scheduled_query_runs_scheduled_query_run"
        """Sigma scheduled query runs scheduled query run."""
        
        GET_SOURCES_SOURCE = "stripe_get_sources_source"
        """Sources source."""
        
        GET_SOURCES_SOURCE_MANDATE_NOTIFICATIONS_MANDATE_NOTIFICATION = "stripe_get_sources_source_mandate_notifications_mandate_notification"
        """Sources source mandate notifications mandate notification."""
        
        GET_SOURCES_SOURCE_SOURCE_TRANSACTIONS = "stripe_get_sources_source_source_transactions"
        """Sources source source transactions."""
        
        GET_SOURCES_SOURCE_SOURCE_TRANSACTIONS_SOURCE_TRANSACTION = "stripe_get_sources_source_source_transactions_source_transaction"
        """Sources source source transactions source transaction."""
        
        GET_SUBSCRIPTIONS = "stripe_get_subscriptions"
        """Subscriptions."""
        
        GET_SUBSCRIPTIONS_SEARCH = "stripe_get_subscriptions_search"
        """Subscriptions search."""
        
        GET_SUBSCRIPTIONS_SUBSCRIPTION_EXPOSED_ID = "stripe_get_subscriptions_subscription_exposed_id"
        """Subscriptions subscription exposed id."""
        
        GET_SUBSCRIPTION_ITEMS = "stripe_get_subscription_items"
        """Subscription items."""
        
        GET_SUBSCRIPTION_ITEMS_ITEM = "stripe_get_subscription_items_item"
        """Subscription items item."""
        
        GET_SUBSCRIPTION_ITEMS_SUBSCRIPTION_ITEM_USAGE_RECORD_SUMMARIES = "stripe_get_subscription_items_subscription_item_usage_record_summaries"
        """Subscription items subscription item usage record summaries."""
        
        GET_SUBSCRIPTION_SCHEDULES = "stripe_get_subscription_schedules"
        """Subscription schedules."""
        
        GET_SUBSCRIPTION_SCHEDULES_SCHEDULE = "stripe_get_subscription_schedules_schedule"
        """Subscription schedules schedule."""
        
        GET_TAX_CALCULATIONS_CALCULATION = "stripe_get_tax_calculations_calculation"
        """Tax calculations calculation."""
        
        GET_TAX_CALCULATIONS_CALCULATION_LINE_ITEMS = "stripe_get_tax_calculations_calculation_line_items"
        """Tax calculations calculation line items."""
        
        GET_TAX_CODES = "stripe_get_tax_codes"
        """Tax codes."""
        
        GET_TAX_CODES_ID = "stripe_get_tax_codes_id"
        """Tax codes id."""
        
        GET_TAX_IDS = "stripe_get_tax_ids"
        """Tax ids."""
        
        GET_TAX_IDS_ID = "stripe_get_tax_ids_id"
        """Tax ids id."""
        
        GET_TAX_RATES = "stripe_get_tax_rates"
        """Tax rates."""
        
        GET_TAX_RATES_TAX_RATE = "stripe_get_tax_rates_tax_rate"
        """Tax rates tax rate."""
        
        GET_TAX_REGISTRATIONS = "stripe_get_tax_registrations"
        """Tax registrations."""
        
        GET_TAX_REGISTRATIONS_ID = "stripe_get_tax_registrations_id"
        """Tax registrations id."""
        
        GET_TAX_SETTINGS = "stripe_get_tax_settings"
        """Tax settings."""
        
        GET_TAX_TRANSACTIONS_TRANSACTION = "stripe_get_tax_transactions_transaction"
        """Tax transactions transaction."""
        
        GET_TAX_TRANSACTIONS_TRANSACTION_LINE_ITEMS = "stripe_get_tax_transactions_transaction_line_items"
        """Tax transactions transaction line items."""
        
        GET_TERMINAL_CONFIGURATIONS = "stripe_get_terminal_configurations"
        """Terminal configurations."""
        
        GET_TERMINAL_CONFIGURATIONS_CONFIGURATION = "stripe_get_terminal_configurations_configuration"
        """Terminal configurations configuration."""
        
        GET_TERMINAL_LOCATIONS = "stripe_get_terminal_locations"
        """Terminal locations."""
        
        GET_TERMINAL_LOCATIONS_LOCATION = "stripe_get_terminal_locations_location"
        """Terminal locations location."""
        
        GET_TERMINAL_READERS = "stripe_get_terminal_readers"
        """Terminal readers."""
        
        GET_TERMINAL_READERS_READER = "stripe_get_terminal_readers_reader"
        """Terminal readers reader."""
        
        GET_TEST_HELPERS_TEST_CLOCKS = "stripe_get_test_helpers_test_clocks"
        """Test helpers test clocks."""
        
        GET_TEST_HELPERS_TEST_CLOCKS_TEST_CLOCK = "stripe_get_test_helpers_test_clocks_test_clock"
        """Test helpers test clocks test clock."""
        
        GET_TOKENS_TOKEN = "stripe_get_tokens_token"
        """Tokens token."""
        
        GET_TOPUPS = "stripe_get_topups"
        """Topups."""
        
        GET_TOPUPS_TOPUP = "stripe_get_topups_topup"
        """Topups topup."""
        
        GET_TRANSFERS = "stripe_get_transfers"
        """Transfers."""
        
        GET_TRANSFERS_ID_REVERSALS = "stripe_get_transfers_id_reversals"
        """Transfers id reversals."""
        
        GET_TRANSFERS_TRANSFER = "stripe_get_transfers_transfer"
        """Transfers transfer."""
        
        GET_TRANSFERS_TRANSFER_REVERSALS_ID = "stripe_get_transfers_transfer_reversals_id"
        """Transfers transfer reversals id."""
        
        GET_TREASURY_CREDIT_REVERSALS = "stripe_get_treasury_credit_reversals"
        """Treasury credit reversals."""
        
        GET_TREASURY_CREDIT_REVERSALS_CREDIT_REVERSAL = "stripe_get_treasury_credit_reversals_credit_reversal"
        """Treasury credit reversals credit reversal."""
        
        GET_TREASURY_DEBIT_REVERSALS = "stripe_get_treasury_debit_reversals"
        """Treasury debit reversals."""
        
        GET_TREASURY_DEBIT_REVERSALS_DEBIT_REVERSAL = "stripe_get_treasury_debit_reversals_debit_reversal"
        """Treasury debit reversals debit reversal."""
        
        GET_TREASURY_FINANCIAL_ACCOUNTS = "stripe_get_treasury_financial_accounts"
        """Treasury financial accounts."""
        
        GET_TREASURY_FINANCIAL_ACCOUNTS_FINANCIAL_ACCOUNT = "stripe_get_treasury_financial_accounts_financial_account"
        """Treasury financial accounts financial account."""
        
        GET_TREASURY_FINANCIAL_ACCOUNTS_FINANCIAL_ACCOUNT_FEATURES = "stripe_get_treasury_financial_accounts_financial_account_features"
        """Treasury financial accounts financial account features."""
        
        GET_TREASURY_INBOUND_TRANSFERS = "stripe_get_treasury_inbound_transfers"
        """Treasury inbound transfers."""
        
        GET_TREASURY_INBOUND_TRANSFERS_ID = "stripe_get_treasury_inbound_transfers_id"
        """Treasury inbound transfers id."""
        
        GET_TREASURY_OUTBOUND_PAYMENTS = "stripe_get_treasury_outbound_payments"
        """Treasury outbound payments."""
        
        GET_TREASURY_OUTBOUND_PAYMENTS_ID = "stripe_get_treasury_outbound_payments_id"
        """Treasury outbound payments id."""
        
        GET_TREASURY_OUTBOUND_TRANSFERS = "stripe_get_treasury_outbound_transfers"
        """Treasury outbound transfers."""
        
        GET_TREASURY_OUTBOUND_TRANSFERS_OUTBOUND_TRANSFER = "stripe_get_treasury_outbound_transfers_outbound_transfer"
        """Treasury outbound transfers outbound transfer."""
        
        GET_TREASURY_RECEIVED_CREDITS = "stripe_get_treasury_received_credits"
        """Treasury received credits."""
        
        GET_TREASURY_RECEIVED_CREDITS_ID = "stripe_get_treasury_received_credits_id"
        """Treasury received credits id."""
        
        GET_TREASURY_RECEIVED_DEBITS = "stripe_get_treasury_received_debits"
        """Treasury received debits."""
        
        GET_TREASURY_RECEIVED_DEBITS_ID = "stripe_get_treasury_received_debits_id"
        """Treasury received debits id."""
        
        GET_TREASURY_TRANSACTIONS = "stripe_get_treasury_transactions"
        """Treasury transactions."""
        
        GET_TREASURY_TRANSACTIONS_ID = "stripe_get_treasury_transactions_id"
        """Treasury transactions id."""
        
        GET_TREASURY_TRANSACTION_ENTRIES = "stripe_get_treasury_transaction_entries"
        """Treasury transaction entries."""
        
        GET_TREASURY_TRANSACTION_ENTRIES_ID = "stripe_get_treasury_transaction_entries_id"
        """Treasury transaction entries id."""
        
        GET_WEBHOOK_ENDPOINTS = "stripe_get_webhook_endpoints"
        """Webhook endpoints."""
        
        GET_WEBHOOK_ENDPOINTS_WEBHOOK_ENDPOINT = "stripe_get_webhook_endpoints_webhook_endpoint"
        """Webhook endpoints webhook endpoint."""
        
        POST_ACCOUNTS = "stripe_post_accounts"
        """Accounts."""
        
        POST_ACCOUNTS_ACCOUNT = "stripe_post_accounts_account"
        """Accounts account."""
        
        POST_ACCOUNTS_ACCOUNT_BANK_ACCOUNTS = "stripe_post_accounts_account_bank_accounts"
        """Accounts account bank accounts."""
        
        POST_ACCOUNTS_ACCOUNT_BANK_ACCOUNTS_ID = "stripe_post_accounts_account_bank_accounts_id"
        """Accounts account bank accounts id."""
        
        POST_ACCOUNTS_ACCOUNT_CAPABILITIES_CAPABILITY = "stripe_post_accounts_account_capabilities_capability"
        """Accounts account capabilities capability."""
        
        POST_ACCOUNTS_ACCOUNT_EXTERNAL_ACCOUNTS = "stripe_post_accounts_account_external_accounts"
        """Accounts account external accounts."""
        
        POST_ACCOUNTS_ACCOUNT_EXTERNAL_ACCOUNTS_ID = "stripe_post_accounts_account_external_accounts_id"
        """Accounts account external accounts id."""
        
        POST_ACCOUNTS_ACCOUNT_LOGIN_LINKS = "stripe_post_accounts_account_login_links"
        """Accounts account login links."""
        
        POST_ACCOUNTS_ACCOUNT_PEOPLE = "stripe_post_accounts_account_people"
        """Accounts account people."""
        
        POST_ACCOUNTS_ACCOUNT_PEOPLE_PERSON = "stripe_post_accounts_account_people_person"
        """Accounts account people person."""
        
        POST_ACCOUNTS_ACCOUNT_PERSONS = "stripe_post_accounts_account_persons"
        """Accounts account persons."""
        
        POST_ACCOUNTS_ACCOUNT_PERSONS_PERSON = "stripe_post_accounts_account_persons_person"
        """Accounts account persons person."""
        
        POST_ACCOUNTS_ACCOUNT_REJECT = "stripe_post_accounts_account_reject"
        """Accounts account reject."""
        
        POST_ACCOUNT_LINKS = "stripe_post_account_links"
        """Account links."""
        
        POST_ACCOUNT_SESSIONS = "stripe_post_account_sessions"
        """Account sessions."""
        
        POST_APPLE_PAY_DOMAINS = "stripe_post_apple_pay_domains"
        """Apple pay domains."""
        
        POST_APPLICATION_FEES_FEE_REFUNDS_ID = "stripe_post_application_fees_fee_refunds_id"
        """Application fees fee refunds id."""
        
        POST_APPLICATION_FEES_ID_REFUND = "stripe_post_application_fees_id_refund"
        """Application fees id refund."""
        
        POST_APPLICATION_FEES_ID_REFUNDS = "stripe_post_application_fees_id_refunds"
        """Application fees id refunds."""
        
        POST_APPS_SECRETS = "stripe_post_apps_secrets"
        """Apps secrets."""
        
        POST_APPS_SECRETS_DELETE = "stripe_post_apps_secrets_delete"
        """Apps secrets delete."""
        
        POST_BILLING_ALERTS = "stripe_post_billing_alerts"
        """Billing alerts."""
        
        POST_BILLING_ALERTS_ID_ACTIVATE = "stripe_post_billing_alerts_id_activate"
        """Billing alerts id activate."""
        
        POST_BILLING_ALERTS_ID_ARCHIVE = "stripe_post_billing_alerts_id_archive"
        """Billing alerts id archive."""
        
        POST_BILLING_ALERTS_ID_DEACTIVATE = "stripe_post_billing_alerts_id_deactivate"
        """Billing alerts id deactivate."""
        
        POST_BILLING_CREDIT_GRANTS = "stripe_post_billing_credit_grants"
        """Billing credit grants."""
        
        POST_BILLING_CREDIT_GRANTS_ID = "stripe_post_billing_credit_grants_id"
        """Billing credit grants id."""
        
        POST_BILLING_CREDIT_GRANTS_ID_EXPIRE = "stripe_post_billing_credit_grants_id_expire"
        """Billing credit grants id expire."""
        
        POST_BILLING_CREDIT_GRANTS_ID_VOID = "stripe_post_billing_credit_grants_id_void"
        """Billing credit grants id void."""
        
        POST_BILLING_METERS = "stripe_post_billing_meters"
        """Billing meters."""
        
        POST_BILLING_METERS_ID = "stripe_post_billing_meters_id"
        """Billing meters id."""
        
        POST_BILLING_METERS_ID_DEACTIVATE = "stripe_post_billing_meters_id_deactivate"
        """Billing meters id deactivate."""
        
        POST_BILLING_METERS_ID_REACTIVATE = "stripe_post_billing_meters_id_reactivate"
        """Billing meters id reactivate."""
        
        POST_BILLING_METER_EVENTS = "stripe_post_billing_meter_events"
        """Billing meter events."""
        
        POST_BILLING_METER_EVENT_ADJUSTMENTS = "stripe_post_billing_meter_event_adjustments"
        """Billing meter event adjustments."""
        
        POST_BILLING_PORTAL_CONFIGURATIONS = "stripe_post_billing_portal_configurations"
        """Billing portal configurations."""
        
        POST_BILLING_PORTAL_CONFIGURATIONS_CONFIGURATION = "stripe_post_billing_portal_configurations_configuration"
        """Billing portal configurations configuration."""
        
        POST_BILLING_PORTAL_SESSIONS = "stripe_post_billing_portal_sessions"
        """Billing portal sessions."""
        
        POST_CHARGES = "stripe_post_charges"
        """Charges."""
        
        POST_CHARGES_CHARGE = "stripe_post_charges_charge"
        """Charges charge."""
        
        POST_CHARGES_CHARGE_CAPTURE = "stripe_post_charges_charge_capture"
        """Charges charge capture."""
        
        POST_CHARGES_CHARGE_DISPUTE = "stripe_post_charges_charge_dispute"
        """Charges charge dispute."""
        
        POST_CHARGES_CHARGE_DISPUTE_CLOSE = "stripe_post_charges_charge_dispute_close"
        """Charges charge dispute close."""
        
        POST_CHARGES_CHARGE_REFUND = "stripe_post_charges_charge_refund"
        """Charges charge refund."""
        
        POST_CHARGES_CHARGE_REFUNDS = "stripe_post_charges_charge_refunds"
        """Charges charge refunds."""
        
        POST_CHARGES_CHARGE_REFUNDS_REFUND = "stripe_post_charges_charge_refunds_refund"
        """Charges charge refunds refund."""
        
        POST_CHECKOUT_SESSIONS = "stripe_post_checkout_sessions"
        """Checkout sessions."""
        
        POST_CHECKOUT_SESSIONS_SESSION = "stripe_post_checkout_sessions_session"
        """Checkout sessions session."""
        
        POST_CHECKOUT_SESSIONS_SESSION_EXPIRE = "stripe_post_checkout_sessions_session_expire"
        """Checkout sessions session expire."""
        
        POST_CLIMATE_ORDERS = "stripe_post_climate_orders"
        """Climate orders."""
        
        POST_CLIMATE_ORDERS_ORDER = "stripe_post_climate_orders_order"
        """Climate orders order."""
        
        POST_CLIMATE_ORDERS_ORDER_CANCEL = "stripe_post_climate_orders_order_cancel"
        """Climate orders order cancel."""
        
        POST_COUPONS = "stripe_post_coupons"
        """Coupons."""
        
        POST_COUPONS_COUPON = "stripe_post_coupons_coupon"
        """Coupons coupon."""
        
        POST_CREDIT_NOTES = "stripe_post_credit_notes"
        """Credit notes."""
        
        POST_CREDIT_NOTES_ID = "stripe_post_credit_notes_id"
        """Credit notes id."""
        
        POST_CREDIT_NOTES_ID_VOID = "stripe_post_credit_notes_id_void"
        """Credit notes id void."""
        
        POST_CUSTOMERS = "stripe_post_customers"
        """Customers."""
        
        POST_CUSTOMERS_CUSTOMER = "stripe_post_customers_customer"
        """Customers customer."""
        
        POST_CUSTOMERS_CUSTOMER_BALANCE_TRANSACTIONS = "stripe_post_customers_customer_balance_transactions"
        """Customers customer balance transactions."""
        
        POST_CUSTOMERS_CUSTOMER_BALANCE_TRANSACTIONS_TRANSACTION = "stripe_post_customers_customer_balance_transactions_transaction"
        """Customers customer balance transactions transaction."""
        
        POST_CUSTOMERS_CUSTOMER_BANK_ACCOUNTS = "stripe_post_customers_customer_bank_accounts"
        """Customers customer bank accounts."""
        
        POST_CUSTOMERS_CUSTOMER_BANK_ACCOUNTS_ID = "stripe_post_customers_customer_bank_accounts_id"
        """Customers customer bank accounts id."""
        
        POST_CUSTOMERS_CUSTOMER_BANK_ACCOUNTS_ID_VERIFY = "stripe_post_customers_customer_bank_accounts_id_verify"
        """Customers customer bank accounts id verify."""
        
        POST_CUSTOMERS_CUSTOMER_CARDS = "stripe_post_customers_customer_cards"
        """Customers customer cards."""
        
        POST_CUSTOMERS_CUSTOMER_CARDS_ID = "stripe_post_customers_customer_cards_id"
        """Customers customer cards id."""
        
        POST_CUSTOMERS_CUSTOMER_CASH_BALANCE = "stripe_post_customers_customer_cash_balance"
        """Customers customer cash balance."""
        
        POST_CUSTOMERS_CUSTOMER_FUNDING_INSTRUCTIONS = "stripe_post_customers_customer_funding_instructions"
        """Customers customer funding instructions."""
        
        POST_CUSTOMERS_CUSTOMER_SOURCES = "stripe_post_customers_customer_sources"
        """Customers customer sources."""
        
        POST_CUSTOMERS_CUSTOMER_SOURCES_ID = "stripe_post_customers_customer_sources_id"
        """Customers customer sources id."""
        
        POST_CUSTOMERS_CUSTOMER_SOURCES_ID_VERIFY = "stripe_post_customers_customer_sources_id_verify"
        """Customers customer sources id verify."""
        
        POST_CUSTOMERS_CUSTOMER_SUBSCRIPTIONS = "stripe_post_customers_customer_subscriptions"
        """Customers customer subscriptions."""
        
        POST_CUSTOMERS_CUSTOMER_SUBSCRIPTIONS_SUBSCRIPTION_EXPOSED_ID = "stripe_post_customers_customer_subscriptions_subscription_exposed_id"
        """Customers customer subscriptions subscription exposed id."""
        
        POST_CUSTOMERS_CUSTOMER_TAX_IDS = "stripe_post_customers_customer_tax_ids"
        """Customers customer tax ids."""
        
        POST_CUSTOMER_SESSIONS = "stripe_post_customer_sessions"
        """Customer sessions."""
        
        POST_DISPUTES_DISPUTE = "stripe_post_disputes_dispute"
        """Disputes dispute."""
        
        POST_DISPUTES_DISPUTE_CLOSE = "stripe_post_disputes_dispute_close"
        """Disputes dispute close."""
        
        POST_ENTITLEMENTS_FEATURES = "stripe_post_entitlements_features"
        """Entitlements features."""
        
        POST_ENTITLEMENTS_FEATURES_ID = "stripe_post_entitlements_features_id"
        """Entitlements features id."""
        
        POST_EPHEMERAL_KEYS = "stripe_post_ephemeral_keys"
        """Ephemeral keys."""
        
        POST_FILES = "stripe_post_files"
        """Files."""
        
        POST_FILE_LINKS = "stripe_post_file_links"
        """File links."""
        
        POST_FILE_LINKS_LINK = "stripe_post_file_links_link"
        """File links link."""
        
        POST_FINANCIAL_CONNECTIONS_ACCOUNTS_ACCOUNT_DISCONNECT = "stripe_post_financial_connections_accounts_account_disconnect"
        """Financial connections accounts account disconnect."""
        
        POST_FINANCIAL_CONNECTIONS_ACCOUNTS_ACCOUNT_REFRESH = "stripe_post_financial_connections_accounts_account_refresh"
        """Financial connections accounts account refresh."""
        
        POST_FINANCIAL_CONNECTIONS_ACCOUNTS_ACCOUNT_SUBSCRIBE = "stripe_post_financial_connections_accounts_account_subscribe"
        """Financial connections accounts account subscribe."""
        
        POST_FINANCIAL_CONNECTIONS_ACCOUNTS_ACCOUNT_UNSUBSCRIBE = "stripe_post_financial_connections_accounts_account_unsubscribe"
        """Financial connections accounts account unsubscribe."""
        
        POST_FINANCIAL_CONNECTIONS_SESSIONS = "stripe_post_financial_connections_sessions"
        """Financial connections sessions."""
        
        POST_FORWARDING_REQUESTS = "stripe_post_forwarding_requests"
        """Forwarding requests."""
        
        POST_IDENTITY_VERIFICATION_SESSIONS = "stripe_post_identity_verification_sessions"
        """Identity verification sessions."""
        
        POST_IDENTITY_VERIFICATION_SESSIONS_SESSION = "stripe_post_identity_verification_sessions_session"
        """Identity verification sessions session."""
        
        POST_IDENTITY_VERIFICATION_SESSIONS_SESSION_CANCEL = "stripe_post_identity_verification_sessions_session_cancel"
        """Identity verification sessions session cancel."""
        
        POST_IDENTITY_VERIFICATION_SESSIONS_SESSION_REDACT = "stripe_post_identity_verification_sessions_session_redact"
        """Identity verification sessions session redact."""
        
        POST_INVOICEITEMS = "stripe_post_invoiceitems"
        """Invoiceitems."""
        
        POST_INVOICEITEMS_INVOICEITEM = "stripe_post_invoiceitems_invoiceitem"
        """Invoiceitems invoiceitem."""
        
        POST_INVOICES = "stripe_post_invoices"
        """Invoices."""
        
        POST_INVOICES_CREATE_PREVIEW = "stripe_post_invoices_create_preview"
        """Invoices create preview."""
        
        POST_INVOICES_INVOICE = "stripe_post_invoices_invoice"
        """Invoices invoice."""
        
        POST_INVOICES_INVOICE_ADD_LINES = "stripe_post_invoices_invoice_add_lines"
        """Invoices invoice add lines."""
        
        POST_INVOICES_INVOICE_FINALIZE = "stripe_post_invoices_invoice_finalize"
        """Invoices invoice finalize."""
        
        POST_INVOICES_INVOICE_LINES_LINE_ITEM_ID = "stripe_post_invoices_invoice_lines_line_item_id"
        """Invoices invoice lines line item id."""
        
        POST_INVOICES_INVOICE_MARK_UNCOLLECTIBLE = "stripe_post_invoices_invoice_mark_uncollectible"
        """Invoices invoice mark uncollectible."""
        
        POST_INVOICES_INVOICE_PAY = "stripe_post_invoices_invoice_pay"
        """Invoices invoice pay."""
        
        POST_INVOICES_INVOICE_REMOVE_LINES = "stripe_post_invoices_invoice_remove_lines"
        """Invoices invoice remove lines."""
        
        POST_INVOICES_INVOICE_SEND = "stripe_post_invoices_invoice_send"
        """Invoices invoice send."""
        
        POST_INVOICES_INVOICE_UPDATE_LINES = "stripe_post_invoices_invoice_update_lines"
        """Invoices invoice update lines."""
        
        POST_INVOICES_INVOICE_VOID = "stripe_post_invoices_invoice_void"
        """Invoices invoice void."""
        
        POST_INVOICE_RENDERING_TEMPLATES_TEMPLATE_ARCHIVE = "stripe_post_invoice_rendering_templates_template_archive"
        """Invoice rendering templates template archive."""
        
        POST_INVOICE_RENDERING_TEMPLATES_TEMPLATE_UNARCHIVE = "stripe_post_invoice_rendering_templates_template_unarchive"
        """Invoice rendering templates template unarchive."""
        
        POST_ISSUING_AUTHORIZATIONS_AUTHORIZATION = "stripe_post_issuing_authorizations_authorization"
        """Issuing authorizations authorization."""
        
        POST_ISSUING_AUTHORIZATIONS_AUTHORIZATION_APPROVE = "stripe_post_issuing_authorizations_authorization_approve"
        """Issuing authorizations authorization approve."""
        
        POST_ISSUING_AUTHORIZATIONS_AUTHORIZATION_DECLINE = "stripe_post_issuing_authorizations_authorization_decline"
        """Issuing authorizations authorization decline."""
        
        POST_ISSUING_CARDHOLDERS = "stripe_post_issuing_cardholders"
        """Issuing cardholders."""
        
        POST_ISSUING_CARDHOLDERS_CARDHOLDER = "stripe_post_issuing_cardholders_cardholder"
        """Issuing cardholders cardholder."""
        
        POST_ISSUING_CARDS = "stripe_post_issuing_cards"
        """Issuing cards."""
        
        POST_ISSUING_CARDS_CARD = "stripe_post_issuing_cards_card"
        """Issuing cards card."""
        
        POST_ISSUING_DISPUTES = "stripe_post_issuing_disputes"
        """Issuing disputes."""
        
        POST_ISSUING_DISPUTES_DISPUTE = "stripe_post_issuing_disputes_dispute"
        """Issuing disputes dispute."""
        
        POST_ISSUING_DISPUTES_DISPUTE_SUBMIT = "stripe_post_issuing_disputes_dispute_submit"
        """Issuing disputes dispute submit."""
        
        POST_ISSUING_PERSONALIZATION_DESIGNS = "stripe_post_issuing_personalization_designs"
        """Issuing personalization designs."""
        
        POST_ISSUING_PERSONALIZATION_DESIGNS_PERSONALIZATION_DESIGN = "stripe_post_issuing_personalization_designs_personalization_design"
        """Issuing personalization designs personalization design."""
        
        POST_ISSUING_SETTLEMENTS_SETTLEMENT = "stripe_post_issuing_settlements_settlement"
        """Issuing settlements settlement."""
        
        POST_ISSUING_TOKENS_TOKEN = "stripe_post_issuing_tokens_token"
        """Issuing tokens token."""
        
        POST_ISSUING_TRANSACTIONS_TRANSACTION = "stripe_post_issuing_transactions_transaction"
        """Issuing transactions transaction."""
        
        POST_LINKED_ACCOUNTS_ACCOUNT_DISCONNECT = "stripe_post_linked_accounts_account_disconnect"
        """Linked accounts account disconnect."""
        
        POST_LINKED_ACCOUNTS_ACCOUNT_REFRESH = "stripe_post_linked_accounts_account_refresh"
        """Linked accounts account refresh."""
        
        POST_LINK_ACCOUNT_SESSIONS = "stripe_post_link_account_sessions"
        """Link account sessions."""
        
        POST_PAYMENT_INTENTS = "stripe_post_payment_intents"
        """Payment intents."""
        
        POST_PAYMENT_INTENTS_INTENT = "stripe_post_payment_intents_intent"
        """Payment intents intent."""
        
        POST_PAYMENT_INTENTS_INTENT_APPLY_CUSTOMER_BALANCE = "stripe_post_payment_intents_intent_apply_customer_balance"
        """Payment intents intent apply customer balance."""
        
        POST_PAYMENT_INTENTS_INTENT_CANCEL = "stripe_post_payment_intents_intent_cancel"
        """Payment intents intent cancel."""
        
        POST_PAYMENT_INTENTS_INTENT_CAPTURE = "stripe_post_payment_intents_intent_capture"
        """Payment intents intent capture."""
        
        POST_PAYMENT_INTENTS_INTENT_CONFIRM = "stripe_post_payment_intents_intent_confirm"
        """Payment intents intent confirm."""
        
        POST_PAYMENT_INTENTS_INTENT_INCREMENT_AUTHORIZATION = "stripe_post_payment_intents_intent_increment_authorization"
        """Payment intents intent increment authorization."""
        
        POST_PAYMENT_INTENTS_INTENT_VERIFY_MICRODEPOSITS = "stripe_post_payment_intents_intent_verify_microdeposits"
        """Payment intents intent verify microdeposits."""
        
        POST_PAYMENT_LINKS = "stripe_post_payment_links"
        """Payment links."""
        
        POST_PAYMENT_LINKS_PAYMENT_LINK = "stripe_post_payment_links_payment_link"
        """Payment links payment link."""
        
        POST_PAYMENT_METHODS = "stripe_post_payment_methods"
        """Payment methods."""
        
        POST_PAYMENT_METHODS_PAYMENT_METHOD = "stripe_post_payment_methods_payment_method"
        """Payment methods payment method."""
        
        POST_PAYMENT_METHODS_PAYMENT_METHOD_ATTACH = "stripe_post_payment_methods_payment_method_attach"
        """Payment methods payment method attach."""
        
        POST_PAYMENT_METHODS_PAYMENT_METHOD_DETACH = "stripe_post_payment_methods_payment_method_detach"
        """Payment methods payment method detach."""
        
        POST_PAYMENT_METHOD_CONFIGURATIONS = "stripe_post_payment_method_configurations"
        """Payment method configurations."""
        
        POST_PAYMENT_METHOD_CONFIGURATIONS_CONFIGURATION = "stripe_post_payment_method_configurations_configuration"
        """Payment method configurations configuration."""
        
        POST_PAYMENT_METHOD_DOMAINS = "stripe_post_payment_method_domains"
        """Payment method domains."""
        
        POST_PAYMENT_METHOD_DOMAINS_PAYMENT_METHOD_DOMAIN = "stripe_post_payment_method_domains_payment_method_domain"
        """Payment method domains payment method domain."""
        
        POST_PAYMENT_METHOD_DOMAINS_PAYMENT_METHOD_DOMAIN_VALIDATE = "stripe_post_payment_method_domains_payment_method_domain_validate"
        """Payment method domains payment method domain validate."""
        
        POST_PAYOUTS = "stripe_post_payouts"
        """Payouts."""
        
        POST_PAYOUTS_PAYOUT = "stripe_post_payouts_payout"
        """Payouts payout."""
        
        POST_PAYOUTS_PAYOUT_CANCEL = "stripe_post_payouts_payout_cancel"
        """Payouts payout cancel."""
        
        POST_PAYOUTS_PAYOUT_REVERSE = "stripe_post_payouts_payout_reverse"
        """Payouts payout reverse."""
        
        POST_PLANS = "stripe_post_plans"
        """Plans."""
        
        POST_PLANS_PLAN = "stripe_post_plans_plan"
        """Plans plan."""
        
        POST_PRICES = "stripe_post_prices"
        """Prices."""
        
        POST_PRICES_PRICE = "stripe_post_prices_price"
        """Prices price."""
        
        POST_PRODUCTS = "stripe_post_products"
        """Products."""
        
        POST_PRODUCTS_ID = "stripe_post_products_id"
        """Products id."""
        
        POST_PRODUCTS_PRODUCT_FEATURES = "stripe_post_products_product_features"
        """Products product features."""
        
        POST_PROMOTION_CODES = "stripe_post_promotion_codes"
        """Promotion codes."""
        
        POST_PROMOTION_CODES_PROMOTION_CODE = "stripe_post_promotion_codes_promotion_code"
        """Promotion codes promotion code."""
        
        POST_QUOTES = "stripe_post_quotes"
        """Quotes."""
        
        POST_QUOTES_QUOTE = "stripe_post_quotes_quote"
        """Quotes quote."""
        
        POST_QUOTES_QUOTE_ACCEPT = "stripe_post_quotes_quote_accept"
        """Quotes quote accept."""
        
        POST_QUOTES_QUOTE_CANCEL = "stripe_post_quotes_quote_cancel"
        """Quotes quote cancel."""
        
        POST_QUOTES_QUOTE_FINALIZE = "stripe_post_quotes_quote_finalize"
        """Quotes quote finalize."""
        
        POST_RADAR_VALUE_LISTS = "stripe_post_radar_value_lists"
        """Radar value lists."""
        
        POST_RADAR_VALUE_LISTS_VALUE_LIST = "stripe_post_radar_value_lists_value_list"
        """Radar value lists value list."""
        
        POST_RADAR_VALUE_LIST_ITEMS = "stripe_post_radar_value_list_items"
        """Radar value list items."""
        
        POST_REFUNDS = "stripe_post_refunds"
        """Refunds."""
        
        POST_REFUNDS_REFUND = "stripe_post_refunds_refund"
        """Refunds refund."""
        
        POST_REFUNDS_REFUND_CANCEL = "stripe_post_refunds_refund_cancel"
        """Refunds refund cancel."""
        
        POST_REPORTING_REPORT_RUNS = "stripe_post_reporting_report_runs"
        """Reporting report runs."""
        
        POST_REVIEWS_REVIEW_APPROVE = "stripe_post_reviews_review_approve"
        """Reviews review approve."""
        
        POST_SETUP_INTENTS = "stripe_post_setup_intents"
        """Setup intents."""
        
        POST_SETUP_INTENTS_INTENT = "stripe_post_setup_intents_intent"
        """Setup intents intent."""
        
        POST_SETUP_INTENTS_INTENT_CANCEL = "stripe_post_setup_intents_intent_cancel"
        """Setup intents intent cancel."""
        
        POST_SETUP_INTENTS_INTENT_CONFIRM = "stripe_post_setup_intents_intent_confirm"
        """Setup intents intent confirm."""
        
        POST_SETUP_INTENTS_INTENT_VERIFY_MICRODEPOSITS = "stripe_post_setup_intents_intent_verify_microdeposits"
        """Setup intents intent verify microdeposits."""
        
        POST_SHIPPING_RATES = "stripe_post_shipping_rates"
        """Shipping rates."""
        
        POST_SHIPPING_RATES_SHIPPING_RATE_TOKEN = "stripe_post_shipping_rates_shipping_rate_token"
        """Shipping rates shipping rate token."""
        
        POST_SOURCES = "stripe_post_sources"
        """Sources."""
        
        POST_SOURCES_SOURCE = "stripe_post_sources_source"
        """Sources source."""
        
        POST_SOURCES_SOURCE_VERIFY = "stripe_post_sources_source_verify"
        """Sources source verify."""
        
        POST_SUBSCRIPTIONS = "stripe_post_subscriptions"
        """Subscriptions."""
        
        POST_SUBSCRIPTIONS_SUBSCRIPTION_EXPOSED_ID = "stripe_post_subscriptions_subscription_exposed_id"
        """Subscriptions subscription exposed id."""
        
        POST_SUBSCRIPTIONS_SUBSCRIPTION_RESUME = "stripe_post_subscriptions_subscription_resume"
        """Subscriptions subscription resume."""
        
        POST_SUBSCRIPTION_ITEMS = "stripe_post_subscription_items"
        """Subscription items."""
        
        POST_SUBSCRIPTION_ITEMS_ITEM = "stripe_post_subscription_items_item"
        """Subscription items item."""
        
        POST_SUBSCRIPTION_ITEMS_SUBSCRIPTION_ITEM_USAGE_RECORDS = "stripe_post_subscription_items_subscription_item_usage_records"
        """Subscription items subscription item usage records."""
        
        POST_SUBSCRIPTION_SCHEDULES = "stripe_post_subscription_schedules"
        """Subscription schedules."""
        
        POST_SUBSCRIPTION_SCHEDULES_SCHEDULE = "stripe_post_subscription_schedules_schedule"
        """Subscription schedules schedule."""
        
        POST_SUBSCRIPTION_SCHEDULES_SCHEDULE_CANCEL = "stripe_post_subscription_schedules_schedule_cancel"
        """Subscription schedules schedule cancel."""
        
        POST_SUBSCRIPTION_SCHEDULES_SCHEDULE_RELEASE = "stripe_post_subscription_schedules_schedule_release"
        """Subscription schedules schedule release."""
        
        POST_TAX_CALCULATIONS = "stripe_post_tax_calculations"
        """Tax calculations."""
        
        POST_TAX_IDS = "stripe_post_tax_ids"
        """Tax ids."""
        
        POST_TAX_RATES = "stripe_post_tax_rates"
        """Tax rates."""
        
        POST_TAX_RATES_TAX_RATE = "stripe_post_tax_rates_tax_rate"
        """Tax rates tax rate."""
        
        POST_TAX_REGISTRATIONS = "stripe_post_tax_registrations"
        """Tax registrations."""
        
        POST_TAX_REGISTRATIONS_ID = "stripe_post_tax_registrations_id"
        """Tax registrations id."""
        
        POST_TAX_SETTINGS = "stripe_post_tax_settings"
        """Tax settings."""
        
        POST_TAX_TRANSACTIONS_CREATE_FROM_CALCULATION = "stripe_post_tax_transactions_create_from_calculation"
        """Tax transactions create from calculation."""
        
        POST_TAX_TRANSACTIONS_CREATE_REVERSAL = "stripe_post_tax_transactions_create_reversal"
        """Tax transactions create reversal."""
        
        POST_TERMINAL_CONFIGURATIONS = "stripe_post_terminal_configurations"
        """Terminal configurations."""
        
        POST_TERMINAL_CONFIGURATIONS_CONFIGURATION = "stripe_post_terminal_configurations_configuration"
        """Terminal configurations configuration."""
        
        POST_TERMINAL_CONNECTION_TOKENS = "stripe_post_terminal_connection_tokens"
        """Terminal connection tokens."""
        
        POST_TERMINAL_LOCATIONS = "stripe_post_terminal_locations"
        """Terminal locations."""
        
        POST_TERMINAL_LOCATIONS_LOCATION = "stripe_post_terminal_locations_location"
        """Terminal locations location."""
        
        POST_TERMINAL_READERS = "stripe_post_terminal_readers"
        """Terminal readers."""
        
        POST_TERMINAL_READERS_READER = "stripe_post_terminal_readers_reader"
        """Terminal readers reader."""
        
        POST_TERMINAL_READERS_READER_CANCEL_ACTION = "stripe_post_terminal_readers_reader_cancel_action"
        """Terminal readers reader cancel action."""
        
        POST_TERMINAL_READERS_READER_PROCESS_PAYMENT_INTENT = "stripe_post_terminal_readers_reader_process_payment_intent"
        """Terminal readers reader process payment intent."""
        
        POST_TERMINAL_READERS_READER_PROCESS_SETUP_INTENT = "stripe_post_terminal_readers_reader_process_setup_intent"
        """Terminal readers reader process setup intent."""
        
        POST_TERMINAL_READERS_READER_REFUND_PAYMENT = "stripe_post_terminal_readers_reader_refund_payment"
        """Terminal readers reader refund payment."""
        
        POST_TERMINAL_READERS_READER_SET_READER_DISPLAY = "stripe_post_terminal_readers_reader_set_reader_display"
        """Terminal readers reader set reader display."""
        
        POST_TEST_HELPERS_CONFIRMATION_TOKENS = "stripe_post_test_helpers_confirmation_tokens"
        """Test helpers confirmation tokens."""
        
        POST_TEST_HELPERS_CUSTOMERS_CUSTOMER_FUND_CASH_BALANCE = "stripe_post_test_helpers_customers_customer_fund_cash_balance"
        """Test helpers customers customer fund cash balance."""
        
        POST_TEST_HELPERS_ISSUING_AUTHORIZATIONS = "stripe_post_test_helpers_issuing_authorizations"
        """Test helpers issuing authorizations."""
        
        POST_TEST_HELPERS_ISSUING_AUTHORIZATIONS_AUTHORIZATION_CAPTURE = "stripe_post_test_helpers_issuing_authorizations_authorization_capture"
        """Test helpers issuing authorizations authorization capture."""
        
        POST_TEST_HELPERS_ISSUING_AUTHORIZATIONS_AUTHORIZATION_EXPIRE = "stripe_post_test_helpers_issuing_authorizations_authorization_expire"
        """Test helpers issuing authorizations authorization expire."""
        
        POST_TEST_HELPERS_ISSUING_AUTHORIZATIONS_AUTHORIZATION_FINALIZE_AMOUNT = "stripe_post_test_helpers_issuing_authorizations_authorization_finalize_amount"
        """Test helpers issuing authorizations authorization finalize amount."""
        
        POST_TEST_HELPERS_ISSUING_AUTHORIZATIONS_AUTHORIZATION_INCREMENT = "stripe_post_test_helpers_issuing_authorizations_authorization_increment"
        """Test helpers issuing authorizations authorization increment."""
        
        POST_TEST_HELPERS_ISSUING_AUTHORIZATIONS_AUTHORIZATION_REVERSE = "stripe_post_test_helpers_issuing_authorizations_authorization_reverse"
        """Test helpers issuing authorizations authorization reverse."""
        
        POST_TEST_HELPERS_ISSUING_CARDS_CARD_SHIPPING_DELIVER = "stripe_post_test_helpers_issuing_cards_card_shipping_deliver"
        """Test helpers issuing cards card shipping deliver."""
        
        POST_TEST_HELPERS_ISSUING_CARDS_CARD_SHIPPING_FAIL = "stripe_post_test_helpers_issuing_cards_card_shipping_fail"
        """Test helpers issuing cards card shipping fail."""
        
        POST_TEST_HELPERS_ISSUING_CARDS_CARD_SHIPPING_RETURN = "stripe_post_test_helpers_issuing_cards_card_shipping_return"
        """Test helpers issuing cards card shipping return."""
        
        POST_TEST_HELPERS_ISSUING_CARDS_CARD_SHIPPING_SHIP = "stripe_post_test_helpers_issuing_cards_card_shipping_ship"
        """Test helpers issuing cards card shipping ship."""
        
        POST_TEST_HELPERS_ISSUING_CARDS_CARD_SHIPPING_SUBMIT = "stripe_post_test_helpers_issuing_cards_card_shipping_submit"
        """Test helpers issuing cards card shipping submit."""
        
        POST_TEST_HELPERS_ISSUING_PERSONALIZATION_DESIGNS_PERSONALIZATION_DESIGN_ACTIVATE = "stripe_post_test_helpers_issuing_personalization_designs_personalization_design_activate"
        """Test helpers issuing personalization designs personalization design activate."""
        
        POST_TEST_HELPERS_ISSUING_PERSONALIZATION_DESIGNS_PERSONALIZATION_DESIGN_DEACTIVATE = "stripe_post_test_helpers_issuing_personalization_designs_personalization_design_deactivate"
        """Test helpers issuing personalization designs personalization design deactivate."""
        
        POST_TEST_HELPERS_ISSUING_PERSONALIZATION_DESIGNS_PERSONALIZATION_DESIGN_REJECT = "stripe_post_test_helpers_issuing_personalization_designs_personalization_design_reject"
        """Test helpers issuing personalization designs personalization design reject."""
        
        POST_TEST_HELPERS_ISSUING_SETTLEMENTS = "stripe_post_test_helpers_issuing_settlements"
        """Test helpers issuing settlements."""
        
        POST_TEST_HELPERS_ISSUING_TRANSACTIONS_CREATE_FORCE_CAPTURE = "stripe_post_test_helpers_issuing_transactions_create_force_capture"
        """Test helpers issuing transactions create force capture."""
        
        POST_TEST_HELPERS_ISSUING_TRANSACTIONS_CREATE_UNLINKED_REFUND = "stripe_post_test_helpers_issuing_transactions_create_unlinked_refund"
        """Test helpers issuing transactions create unlinked refund."""
        
        POST_TEST_HELPERS_ISSUING_TRANSACTIONS_TRANSACTION_REFUND = "stripe_post_test_helpers_issuing_transactions_transaction_refund"
        """Test helpers issuing transactions transaction refund."""
        
        POST_TEST_HELPERS_REFUNDS_REFUND_EXPIRE = "stripe_post_test_helpers_refunds_refund_expire"
        """Test helpers refunds refund expire."""
        
        POST_TEST_HELPERS_TERMINAL_READERS_READER_PRESENT_PAYMENT_METHOD = "stripe_post_test_helpers_terminal_readers_reader_present_payment_method"
        """Test helpers terminal readers reader present payment method."""
        
        POST_TEST_HELPERS_TEST_CLOCKS = "stripe_post_test_helpers_test_clocks"
        """Test helpers test clocks."""
        
        POST_TEST_HELPERS_TEST_CLOCKS_TEST_CLOCK_ADVANCE = "stripe_post_test_helpers_test_clocks_test_clock_advance"
        """Test helpers test clocks test clock advance."""
        
        POST_TEST_HELPERS_TREASURY_INBOUND_TRANSFERS_ID_FAIL = "stripe_post_test_helpers_treasury_inbound_transfers_id_fail"
        """Test helpers treasury inbound transfers id fail."""
        
        POST_TEST_HELPERS_TREASURY_INBOUND_TRANSFERS_ID_RETURN = "stripe_post_test_helpers_treasury_inbound_transfers_id_return"
        """Test helpers treasury inbound transfers id return."""
        
        POST_TEST_HELPERS_TREASURY_INBOUND_TRANSFERS_ID_SUCCEED = "stripe_post_test_helpers_treasury_inbound_transfers_id_succeed"
        """Test helpers treasury inbound transfers id succeed."""
        
        POST_TEST_HELPERS_TREASURY_OUTBOUND_PAYMENTS_ID = "stripe_post_test_helpers_treasury_outbound_payments_id"
        """Test helpers treasury outbound payments id."""
        
        POST_TEST_HELPERS_TREASURY_OUTBOUND_PAYMENTS_ID_FAIL = "stripe_post_test_helpers_treasury_outbound_payments_id_fail"
        """Test helpers treasury outbound payments id fail."""
        
        POST_TEST_HELPERS_TREASURY_OUTBOUND_PAYMENTS_ID_POST = "stripe_post_test_helpers_treasury_outbound_payments_id_post"
        """Test helpers treasury outbound payments id post."""
        
        POST_TEST_HELPERS_TREASURY_OUTBOUND_PAYMENTS_ID_RETURN = "stripe_post_test_helpers_treasury_outbound_payments_id_return"
        """Test helpers treasury outbound payments id return."""
        
        POST_TEST_HELPERS_TREASURY_OUTBOUND_TRANSFERS_OUTBOUND_TRANSFER = "stripe_post_test_helpers_treasury_outbound_transfers_outbound_transfer"
        """Test helpers treasury outbound transfers outbound transfer."""
        
        POST_TEST_HELPERS_TREASURY_OUTBOUND_TRANSFERS_OUTBOUND_TRANSFER_FAIL = "stripe_post_test_helpers_treasury_outbound_transfers_outbound_transfer_fail"
        """Test helpers treasury outbound transfers outbound transfer fail."""
        
        POST_TEST_HELPERS_TREASURY_OUTBOUND_TRANSFERS_OUTBOUND_TRANSFER_POST = "stripe_post_test_helpers_treasury_outbound_transfers_outbound_transfer_post"
        """Test helpers treasury outbound transfers outbound transfer post."""
        
        POST_TEST_HELPERS_TREASURY_OUTBOUND_TRANSFERS_OUTBOUND_TRANSFER_RETURN = "stripe_post_test_helpers_treasury_outbound_transfers_outbound_transfer_return"
        """Test helpers treasury outbound transfers outbound transfer return."""
        
        POST_TEST_HELPERS_TREASURY_RECEIVED_CREDITS = "stripe_post_test_helpers_treasury_received_credits"
        """Test helpers treasury received credits."""
        
        POST_TEST_HELPERS_TREASURY_RECEIVED_DEBITS = "stripe_post_test_helpers_treasury_received_debits"
        """Test helpers treasury received debits."""
        
        POST_TOKENS = "stripe_post_tokens"
        """Tokens."""
        
        POST_TOPUPS = "stripe_post_topups"
        """Topups."""
        
        POST_TOPUPS_TOPUP = "stripe_post_topups_topup"
        """Topups topup."""
        
        POST_TOPUPS_TOPUP_CANCEL = "stripe_post_topups_topup_cancel"
        """Topups topup cancel."""
        
        POST_TRANSFERS = "stripe_post_transfers"
        """Transfers."""
        
        POST_TRANSFERS_ID_REVERSALS = "stripe_post_transfers_id_reversals"
        """Transfers id reversals."""
        
        POST_TRANSFERS_TRANSFER = "stripe_post_transfers_transfer"
        """Transfers transfer."""
        
        POST_TRANSFERS_TRANSFER_REVERSALS_ID = "stripe_post_transfers_transfer_reversals_id"
        """Transfers transfer reversals id."""
        
        POST_TREASURY_CREDIT_REVERSALS = "stripe_post_treasury_credit_reversals"
        """Treasury credit reversals."""
        
        POST_TREASURY_DEBIT_REVERSALS = "stripe_post_treasury_debit_reversals"
        """Treasury debit reversals."""
        
        POST_TREASURY_FINANCIAL_ACCOUNTS = "stripe_post_treasury_financial_accounts"
        """Treasury financial accounts."""
        
        POST_TREASURY_FINANCIAL_ACCOUNTS_FINANCIAL_ACCOUNT = "stripe_post_treasury_financial_accounts_financial_account"
        """Treasury financial accounts financial account."""
        
        POST_TREASURY_FINANCIAL_ACCOUNTS_FINANCIAL_ACCOUNT_FEATURES = "stripe_post_treasury_financial_accounts_financial_account_features"
        """Treasury financial accounts financial account features."""
        
        POST_TREASURY_INBOUND_TRANSFERS = "stripe_post_treasury_inbound_transfers"
        """Treasury inbound transfers."""
        
        POST_TREASURY_INBOUND_TRANSFERS_INBOUND_TRANSFER_CANCEL = "stripe_post_treasury_inbound_transfers_inbound_transfer_cancel"
        """Treasury inbound transfers inbound transfer cancel."""
        
        POST_TREASURY_OUTBOUND_PAYMENTS = "stripe_post_treasury_outbound_payments"
        """Treasury outbound payments."""
        
        POST_TREASURY_OUTBOUND_PAYMENTS_ID_CANCEL = "stripe_post_treasury_outbound_payments_id_cancel"
        """Treasury outbound payments id cancel."""
        
        POST_TREASURY_OUTBOUND_TRANSFERS = "stripe_post_treasury_outbound_transfers"
        """Treasury outbound transfers."""
        
        POST_TREASURY_OUTBOUND_TRANSFERS_OUTBOUND_TRANSFER_CANCEL = "stripe_post_treasury_outbound_transfers_outbound_transfer_cancel"
        """Treasury outbound transfers outbound transfer cancel."""
        
        POST_WEBHOOK_ENDPOINTS = "stripe_post_webhook_endpoints"
        """Webhook endpoints."""
        
        POST_WEBHOOK_ENDPOINTS_WEBHOOK_ENDPOINT = "stripe_post_webhook_endpoints_webhook_endpoint"
        """Webhook endpoints webhook endpoint."""
        

    class Youtube(str, Enum):
        def get_api_service(self) -> APIService:
            return APIService.YOUTUBE
        
        ABUSE_REPORTS_INSERT = "youtube_data_abuse_reports_insert"
        """Abuse reports insert."""
        
        ACTIVITIES_LIST = "youtube_data_activities_list"
        """Activities list."""
        
        CAPTIONS_DELETE = "youtube_data_captions_delete"
        """Captions delete."""
        
        CAPTIONS_DOWNLOAD = "youtube_data_captions_download"
        """Captions download."""
        
        CAPTIONS_INSERT = "youtube_data_captions_insert"
        """Captions insert."""
        
        CAPTIONS_LIST = "youtube_data_captions_list"
        """Captions list."""
        
        CAPTIONS_UPDATE = "youtube_data_captions_update"
        """Captions update."""
        
        CHANNELS_LIST = "youtube_data_channels_list"
        """Channels list."""
        
        CHANNELS_UPDATE = "youtube_data_channels_update"
        """Channels update."""
        
        CHANNEL_BANNERS_INSERT = "youtube_data_channel_banners_insert"
        """Channel banners insert."""
        
        CHANNEL_SECTIONS_DELETE = "youtube_data_channel_sections_delete"
        """Channel sections delete."""
        
        CHANNEL_SECTIONS_INSERT = "youtube_data_channel_sections_insert"
        """Channel sections insert."""
        
        CHANNEL_SECTIONS_LIST = "youtube_data_channel_sections_list"
        """Channel sections list."""
        
        CHANNEL_SECTIONS_UPDATE = "youtube_data_channel_sections_update"
        """Channel sections update."""
        
        COMMENTS_DELETE = "youtube_data_comments_delete"
        """Comments delete."""
        
        COMMENTS_INSERT = "youtube_data_comments_insert"
        """Comments insert."""
        
        COMMENTS_LIST = "youtube_data_comments_list"
        """Comments list."""
        
        COMMENTS_MARK_AS_SPAM = "youtube_data_comments_mark_as_spam"
        """Comments mark as spam."""
        
        COMMENTS_SET_MODERATION_STATUS = "youtube_data_comments_set_moderation_status"
        """Comments set moderation status."""
        
        COMMENTS_UPDATE = "youtube_data_comments_update"
        """Comments update."""
        
        COMMENT_THREADS_INSERT = "youtube_data_comment_threads_insert"
        """Comment threads insert."""
        
        COMMENT_THREADS_LIST = "youtube_data_comment_threads_list"
        """Comment threads list."""
        
        I18N_LANGUAGES_LIST = "youtube_data_i18n_languages_list"
        """I18n languages list."""
        
        I18N_REGIONS_LIST = "youtube_data_i18n_regions_list"
        """I18n regions list."""
        
        LIVE_BROADCASTS_BIND = "youtube_data_live_broadcasts_bind"
        """Live broadcasts bind."""
        
        LIVE_BROADCASTS_DELETE = "youtube_data_live_broadcasts_delete"
        """Live broadcasts delete."""
        
        LIVE_BROADCASTS_INSERT = "youtube_data_live_broadcasts_insert"
        """Live broadcasts insert."""
        
        LIVE_BROADCASTS_INSERT_CUEPOINT = "youtube_data_live_broadcasts_insert_cuepoint"
        """Live broadcasts insert cuepoint."""
        
        LIVE_BROADCASTS_LIST = "youtube_data_live_broadcasts_list"
        """Live broadcasts list."""
        
        LIVE_BROADCASTS_TRANSITION = "youtube_data_live_broadcasts_transition"
        """Live broadcasts transition."""
        
        LIVE_BROADCASTS_UPDATE = "youtube_data_live_broadcasts_update"
        """Live broadcasts update."""
        
        LIVE_CHAT_BANS_DELETE = "youtube_data_live_chat_bans_delete"
        """Live chat bans delete."""
        
        LIVE_CHAT_BANS_INSERT = "youtube_data_live_chat_bans_insert"
        """Live chat bans insert."""
        
        LIVE_CHAT_MESSAGES_DELETE = "youtube_data_live_chat_messages_delete"
        """Live chat messages delete."""
        
        LIVE_CHAT_MESSAGES_INSERT = "youtube_data_live_chat_messages_insert"
        """Live chat messages insert."""
        
        LIVE_CHAT_MESSAGES_LIST = "youtube_data_live_chat_messages_list"
        """Live chat messages list."""
        
        LIVE_CHAT_MODERATORS_DELETE = "youtube_data_live_chat_moderators_delete"
        """Live chat moderators delete."""
        
        LIVE_CHAT_MODERATORS_INSERT = "youtube_data_live_chat_moderators_insert"
        """Live chat moderators insert."""
        
        LIVE_CHAT_MODERATORS_LIST = "youtube_data_live_chat_moderators_list"
        """Live chat moderators list."""
        
        LIVE_STREAMS_DELETE = "youtube_data_live_streams_delete"
        """Live streams delete."""
        
        LIVE_STREAMS_INSERT = "youtube_data_live_streams_insert"
        """Live streams insert."""
        
        LIVE_STREAMS_LIST = "youtube_data_live_streams_list"
        """Live streams list."""
        
        LIVE_STREAMS_UPDATE = "youtube_data_live_streams_update"
        """Live streams update."""
        
        MEMBERSHIPS_LEVELS_LIST = "youtube_data_memberships_levels_list"
        """Memberships levels list."""
        
        MEMBERS_LIST = "youtube_data_members_list"
        """Members list."""
        
        PLAYLISTS_DELETE = "youtube_data_playlists_delete"
        """Playlists delete."""
        
        PLAYLISTS_INSERT = "youtube_data_playlists_insert"
        """Playlists insert."""
        
        PLAYLISTS_LIST = "youtube_data_playlists_list"
        """Playlists list."""
        
        PLAYLISTS_UPDATE = "youtube_data_playlists_update"
        """Playlists update."""
        
        PLAYLIST_ITEMS_DELETE = "youtube_data_playlist_items_delete"
        """Playlist items delete."""
        
        PLAYLIST_ITEMS_INSERT = "youtube_data_playlist_items_insert"
        """Playlist items insert."""
        
        PLAYLIST_ITEMS_LIST = "youtube_data_playlist_items_list"
        """Playlist items list."""
        
        PLAYLIST_ITEMS_UPDATE = "youtube_data_playlist_items_update"
        """Playlist items update."""
        
        SEARCH_LIST = "youtube_data_search_list"
        """Search list."""
        
        SUBSCRIPTIONS_DELETE = "youtube_data_subscriptions_delete"
        """Subscriptions delete."""
        
        SUBSCRIPTIONS_INSERT = "youtube_data_subscriptions_insert"
        """Subscriptions insert."""
        
        SUBSCRIPTIONS_LIST = "youtube_data_subscriptions_list"
        """Subscriptions list."""
        
        SUPER_CHAT_EVENTS_LIST = "youtube_data_super_chat_events_list"
        """Super chat events list."""
        
        TESTS_INSERT = "youtube_data_tests_insert"
        """Tests insert."""
        
        THIRD_PARTY_LINKS_DELETE = "youtube_data_third_party_links_delete"
        """Third party links delete."""
        
        THIRD_PARTY_LINKS_INSERT = "youtube_data_third_party_links_insert"
        """Third party links insert."""
        
        THIRD_PARTY_LINKS_LIST = "youtube_data_third_party_links_list"
        """Third party links list."""
        
        THIRD_PARTY_LINKS_UPDATE = "youtube_data_third_party_links_update"
        """Third party links update."""
        
        THUMBNAILS_SET = "youtube_data_thumbnails_set"
        """Thumbnails set."""
        
        VIDEOS_DELETE = "youtube_data_videos_delete"
        """Videos delete."""
        
        VIDEOS_GET_RATING = "youtube_data_videos_get_rating"
        """Videos get rating."""
        
        VIDEOS_INSERT = "youtube_data_videos_insert"
        """Videos insert."""
        
        VIDEOS_LIST = "youtube_data_videos_list"
        """Videos list."""
        
        VIDEOS_RATE = "youtube_data_videos_rate"
        """Videos rate."""
        
        VIDEOS_REPORT_ABUSE = "youtube_data_videos_report_abuse"
        """Videos report abuse."""
        
        VIDEOS_UPDATE = "youtube_data_videos_update"
        """Videos update."""
        
        VIDEO_ABUSE_REPORT_REASONS_LIST = "youtube_data_video_abuse_report_reasons_list"
        """Video abuse report reasons list."""
        
        VIDEO_CATEGORIES_LIST = "youtube_data_video_categories_list"
        """Video categories list."""
        
        WATERMARKS_SET = "youtube_data_watermarks_set"
        """Watermarks set."""
        
        WATERMARKS_UNSET = "youtube_data_watermarks_unset"
        """Watermarks unset."""
        
        YOUTUBE_V3_UPDATE_COMMENT_THREADS = "youtube_data_youtube_v3_update_comment_threads"
        """Youtube v3 update comment threads."""
        

    class Zoom(str, Enum):
        def get_api_service(self) -> APIService:
            return APIService.ZOOM
        
        ACCOUNT = "zoom_account"
        """Account."""
        
        ACCOUNTS = "zoom_accounts"
        """Accounts."""
        
        ACCOUNT_BILLING = "zoom_account_billing"
        """Billing."""
        
        ACCOUNT_BILLING_INVOICES = "zoom_account_billing_invoices"
        """Billing invoices."""
        
        ACCOUNT_BILLING_UPDATE = "zoom_account_billing_update"
        """Billing update."""
        
        ACCOUNT_CALL_LOGS = "zoom_account_call_logs"
        """Call logs."""
        
        ACCOUNT_CREATE = "zoom_account_create"
        """Create."""
        
        ACCOUNT_DISASSOCIATE = "zoom_account_disassociate"
        """Disassociate."""
        
        ACCOUNT_MANAGED_DOMAIN = "zoom_account_managed_domain"
        """Managed domain."""
        
        ACCOUNT_OPTIONS_UPDATE = "zoom_account_options_update"
        """Options update."""
        
        ACCOUNT_PLANS = "zoom_account_plans"
        """Plans."""
        
        ACCOUNT_PLAN_ADDON_CANCEL = "zoom_account_plan_addon_cancel"
        """Plan addon cancel."""
        
        ACCOUNT_PLAN_ADDON_CREATE = "zoom_account_plan_addon_create"
        """Plan addon create."""
        
        ACCOUNT_PLAN_ADDON_UPDATE = "zoom_account_plan_addon_update"
        """Plan addon update."""
        
        ACCOUNT_PLAN_BASE_DELETE = "zoom_account_plan_base_delete"
        """Plan base delete."""
        
        ACCOUNT_PLAN_BASE_UPDATE = "zoom_account_plan_base_update"
        """Plan base update."""
        
        ACCOUNT_PLAN_CREATE = "zoom_account_plan_create"
        """Plan create."""
        
        ACCOUNT_SETTINGS = "zoom_account_settings"
        """Settings."""
        
        ACCOUNT_SETTINGS_UPDATE = "zoom_account_settings_update"
        """Settings update."""
        
        ACCOUNT_TRUSTED_DOMAIN = "zoom_account_trusted_domain"
        """Trusted domain."""
        
        ADD_ANUMBER_TO_BLOCKED_LIST = "zoom_add_anumber_to_blocked_list"
        """Anumber to blocked list."""
        
        ADD_AROOM = "zoom_add_aroom"
        """Aroom."""
        
        ADD_AUTO_RECEPTIONIST = "zoom_add_auto_receptionist"
        """Auto receptionist."""
        
        ADD_AZRLOCATION = "zoom_add_azrlocation"
        """Azrlocation."""
        
        ADD_BATCH_WEBINAR_REGISTRANTS = "zoom_add_batch_webinar_registrants"
        """Batch webinar registrants."""
        
        ADD_BYOCNUMBER = "zoom_add_byocnumber"
        """Byocnumber."""
        
        ADD_CALLOUT_COUNTRIES = "zoom_add_callout_countries"
        """Callout countries."""
        
        ADD_COMMON_AREA_PHONE = "zoom_add_common_area_phone"
        """Common area phone."""
        
        ADD_INTERNAL_NUMBERS = "zoom_add_internal_numbers"
        """Internal numbers."""
        
        ADD_MEMBERS_TO_CALL_QUEUE = "zoom_add_members_to_call_queue"
        """Members to call queue."""
        
        ADD_MEMBERS_TO_SHARED_LINE_GROUP = "zoom_add_members_to_shared_line_group"
        """Members to shared line group."""
        
        ADD_PHONE_DEVICE = "zoom_add_phone_device"
        """Phone device."""
        
        ADD_ROLE_MEMBERS = "zoom_add_role_members"
        """Role members."""
        
        ADD_SETTING_TEMPLATE = "zoom_add_setting_template"
        """Setting template."""
        
        ADD_USER_SETTING = "zoom_add_user_setting"
        """User setting."""
        
        ASSIGN_CALLING_PLAN = "zoom_assign_calling_plan"
        """Calling plan."""
        
        ASSIGN_PHONE_NUMBER = "zoom_assign_phone_number"
        """Phone number."""
        
        ASSIGN_PHONE_NUMBERS_AUTO_RECEPTIONIST = "zoom_assign_phone_numbers_auto_receptionist"
        """Phone numbers auto receptionist."""
        
        ASSIGN_PHONE_NUMBERS_SLG = "zoom_assign_phone_numbers_slg"
        """Phone numbers slg."""
        
        ASSIGN_PHONE_TO_CALL_QUEUE = "zoom_assign_phone_to_call_queue"
        """Phone to call queue."""
        
        ASSIGN_SIPCONFIG = "zoom_assign_sipconfig"
        """Sipconfig."""
        
        ASSIGN_SIPTRUNKS = "zoom_assign_siptrunks"
        """Siptrunks."""
        
        ASSIGN_SIP_TRUNK_NUMBERS = "zoom_assign_sip_trunk_numbers"
        """Sip trunk numbers."""
        
        CHANGE_CALL_QUEUE_MANAGER = "zoom_change_call_queue_manager"
        """Call queue manager."""
        
        CHANGE_MAIN_COMPANY_NUMBER = "zoom_change_main_company_number"
        """Main company number."""
        
        CHANGE_PARENT_LOCATION = "zoom_change_parent_location"
        """Parent location."""
        
        CHANGE_ZOOM_ROOMS_APP_VERSION = "zoom_change_zoom_rooms_app_version"
        """Zoom rooms app version."""
        
        CHANGE_ZRLOCATION = "zoom_change_zrlocation"
        """Zrlocation."""
        
        CHECK_IN_ROOMS = "zoom_check_in_rooms"
        """In rooms."""
        
        CREATE_ASHARED_LINE_GROUP = "zoom_create_ashared_line_group"
        """Ashared line group."""
        
        CREATE_BATCH_POLLS = "zoom_create_batch_polls"
        """Batch polls."""
        
        CREATE_CALL_QUEUE = "zoom_create_call_queue"
        """Call queue."""
        
        CREATE_CHANNEL = "zoom_create_channel"
        """Channel."""
        
        CREATE_PHONE_SITE = "zoom_create_phone_site"
        """Phone site."""
        
        CREATE_ROLE = "zoom_create_role"
        """Role."""
        
        CREATE_SIPPHONE = "zoom_create_sipphone"
        """Sipphone."""
        
        DASHBOARD_CLIENT_FEEDBACK = "zoom_dashboard_client_feedback"
        """Client feedback."""
        
        DASHBOARD_CLIENT_FEEDBACK_DETAIL = "zoom_dashboard_client_feedback_detail"
        """Client feedback detail."""
        
        DASHBOARD_CRC = "zoom_dashboard_crc"
        """Crc."""
        
        DASHBOARD_IM = "zoom_dashboard_im"
        """Im."""
        
        DASHBOARD_ISSUE_DETAIL_ZOOM_ROOM = "zoom_dashboard_issue_detail_zoom_room"
        """Issue detail zoom room."""
        
        DASHBOARD_ISSUE_ZOOM_ROOM = "zoom_dashboard_issue_zoom_room"
        """Issue zoom room."""
        
        DASHBOARD_MEETINGS = "zoom_dashboard_meetings"
        """Meetings."""
        
        DASHBOARD_MEETING_DETAIL = "zoom_dashboard_meeting_detail"
        """Meeting detail."""
        
        DASHBOARD_MEETING_PARTICIPANTS = "zoom_dashboard_meeting_participants"
        """Meeting participants."""
        
        DASHBOARD_MEETING_PARTICIPANTS_QOS = "zoom_dashboard_meeting_participants_qos"
        """Meeting participants qos."""
        
        DASHBOARD_MEETING_PARTICIPANT_QOS = "zoom_dashboard_meeting_participant_qos"
        """Meeting participant qos."""
        
        DASHBOARD_MEETING_PARTICIPANT_SHARE = "zoom_dashboard_meeting_participant_share"
        """Meeting participant share."""
        
        DASHBOARD_WEBINARS = "zoom_dashboard_webinars"
        """Webinars."""
        
        DASHBOARD_WEBINAR_DETAIL = "zoom_dashboard_webinar_detail"
        """Webinar detail."""
        
        DASHBOARD_WEBINAR_PARTICIPANTS = "zoom_dashboard_webinar_participants"
        """Webinar participants."""
        
        DASHBOARD_WEBINAR_PARTICIPANTS_QOS = "zoom_dashboard_webinar_participants_qos"
        """Webinar participants qos."""
        
        DASHBOARD_WEBINAR_PARTICIPANT_QOS = "zoom_dashboard_webinar_participant_qos"
        """Webinar participant qos."""
        
        DASHBOARD_WEBINAR_PARTICIPANT_SHARE = "zoom_dashboard_webinar_participant_share"
        """Webinar participant share."""
        
        DASHBOARD_ZOOM_ROOM = "zoom_dashboard_zoom_room"
        """Zoom room."""
        
        DASHBOARD_ZOOM_ROOMS = "zoom_dashboard_zoom_rooms"
        """Zoom rooms."""
        
        DASHBOARD_ZOOM_ROOM_ISSUE = "zoom_dashboard_zoom_room_issue"
        """Zoom room issue."""
        
        DELETE_ABLOCKED_LIST = "zoom_delete_ablocked_list"
        """Ablocked list."""
        
        DELETE_ACALL_QUEUE = "zoom_delete_acall_queue"
        """Acall queue."""
        
        DELETE_ACHATBOT_MESSAGE = "zoom_delete_achatbot_message"
        """Achatbot message."""
        
        DELETE_ADEVICE = "zoom_delete_adevice"
        """Adevice."""
        
        DELETE_ALL_SIP_NUMBERS = "zoom_delete_all_sip_numbers"
        """All sip numbers."""
        
        DELETE_AMEMBER_SLG = "zoom_delete_amember_slg"
        """Amember slg."""
        
        DELETE_APHONE_NUMBER_SLG = "zoom_delete_aphone_number_slg"
        """Aphone number slg."""
        
        DELETE_ASHARED_LINE_GROUP = "zoom_delete_ashared_line_group"
        """Ashared line group."""
        
        DELETE_AZOOM_ROOM = "zoom_delete_azoom_room"
        """Azoom room."""
        
        DELETE_CALL_LOG = "zoom_delete_call_log"
        """Call log."""
        
        DELETE_CHANNEL = "zoom_delete_channel"
        """Channel."""
        
        DELETE_CHAT_MESSAGE = "zoom_delete_chat_message"
        """Chat message."""
        
        DELETE_COMMON_AREA_PHONE = "zoom_delete_common_area_phone"
        """Common area phone."""
        
        DELETE_INTERNAL_CALL_OUT_COUNTRY = "zoom_delete_internal_call_out_country"
        """Internal call out country."""
        
        DELETE_INTERNAL_NUMBER = "zoom_delete_internal_number"
        """Internal number."""
        
        DELETE_MEMBERS_OF_SLG = "zoom_delete_members_of_slg"
        """Members of slg."""
        
        DELETE_PHONE_SITE = "zoom_delete_phone_site"
        """Phone site."""
        
        DELETE_ROLE = "zoom_delete_role"
        """Role."""
        
        DELETE_SIPPHONE = "zoom_delete_sipphone"
        """Sipphone."""
        
        DELETE_SIPTRUNK = "zoom_delete_siptrunk"
        """Siptrunk."""
        
        DELETE_USER_LEVEL_CHANNEL = "zoom_delete_user_level_channel"
        """User level channel."""
        
        DELETE_USER_SETTING = "zoom_delete_user_setting"
        """User setting."""
        
        DELETE_VOICEMAIL = "zoom_delete_voicemail"
        """Voicemail."""
        
        DELETE_WEBINAR_REGISTRANT = "zoom_delete_webinar_registrant"
        """Webinar registrant."""
        
        DEL_GROUP_VB = "zoom_del_group_vb"
        """Group vb."""
        
        DEL_USER_VB = "zoom_del_user_vb"
        """User vb."""
        
        DEL_VB = "zoom_del_vb"
        """Vb."""
        
        DEVICE_CREATE = "zoom_device_create"
        """Create."""
        
        DEVICE_DELETE = "zoom_device_delete"
        """Delete."""
        
        DEVICE_LIST = "zoom_device_list"
        """List."""
        
        DEVICE_UPDATE = "zoom_device_update"
        """Update."""
        
        DOWNLOAD_INVOICE_PDF = "zoom_download_invoice_pdf"
        """Invoice pdf."""
        
        EDIT_CHATBOT_MESSAGE = "zoom_edit_chatbot_message"
        """Chatbot message."""
        
        EDIT_MESSAGE = "zoom_edit_message"
        """Message."""
        
        GET_ABLOCKED_LIST = "zoom_get_ablocked_list"
        """Ablocked list."""
        
        GET_ACALL_QUEUE = "zoom_get_acall_queue"
        """Acall queue."""
        
        GET_ACCOUNT_BILLING_INVOICE = "zoom_get_account_billing_invoice"
        """Account billing invoice."""
        
        GET_ACCOUNT_CLOUD_RECORDING = "zoom_get_account_cloud_recording"
        """Account cloud recording."""
        
        GET_ACCOUNT_LOCK_SETTINGS = "zoom_get_account_lock_settings"
        """Account lock settings."""
        
        GET_ACOMMON_AREA_PHONE = "zoom_get_acommon_area_phone"
        """Acommon area phone."""
        
        GET_ADEVICE = "zoom_get_adevice"
        """Adevice."""
        
        GET_ASHARED_LINE_GROUP = "zoom_get_ashared_line_group"
        """Ashared line group."""
        
        GET_ASITE = "zoom_get_asite"
        """Asite."""
        
        GET_CALL_LOG_METRICS_DETAILS = "zoom_get_call_log_metrics_details"
        """Call log metrics details."""
        
        GET_CALL_QO_S = "zoom_get_call_qo_s"
        """Call qo s."""
        
        GET_CALL_QUEUE_RECORDINGS = "zoom_get_call_queue_recordings"
        """Call queue recordings."""
        
        GET_CHANNEL = "zoom_get_channel"
        """Channel."""
        
        GET_CHANNELS = "zoom_get_channels"
        """Channels."""
        
        GET_CHAT_MESSAGES = "zoom_get_chat_messages"
        """Chat messages."""
        
        GET_GROUP_LOCK_SETTINGS = "zoom_get_group_lock_settings"
        """Group lock settings."""
        
        GET_GROUP_SETTINGS = "zoom_get_group_settings"
        """Group settings."""
        
        GET_LIVE_STREAM_DETAILS = "zoom_get_live_stream_details"
        """Live stream details."""
        
        GET_PHONE_NUMBER_DETAILS = "zoom_get_phone_number_details"
        """Phone number details."""
        
        GET_PHONE_RECORDINGS = "zoom_get_phone_recordings"
        """Phone recordings."""
        
        GET_PLAN_USAGE = "zoom_get_plan_usage"
        """Plan usage."""
        
        GET_PSOPERATION_LOGS = "zoom_get_psoperation_logs"
        """Psoperation logs."""
        
        GET_ROLE_INFORMATION = "zoom_get_role_information"
        """Role information."""
        
        GET_SETTING_TEMPLATE = "zoom_get_setting_template"
        """Setting template."""
        
        GET_TRACKING_SOURCES = "zoom_get_tracking_sources"
        """Tracking sources."""
        
        GET_USER_CONTACT = "zoom_get_user_contact"
        """User contact."""
        
        GET_USER_CONTACTS = "zoom_get_user_contacts"
        """User contacts."""
        
        GET_USER_LEVEL_CHANNEL = "zoom_get_user_level_channel"
        """User level channel."""
        
        GET_ZRACCOUNT_PROFILE = "zoom_get_zraccount_profile"
        """Zraccount profile."""
        
        GET_ZRACCOUNT_SETTINGS = "zoom_get_zraccount_settings"
        """Zraccount settings."""
        
        GET_ZRLOCATION_PROFILE = "zoom_get_zrlocation_profile"
        """Zrlocation profile."""
        
        GET_ZRLOCATION_SETTINGS = "zoom_get_zrlocation_settings"
        """Zrlocation settings."""
        
        GET_ZRLOCATION_STRUCTURE = "zoom_get_zrlocation_structure"
        """Zrlocation structure."""
        
        GET_ZRPROFILE = "zoom_get_zrprofile"
        """Zrprofile."""
        
        GET_ZRSETTINGS = "zoom_get_zrsettings"
        """Zrsettings."""
        
        GROUP = "zoom_group"
        """Group."""
        
        GROUPS = "zoom_groups"
        """Groups."""
        
        GROUP_CREATE = "zoom_group_create"
        """Create."""
        
        GROUP_DELETE = "zoom_group_delete"
        """Delete."""
        
        GROUP_LOCKED_SETTINGS = "zoom_group_locked_settings"
        """Locked settings."""
        
        GROUP_MEMBERS = "zoom_group_members"
        """Members."""
        
        GROUP_MEMBERS_CREATE = "zoom_group_members_create"
        """Members create."""
        
        GROUP_MEMBERS_DELETE = "zoom_group_members_delete"
        """Members delete."""
        
        GROUP_UPDATE = "zoom_group_update"
        """Update."""
        
        IM_CHAT_MESSAGES = "zoom_im_chat_messages"
        """Chat messages."""
        
        IM_CHAT_SESSIONS = "zoom_im_chat_sessions"
        """Chat sessions."""
        
        IM_GROUP = "zoom_im_group"
        """Group."""
        
        IM_GROUPS = "zoom_im_groups"
        """Groups."""
        
        IM_GROUP_CREATE = "zoom_im_group_create"
        """Group create."""
        
        IM_GROUP_DELETE = "zoom_im_group_delete"
        """Group delete."""
        
        IM_GROUP_MEMBERS = "zoom_im_group_members"
        """Group members."""
        
        IM_GROUP_MEMBERS_CREATE = "zoom_im_group_members_create"
        """Group members create."""
        
        IM_GROUP_MEMBERS_DELETE = "zoom_im_group_members_delete"
        """Group members delete."""
        
        IM_GROUP_UPDATE = "zoom_im_group_update"
        """Group update."""
        
        INVITE_CHANNEL_MEMBERS = "zoom_invite_channel_members"
        """Channel members."""
        
        IN_MEETING_RECORDING_CONTROL = "zoom_in_meeting_recording_control"
        """Meeting recording control."""
        
        JOIN_CHANNEL = "zoom_join_channel"
        """Channel."""
        
        LEAVE_CHANNEL = "zoom_leave_channel"
        """Channel."""
        
        LISTIMMESSAGES = "zoom_listimmessages"
        """Listimmessages."""
        
        LIST_ACCOUNT_PHONE_NUMBERS = "zoom_list_account_phone_numbers"
        """Account phone numbers."""
        
        LIST_ARCHIVED_FILES = "zoom_list_archived_files"
        """Archived files."""
        
        LIST_BLOCKED_LIST = "zoom_list_blocked_list"
        """Blocked list."""
        
        LIST_BYOCSIPTRUNK = "zoom_list_byocsiptrunk"
        """Byocsiptrunk."""
        
        LIST_CALLING_PLANS = "zoom_list_calling_plans"
        """Calling plans."""
        
        LIST_CALL_LOGS_METRICS = "zoom_list_call_logs_metrics"
        """Call logs metrics."""
        
        LIST_CALL_QUEUES = "zoom_list_call_queues"
        """Call queues."""
        
        LIST_CHANNEL_MEMBERS = "zoom_list_channel_members"
        """Channel members."""
        
        LIST_COMMON_AREA_PHONES = "zoom_list_common_area_phones"
        """Common area phones."""
        
        LIST_DIGITAL_SIGNAGE_CONTENT = "zoom_list_digital_signage_content"
        """Digital signage content."""
        
        LIST_INTERNAL_CALLOUT_COUNTRIES = "zoom_list_internal_callout_countries"
        """Internal callout countries."""
        
        LIST_INTERNAL_NUMBERS = "zoom_list_internal_numbers"
        """Internal numbers."""
        
        LIST_MEETING_SATISFACTION = "zoom_list_meeting_satisfaction"
        """Meeting satisfaction."""
        
        LIST_MEETING_TEMPLATES = "zoom_list_meeting_templates"
        """Meeting templates."""
        
        LIST_PAST_MEETING_FILES = "zoom_list_past_meeting_files"
        """Past meeting files."""
        
        LIST_PAST_MEETING_POLLS = "zoom_list_past_meeting_polls"
        """Past meeting polls."""
        
        LIST_PAST_WEBINAR_FILES = "zoom_list_past_webinar_files"
        """Past webinar files."""
        
        LIST_PAST_WEBINAR_POLL_RESULTS = "zoom_list_past_webinar_poll_results"
        """Past webinar poll results."""
        
        LIST_PAST_WEBINAR_QA = "zoom_list_past_webinar_qa"
        """Past webinar qa."""
        
        LIST_PHONE_DEVICES = "zoom_list_phone_devices"
        """Phone devices."""
        
        LIST_PHONE_SITES = "zoom_list_phone_sites"
        """Phone sites."""
        
        LIST_PHONE_USERS = "zoom_list_phone_users"
        """Phone users."""
        
        LIST_SETTING_TEMPLATES = "zoom_list_setting_templates"
        """Setting templates."""
        
        LIST_SHARED_LINE_GROUPS = "zoom_list_shared_line_groups"
        """Shared line groups."""
        
        LIST_SIPTRUNKS = "zoom_list_siptrunks"
        """Siptrunks."""
        
        LIST_SIP_PHONES = "zoom_list_sip_phones"
        """Sip phones."""
        
        LIST_SIP_TRUNK_NUMBERS = "zoom_list_sip_trunk_numbers"
        """Sip trunk numbers."""
        
        LIST_WEBINAR_PARTICIPANTS = "zoom_list_webinar_participants"
        """Webinar participants."""
        
        LIST_WEBINAR_TEMPLATES = "zoom_list_webinar_templates"
        """Webinar templates."""
        
        LIST_ZOOM_ROOMS = "zoom_list_zoom_rooms"
        """Zoom rooms."""
        
        LIST_ZRDEVICES = "zoom_list_zrdevices"
        """Zrdevices."""
        
        LIST_ZRLOCATIONS = "zoom_list_zrlocations"
        """Zrlocations."""
        
        MANAGE_E911SIGNAGE = "zoom_manage_e911signage"
        """E911signage."""
        
        MEETING = "zoom_meeting"
        """Meeting."""
        
        MEETINGREGISTRANTDELETE = "zoom_meetingregistrantdelete"
        """Meetingregistrantdelete."""
        
        MEETINGS = "zoom_meetings"
        """Meetings."""
        
        MEETING_CREATE = "zoom_meeting_create"
        """Create."""
        
        MEETING_DELETE = "zoom_meeting_delete"
        """Delete."""
        
        MEETING_INVITATION = "zoom_meeting_invitation"
        """Invitation."""
        
        MEETING_LIVE_STREAM_STATUS_UPDATE = "zoom_meeting_live_stream_status_update"
        """Live stream status update."""
        
        MEETING_LIVE_STREAM_UPDATE = "zoom_meeting_live_stream_update"
        """Live stream update."""
        
        MEETING_POLLS = "zoom_meeting_polls"
        """Polls."""
        
        MEETING_POLL_CREATE = "zoom_meeting_poll_create"
        """Poll create."""
        
        MEETING_POLL_DELETE = "zoom_meeting_poll_delete"
        """Poll delete."""
        
        MEETING_POLL_GET = "zoom_meeting_poll_get"
        """Poll get."""
        
        MEETING_POLL_UPDATE = "zoom_meeting_poll_update"
        """Poll update."""
        
        MEETING_RECORDING_REGISTRANTS = "zoom_meeting_recording_registrants"
        """Recording registrants."""
        
        MEETING_RECORDING_REGISTRANT_CREATE = "zoom_meeting_recording_registrant_create"
        """Recording registrant create."""
        
        MEETING_RECORDING_REGISTRANT_STATUS = "zoom_meeting_recording_registrant_status"
        """Recording registrant status."""
        
        MEETING_REGISTRANTS = "zoom_meeting_registrants"
        """Registrants."""
        
        MEETING_REGISTRANTS_QUESTIONS_GET = "zoom_meeting_registrants_questions_get"
        """Registrants questions get."""
        
        MEETING_REGISTRANT_CREATE = "zoom_meeting_registrant_create"
        """Registrant create."""
        
        MEETING_REGISTRANT_QUESTION_UPDATE = "zoom_meeting_registrant_question_update"
        """Registrant question update."""
        
        MEETING_REGISTRANT_STATUS = "zoom_meeting_registrant_status"
        """Registrant status."""
        
        MEETING_STATUS = "zoom_meeting_status"
        """Status."""
        
        MEETING_UPDATE = "zoom_meeting_update"
        """Update."""
        
        PARTICIPANT_FEEDBACK = "zoom_participant_feedback"
        """Feedback."""
        
        PARTICIPANT_WEBINAR_FEEDBACK = "zoom_participant_webinar_feedback"
        """Webinar feedback."""
        
        PAST_MEETINGS = "zoom_past_meetings"
        """Meetings."""
        
        PAST_MEETING_DETAILS = "zoom_past_meeting_details"
        """Meeting details."""
        
        PAST_MEETING_PARTICIPANTS = "zoom_past_meeting_participants"
        """Meeting participants."""
        
        PAST_WEBINARS = "zoom_past_webinars"
        """Webinars."""
        
        PHONE_USER = "zoom_phone_user"
        """User."""
        
        PHONE_USER_CALL_LOGS = "zoom_phone_user_call_logs"
        """User call logs."""
        
        PHONE_USER_RECORDINGS = "zoom_phone_user_recordings"
        """User recordings."""
        
        PHONE_USER_SETTINGS = "zoom_phone_user_settings"
        """User settings."""
        
        PHONE_USER_VOICE_MAILS = "zoom_phone_user_voice_mails"
        """User voice mails."""
        
        POST_PHONE_SIPTRUNK = "zoom_post_phone_siptrunk"
        """Phone siptrunk."""
        
        RECORDINGS_LIST = "zoom_recordings_list"
        """List."""
        
        RECORDING_DELETE = "zoom_recording_delete"
        """Delete."""
        
        RECORDING_DELETE_ONE = "zoom_recording_delete_one"
        """Delete one."""
        
        RECORDING_GET = "zoom_recording_get"
        """Get."""
        
        RECORDING_REGISTRANTS_QUESTIONS_GET = "zoom_recording_registrants_questions_get"
        """Registrants questions get."""
        
        RECORDING_REGISTRANT_QUESTION_UPDATE = "zoom_recording_registrant_question_update"
        """Registrant question update."""
        
        RECORDING_SETTINGS_UPDATE = "zoom_recording_settings_update"
        """Settings update."""
        
        RECORDING_SETTING_UPDATE = "zoom_recording_setting_update"
        """Setting update."""
        
        RECORDING_STATUS_UPDATE = "zoom_recording_status_update"
        """Status update."""
        
        RECORDING_STATUS_UPDATE_ONE = "zoom_recording_status_update_one"
        """Status update one."""
        
        REMOVE_ACHANNEL_MEMBER = "zoom_remove_achannel_member"
        """Achannel member."""
        
        REMOVE_AUSER_LEVEL_CHANNEL_MEMBER = "zoom_remove_auser_level_channel_member"
        """Auser level channel member."""
        
        REPORT_CLOUD_RECORDING = "zoom_report_cloud_recording"
        """Cloud recording."""
        
        REPORT_DAILY = "zoom_report_daily"
        """Daily."""
        
        REPORT_MEETINGS = "zoom_report_meetings"
        """Meetings."""
        
        REPORT_MEETING_DETAILS = "zoom_report_meeting_details"
        """Meeting details."""
        
        REPORT_MEETING_PARTICIPANTS = "zoom_report_meeting_participants"
        """Meeting participants."""
        
        REPORT_MEETING_POLLS = "zoom_report_meeting_polls"
        """Meeting polls."""
        
        REPORT_OPERATION_LOGS = "zoom_report_operation_logs"
        """Operation logs."""
        
        REPORT_SIGN_IN_SIGN_OUT_ACTIVITIES = "zoom_report_sign_in_sign_out_activities"
        """Sign in sign out activities."""
        
        REPORT_TELEPHONE = "zoom_report_telephone"
        """Telephone."""
        
        REPORT_USERS = "zoom_report_users"
        """Users."""
        
        REPORT_WEBINAR_DETAILS = "zoom_report_webinar_details"
        """Webinar details."""
        
        REPORT_WEBINAR_PARTICIPANTS = "zoom_report_webinar_participants"
        """Webinar participants."""
        
        REPORT_WEBINAR_POLLS = "zoom_report_webinar_polls"
        """Webinar polls."""
        
        REPORT_WEBINAR_QA = "zoom_report_webinar_qa"
        """Webinar qa."""
        
        ROLES = "zoom_roles"
        """Roles."""
        
        ROLE_MEMBERS = "zoom_role_members"
        """Members."""
        
        ROLE_MEMBER_DELETE = "zoom_role_member_delete"
        """Member delete."""
        
        SEARCH_COMPANY_CONTACTS = "zoom_search_company_contacts"
        """Company contacts."""
        
        SENDA_CHAT_MESSAGE = "zoom_senda_chat_message"
        """Chat message."""
        
        SENDCHATBOT = "zoom_sendchatbot"
        """Sendchatbot."""
        
        SENDIMMESSAGES = "zoom_sendimmessages"
        """Sendimmessages."""
        
        SET_UP_ACCOUNT = "zoom_set_up_account"
        """Up account."""
        
        SWITCH_USER_ACCOUNT = "zoom_switch_user_account"
        """User account."""
        
        TRACKINGFIELD_CREATE = "zoom_trackingfield_create"
        """Create."""
        
        TRACKINGFIELD_DELETE = "zoom_trackingfield_delete"
        """Delete."""
        
        TRACKINGFIELD_GET = "zoom_trackingfield_get"
        """Get."""
        
        TRACKINGFIELD_LIST = "zoom_trackingfield_list"
        """List."""
        
        TRACKINGFIELD_UPDATE = "zoom_trackingfield_update"
        """Update."""
        
        TSP = "zoom_tsp"
        """Tsp."""
        
        TSP_UPDATE = "zoom_tsp_update"
        """Update."""
        
        TSP_URL_UPDATE = "zoom_tsp_url_update"
        """Url update."""
        
        UNASSIGN_ALL_MEMBERS = "zoom_unassign_all_members"
        """All members."""
        
        UNASSIGN_ALL_PHONE_NUMS_AUTO_RECEPTIONIST = "zoom_unassign_all_phone_nums_auto_receptionist"
        """All phone nums auto receptionist."""
        
        UNASSIGN_APHONE_NUM_AUTO_RECEPTIONIST = "zoom_unassign_aphone_num_auto_receptionist"
        """Aphone num auto receptionist."""
        
        UNASSIGN_APHONE_NUM_CALL_QUEUE = "zoom_unassign_aphone_num_call_queue"
        """Aphone num call queue."""
        
        UNASSIGN_CALLING_PLAN = "zoom_unassign_calling_plan"
        """Calling plan."""
        
        UNASSIGN_MEMBER_FROM_CALL_QUEUE = "zoom_unassign_member_from_call_queue"
        """Member from call queue."""
        
        UNASSIGN_PHONE_NUMBER = "zoom_unassign_phone_number"
        """Phone number."""
        
        UN_ASSIGN_PHONE_NUM_CALL_QUEUE = "zoom_un_assign_phone_num_call_queue"
        """Assign phone num call queue."""
        
        UPDATE_ACCOUNT_LOCK_SETTINGS = "zoom_update_account_lock_settings"
        """Account lock settings."""
        
        UPDATE_ACCOUNT_OWNER = "zoom_update_account_owner"
        """Account owner."""
        
        UPDATE_ADEVICE = "zoom_update_adevice"
        """Adevice."""
        
        UPDATE_AGROUP_MEMBER = "zoom_update_agroup_member"
        """Agroup member."""
        
        UPDATE_ASHARED_LINE_GROUP = "zoom_update_ashared_line_group"
        """Ashared line group."""
        
        UPDATE_AUTO_RECEPTIONIST = "zoom_update_auto_receptionist"
        """Auto receptionist."""
        
        UPDATE_BLOCKED_LIST = "zoom_update_blocked_list"
        """Blocked list."""
        
        UPDATE_CALL_QUEUE = "zoom_update_call_queue"
        """Call queue."""
        
        UPDATE_CHANNEL = "zoom_update_channel"
        """Channel."""
        
        UPDATE_COMMON_AREA_PHONE = "zoom_update_common_area_phone"
        """Common area phone."""
        
        UPDATE_GROUP_SETTINGS = "zoom_update_group_settings"
        """Group settings."""
        
        UPDATE_PHONE_NUMBER_DETAILS = "zoom_update_phone_number_details"
        """Phone number details."""
        
        UPDATE_PHONE_SETTINGS = "zoom_update_phone_settings"
        """Phone settings."""
        
        UPDATE_PHONE_SIPTRUNK = "zoom_update_phone_siptrunk"
        """Phone siptrunk."""
        
        UPDATE_PRESENCE_STATUS = "zoom_update_presence_status"
        """Presence status."""
        
        UPDATE_ROLE = "zoom_update_role"
        """Role."""
        
        UPDATE_ROOM_PROFILE = "zoom_update_room_profile"
        """Room profile."""
        
        UPDATE_SETTING_TEMPLATE = "zoom_update_setting_template"
        """Setting template."""
        
        UPDATE_SIPPHONE = "zoom_update_sipphone"
        """Sipphone."""
        
        UPDATE_SITE_DETAILS = "zoom_update_site_details"
        """Site details."""
        
        UPDATE_USER_LEVEL_CHANNEL = "zoom_update_user_level_channel"
        """User level channel."""
        
        UPDATE_USER_PROFILE = "zoom_update_user_profile"
        """User profile."""
        
        UPDATE_USER_SETTING = "zoom_update_user_setting"
        """User setting."""
        
        UPDATE_ZOOM_ROOMS_LOCATION_STRUCTURE = "zoom_update_zoom_rooms_location_structure"
        """Zoom rooms location structure."""
        
        UPDATE_ZOOM_ROOM_ACC_SETTINGS = "zoom_update_zoom_room_acc_settings"
        """Zoom room acc settings."""
        
        UPDATE_ZRACC_PROFILE = "zoom_update_zracc_profile"
        """Zracc profile."""
        
        UPDATE_ZRLOCATION_PROFILE = "zoom_update_zrlocation_profile"
        """Zrlocation profile."""
        
        UPDATE_ZRLOCATION_SETTINGS = "zoom_update_zrlocation_settings"
        """Zrlocation settings."""
        
        UPDATE_ZRSETTINGS = "zoom_update_zrsettings"
        """Zrsettings."""
        
        UPLOAD_GROUP_VB = "zoom_upload_group_vb"
        """Group vb."""
        
        UPLOAD_VB = "zoom_upload_vb"
        """Vb."""
        
        UPLOAD_VBUSER = "zoom_upload_vbuser"
        """Vbuser."""
        
        USER = "zoom_user"
        """User."""
        
        USERS = "zoom_users"
        """Users."""
        
        USER_ASSISTANTS = "zoom_user_assistants"
        """Assistants."""
        
        USER_ASSISTANTS_DELETE = "zoom_user_assistants_delete"
        """Assistants delete."""
        
        USER_ASSISTANT_CREATE = "zoom_user_assistant_create"
        """Assistant create."""
        
        USER_ASSISTANT_DELETE = "zoom_user_assistant_delete"
        """Assistant delete."""
        
        USER_CREATE = "zoom_user_create"
        """Create."""
        
        USER_DELETE = "zoom_user_delete"
        """Delete."""
        
        USER_EMAIL = "zoom_user_email"
        """Email."""
        
        USER_EMAIL_UPDATE = "zoom_user_email_update"
        """Email update."""
        
        USER_PACS = "zoom_user_pacs"
        """Pacs."""
        
        USER_PASSWORD = "zoom_user_password"
        """Password."""
        
        USER_PERMISSION = "zoom_user_permission"
        """Permission."""
        
        USER_PICTURE = "zoom_user_picture"
        """Picture."""
        
        USER_SCHEDULERS = "zoom_user_schedulers"
        """Schedulers."""
        
        USER_SCHEDULERS_DELETE = "zoom_user_schedulers_delete"
        """Schedulers delete."""
        
        USER_SCHEDULER_DELETE = "zoom_user_scheduler_delete"
        """Scheduler delete."""
        
        USER_SETTINGS = "zoom_user_settings"
        """Settings."""
        
        USER_SETTINGS_UPDATE = "zoom_user_settings_update"
        """Settings update."""
        
        USER_SSOTOKEN_DELETE = "zoom_user_ssotoken_delete"
        """Ssotoken delete."""
        
        USER_STATUS = "zoom_user_status"
        """Status."""
        
        USER_TOKEN = "zoom_user_token"
        """Token."""
        
        USER_TSP = "zoom_user_tsp"
        """Tsp."""
        
        USER_TSPCREATE = "zoom_user_tspcreate"
        """Tspcreate."""
        
        USER_TSPDELETE = "zoom_user_tspdelete"
        """Tspdelete."""
        
        USER_TSPS = "zoom_user_tsps"
        """Tsps."""
        
        USER_TSPUPDATE = "zoom_user_tspupdate"
        """Tspupdate."""
        
        USER_UPDATE = "zoom_user_update"
        """Update."""
        
        USER_VANITY_NAME = "zoom_user_vanity_name"
        """Vanity name."""
        
        USER_ZAK = "zoom_user_zak"
        """Zak."""
        
        WEBINAR = "zoom_webinar"
        """Webinar."""
        
        WEBINARS = "zoom_webinars"
        """Webinars."""
        
        WEBINAR_ABSENTEES = "zoom_webinar_absentees"
        """Absentees."""
        
        WEBINAR_CREATE = "zoom_webinar_create"
        """Create."""
        
        WEBINAR_DELETE = "zoom_webinar_delete"
        """Delete."""
        
        WEBINAR_PANELISTS = "zoom_webinar_panelists"
        """Panelists."""
        
        WEBINAR_PANELISTS_DELETE = "zoom_webinar_panelists_delete"
        """Panelists delete."""
        
        WEBINAR_PANELIST_CREATE = "zoom_webinar_panelist_create"
        """Panelist create."""
        
        WEBINAR_PANELIST_DELETE = "zoom_webinar_panelist_delete"
        """Panelist delete."""
        
        WEBINAR_POLLS = "zoom_webinar_polls"
        """Polls."""
        
        WEBINAR_POLL_CREATE = "zoom_webinar_poll_create"
        """Poll create."""
        
        WEBINAR_POLL_DELETE = "zoom_webinar_poll_delete"
        """Poll delete."""
        
        WEBINAR_POLL_GET = "zoom_webinar_poll_get"
        """Poll get."""
        
        WEBINAR_POLL_UPDATE = "zoom_webinar_poll_update"
        """Poll update."""
        
        WEBINAR_REGISTRANTS = "zoom_webinar_registrants"
        """Registrants."""
        
        WEBINAR_REGISTRANTS_QUESTIONS_GET = "zoom_webinar_registrants_questions_get"
        """Registrants questions get."""
        
        WEBINAR_REGISTRANT_CREATE = "zoom_webinar_registrant_create"
        """Registrant create."""
        
        WEBINAR_REGISTRANT_GET = "zoom_webinar_registrant_get"
        """Registrant get."""
        
        WEBINAR_REGISTRANT_QUESTION_UPDATE = "zoom_webinar_registrant_question_update"
        """Registrant question update."""
        
        WEBINAR_REGISTRANT_STATUS = "zoom_webinar_registrant_status"
        """Registrant status."""
        
        WEBINAR_STATUS = "zoom_webinar_status"
        """Status."""
        
        WEBINAR_UPDATE = "zoom_webinar_update"
        """Update."""    
    
    class BraveSearch(str, Enum):
        def get_api_service(self) -> APIService:
            return APIService.BRAVE_SEARCH
        SEARCH = "brave_search_get_web_search_results"
        """Search for information using Brave Search."""
    
    class Airtable(str, Enum):
        def get_api_service(self) -> APIService:
            return APIService.AIRTABLE
        GET_USER_INFO = "airtable_get_user_info"
        """Retrieve information about the user's Airtable account."""
        RECORDS_LIST = "airtable_records_list"
        """Retrieve a list of all records in a table."""
        RECORDS_UPDATE_MULTIPLE = "airtable_records_update_multiple"
        """Update multiple records in a table."""
        RECORDS_REPLACE_MULTIPLE = "airtable_records_replace_multiple"
        """Replace multiple records in a table."""
        RECORDS_CREATE = "airtable_records_create"
        """Create a new record in a table."""
        RECORDS_DELETE_MULTIPLE = "airtable_records_delete_multiple"
        """Delete multiple records from a table."""
        RECORDS_GET = "airtable_records_get"
        """Retrieve a specific record from a table."""
        RECORDS_REPLACE = "airtable_records_replace"
        """Replace a specific record in a table."""
        RECORDS_UPDATE = "airtable_records_update"
        """Update a specific record in a table."""
        RECORDS_DELETE = "airtable_records_delete"
        """Delete a specific record from a table."""
        RECORDS_SYNC_CSV = "airtable_records_sync_csv"
        """Sync data from a CSV file into a table."""
        RECORDS_UPLOAD_ATTACHMENT = "airtable_records_upload_attachment"
        """Upload an attachment to a record."""
        FIELDS_UPDATE = "airtable_fields_update"
        """Update a specific field in a table."""
        FIELDS_CREATE = "airtable_fields_create"
        """Create a new field in a table."""
        COMMENTS_LIST = "airtable_comments_list"
        """Retrieve a list of all comments on a record."""
        COMMENTS_UPDATE = "airtable_comments_update"
        """Update a specific comment on a record."""
        COMMENTS_CREATE = "airtable_comments_create"
        """Create a new comment on a record."""
        COMMENTS_DELETE = "airtable_comments_delete"
        """Delete a comment from a record."""
        TABLES_UPDATE = "airtable_tables_update"
        """Update a specific table in a base."""
        TABLES_CREATE = "airtable_tables_create"
        """Create a new table in a base."""
        BASES_LIST = "airtable_bases_list"
        """Retrieve a list of all bases in the user's Airtable account."""
        BASES_SCHEMA = "airtable_bases_schema"
        """Retrieve the schema of a base."""
        BASES_CREATE = "airtable_bases_create"
        """Create a new base in the user's Airtable account."""
        WEBHOOKS_LIST_PAYLOADS = "airtable_webhooks_list_payloads"
        """Retrieve a list of all webhooks in a base."""
        WEBHOOKS_LIST = "airtable_webhooks_list"
        """Retrieve a list of all webhooks in a base."""
        WEBHOOKS_CREATE = "airtable_webhooks_create"
        """Create a new webhook in a base."""
        WEBHOOKS_DELETE = "airtable_webhooks_delete"
        """Delete a webhook from a base."""
        WEBHOOKS_ENABLE_NOTIFICATIONS = "airtable_webhooks_enable_notifications"
        """Enable notifications for a webhook."""
        WEBHOOKS_REFRESH = "airtable_webhooks_refresh"
        """Refresh a webhook."""
        VIEWS_LIST = "airtable_views_list"
        """Retrieve a list of all views in a base."""
        VIEWS_GET_METADATA = "airtable_views_get"
        """Retrieve a specific view metadatafrom a base."""
        VIEWS_DELETE = "airtable_views_delete"
        """Delete a view from a base."""


    class Gmail(str, Enum):
        def get_api_service(self) -> APIService:
            return APIService.GMAIL
            
        DRAFTS_LIST = "gmail_users_drafts_list"
        """Retrieve a list of all email drafts in the user's Gmail account. This endpoint allows you to access drafts that are saved but not yet sent, providing an overview of unsent messages."""
        DRAFTS_CREATE = "gmail_users_drafts_create"
        """Creates a new email draft in the user's Gmail account. This draft is labeled as 'DRAFT' and can be edited or sent later. It allows users to save a message they are composing without sending it immediately."""
        DRAFTS_SEND = "gmail_users_drafts_send"
        """Sends the existing draft to the specified recipients. This endpoint finalizes the draft and delivers it to the email addresses listed in the 'To', 'Cc', and 'Bcc' fields."""
        DRAFTS_DELETE = "gmail_users_drafts_delete"
        """Permanently deletes the specified draft from the user's Gmail account. This action cannot be undone."""
        DRAFTS_GET = "gmail_users_drafts_get"
        """Retrieves the details of a specific email draft by its ID. This includes information such as the draft's subject, recipients, and content."""
        DRAFTS_UPDATE = "gmail_users_drafts_update"
        """Updates the content of an existing email draft. This endpoint replaces the current draft content with new information, allowing for modifications before sending."""

        HISTORY_LIST = "gmail_users_history_list"
        """Retrieve a chronological list of changes made to the user's Gmail account. This includes modifications to messages, labels, and other mailbox activities, providing a history of actions."""

        LABELS_LIST = "gmail_users_labels_list"
        """Retrieve a list of all labels associated with the user's Gmail account. Labels help organize emails and can be used to categorize messages for easier management."""
        LABELS_CREATE = "gmail_users_labels_create"
        """Create a new label in the user's Gmail account. Labels are used to categorize and organize emails, making it easier to manage and find messages."""
        LABELS_DELETE = "gmail_users_labels_delete"
        """Permanently delete a specific label from the user's Gmail account. This action removes the label from all messages and threads it was applied to."""
        LABELS_GET = "gmail_users_labels_get"
        """Retrieve the details of a specific label by its ID. This includes information such as the label's name and its associated settings."""
        LABELS_PATCH = "gmail_users_labels_patch"
        """Partially update the specified label. This method supports patch semantics."""
        LABELS_UPDATE = "gmail_users_labels_update"
        """Updates the specified label. This method replaces the current label settings with the new values provided."""

        MESSAGES_LIST = "gmail_users_messages_list"
        """Retrieve a list of messages in the user's mailbox. This endpoint allows you to access all messages, including those in the trash, providing a comprehensive view of the user's email history."""
        MESSAGES_INSERT = "gmail_users_messages_insert"
        """Imports a message into only this user's mailbox, with standard email delivery scanning and classification similar to receiving via SMTP. This method doesn't perform SPF checks, so it might not work for some spam messages, such as those attempting to perform domain spoofing. This method does not send a message."""
        MESSAGES_BATCH_DELETE = "gmail_users_messages_batchDelete"
        """Deletes many messages by message ID. Provides no guarantees that messages were not already deleted or even existed at all."""
        MESSAGES_BATCH_MODIFY = "gmail_users_messages_batchModify"
        """Modifies the labels on the specified messages."""
        MESSAGES_IMPORT = "gmail_users_messages_import"
        """Directly inserts a message into only this user's mailbox similar to `IMAP APPEND`, bypassing most scanning and classification. Does not send a message."""
        MESSAGES_SEND = "gmail_users_messages_send"
        """Sends the specified message to the recipients in the `To`, `Cc`, and `Bcc` headers. For example usage, see [Sending email](https://developers.google.com/gmail/api/guides/sending)."""
        MESSAGES_DELETE = "gmail_users_messages_delete"
        """Immediately and permanently deletes the specified message. This operation cannot be undone."""
        MESSAGES_GET = "gmail_users_messages_get"
        """Gets the specified message."""
        MESSAGES_MODIFY = "gmail_users_messages_modify"
        """Modifies the labels on the specified message."""
        MESSAGES_TRASH = "gmail_users_messages_trash"
        """Moves the specified message to the trash."""
        MESSAGES_UNTRASH = "gmail_users_messages_untrash"
        """Removes the specified message from the trash."""
        MESSAGES_ATTACHMENTS_GET = "gmail_users_messages_attachments_get"
        """Gets the specified message attachment."""

        GET_PROFILE = "gmail_users_getProfile"
        """Gets the current user's Gmail profile."""

        SETTINGS_GET_AUTO_FORWARDING = "gmail_users_settings_getAutoForwarding"
        """Gets the auto-forwarding setting for the specified account."""
        SETTINGS_UPDATE_AUTO_FORWARDING = "gmail_users_settings_updateAutoForwarding"
        """Updates the auto-forwarding setting for the specified account."""

        SETTINGS_GET_VACATION = "gmail_users_settings_getVacation"
        """Retrieve the current vacation responder settings for a Gmail account.
        The vacation responder automatically replies to incoming emails with a specified
        message when enabled."""
        SETTINGS_UPDATE_VACATION = "gmail_users_settings_updateVacation"
        """Update the vacation responder settings for a Gmail account. This
        includes setting the message, start and end dates, and whether the responder
        is active."""

        STOP = "gmail_users_stop"
        """Stop receiving push notifications for the given user mailbox."""

        THREADS_LIST = "gmail_users_threads_list"
        """Lists the threads in the user's mailbox."""
        THREADS_DELETE = "gmail_users_threads_delete"
        """Immediately and permanently deletes the specified thread. Any message that belongs to the thread is also deleted. This operation cannot be undone. Prefer `threads.trash` instead."""
        THREADS_GET = "gmail_users_threads_get"
        """Gets the specified thread."""
        THREADS_MODIFY = "gmail_users_threads_modify"
        """Modifies the labels on the specified thread. This applies to all messages in the thread."""
        THREADS_TRASH = "gmail_users_threads_trash"
        """Moves the specified thread to the trash. Any message that belongs to the thread is also moved to the trash."""
        THREADS_UNTRASH = "gmail_users_threads_untrash"
        """Removes the specified thread from the trash. Any message that belongs to the thread is also removed from the trash."""

        WATCH = "gmail_users_watch"
        """Set up or update push notification watch for the given user mailbox."""
        
    class Shopify(str, Enum):
        def get_api_service(self) -> APIService:
            return APIService.SHOPIFY
        
        GET_PRODUCTS = "shopify_product_get"
        """Retrieve a list of all products in the user's Shopify account."""
        UPDATE_PRODUCT = "shopify_product_update"
        """Update a specific product in the user's Shopify account."""

ActionType = Union[Action.Airtable, Action.Gmail]

