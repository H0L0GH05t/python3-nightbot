from . import oauth2
from .bind import bind_method
from .models import MediaShortcode, Media, User, Location, Tag, Comment, Relationship

CUSTOM_CMD_PARAMETERS = ["coolDown", "message", "name", "userLevel"]
DEFAULT_CMD_PARAMETERS = ["coolDown", "enabled", "userLevel"]
REGULARS_PARAMETERS = ["limit", "offset", "q"]

SUPPORTED_FORMATS = ['json']


class NightbotAPI(oauth2.OAuth2API):

    host = "api.nightbot.tv"
    base_path = "/1"
    access_token_field = "access_token"
    authorize_url = "https://api.nightbot.tv/oauth2/authorize"
    access_token_url = "https://api.nightbot.tv/oauth2/token"
    protocol = "https"
    api_name = "Nightbot"
    x_ratelimit_remaining  = None
    x_ratelimit = None

    def __init__(self, *args, **kwargs):
        format = kwargs.get('format', 'json')
        if format in SUPPORTED_FORMATS:
            self.format = format
        else:
            raise Exception("Unsupported format")
        super(NightbotAPI, self).__init__(**kwargs)

    # Scope: channel
    # https://api-docs.nightbot.tv/#channel-resource
    get_chanel = bind_method(
                path="/channel",
                accepts_parameters=[],
                response_type="entry",
                root_class=Channel)
    # Get the current API user's channel information

    join_channel = bind_method(
                path="/channel/join",
                method="POST",
                accepts_parameters=[],
                response_type="empty") #Returns status
    # Makes Nightbot join (enter) the current user's chanel

    part_channel = bind_method(
                path="/channel/part",
                method="POST",
                accepts_parameters=[],
                response_type="empty") #Returns status
    # Makes Nightbot part (leave) the current user’s channel


    #Scope: channel_send
    send_channel_msg = bind_method(
                path="/channel/send",
                method="POST",
                accepts_parameters=['message'], # Required. Max len: 400 char
                response_type="empty") #Returns status
    # Makes Nightbot send a message to the channel
    # Note: rate limited to 1 request per 5 seconds

    # Scope commands
    # https://api-docs.nightbot.tv/#commands
    get_custom_cmds = bind_method(
                path="/commands",
                accepts_parameters=[],
                response_type="list",
                root_class=Command)
    # Gets the current API user’s custom commands list

    add_custom_cmd = bind_method(
                path="/commands",
                method="POST",
                accepts_parameters=CUSTOM_CMD_PARAMETERS,
                response_type="entry",
                root_class=Command)
    # Adds a new custom command to the current user’s channel
    # For params see: https://api-docs.nightbot.tv/#add-new-custom-command

    get_custom_cmd_by_id = bind_method(
                path="/commands/{cmd_id}",
                accepts_parameters=['cmd_id'],
                response_type="entry",
                root_class=Command)
    # Looks up a custom command by id

    edit_custom_cmd_by_id = bind_method(
                path="/commands/{cmd_id}",
                method="PUT",
                accepts_parameters=CUSTOM_CMD_PARAMETERS + ['media_id'],
                response_type="entry",
                root_class=Command)
    # Edits a custom command by its id.

    del_custom_cmd_by_id = bind_method(
                path="/commands/{cmd_id}",
                method="DELETE",
                accepts_parameters=['media_id'],
                response_type="empty", #Returns status
                root_class=Command)
    # Deletes a custom command by id

    #Scope: commands_default
    get_default_cmds = bind_method(
                path="/commands/default",
                accepts_parameters=[],
                response_type="list",
                root_class=Command)
    # Gets the current API user’s default commands list

    get_default_cmd_by_name = bind_method(
                path="/commands/default/{name}",
                accepts_parameters=['name'],
                response_type="empty",
                root_class=Command)
    # Looks up a default command by name

    edit_default_cmd_by_name = bind_method(
                path="/commands/default/{name}",
                method="PUT",
                accepts_parameters=DEFAULT_CMD_PARAMETERS + ['name'],
                response_type="empty",
                root_class=Command)
    # Edits a default command by its name.

    #https://api-docs.nightbot.tv/#me
    get_current_user = bind_method(
                path="/me",
                response_type="entry",
                root_class=User)
    # Gets the current API user’s information

    #https://api-docs.nightbot.tv/#regulars
    #Scope: regulars
    get_regulars = bind_method(
                path="/regulars",
                accepts_parameters=REGULARS_PARAMETERS,
                response_type="entry",
                root_class=User)
    # Gets the current API user’s regulars list

    add_regular = bind_method(
                path="/regulars",
                accepts_parameters=["name"],
                response_type="entry",
                method="POST",
                root_class=User)
    # Adds a new regular to the current user’s channel

    get_regular_by_id = bind_method(
                path="/regulars/{id}",
                accepts_parameters=["id"],
                response_type="entry",
                root_class=User)
    # Looks up a regular by id

    delete_regular_by_id = bind_method(
                path="/regulars/{id}",
                accepts_parameters=["id"],
                root_class=User,
                method="DELETE",
                response_type="empty")
    # Deletes a regular by id

    location_recent_media = bind_method(
                path="/locations/{location_id}/media/recent/",
                accepts_parameters=MEDIA_ACCEPT_PARAMETERS + ['location_id'],
                root_class=Media,
                paginates=True)

    location_search = bind_method(
                path="/locations/search",
                accepts_parameters=SEARCH_ACCEPT_PARAMETERS + ['lat', 'lng', 'foursquare_id', 'foursquare_v2_id'],
                root_class=Location)

    location = bind_method(
                path="/locations/{location_id}",
                accepts_parameters=["location_id"],
                root_class=Location,
                response_type="entry")

    geography_recent_media = bind_method(
                path="/geographies/{geography_id}/media/recent/",
                accepts_parameters=MEDIA_ACCEPT_PARAMETERS + ["geography_id"],
                root_class=Media,
                paginates=True)

    tag_recent_media = bind_method(
                path="/tags/{tag_name}/media/recent/",
                accepts_parameters=['count', 'max_tag_id', 'tag_name'],
                root_class=Media,
                paginates=True)

    tag_search = bind_method(
                path="/tags/search",
                accepts_parameters=SEARCH_ACCEPT_PARAMETERS,
                root_class=Tag,
                paginates=True)

    tag = bind_method(
                path="/tags/{tag_name}",
                accepts_parameters=["tag_name"],
                root_class=Tag,
                response_type="entry")

    user_incoming_requests = bind_method(
                path="/users/self/requested-by",
                root_class=User)

    change_user_relationship = bind_method(
                method="POST",
                path="/users/{user_id}/relationship",
                signature=True,
                root_class=Relationship,
                accepts_parameters=["user_id", "action"],
                paginates=True,
                requires_target_user=True,
                response_type="entry")

    user_relationship = bind_method(
                method="GET",
                path="/users/{user_id}/relationship",
                root_class=Relationship,
                accepts_parameters=["user_id"],
                paginates=False,
                requires_target_user=True,
                response_type="entry")

    def _make_relationship_shortcut(action):
        def _inner(self, *args, **kwargs):
            return self.change_user_relationship(user_id=kwargs.get("user_id"),
                                                 action=action)
        return _inner

    follow_user = _make_relationship_shortcut('follow')
    unfollow_user = _make_relationship_shortcut('unfollow')
    block_user = _make_relationship_shortcut('block')
    unblock_user = _make_relationship_shortcut('unblock')
    approve_user_request = _make_relationship_shortcut('approve')
    ignore_user_request = _make_relationship_shortcut('ignore')

    def _make_subscription_action(method, include=None, exclude=None):
        accepts_parameters = ["object",
                              "aspect",
                              "object_id",  # Optional if subscribing to all users
                              "callback_url",
                              "lat",  # Geography
                              "lng",  # Geography
                              "radius",  # Geography
                              "verify_token"]

        if include:
            accepts_parameters.extend(include)
        if exclude:
            accepts_parameters = [x for x in accepts_parameters if x not in exclude]
        signature = False if method == 'GET' else True
        return bind_method(
            path="/subscriptions",
            method=method,
            accepts_parameters=accepts_parameters,
            include_secret=True,
            objectify_response=False,
            signature=signature,
        )

    create_subscription = _make_subscription_action('POST')
    list_subscriptions = _make_subscription_action('GET')
    delete_subscriptions = _make_subscription_action('DELETE', exclude=['object_id'], include=['id'])
