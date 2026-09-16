# Interactions API Reference

> Sumber: https://discordpy.readthedocs.io/en/latest/interactions/api.html

# Interactions API Reference¶

The following section outlines the API of interactions, as implemented by the library.

For documentation about the rest of the library, check [API Reference](../api.html).

## Models¶

Similar to [Discord Models](../api.html#discord-api-models), these are not meant to be constructed by the user.

### Interaction¶

Attributes

  * app_permissions
  * application_id
  * channel
  * channel_id
  * client
  * command
  * command_failed
  * command_id
  * context
  * created_at
  * custom_id
  * data
  * entitlement_sku_ids
  * entitlements
  * expires_at
  * extras
  * filesize_limit
  * followup
  * guild
  * guild_id
  * guild_locale
  * id
  * locale
  * message
  * namespace
  * permissions
  * response
  * token
  * type
  * user



Methods

  * asyncdelete_original_response
  * asyncedit_original_response
  * defis_expired
  * defis_guild_integration
  * defis_user_integration
  * asyncoriginal_response
  * asynctranslate



_class _discord.Interaction¶
    

Represents a Discord interaction.

An interaction happens when a user does an action that needs to be notified. Current examples are slash commands and components.

New in version 2.0.

id¶
    

The interaction’s ID.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

type¶
    

The interaction type.

Type
    

`InteractionType`

guild_id¶
    

The guild ID the interaction was sent from.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

channel¶
    

The channel the interaction was sent from.

Note that due to a Discord limitation, if sent from a DM channel [`recipient`](../api.html#discord.DMChannel.recipient "discord.DMChannel.recipient") is `None`.

Type
    

Optional[Union[[`abc.GuildChannel`](../api.html#discord.abc.GuildChannel "discord.abc.GuildChannel"), [`abc.PrivateChannel`](../api.html#discord.abc.PrivateChannel "discord.abc.PrivateChannel"), [`Thread`](../api.html#discord.Thread "discord.Thread")]]

entitlement_sku_ids¶
    

The entitlement SKU IDs that the user has.

Type
    

List[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

entitlements¶
    

The entitlements that the guild or user has.

Type
    

List[[`Entitlement`](../api.html#discord.Entitlement "discord.Entitlement")]

application_id¶
    

The application ID that the interaction was for.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

user¶
    

The user or member that sent the interaction.

Type
    

Union[[`User`](../api.html#discord.User "discord.User"), [`Member`](../api.html#discord.Member "discord.Member")]

message¶
    

The message that sent this interaction.

This is only available for `InteractionType.component` interactions.

Type
    

Optional[[`Message`](../api.html#discord.Message "discord.Message")]

token¶
    

The token to continue the interaction. These are valid for 15 minutes.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

data¶
    

The raw interaction data.

Type
    

[`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")

locale¶
    

The locale of the user invoking the interaction.

Type
    

[`Locale`](../api.html#discord.Locale "discord.Locale")

guild_locale¶
    

The preferred locale of the guild the interaction was sent from, if any.

Type
    

Optional[[`Locale`](../api.html#discord.Locale "discord.Locale")]

extras¶
    

A dictionary that can be used to store extraneous data for use during interaction processing. The library will not touch any values or keys within this dictionary.

Type
    

[`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")

command_failed¶
    

Whether the command associated with this interaction failed to execute. This includes checks and execution.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

context¶
    

The context of the interaction.

New in version 2.4.

Type
    

`AppCommandContext`

filesize_limit¶
    

The maximum number of bytes a file can have when responding to this interaction.

New in version 2.6.

Type
    

[int](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _client¶
    

The client that is handling this interaction.

Note that [`AutoShardedClient`](../api.html#discord.AutoShardedClient "discord.AutoShardedClient"), [`Bot`](../ext/commands/api.html#discord.ext.commands.Bot "discord.ext.commands.Bot"), and [`AutoShardedBot`](../ext/commands/api.html#discord.ext.commands.AutoShardedBot "discord.ext.commands.AutoShardedBot") are all subclasses of client.

Type
    

[`Client`](../api.html#discord.Client "discord.Client")

_property _guild¶
    

The guild the interaction was sent from.

Type
    

Optional[[`Guild`](../api.html#discord.Guild "discord.Guild")]

_property _channel_id¶
    

The ID of the channel the interaction was sent from.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _permissions¶
    

The resolved permissions of the member in the channel, including overwrites.

In a non-guild context where this doesn’t apply, an empty permissions object is returned.

Type
    

[`Permissions`](../api.html#discord.Permissions "discord.Permissions")

_property _app_permissions¶
    

The resolved permissions of the application or the bot, including overwrites.

Type
    

[`Permissions`](../api.html#discord.Permissions "discord.Permissions")

namespace¶
    

The resolved namespace for this interaction.

If the interaction is not an application command related interaction or the client does not have a tree attached to it then this returns an empty namespace.

Type
    

`app_commands.Namespace`

command¶
    

The command being called from this interaction.

If the interaction is not an application command related interaction or the command is not found in the client’s attached tree then `None` is returned.

Type
    

Optional[Union[`app_commands.Command`, `app_commands.ContextMenu`]]

command_id¶
    

The ID of the command that triggered this interaction.

Only applicable if `type` is one of, `InteractionType.application_command` or `InteractionType.autocomplete`.

New in version 2.7.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

response¶
    

Returns an object responsible for handling responding to the interaction.

A response can only be done once. If secondary messages need to be sent, consider using `followup` instead.

Type
    

`InteractionResponse`

followup¶
    

Returns the follow up webhook for follow up interactions.

Type
    

[`Webhook`](../api.html#discord.Webhook "discord.Webhook")

_property _created_at¶
    

When the interaction was created.

Type
    

[`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "\(in Python v3.14\)")

_property _expires_at¶
    

When the interaction expires.

Type
    

[`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "\(in Python v3.14\)")

custom_id¶
    

The custom ID of the component that triggered this interaction.

Only applicable if `type` is one of, `InteractionType.component` or `InteractionType.modal_submit`.

New in version 2.7.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

is_expired()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Returns `True` if the interaction is expired.

is_guild_integration()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Returns `True` if the interaction is a guild integration.

New in version 2.4.

is_user_integration()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Returns `True` if the interaction is a user integration.

New in version 2.4.

_await _original_response()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Fetches the original interaction response message associated with the interaction.

If the interaction response was a newly created message (i.e. through `InteractionResponse.send_message()` or `InteractionResponse.defer()`, where `thinking` is `True`) then this returns the message that was sent using that response. Otherwise, this returns the message that triggered the interaction (i.e. through a component).

Repeated calls to this will return a cached value.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Fetching the original response message failed.

  * [**ClientException**](../api.html#discord.ClientException "discord.ClientException") – The channel for the message could not be resolved.

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The interaction response message does not exist.



Returns
    

The original interaction response message.

Return type
    

InteractionMessage

_await _edit_original_response(_*_ , _content =..._, _embeds =..._, _embed =..._, _attachments =..._, _view =..._, _allowed_mentions =None_, _poll =..._)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Edits the original interaction response message.

This is a lower level interface to `InteractionMessage.edit()` in case you do not want to fetch the message and save an HTTP request.

This method is also the only way to edit the original message if the message sent was ephemeral.

Parameters
    

  * **content** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The content to edit the message with or `None` to clear it.

  * **embeds** (List[[`Embed`](../api.html#discord.Embed "discord.Embed")]) – A list of embeds to edit the message with.

  * **embed** (Optional[[`Embed`](../api.html#discord.Embed "discord.Embed")]) – The embed to edit the message with. `None` suppresses the embeds. This should not be mixed with the `embeds` parameter.

  * **attachments** (List[Union[[`Attachment`](../api.html#discord.Attachment "discord.Attachment"), [`File`](../api.html#discord.File "discord.File")]]) – 

A list of attachments to keep in the message as well as new files to upload. If `[]` is passed then all attachments are removed.

Note

New files will always appear after current attachments.

  * **allowed_mentions** ([`AllowedMentions`](../api.html#discord.AllowedMentions "discord.AllowedMentions")) – Controls the mentions being processed in this message. See [`abc.Messageable.send()`](../api.html#discord.abc.Messageable.send "discord.abc.Messageable.send") for more information.

  * **view** (Optional[Union[`View`, `LayoutView`]]) – 

The updated view to update this message with. If `None` is passed then the view is removed.

Note

If you want to update the message to have a `LayoutView`, you must explicitly set the `content`, `embed`, `embeds`, and `attachments` parameters to `None` if the previous message had any.

  * **poll** ([`Poll`](../api.html#discord.Poll "discord.Poll")) – 

The poll to create when editing the message.

New in version 2.5.

Note

This is only accepted when the response type is `InteractionResponseType.deferred_channel_message`.



Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Editing the message failed.

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The interaction response message does not exist.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – Edited a message that is not yours.

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – You specified both `embed` and `embeds`

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – The length of `embeds` was invalid.



Returns
    

The newly edited message.

Return type
    

`InteractionMessage`

_await _delete_original_response()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Deletes the original interaction response message.

This is a lower level interface to `InteractionMessage.delete()` in case you do not want to fetch the message and save an HTTP request.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Deleting the message failed.

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The interaction response message does not exist or has already been deleted.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – Deleted a message that is not yours.




_await _translate(_string_ , _*_ , _locale =..._, _data =..._)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Translates a string using the set `Translator`.

New in version 2.1.

Parameters
    

  * **string** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The string to translate. `locale_str` can be used to add more context, information, or any metadata necessary.

  * **locale** ([`Locale`](../api.html#discord.Locale "discord.Locale")) – The locale to use, this is handy if you want the translation for a specific locale. Defaults to the user’s `locale`.

  * **data** (_Any_) – The extraneous data that is being translated. If not specified, either `command` or `message` will be passed, depending on which is available in the context.



Returns
    

The translated string, or `None` if a translator was not set.

Return type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

### InteractionResponse¶

Attributes

  * type



Methods

  * asyncautocomplete
  * asyncdefer
  * asyncedit_message
  * defis_done
  * asynclaunch_activity
  * asyncpong
  * asyncsend_message
  * asyncsend_modal



_class _discord.InteractionResponse¶
    

Represents a Discord interaction response.

This type can be accessed through `Interaction.response`.

New in version 2.0.

is_done()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Indicates whether an interaction response has been done before.

An interaction can only be responded to once.

_property _type¶
    

The type of response that was sent, `None` if response is not done.

Type
    

`InteractionResponseType`

_await _defer(_*_ , _ephemeral =False_, _thinking =False_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Defers the interaction response.

This is typically used when the interaction is acknowledged and a secondary action will be done later.

This is only supported with the following interaction types:

  * `InteractionType.application_command`

  * `InteractionType.component`

  * `InteractionType.modal_submit`




Changed in version 2.5: This now returns a `InteractionCallbackResponse` instance.

Parameters
    

  * **ephemeral** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Indicates whether the deferred message will eventually be ephemeral. This only applies to `InteractionType.application_command` interactions, or if `thinking` is `True`.

  * **thinking** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Indicates whether the deferred type should be `InteractionResponseType.deferred_channel_message` instead of the default `InteractionResponseType.deferred_message_update` if both are valid. In UI terms, this is represented as if the bot is thinking of a response. It is your responsibility to eventually send a followup message via `Interaction.followup` to make this thinking state go away. Application commands (AKA Slash commands) cannot use `InteractionResponseType.deferred_message_update`.



Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Deferring the interaction failed.

  * [**InteractionResponded**](../api.html#discord.InteractionResponded "discord.InteractionResponded") – This interaction has already been responded to before.



Returns
    

The interaction callback resource, or `None`.

Return type
    

Optional[`InteractionCallbackResponse`]

_await _pong()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Pongs the ping interaction.

This should rarely be used.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Ponging the interaction failed.

  * [**InteractionResponded**](../api.html#discord.InteractionResponded "discord.InteractionResponded") – This interaction has already been responded to before.




_await _send_message(_content =None_, _*_ , _embed =..._, _embeds =..._, _file =..._, _files =..._, _view =..._, _tts =False_, _ephemeral =False_, _allowed_mentions =..._, _suppress_embeds =False_, _silent =False_, _delete_after =None_, _poll =..._)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Responds to this interaction by sending a message.

Changed in version 2.5: This now returns a `InteractionCallbackResponse` instance.

Parameters
    

  * **content** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The content of the message to send.

  * **embeds** (List[[`Embed`](../api.html#discord.Embed "discord.Embed")]) – A list of embeds to send with the content. Maximum of 10. This cannot be mixed with the `embed` parameter.

  * **embed** ([`Embed`](../api.html#discord.Embed "discord.Embed")) – The rich embed for the content to send. This cannot be mixed with `embeds` parameter.

  * **file** ([`File`](../api.html#discord.File "discord.File")) – The file to upload.

  * **files** (List[[`File`](../api.html#discord.File "discord.File")]) – A list of files to upload. Must be a maximum of 10.

  * **tts** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Indicates if the message should be sent using text-to-speech.

  * **view** (Union[`discord.ui.View`, `discord.ui.LayoutView`]) – The view to send with the message.

  * **ephemeral** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Indicates if the message should only be visible to the user who started the interaction. If a view is sent with an ephemeral message and it has no timeout set then the timeout is set to 15 minutes.

  * **allowed_mentions** ([`AllowedMentions`](../api.html#discord.AllowedMentions "discord.AllowedMentions")) – Controls the mentions being processed in this message. See [`abc.Messageable.send()`](../api.html#discord.abc.Messageable.send "discord.abc.Messageable.send") for more information.

  * **suppress_embeds** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether to suppress embeds for the message. This sends the message without any embeds if set to `True`.

  * **silent** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether to suppress push and desktop notifications for the message. This will increment the mention counter in the UI, but will not actually send a notification.

New in version 2.2.

  * **delete_after** ([`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")) – 

If provided, the number of seconds to wait in the background before deleting the message we just sent. If the deletion fails, then it is silently ignored.

New in version 2.1.

  * **poll** ([`Poll`](../api.html#discord.Poll "discord.Poll")) – 

The poll to send with this message.

New in version 2.4.



Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Sending the message failed.

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – You specified both `embed` and `embeds` or `file` and `files`.

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – The length of `embeds` was invalid.

  * [**InteractionResponded**](../api.html#discord.InteractionResponded "discord.InteractionResponded") – This interaction has already been responded to before.



Returns
    

The interaction callback data.

Return type
    

`InteractionCallbackResponse`

_await _edit_message(_*_ , _content =..._, _embed =..._, _embeds =..._, _attachments =..._, _view =..._, _allowed_mentions =..._, _delete_after =None_, _suppress_embeds =..._)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Responds to this interaction by editing the original message of a component or modal interaction.

Changed in version 2.5: This now returns a `InteractionCallbackResponse` instance.

Parameters
    

  * **content** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The new content to replace the message with. `None` removes the content.

  * **embeds** (List[[`Embed`](../api.html#discord.Embed "discord.Embed")]) – A list of embeds to edit the message with.

  * **embed** (Optional[[`Embed`](../api.html#discord.Embed "discord.Embed")]) – The embed to edit the message with. `None` suppresses the embeds. This should not be mixed with the `embeds` parameter.

  * **attachments** (List[Union[[`Attachment`](../api.html#discord.Attachment "discord.Attachment"), [`File`](../api.html#discord.File "discord.File")]]) – 

A list of attachments to keep in the message as well as new files to upload. If `[]` is passed then all attachments are removed.

Note

New files will always appear after current attachments.

  * **view** (Optional[Union[`View`, `LayoutView`]]) – 

The updated view to update this message with. If `None` is passed then the view is removed.

Note

To update the message to add a `LayoutView`, you must explicitly set the `content`, `embed`, `embeds`, and `attachments` parameters to either `None` or an empty array, as appropriate.

  * **allowed_mentions** (Optional[[`AllowedMentions`](../api.html#discord.AllowedMentions "discord.AllowedMentions")]) – Controls the mentions being processed in this message. See [`Message.edit()`](../api.html#discord.Message.edit "discord.Message.edit") for more information.

  * **delete_after** ([`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")) – 

If provided, the number of seconds to wait in the background before deleting the message we just edited. If the deletion fails, then it is silently ignored.

New in version 2.2.

  * **suppress_embeds** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether to suppress embeds for the message. This removes all the embeds if set to `True`. If set to `False` this brings the embeds back if they were suppressed. Using this parameter requires [`manage_messages`](../api.html#discord.Permissions.manage_messages "discord.Permissions.manage_messages").

New in version 2.4.



Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Editing the message failed.

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – You specified both `embed` and `embeds`.

  * [**InteractionResponded**](../api.html#discord.InteractionResponded "discord.InteractionResponded") – This interaction has already been responded to before.



Returns
    

The interaction callback data, or `None` if editing the message was not possible.

Return type
    

Optional[`InteractionCallbackResponse`]

_await _send_modal(_modal_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Responds to this interaction by sending a modal.

Changed in version 2.5: This now returns a `InteractionCallbackResponse` instance.

Parameters
    

**modal** (`Modal`) – The modal to send.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Sending the modal failed.

  * [**InteractionResponded**](../api.html#discord.InteractionResponded "discord.InteractionResponded") – This interaction has already been responded to before.



Returns
    

The interaction callback data.

Return type
    

`InteractionCallbackResponse`

_await _autocomplete(_choices_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Responds to this interaction by giving the user the choices they can use.

Parameters
    

**choices** (List[`Choice`]) – The list of new choices as the user is typing.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Sending the choices failed.

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – This interaction cannot respond with autocomplete.

  * [**InteractionResponded**](../api.html#discord.InteractionResponded "discord.InteractionResponded") – This interaction has already been responded to before.




_await _launch_activity()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Responds to this interaction by launching the activity associated with the app. Only available for apps with activities enabled.

New in version 2.6.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Launching the activity failed.

  * [**InteractionResponded**](../api.html#discord.InteractionResponded "discord.InteractionResponded") – This interaction has already been responded to before.



Returns
    

The interaction callback data.

Return type
    

`InteractionCallbackResponse`

### InteractionCallbackResponse¶

Attributes

  * activity_id
  * id
  * message_id
  * resource
  * type



Methods

  * defis_ephemeral
  * defis_thinking



_class _discord.InteractionCallbackResponse¶
    

Represents an interaction response callback.

New in version 2.5.

id¶
    

The interaction ID.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

type¶
    

The interaction callback response type.

Type
    

`InteractionResponseType`

resource¶
    

The resource that the interaction response created. If a message was sent, this will be a `InteractionMessage`. If an activity was launched this will be a `InteractionCallbackActivityInstance`. In any other case, this will be `None`.

Type
    

Optional[Union[`InteractionMessage`, `InteractionCallbackActivityInstance`]]

message_id¶
    

The message ID of the resource. Only available if the resource is a `InteractionMessage`.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

activity_id¶
    

The activity ID of the resource. Only available if the resource is a `InteractionCallbackActivityInstance`.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

is_thinking()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Whether the response was a thinking defer.

is_ephemeral()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Whether the response was ephemeral.

### InteractionCallbackActivityInstance¶

Attributes

  * id



_class _discord.InteractionCallbackActivityInstance¶
    

Represents an activity instance launched as an interaction response.

New in version 2.5.

id¶
    

The activity instance ID.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

### InteractionMessage¶

Attributes

  * clean_content
  * created_at
  * edited_at
  * interaction
  * jump_url
  * pinned_at
  * raw_channel_mentions
  * raw_mentions
  * raw_role_mentions
  * system_content
  * thread



Methods

  * asyncadd_files
  * asyncadd_reaction
  * asyncclear_reaction
  * asyncclear_reactions
  * asynccreate_thread
  * asyncdelete
  * asyncedit
  * asyncend_poll
  * asyncfetch
  * asyncfetch_thread
  * asyncforward
  * defis_forwardable
  * defis_system
  * asyncpin
  * asyncpublish
  * asyncremove_attachments
  * asyncremove_reaction
  * asyncreply
  * defto_reference
  * asyncunpin



_class _discord.InteractionMessage¶
    

Represents the original interaction response message.

This allows you to edit or delete the message associated with the interaction response. To retrieve this object see `Interaction.original_response()`.

This inherits from [`discord.Message`](../api.html#discord.Message "discord.Message") with changes to `edit()` and `delete()` to work.

New in version 2.0.

_await _add_reaction(_emoji_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Adds a reaction to the message.

The emoji may be a unicode emoji or a custom guild [`Emoji`](../api.html#discord.Emoji "discord.Emoji").

You must have [`read_message_history`](../api.html#discord.Permissions.read_message_history "discord.Permissions.read_message_history") to do this. If nobody else has reacted to the message using this emoji, [`add_reactions`](../api.html#discord.Permissions.add_reactions "discord.Permissions.add_reactions") is required.

Changed in version 2.0: `emoji` parameter is now positional-only.

Changed in version 2.0: This function will now raise [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") instead of `InvalidArgument`.

Parameters
    

**emoji** (Union[[`Emoji`](../api.html#discord.Emoji "discord.Emoji"), [`Reaction`](../api.html#discord.Reaction "discord.Reaction"), [`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The emoji to react with.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Adding the reaction failed.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have the proper permissions to react to the message.

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The emoji you specified was not found.

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The emoji parameter is invalid.




clean_content¶
    

A property that returns the content in a “cleaned up” manner. This basically means that mentions are transformed into the way the client shows them. e.g. `<#id>` will transform into `#name`.

This will also transform @everyone and @here mentions into non-mentions.

Note

This _does not_ affect markdown. If you want to escape or remove markdown then use [`utils.escape_markdown()`](../api.html#discord.utils.escape_markdown "discord.utils.escape_markdown") or [`utils.remove_markdown()`](../api.html#discord.utils.remove_markdown "discord.utils.remove_markdown") respectively, along with this function.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_await _clear_reaction(_emoji_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Clears a specific reaction from the message.

The emoji may be a unicode emoji or a custom guild [`Emoji`](../api.html#discord.Emoji "discord.Emoji").

You must have [`manage_messages`](../api.html#discord.Permissions.manage_messages "discord.Permissions.manage_messages") to do this.

New in version 1.3.

Changed in version 2.0: This function will now raise [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") instead of `InvalidArgument`.

Parameters
    

**emoji** (Union[[`Emoji`](../api.html#discord.Emoji "discord.Emoji"), [`Reaction`](../api.html#discord.Reaction "discord.Reaction"), [`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The emoji to clear.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Clearing the reaction failed.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have the proper permissions to clear the reaction.

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The emoji you specified was not found.

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The emoji parameter is invalid.




_await _clear_reactions()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Removes all the reactions from the message.

You must have [`manage_messages`](../api.html#discord.Permissions.manage_messages "discord.Permissions.manage_messages") to do this.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Removing the reactions failed.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have the proper permissions to remove all the reactions.




_await _create_thread(_*_ , _name_ , _auto_archive_duration =..._, _slowmode_delay =None_, _reason =None_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Creates a public thread from this message.

You must have [`create_public_threads`](../api.html#discord.Permissions.create_public_threads "discord.Permissions.create_public_threads") in order to create a public thread from a message.

The channel this message belongs in must be a [`TextChannel`](../api.html#discord.TextChannel "discord.TextChannel").

New in version 2.0.

Parameters
    

  * **name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The name of the thread.

  * **auto_archive_duration** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – 

The duration in minutes before a thread is automatically hidden from the channel list. If not provided, the channel’s default auto archive duration is used.

Must be one of `60`, `1440`, `4320`, or `10080`, if provided.

  * **slowmode_delay** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – Specifies the slowmode rate limit for user in this channel, in seconds. The maximum value possible is `21600`. By default no slowmode rate limit if this is `None`.

  * **reason** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The reason for creating a new thread. Shows up on the audit log.



Raises
    

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have permissions to create a thread.

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Creating the thread failed.

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – This message does not have guild info attached.



Returns
    

The created thread.

Return type
    

[`Thread`](../api.html#discord.Thread "discord.Thread")

_property _created_at¶
    

The message’s creation time in UTC.

Type
    

[`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "\(in Python v3.14\)")

_await _edit(_*_ , _content =..._, _embeds =..._, _embed =..._, _attachments =..._, _view =..._, _allowed_mentions =None_, _delete_after =None_, _poll =..._)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Edits the message.

Parameters
    

  * **content** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The content to edit the message with or `None` to clear it.

  * **embeds** (List[[`Embed`](../api.html#discord.Embed "discord.Embed")]) – A list of embeds to edit the message with.

  * **embed** (Optional[[`Embed`](../api.html#discord.Embed "discord.Embed")]) – The embed to edit the message with. `None` suppresses the embeds. This should not be mixed with the `embeds` parameter.

  * **attachments** (List[Union[[`Attachment`](../api.html#discord.Attachment "discord.Attachment"), [`File`](../api.html#discord.File "discord.File")]]) – 

A list of attachments to keep in the message as well as new files to upload. If `[]` is passed then all attachments are removed.

Note

New files will always appear after current attachments.

  * **allowed_mentions** ([`AllowedMentions`](../api.html#discord.AllowedMentions "discord.AllowedMentions")) – Controls the mentions being processed in this message. See [`abc.Messageable.send()`](../api.html#discord.abc.Messageable.send "discord.abc.Messageable.send") for more information.

  * **view** (Optional[Union[`View`, `LayoutView`]]) – 

The updated view to update this message with. If `None` is passed then the view is removed.

Note

If you want to update the message to have a `LayoutView`, you must explicitly set the `content`, `embed`, `embeds`, and `attachments` parameters to `None` if the previous message had any.

  * **delete_after** (Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]) – 

If provided, the number of seconds to wait in the background before deleting the message we just sent. If the deletion fails, then it is silently ignored.

New in version 2.2.

  * **poll** ([`Poll`](../api.html#discord.Poll "discord.Poll")) – 

The poll to create when editing the message.

New in version 2.5.

Note

This is only accepted if the interaction response’s `InteractionResponse.type` attribute is `InteractionResponseType.deferred_channel_message`.



Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Editing the message failed.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – Edited a message that is not yours.

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – You specified both `embed` and `embeds`

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – The length of `embeds` was invalid.



Returns
    

The newly edited message.

Return type
    

`InteractionMessage`

_property _edited_at¶
    

An aware UTC datetime object containing the edited time of the message.

Type
    

Optional[[`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "\(in Python v3.14\)")]

_await _end_poll()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Ends the [`Poll`](../api.html#discord.Poll "discord.Poll") attached to this message.

This can only be done if you are the message author.

If the poll was successfully ended, then it returns the updated [`Message`](../api.html#discord.Message "discord.Message").

Raises
    

[**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Ending the poll failed.

Returns
    

The updated message.

Return type
    

[`Message`](../api.html#discord.Message "discord.Message")

_await _fetch()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Fetches the partial message to a full [`Message`](../api.html#discord.Message "discord.Message").

Raises
    

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The message was not found.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have the permissions required to get a message.

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Retrieving the message failed.



Returns
    

The full message.

Return type
    

[`Message`](../api.html#discord.Message "discord.Message")

_await _fetch_thread()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Retrieves the public thread attached to this message.

Note

This method is an API call. For general usage, consider `thread` instead.

New in version 2.4.

Raises
    

  * [**InvalidData**](../api.html#discord.InvalidData "discord.InvalidData") – An unknown channel type was received from Discord or the guild the thread belongs to is not the same as the one in this object points to.

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Retrieving the thread failed.

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – There is no thread attached to this message.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have permission to fetch this channel.



Returns
    

The public thread attached to this message.

Return type
    

[`Thread`](../api.html#discord.Thread "discord.Thread")

_await _forward(_destination_ , _*_ , _fail_if_not_exists =True_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Forwards this message to a channel.

New in version 2.5.

Parameters
    

  * **destination** ([`Messageable`](../api.html#discord.abc.Messageable "discord.abc.Messageable")) – The channel to forward this message to.

  * **fail_if_not_exists** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether replying using the message reference should raise [`HTTPException`](../api.html#discord.HTTPException "discord.HTTPException") if the message no longer exists or Discord could not fetch the message.



Raises
    

[**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Forwarding the message failed.

Returns
    

The message sent to the channel.

Return type
    

[`Message`](../api.html#discord.Message "discord.Message")

_property _interaction¶
    

The interaction that this message is a response to.

New in version 2.0.

Deprecated since version 2.4: This attribute is deprecated and will be removed in a future version. Use [`interaction_metadata`](../api.html#discord.Message.interaction_metadata "discord.Message.interaction_metadata") instead.

Type
    

Optional[`MessageInteraction`]

is_forwardable()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Whether the message can be forwarded using [`Message.forward()`](../api.html#discord.Message.forward "discord.Message.forward").

A message is forwardable only if it is a basic message type and does not contain a poll, call, or activity, and is not a system message.

New in version 2.7.

is_system()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Whether the message is a system message.

A system message is a message that is constructed entirely by the Discord API in response to something.

New in version 1.3.

_property _jump_url¶
    

Returns a URL that allows the client to jump to this message.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_await _pin(_*_ , _reason =None_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Pins the message.

You must have [`pin_messages`](../api.html#discord.Permissions.pin_messages "discord.Permissions.pin_messages") to do this in a non-private channel context.

Parameters
    

**reason** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – 

The reason for pinning the message. Shows up on the audit log.

New in version 1.4.

Raises
    

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have permissions to pin the message.

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The message or channel was not found or deleted.

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Pinning the message failed, probably due to the channel having more than 250 pinned messages.




_property _pinned_at¶
    

An aware UTC datetime object containing the time when the message was pinned.

Note

This is only set for messages that are returned by [`abc.Messageable.pins()`](../api.html#discord.abc.Messageable.pins "discord.abc.Messageable.pins").

New in version 2.6.

Type
    

Optional[[`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "\(in Python v3.14\)")]

_await _publish()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Publishes this message to the channel’s followers.

The message must have been sent in a news channel. You must have [`send_messages`](../api.html#discord.Permissions.send_messages "discord.Permissions.send_messages") to do this.

If the message is not your own then [`manage_messages`](../api.html#discord.Permissions.manage_messages "discord.Permissions.manage_messages") is also needed.

Raises
    

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have the proper permissions to publish this message or the channel is not a news channel.

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Publishing the message failed.




raw_channel_mentions¶
    

A property that returns an array of channel IDs matched with the syntax of `<#channel_id>` in the message content.

Type
    

List[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

raw_mentions¶
    

A property that returns an array of user IDs matched with the syntax of `<@user_id>` in the message content.

This allows you to receive the user IDs of mentioned users even in a private message context.

Type
    

List[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

raw_role_mentions¶
    

A property that returns an array of role IDs matched with the syntax of `<@&role_id>` in the message content.

Type
    

List[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_await _remove_reaction(_emoji_ , _member_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Remove a reaction by the member from the message.

The emoji may be a unicode emoji or a custom guild [`Emoji`](../api.html#discord.Emoji "discord.Emoji").

If the reaction is not your own (i.e. `member` parameter is not you) then [`manage_messages`](../api.html#discord.Permissions.manage_messages "discord.Permissions.manage_messages") is needed.

The `member` parameter must represent a member and meet the [`abc.Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake") abc.

Changed in version 2.0: This function will now raise [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") instead of `InvalidArgument`.

Parameters
    

  * **emoji** (Union[[`Emoji`](../api.html#discord.Emoji "discord.Emoji"), [`Reaction`](../api.html#discord.Reaction "discord.Reaction"), [`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The emoji to remove.

  * **member** ([`abc.Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")) – The member for which to remove the reaction.



Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Removing the reaction failed.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have the proper permissions to remove the reaction.

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The member or emoji you specified was not found.

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The emoji parameter is invalid.




_await _reply(_content =None_, _** kwargs_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A shortcut method to [`abc.Messageable.send()`](../api.html#discord.abc.Messageable.send "discord.abc.Messageable.send") to reply to the [`Message`](../api.html#discord.Message "discord.Message").

New in version 1.6.

Changed in version 2.0: This function will now raise [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") or [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") instead of `InvalidArgument`.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Sending the message failed.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have the proper permissions to send the message.

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – The `files` list is not of the appropriate size

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – You specified both `file` and `files`.



Returns
    

The message that was sent.

Return type
    

[`Message`](../api.html#discord.Message "discord.Message")

system_content¶
    

A property that returns the content that is rendered regardless of the [`Message.type`](../api.html#discord.Message.type "discord.Message.type").

In the case of [`MessageType.default`](../api.html#discord.MessageType.default "discord.MessageType.default") and [`MessageType.reply`](../api.html#discord.MessageType.reply "discord.MessageType.reply"), this just returns the regular [`Message.content`](../api.html#discord.Message.content "discord.Message.content"). Otherwise this returns an English message denoting the contents of the system message.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _thread¶
    

The public thread created from this message, if it exists.

Note

For messages received via the gateway this does not retrieve archived threads, as they are not retained in the internal cache. Use `fetch_thread()` instead.

New in version 2.4.

Type
    

Optional[[`Thread`](../api.html#discord.Thread "discord.Thread")]

to_reference(_*_ , _fail_if_not_exists=True_ , _type= <MessageReferenceType.default: 0>_)¶
    

Creates a [`MessageReference`](../api.html#discord.MessageReference "discord.MessageReference") from the current message.

New in version 1.6.

Parameters
    

  * **fail_if_not_exists** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether the referenced message should raise [`HTTPException`](../api.html#discord.HTTPException "discord.HTTPException") if the message no longer exists or Discord could not fetch the message.

New in version 1.7.

  * **type** ([`MessageReferenceType`](../api.html#discord.MessageReferenceType "discord.MessageReferenceType")) – 

The type of message reference.

New in version 2.5.



Returns
    

The reference to this message.

Return type
    

[`MessageReference`](../api.html#discord.MessageReference "discord.MessageReference")

_await _unpin(_*_ , _reason =None_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Unpins the message.

You must have [`pin_messages`](../api.html#discord.Permissions.pin_messages "discord.Permissions.pin_messages") to do this in a non-private channel context.

Parameters
    

**reason** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – 

The reason for unpinning the message. Shows up on the audit log.

New in version 1.4.

Raises
    

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have permissions to unpin the message.

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The message or channel was not found or deleted.

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Unpinning the message failed.




_await _add_files(_* files_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Adds new files to the end of the message attachments.

New in version 2.0.

Parameters
    

***files** ([`File`](../api.html#discord.File "discord.File")) – New files to add to the message.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Editing the message failed.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – Tried to edit a message that isn’t yours.



Returns
    

The newly edited message.

Return type
    

`InteractionMessage`

_await _remove_attachments(_* attachments_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Removes attachments from the message.

New in version 2.0.

Parameters
    

***attachments** ([`Attachment`](../api.html#discord.Attachment "discord.Attachment")) – Attachments to remove from the message.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Editing the message failed.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – Tried to edit a message that isn’t yours.



Returns
    

The newly edited message.

Return type
    

`InteractionMessage`

_await _delete(_*_ , _delay =None_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Deletes the message.

Parameters
    

**delay** (Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]) – If provided, the number of seconds to wait before deleting the message. The waiting is done in the background and deletion failures are ignored.

Raises
    

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have proper permissions to delete the message.

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The message was deleted already.

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Deleting the message failed.




### MessageInteraction¶

Attributes

  * created_at
  * id
  * name
  * type
  * user



_class _discord.MessageInteraction¶
    

Represents the interaction that a [`Message`](../api.html#discord.Message "discord.Message") is a response to.

New in version 2.0.

x == y
    

Checks if two message interactions are equal.

x != y
    

Checks if two message interactions are not equal.

hash(x)
    

Returns the message interaction’s hash.

id¶
    

The interaction ID.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

type¶
    

The interaction type.

Type
    

`InteractionType`

name¶
    

The name of the interaction.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

user¶
    

The user or member that invoked the interaction.

Type
    

Union[[`User`](../api.html#discord.User "discord.User"), [`Member`](../api.html#discord.Member "discord.Member")]

_property _created_at¶
    

The interaction’s creation time in UTC.

Type
    

[`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "\(in Python v3.14\)")

### MessageInteractionMetadata¶

Attributes

  * created_at
  * id
  * interacted_message
  * interacted_message_id
  * modal_interaction
  * original_response_message
  * original_response_message_id
  * target_message
  * target_message_id
  * target_user
  * type
  * user



Methods

  * defis_guild_integration
  * defis_user_integration



_class _discord.MessageInteractionMetadata¶
    

Represents the interaction metadata of a [`Message`](../api.html#discord.Message "discord.Message") if it was sent in response to an interaction.

New in version 2.4.

x == y
    

Checks if two message interactions are equal.

x != y
    

Checks if two message interactions are not equal.

hash(x)
    

Returns the message interaction’s hash.

id¶
    

The interaction ID.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

type¶
    

The interaction type.

Type
    

`InteractionType`

user¶
    

The user that invoked the interaction.

Type
    

[`User`](../api.html#discord.User "discord.User")

original_response_message_id¶
    

The ID of the original response message if the message is a follow-up.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

interacted_message_id¶
    

The ID of the message that contains the interactive components, if applicable.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

modal_interaction¶
    

The metadata of the modal submit interaction that triggered this interaction, if applicable.

Type
    

Optional[`MessageInteractionMetadata`]

target_user¶
    

The user the command was run on, only applicable to user context menus.

New in version 2.5.

Type
    

Optional[[`User`](../api.html#discord.User "discord.User")]

target_message_id¶
    

The ID of the message the command was run on, only applicable to message context menus.

New in version 2.5.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _created_at¶
    

The interaction’s creation time in UTC.

Type
    

[`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "\(in Python v3.14\)")

_property _original_response_message¶
    

The original response message if the message is a follow-up and is found in cache.

Type
    

Optional[[`Message`](../api.html#discord.Message "discord.Message")]

_property _interacted_message¶
    

The message that contains the interactive components, if applicable and is found in cache.

Type
    

Optional[[`Message`](../api.html#discord.Message "discord.Message")]

_property _target_message¶
    

The target message, if applicable and is found in cache.

New in version 2.5.

Type
    

Optional[[`Message`](../api.html#discord.Message "discord.Message")]

is_guild_integration()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Returns `True` if the interaction is a guild integration.

is_user_integration()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Returns `True` if the interaction is a user integration.

### Component¶

Attributes

  * type



_class _discord.Component¶
    

Represents a Discord Bot UI Kit Component.

The components supported by Discord are:

  * `ActionRow`

  * `Button`

  * `SelectMenu`

  * `TextInput`

  * `SectionComponent`

  * `TextDisplay`

  * `ThumbnailComponent`

  * `MediaGalleryComponent`

  * `FileComponent`

  * `SeparatorComponent`

  * `Container`

  * `LabelComponent`

  * `FileUploadComponent`




This class is abstract and cannot be instantiated.

New in version 2.0.

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### ActionRow¶

Attributes

  * children
  * id
  * type



_class _discord.ActionRow¶
    

Represents a Discord Bot UI Kit Action Row.

This is a component that holds up to 5 children components in a row.

This inherits from `Component`.

New in version 2.0.

children¶
    

The children components that this holds, if any.

Type
    

List[Union[`Button`, `SelectMenu`, `TextInput`]]

id¶
    

The ID of this component.

New in version 2.6.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### Button¶

Attributes

  * custom_id
  * disabled
  * emoji
  * id
  * label
  * sku_id
  * style
  * type
  * url



_class _discord.Button¶
    

Represents a button from the Discord Bot UI Kit.

This inherits from `Component`.

Note

The user constructible and usable type to create a button is `discord.ui.Button` not this one.

New in version 2.0.

style¶
    

The style of the button.

Type
    

`ButtonStyle`

custom_id¶
    

The ID of the button that gets received during an interaction. If this button is for a URL, it does not have a custom ID.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

url¶
    

The URL this button sends you to.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

disabled¶
    

Whether the button is disabled or not.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

label¶
    

The label of the button, if any.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

emoji¶
    

The emoji of the button, if available.

Type
    

Optional[[`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji")]

sku_id¶
    

The SKU ID this button sends you to, if available.

New in version 2.4.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

id¶
    

The ID of this component.

New in version 2.6.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### SelectMenu¶

Attributes

  * channel_types
  * custom_id
  * disabled
  * id
  * max_values
  * min_values
  * options
  * placeholder
  * required
  * type



_class _discord.SelectMenu¶
    

Represents a select menu from the Discord Bot UI Kit.

A select menu is functionally the same as a dropdown, however on mobile it renders a bit differently.

Note

The user constructible and usable type to create a select menu is `discord.ui.Select` not this one.

New in version 2.0.

type¶
    

The type of component.

Type
    

`ComponentType`

custom_id¶
    

The ID of the select menu that gets received during an interaction.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

placeholder¶
    

The placeholder text that is shown if nothing is selected, if any.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

min_values¶
    

The minimum number of items that must be chosen for this select menu. Defaults to 1 and must be between 0 and 25.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

max_values¶
    

The maximum number of items that must be chosen for this select menu. Defaults to 1 and must be between 1 and 25.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

options¶
    

A list of options that can be selected in this menu.

Type
    

List[`SelectOption`]

disabled¶
    

Whether the select is disabled or not.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

channel_types¶
    

A list of channel types that are allowed to be chosen in this select menu.

Type
    

List[[`ChannelType`](../api.html#discord.ChannelType "discord.ChannelType")]

id¶
    

The ID of this component.

New in version 2.6.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

required¶
    

Whether the select is required. Only applicable within modals.

New in version 2.6.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

### TextInput¶

Attributes

  * custom_id
  * default
  * id
  * label
  * max_length
  * min_length
  * placeholder
  * required
  * style
  * type
  * value



_class _discord.TextInput¶
    

Represents a text input from the Discord Bot UI Kit.

Note

The user constructible and usable type to create a text input is `discord.ui.TextInput` not this one.

New in version 2.0.

custom_id¶
    

The ID of the text input that gets received during an interaction.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

label¶
    

The label to display above the text input.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

style¶
    

The style of the text input.

Type
    

`TextStyle`

placeholder¶
    

The placeholder text to display when the text input is empty.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

value¶
    

The default value of the text input.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

required¶
    

Whether the text input is required.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

min_length¶
    

The minimum length of the text input.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

max_length¶
    

The maximum length of the text input.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

id¶
    

The ID of this component.

New in version 2.6.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _type¶
    

The type of component.

Type
    

`ComponentType`

_property _default¶
    

The default value of the text input.

This is an alias to `value`.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

### LabelComponent¶

Attributes

  * component
  * description
  * id
  * label
  * type



_class _discord.LabelComponent¶
    

Represents a label component from the Discord Bot UI Kit.

This inherits from `Component`.

Note

The user constructible and usable type for creating a label is `discord.ui.Label` not this one.

New in version 2.6.

label¶
    

The label text to display.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

description¶
    

The description text to display below the label, if any.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

component¶
    

The component that this label is associated with.

Type
    

`Component`

id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### SectionComponent¶

Attributes

  * accessory
  * children
  * id
  * type



_class _discord.SectionComponent¶
    

Represents a section from the Discord Bot UI Kit.

This inherits from `Component`.

Note

The user constructible and usable type to create a section is `discord.ui.Section` not this one.

New in version 2.6.

children¶
    

The components on this section.

Type
    

List[`TextDisplay`]

accessory¶
    

The section accessory.

Type
    

`Component`

id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### ThumbnailComponent¶

Attributes

  * description
  * id
  * media
  * spoiler
  * type



_class _discord.ThumbnailComponent¶
    

Represents a Thumbnail from the Discord Bot UI Kit.

This inherits from `Component`.

Note

The user constructible and usable type to create a thumbnail is `discord.ui.Thumbnail` not this one.

New in version 2.6.

media¶
    

The media for this thumbnail.

Type
    

`UnfurledMediaItem`

description¶
    

The description shown within this thumbnail.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

spoiler¶
    

Whether this thumbnail is flagged as a spoiler.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### TextDisplay¶

Attributes

  * content
  * id
  * type



_class _discord.TextDisplay¶
    

Represents a text display from the Discord Bot UI Kit.

This inherits from `Component`.

Note

The user constructible and usable type to create a text display is `discord.ui.TextDisplay` not this one.

New in version 2.6.

content¶
    

The content that this display shows.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### MediaGalleryComponent¶

Attributes

  * id
  * items
  * type



_class _discord.MediaGalleryComponent¶
    

Represents a Media Gallery component from the Discord Bot UI Kit.

This inherits from `Component`.

Note

The user constructible and usable type for creating a media gallery is `discord.ui.MediaGallery` not this one.

New in version 2.6.

items¶
    

The items this gallery has.

Type
    

List[`MediaGalleryItem`]

id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### FileComponent¶

Attributes

  * id
  * media
  * name
  * size
  * spoiler
  * type



_class _discord.FileComponent¶
    

Represents a File component from the Discord Bot UI Kit.

This inherits from `Component`.

Note

The user constructible and usable type for create a file component is `discord.ui.File` not this one.

New in version 2.6.

media¶
    

The unfurled attachment contents of the file.

Type
    

`UnfurledMediaItem`

spoiler¶
    

Whether this file is flagged as a spoiler.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

name¶
    

The displayed file name, only available when received from the API.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

size¶
    

The file size in MiB, only available when received from the API.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### SeparatorComponent¶

Attributes

  * id
  * spacing
  * type
  * visible



_class _discord.SeparatorComponent¶
    

Represents a Separator from the Discord Bot UI Kit.

This inherits from `Component`.

Note

The user constructible and usable type for creating a separator is `discord.ui.Separator` not this one.

New in version 2.6.

spacing¶
    

The spacing size of the separator.

Type
    

`SeparatorSpacing`

visible¶
    

Whether this separator is visible and shows a divider.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### Container¶

Attributes

  * accent_color
  * accent_colour
  * children
  * id
  * spoiler
  * type



_class _discord.Container¶
    

Represents a Container from the Discord Bot UI Kit.

This inherits from `Component`.

Note

The user constructible and usable type for creating a container is `discord.ui.Container` not this one.

New in version 2.6.

children¶
    

This container’s children.

Type
    

`Component`

spoiler¶
    

Whether this container is flagged as a spoiler.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _accent_colour¶
    

The container’s accent colour.

Type
    

Optional[[`Colour`](../api.html#discord.Colour "discord.Colour")]

_property _accent_color¶
    

The container’s accent colour.

Type
    

Optional[[`Colour`](../api.html#discord.Colour "discord.Colour")]

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### FileUploadComponent¶

Attributes

  * custom_id
  * id
  * max_values
  * min_values
  * required
  * type



_class _discord.FileUploadComponent¶
    

Represents a file upload component from the Discord Bot UI Kit.

This inherits from `Component`.

Note

The user constructible and usable type for creating a file upload is `discord.ui.FileUpload` not this one.

New in version 2.7.

custom_id¶
    

The ID of the component that gets received during an interaction.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

min_values¶
    

The minimum number of files that must be uploaded for this component. Defaults to 1 and must be between 0 and 10.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

max_values¶
    

The maximum number of files that must be uploaded for this component. Defaults to 1 and must be between 1 and 10.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

required¶
    

Whether the component is required. Defaults to `True`.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### RadioGroupComponent¶

Attributes

  * custom_id
  * id
  * options
  * required
  * type



_class _discord.RadioGroupComponent¶
    

Represents a radio group component from the Discord Bot UI Kit.

This inherits from `Component`.

Note

The user constructible and usable type for creating a radio group is `discord.ui.RadioGroup` not this one.

New in version 2.7.

custom_id¶
    

The ID of the component that gets received during an interaction.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

required¶
    

Whether the component is required. Defaults to `True`.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

options¶
    

A list of options that can be selected in this group.

Type
    

List[`RadioGroupOption`]

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### CheckboxComponent¶

Attributes

  * custom_id
  * default
  * id
  * type



_class _discord.CheckboxComponent¶
    

Represents a checkbox component from the Discord Bot UI Kit.

This inherits from `Component`.

Note

The user constructible and usable type for creating a checkbox is `discord.ui.Checkbox` not this one.

New in version 2.7.

custom_id¶
    

The ID of the component that gets received during an interaction.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

default¶
    

Whether this checkbox is selected by default.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### CheckboxGroupComponent¶

Attributes

  * custom_id
  * id
  * max_values
  * min_values
  * options
  * required
  * type



_class _discord.CheckboxGroupComponent¶
    

Represents a checkbox group component from the Discord Bot UI Kit.

This inherits from `Component`.

Note

The user constructible and usable type for creating a checkbox group is `discord.ui.CheckboxGroup` not this one.

New in version 2.7.

custom_id¶
    

The ID of the component that gets received during an interaction.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

required¶
    

Whether the component is required. Defaults to `True`.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

min_values¶
    

The minimum number of options that must be selected in this component. Must be between 0 and 10. Defaults to 0.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

max_values¶
    

The maximum number of options that can be selected in this component. Must be between 1 and 10. Defaults to 1.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

options¶
    

A list of options that can be selected in this group.

Type
    

List[`CheckboxGroupOption`]

_property _type¶
    

The type of component.

Type
    

`ComponentType`

### AppCommand¶

Attributes

  * allowed_contexts
  * allowed_installs
  * application_id
  * default_member_permissions
  * description
  * description_localizations
  * dm_permission
  * guild
  * guild_id
  * id
  * mention
  * name
  * name_localizations
  * nsfw
  * options
  * type



Methods

  * asyncdelete
  * asyncedit
  * asyncfetch_permissions



_class _discord.app_commands.AppCommand¶
    

Represents an application command.

In common parlance this is referred to as a “Slash Command” or a “Context Menu Command”.

New in version 2.0.

x == y
    

Checks if two application commands are equal.

x != y
    

Checks if two application commands are not equal.

hash(x)
    

Returns the application command’s hash.

str(x)
    

Returns the application command’s name.

id¶
    

The application command’s ID.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

application_id¶
    

The application command’s application’s ID.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

type¶
    

The application command’s type.

Type
    

`AppCommandType`

name¶
    

The application command’s name.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

description¶
    

The application command’s description.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

name_localizations¶
    

The localised names of the application command. Used for display purposes.

Type
    

Dict[[`Locale`](../api.html#discord.Locale "discord.Locale"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

description_localizations¶
    

The localised descriptions of the application command. Used for display purposes.

Type
    

Dict[[`Locale`](../api.html#discord.Locale "discord.Locale"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

options¶
    

A list of options.

Type
    

List[Union[`Argument`, `AppCommandGroup`]]

default_member_permissions¶
    

The default member permissions that can run this command.

Type
    

Optional[[`Permissions`](../api.html#discord.Permissions "discord.Permissions")]

dm_permission¶
    

A boolean that indicates whether this command can be run in direct messages.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

allowed_contexts¶
    

The contexts that this command is allowed to be used in. Overrides the `dm_permission` attribute.

New in version 2.4.

Type
    

Optional[`AppCommandContext`]

allowed_installs¶
    

The installation contexts that this command is allowed to be installed in.

New in version 2.4.

Type
    

Optional[`AppInstallationType`]

guild_id¶
    

The ID of the guild this command is registered in. A value of `None` denotes that it is a global command.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

nsfw¶
    

Whether the command is NSFW and should only work in NSFW channels.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _mention¶
    

Returns a string that allows you to mention the given AppCommand.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _guild¶
    

Returns the guild this command is registered to if it exists.

Type
    

Optional[[`Guild`](../api.html#discord.Guild "discord.Guild")]

_await _delete()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Deletes the application command.

Raises
    

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The application command was not found.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have permission to delete this application command.

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Deleting the application command failed.

  * [**MissingApplicationID**](../api.html#discord.MissingApplicationID "discord.MissingApplicationID") – The client does not have an application ID.




_await _edit(_*_ , _name =..._, _description =..._, _default_member_permissions =..._, _dm_permission =..._, _options =..._)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Edits the application command.

Parameters
    

  * **name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The new name for the application command.

  * **description** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The new description for the application command.

  * **default_member_permissions** (Optional[[`Permissions`](../api.html#discord.Permissions "discord.Permissions")]) – The new default permissions needed to use this application command. Pass value of `None` to remove any permission requirements.

  * **dm_permission** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Indicates if the application command can be used in DMs.

  * **options** (List[Union[`Argument`, `AppCommandGroup`]]) – List of new options for this application command.



Raises
    

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The application command was not found.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have permission to edit this application command.

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Editing the application command failed.

  * [**MissingApplicationID**](../api.html#discord.MissingApplicationID "discord.MissingApplicationID") – The client does not have an application ID.



Returns
    

The newly edited application command.

Return type
    

`AppCommand`

_await _fetch_permissions(_guild_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Retrieves this command’s permission in the guild.

Parameters
    

**guild** ([`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")) – The guild to retrieve the permissions from.

Raises
    

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have permission to fetch the application command’s permissions.

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Fetching the application command’s permissions failed.

  * [**MissingApplicationID**](../api.html#discord.MissingApplicationID "discord.MissingApplicationID") – The client does not have an application ID.

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The application command’s permissions could not be found. This can also indicate that the permissions are synced with the guild (i.e. they are unchanged from the default).



Returns
    

An object representing the application command’s permissions in the guild.

Return type
    

`GuildAppCommandPermissions`

### AppCommandGroup¶

Attributes

  * description
  * description_localizations
  * mention
  * name
  * name_localizations
  * options
  * parent
  * qualified_name
  * type



_class _discord.app_commands.AppCommandGroup¶
    

Represents an application command subcommand.

New in version 2.0.

type¶
    

The type of subcommand.

Type
    

`AppCommandOptionType`

name¶
    

The name of the subcommand.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

description¶
    

The description of the subcommand.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

name_localizations¶
    

The localised names of the subcommand. Used for display purposes.

Type
    

Dict[[`Locale`](../api.html#discord.Locale "discord.Locale"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

description_localizations¶
    

The localised descriptions of the subcommand. Used for display purposes.

Type
    

Dict[[`Locale`](../api.html#discord.Locale "discord.Locale"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

options¶
    

A list of options.

Type
    

List[Union[`Argument`, `AppCommandGroup`]]

parent¶
    

The parent application command.

Type
    

Union[`AppCommand`, `AppCommandGroup`]

_property _qualified_name¶
    

Returns the fully qualified command name.

The qualified name includes the parent name as well. For example, in a command like `/foo bar` the qualified name is `foo bar`.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _mention¶
    

Returns a string that allows you to mention the given AppCommandGroup.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

### AppCommandChannel¶

Attributes

  * category_id
  * created_at
  * flags
  * guild
  * guild_id
  * id
  * jump_url
  * last_message_id
  * mention
  * name
  * nsfw
  * permissions
  * position
  * slowmode_delay
  * topic
  * type



Methods

  * asyncfetch
  * defis_news
  * defis_nsfw
  * defresolve



_class _discord.app_commands.AppCommandChannel¶
    

Represents an application command partially resolved channel object.

New in version 2.0.

x == y
    

Checks if two channels are equal.

x != y
    

Checks if two channels are not equal.

hash(x)
    

Returns the channel’s hash.

str(x)
    

Returns the channel’s name.

id¶
    

The ID of the channel.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

type¶
    

The type of channel.

Type
    

[`ChannelType`](../api.html#discord.ChannelType "discord.ChannelType")

name¶
    

The name of the channel.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

permissions¶
    

The resolved permissions of the user who invoked the application command in that channel.

Type
    

[`Permissions`](../api.html#discord.Permissions "discord.Permissions")

guild_id¶
    

The guild ID this channel belongs to.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

category_id¶
    

The category channel ID this channel belongs to, if applicable.

New in version 2.6.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

topic¶
    

The channel’s topic. `None` if it doesn’t exist.

New in version 2.6.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

position¶
    

The position in the channel list. This is a number that starts at 0. e.g. the top channel is position 0.

New in version 2.6.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

last_message_id¶
    

The last message ID of the message sent to this channel. It may _not_ point to an existing or valid message.

New in version 2.6.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

slowmode_delay¶
    

The number of seconds a member must wait between sending messages in this channel. A value of `0` denotes that it is disabled. Bots and users with [`bypass_slowmode`](../api.html#discord.Permissions.bypass_slowmode "discord.Permissions.bypass_slowmode") bypass slowmode.

New in version 2.6.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

nsfw¶
    

If the channel is marked as “not safe for work” or “age restricted”.

New in version 2.6.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _guild¶
    

The channel’s guild, from cache, if found.

Type
    

Optional[[`Guild`](../api.html#discord.Guild "discord.Guild")]

_property _flags¶
    

The flags associated with this channel object.

New in version 2.6.

Type
    

[`ChannelFlags`](../api.html#discord.ChannelFlags "discord.ChannelFlags")

is_nsfw()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Checks if the channel is NSFW.

New in version 2.6.

is_news()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Checks if the channel is a news channel.

New in version 2.6.

resolve()¶
    

Resolves the application command channel to the appropriate channel from cache if found.

Returns
    

The resolved guild channel or `None` if not found in cache.

Return type
    

Optional[[`abc.GuildChannel`](../api.html#discord.abc.GuildChannel "discord.abc.GuildChannel")]

_await _fetch()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Fetches the partial channel to a full [`abc.GuildChannel`](../api.html#discord.abc.GuildChannel "discord.abc.GuildChannel").

Raises
    

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The channel was not found.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have the permissions required to get a channel.

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Retrieving the channel failed.



Returns
    

The full channel.

Return type
    

[`abc.GuildChannel`](../api.html#discord.abc.GuildChannel "discord.abc.GuildChannel")

_property _mention¶
    

The string that allows you to mention the channel.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _jump_url¶
    

Returns a URL that allows the client to jump to the channel.

New in version 2.6.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _created_at¶
    

An aware timestamp of when this channel was created in UTC.

Type
    

[`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "\(in Python v3.14\)")

### AppCommandThread¶

Attributes

  * applied_tags
  * archive_timestamp
  * archived
  * archiver_id
  * auto_archive_duration
  * created_at
  * flags
  * guild
  * guild_id
  * id
  * invitable
  * jump_url
  * last_message_id
  * locked
  * member_count
  * mention
  * message_count
  * name
  * owner
  * owner_id
  * parent
  * parent_id
  * permissions
  * slowmode_delay
  * total_message_sent
  * type



Methods

  * asyncfetch
  * defresolve



_class _discord.app_commands.AppCommandThread¶
    

Represents an application command partially resolved thread object.

New in version 2.0.

x == y
    

Checks if two thread are equal.

x != y
    

Checks if two thread are not equal.

hash(x)
    

Returns the thread’s hash.

str(x)
    

Returns the thread’s name.

id¶
    

The ID of the thread.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

type¶
    

The type of thread.

Type
    

[`ChannelType`](../api.html#discord.ChannelType "discord.ChannelType")

name¶
    

The name of the thread.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

parent_id¶
    

The parent text channel ID this thread belongs to.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

owner_id¶
    

The user’s ID that created this thread.

New in version 2.6.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

last_message_id¶
    

The last message ID of the message sent to this thread. It may _not_ point to an existing or valid message.

New in version 2.6.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

slowmode_delay¶
    

The number of seconds a member must wait between sending messages in this thread. A value of `0` denotes that it is disabled. Bots and users with [`bypass_slowmode`](../api.html#discord.Permissions.bypass_slowmode "discord.Permissions.bypass_slowmode") bypass slowmode.

New in version 2.6.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

message_count¶
    

An approximate number of messages in this thread.

New in version 2.6.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

member_count¶
    

An approximate number of members in this thread. This caps at 50.

New in version 2.6.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

total_message_sent¶
    

The total number of messages sent, including deleted messages.

New in version 2.6.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

permissions¶
    

The resolved permissions of the user who invoked the application command in that thread.

Type
    

[`Permissions`](../api.html#discord.Permissions "discord.Permissions")

guild_id¶
    

The guild ID this thread belongs to.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

archived¶
    

Whether the thread is archived.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

locked¶
    

Whether the thread is locked.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

invitable¶
    

Whether non-moderators can add other non-moderators to this thread. This is always `True` for public threads.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

archiver_id¶
    

The user’s ID that archived this thread.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

auto_archive_duration¶
    

The duration in minutes until the thread is automatically hidden from the channel list. Usually a value of 60, 1440, 4320 and 10080.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

archive_timestamp¶
    

An aware timestamp of when the thread’s archived status was last updated in UTC.

Type
    

[`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "\(in Python v3.14\)")

_property _guild¶
    

The channel’s guild, from cache, if found.

Type
    

Optional[[`Guild`](../api.html#discord.Guild "discord.Guild")]

_property _applied_tags¶
    

A list of tags applied to this thread.

New in version 2.6.

Type
    

List[[`ForumTag`](../api.html#discord.ForumTag "discord.ForumTag")]

_property _parent¶
    

The parent channel this thread belongs to.

Type
    

Optional[Union[[`ForumChannel`](../api.html#discord.ForumChannel "discord.ForumChannel"), [`TextChannel`](../api.html#discord.TextChannel "discord.TextChannel")]]

_property _flags¶
    

The flags associated with this thread.

New in version 2.6.

Type
    

[`ChannelFlags`](../api.html#discord.ChannelFlags "discord.ChannelFlags")

_property _owner¶
    

The member this thread belongs to.

New in version 2.6.

Type
    

Optional[[`Member`](../api.html#discord.Member "discord.Member")]

_property _mention¶
    

The string that allows you to mention the thread.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _jump_url¶
    

Returns a URL that allows the client to jump to the thread.

New in version 2.6.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _created_at¶
    

An aware timestamp of when the thread was created in UTC.

Note

This timestamp only exists for threads created after 9 January 2022, otherwise returns `None`.

resolve()¶
    

Resolves the application command channel to the appropriate channel from cache if found.

Returns
    

The resolved guild channel or `None` if not found in cache.

Return type
    

Optional[[`abc.GuildChannel`](../api.html#discord.abc.GuildChannel "discord.abc.GuildChannel")]

_await _fetch()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Fetches the partial channel to a full [`Thread`](../api.html#discord.Thread "discord.Thread").

Raises
    

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The thread was not found.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – You do not have the permissions required to get a thread.

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Retrieving the thread failed.



Returns
    

The full thread.

Return type
    

[`Thread`](../api.html#discord.Thread "discord.Thread")

### AppCommandPermissions¶

Attributes

  * guild
  * id
  * permission
  * target
  * type



_class _discord.app_commands.AppCommandPermissions¶
    

Represents the permissions for an application command.

New in version 2.0.

guild¶
    

The guild associated with this permission.

Type
    

[`Guild`](../api.html#discord.Guild "discord.Guild")

id¶
    

The ID of the permission target, such as a role, channel, or guild. The special `guild_id - 1` sentinel is used to represent “all channels”.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

target¶
    

The role, user, or channel associated with this permission. This could also be the `AllChannels` sentinel type. Falls back to [`Object`](../api.html#discord.Object "discord.Object") if the target could not be found in the cache.

Type
    

Any

type¶
    

The type of permission.

Type
    

`AppCommandPermissionType`

permission¶
    

The permission value. `True` for allow, `False` for deny.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

### AppCommandContext¶

Attributes

  * dm_channel
  * guild
  * private_channel



_class _discord.app_commands.AppCommandContext(_*_ , _guild =None_, _dm_channel =None_, _private_channel =None_)¶
    

Wraps up the Discord `Command` execution context.

New in version 2.4.

Parameters
    

  * **guild** (Optional[[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")]) – Whether the context allows usage in a guild.

  * **dm_channel** (Optional[[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")]) – Whether the context allows usage in a DM channel.

  * **private_channel** (Optional[[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")]) – Whether the context allows usage in a DM or a GDM channel.




_property _guild¶
    

Whether the context allows usage in a guild.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _dm_channel¶
    

Whether the context allows usage in a DM channel.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _private_channel¶
    

Whether the context allows usage in a DM or a GDM channel.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

### AppInstallationType¶

Attributes

  * guild
  * user



_class _discord.app_commands.AppInstallationType(_*_ , _guild =None_, _user =None_)¶
    

Represents the installation location of an application command.

New in version 2.4.

Parameters
    

  * **guild** (Optional[[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")]) – Whether the integration is a guild install.

  * **user** (Optional[[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")]) – Whether the integration is a user install.




_property _guild¶
    

Whether the integration is a guild install.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _user¶
    

Whether the integration is a user install.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

### GuildAppCommandPermissions¶

Attributes

  * application_id
  * command
  * guild
  * guild_id
  * id
  * permissions



_class _discord.app_commands.GuildAppCommandPermissions¶
    

Represents the permissions for an application command in a guild.

New in version 2.0.

application_id¶
    

The application ID.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

command¶
    

The application command associated with the permissions.

Type
    

`AppCommand`

id¶
    

ID of the command or the application ID. When this is the application ID instead of a command ID, the permissions apply to all commands that do not contain explicit overwrites.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

guild_id¶
    

The guild ID associated with the permissions.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

permissions¶
    

The permissions, this is a max of 100.

Type
    

List[`AppCommandPermissions`]

_property _guild¶
    

The guild associated with the permissions.

Type
    

[`Guild`](../api.html#discord.Guild "discord.Guild")

### Argument¶

Attributes

  * autocomplete
  * channel_types
  * choices
  * description
  * description_localizations
  * max_length
  * max_value
  * min_length
  * min_value
  * name
  * name_localizations
  * parent
  * required
  * type



_class _discord.app_commands.Argument¶
    

Represents an application command argument.

New in version 2.0.

type¶
    

The type of argument.

Type
    

`AppCommandOptionType`

name¶
    

The name of the argument.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

description¶
    

The description of the argument.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

name_localizations¶
    

The localised names of the argument. Used for display purposes.

Type
    

Dict[[`Locale`](../api.html#discord.Locale "discord.Locale"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

description_localizations¶
    

The localised descriptions of the argument. Used for display purposes.

Type
    

Dict[[`Locale`](../api.html#discord.Locale "discord.Locale"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

required¶
    

Whether the argument is required.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

choices¶
    

A list of choices for the command to choose from for this argument.

Type
    

List[`Choice`]

parent¶
    

The parent application command that has this argument.

Type
    

Union[`AppCommand`, `AppCommandGroup`]

channel_types¶
    

The channel types that are allowed for this parameter.

Type
    

List[[`ChannelType`](../api.html#discord.ChannelType "discord.ChannelType")]

min_value¶
    

The minimum supported value for this parameter.

Type
    

Optional[Union[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)"), [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]]

max_value¶
    

The maximum supported value for this parameter.

Type
    

Optional[Union[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)"), [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]]

min_length¶
    

The minimum allowed length for this parameter.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

max_length¶
    

The maximum allowed length for this parameter.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

autocomplete¶
    

Whether the argument has autocomplete.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

### AllChannels¶

Attributes

  * guild
  * id



_class _discord.app_commands.AllChannels¶
    

Represents all channels for application command permissions.

New in version 2.0.

guild¶
    

The guild the application command permission is for.

Type
    

[`Guild`](../api.html#discord.Guild "discord.Guild")

_property _id¶
    

The ID sentinel used to represent all channels. Equivalent to the guild’s ID minus 1.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

## Data Classes¶

Similar to [Data Classes](../api.html#discord-api-data), these can be received and constructed by users.

### SelectOption¶

Attributes

  * default
  * description
  * emoji
  * label
  * value



_class _discord.SelectOption(_*_ , _label_ , _value =..._, _description =None_, _emoji =None_, _default =False_)¶
    

Represents a select menu’s option.

These can be created by users.

New in version 2.0.

Parameters
    

  * **label** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The label of the option. This is displayed to users. Can only be up to 100 characters.

  * **value** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The value of the option. This is not displayed to users. If not provided when constructed then it defaults to the label. Can only be up to 100 characters.

  * **description** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – An additional description of the option, if any. Can only be up to 100 characters.

  * **emoji** (Optional[Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`Emoji`](../api.html#discord.Emoji "discord.Emoji"), [`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji")]]) – The emoji of the option, if available.

  * **default** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this option is selected by default.




label¶
    

The label of the option. This is displayed to users.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

value¶
    

The value of the option. This is not displayed to users. If not provided when constructed then it defaults to the label.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

description¶
    

An additional description of the option, if any.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

default¶
    

Whether this option is selected by default.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _emoji¶
    

The emoji of the option, if available.

Type
    

Optional[[`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji")]

### SelectDefaultValue¶

Attributes

  * type



Methods

  * clsSelectDefaultValue.from_channel
  * clsSelectDefaultValue.from_role
  * clsSelectDefaultValue.from_user



_class _discord.SelectDefaultValue(_*_ , _id_ , _type_)¶
    

Represents a select menu’s default value.

These can be created by users.

New in version 2.4.

Parameters
    

  * **id** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The id of a role, user, or channel.

  * **type** ([`SelectDefaultValueType`](../api.html#discord.SelectDefaultValueType "discord.SelectDefaultValueType")) – The type of value that `id` represents.




_property _type¶
    

The type of value that `id` represents.

Type
    

[`SelectDefaultValueType`](../api.html#discord.SelectDefaultValueType "discord.SelectDefaultValueType")

_classmethod _from_channel(_channel_ , _/_)¶
    

Creates a `SelectDefaultValue` with the type set to [`channel`](../api.html#discord.SelectDefaultValueType.channel "discord.SelectDefaultValueType.channel").

Parameters
    

**channel** ([`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")) – The channel to create the default value for.

Returns
    

The default value created with the channel.

Return type
    

`SelectDefaultValue`

_classmethod _from_role(_role_ , _/_)¶
    

Creates a `SelectDefaultValue` with the type set to [`role`](../api.html#discord.SelectDefaultValueType.role "discord.SelectDefaultValueType.role").

Parameters
    

**role** ([`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")) – The role to create the default value for.

Returns
    

The default value created with the role.

Return type
    

`SelectDefaultValue`

_classmethod _from_user(_user_ , _/_)¶
    

Creates a `SelectDefaultValue` with the type set to [`user`](../api.html#discord.SelectDefaultValueType.user "discord.SelectDefaultValueType.user").

Parameters
    

**user** ([`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")) – The user to create the default value for.

Returns
    

The default value created with the user.

Return type
    

`SelectDefaultValue`

### Choice¶

_class _discord.app_commands.Choice(_*_ , _name_ , _value_)¶
    

Represents an application command argument choice.

New in version 2.0.

x == y
    

Checks if two choices are equal.

x != y
    

Checks if two choices are not equal.

hash(x)
    

Returns the choice’s hash.

Parameters
    

  * **name** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The name of the choice. Used for display purposes. Can only be up to 100 characters.

  * **name_localizations** (Dict[[`Locale`](../api.html#discord.Locale "discord.Locale"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The localised names of the choice. Used for display purposes.

  * **value** (Union[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]) – The value of the choice. If it’s a string, it can only be up to 100 characters long.




### UnfurledMediaItem¶

Attributes

  * attachment_id
  * content_type
  * flags
  * height
  * loading_state
  * placeholder
  * proxy_url
  * url
  * width



_class _discord.UnfurledMediaItem(_url_)¶
    

Represents an unfurled media item.

New in version 2.6.

Parameters
    

**url** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The URL of this media item. This can be an arbitrary url or a reference to a local file uploaded as an attachment within the message, which can be accessed with the `attachment://<filename>` format.

url¶
    

The URL of this media item.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

proxy_url¶
    

The proxy URL. This is a cached version of the `url` in the case of images. When the message is deleted, this URL might be valid for a few minutes or not valid at all.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

height¶
    

The media item’s height, in pixels. Only applicable to images and videos.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

width¶
    

The media item’s width, in pixels. Only applicable to images and videos.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

content_type¶
    

The media item’s [media type](https://en.wikipedia.org/wiki/Media_type)

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

placeholder¶
    

The media item’s placeholder.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

loading_state¶
    

The loading state of this media item.

Type
    

Optional[[`MediaItemLoadingState`](../api.html#discord.MediaItemLoadingState "discord.MediaItemLoadingState")]

attachment_id¶
    

The attachment id this media item points to, only available if the url points to a local file uploaded within the component message.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _flags¶
    

This media item’s flags.

Type
    

[`AttachmentFlags`](../api.html#discord.AttachmentFlags "discord.AttachmentFlags")

### MediaGalleryItem¶

Attributes

  * media



_class _discord.MediaGalleryItem(_media_ , _*_ , _description =..._, _spoiler =..._)¶
    

Represents a `MediaGalleryComponent` media item.

New in version 2.6.

Parameters
    

  * **media** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`discord.File`](../api.html#discord.File "discord.File"), `UnfurledMediaItem`]) – The media item data. This can be a string representing a local file uploaded as an attachment in the message, which can be accessed using the `attachment://<filename>` format, or an arbitrary url.

  * **description** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The description to show within this item. Up to 256 characters. Defaults to `None`.

  * **spoiler** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this item should be flagged as a spoiler.




_property _media¶
    

This item’s media data.

Type
    

`UnfurledMediaItem`

### RadioGroupOption¶

Attributes

  * default
  * description
  * label
  * value



_class _discord.RadioGroupOption¶
    

Represents a radio group’s option

These can be created by users.

New in version 2.7.

Parameters
    

  * **label** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The label of the option. This is displayed to users. Can only be up to 100 characters.

  * **value** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The value of the option. This is not displayed to users. If not provided when constructed then it defaults to the label. Can only be up to 100 characters.

  * **description** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – An additional description of the option, if any. Can only be up to 100 characters.

  * **default** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this option is selected by default.




label¶
    

The label of the option. This is displayed to users.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

value¶
    

The value of the option. This is not displayed to users. If not provided when constructed then it defaults to the label.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

description¶
    

An additional description of the option, if any.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

default¶
    

Whether this option is selected by default.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

### CheckboxGroupOption¶

Attributes

  * default
  * description
  * label
  * value



_class _discord.CheckboxGroupOption¶
    

Represents a checkbox group’s option

These can be created by users.

New in version 2.7.

Parameters
    

  * **label** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The label of the option. This is displayed to users. Can only be up to 100 characters.

  * **value** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The value of the option. This is not displayed to users. If not provided when constructed then it defaults to the label. Can only be up to 100 characters.

  * **description** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – An additional description of the option, if any. Can only be up to 100 characters.

  * **default** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this option is selected by default.




label¶
    

The label of the option. This is displayed to users.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

value¶
    

The value of the option. This is not displayed to users. If not provided when constructed then it defaults to the label.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

description¶
    

An additional description of the option, if any.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

default¶
    

Whether this option is selected by default.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

## Enumerations¶

_class _discord.InteractionType¶
    

Specifies the type of `Interaction`.

New in version 2.0.

ping¶
    

Represents Discord pinging to see if the interaction response server is alive.

application_command¶
    

Represents a slash command interaction.

component¶
    

Represents a component based interaction, i.e. using the Discord Bot UI Kit.

autocomplete¶
    

Represents an auto complete interaction.

modal_submit¶
    

Represents submission of a modal interaction.

_class _discord.InteractionResponseType¶
    

Specifies the response type for the interaction.

New in version 2.0.

pong¶
    

Pongs the interaction when given a ping.

See also `InteractionResponse.pong()`

channel_message¶
    

Respond to the interaction with a message.

See also `InteractionResponse.send_message()`

deferred_channel_message¶
    

Responds to the interaction with a message at a later time.

See also `InteractionResponse.defer()`

deferred_message_update¶
    

Acknowledges the component interaction with a promise that the message will update later (though there is no need to actually update the message).

See also `InteractionResponse.defer()`

message_update¶
    

Responds to the interaction by editing the message.

See also `InteractionResponse.edit_message()`

autocomplete_result¶
    

Responds to the autocomplete interaction with suggested choices.

See also `InteractionResponse.autocomplete()`

modal¶
    

Responds to the interaction with a modal.

See also `InteractionResponse.send_modal()`

_class _discord.ComponentType¶
    

Represents the component type of a component.

New in version 2.0.

action_row¶
    

Represents a component which holds different components in a row.

button¶
    

Represents a button component.

text_input¶
    

Represents a text box component.

select¶
    

Represents a select component.

string_select¶
    

An alias to `select`. Represents a default select component.

user_select¶
    

Represents a user select component.

role_select¶
    

Represents a role select component.

mentionable_select¶
    

Represents a select in which both users and roles can be selected.

channel_select¶
    

Represents a channel select component.

section¶
    

Represents a component which holds different components in a section.

New in version 2.6.

text_display¶
    

Represents a text display component.

New in version 2.6.

thumbnail¶
    

Represents a thumbnail component.

New in version 2.6.

media_gallery¶
    

Represents a media gallery component.

New in version 2.6.

file¶
    

Represents a file component.

New in version 2.6.

separator¶
    

Represents a separator component.

New in version 2.6.

container¶
    

Represents a component which holds different components in a container.

New in version 2.6.

label¶
    

Represents a label container component, usually in a modal.

New in version 2.6.

file_upload¶
    

Represents a file upload component, usually in a modal.

New in version 2.7.

radio_group¶
    

Represents a radio group component.

New in version 2.7.

checkbox_group¶
    

Represents a checkbox group component.

New in version 2.7.

checkbox¶
    

Represents a checkbox component.

New in version 2.7.

_class _discord.ButtonStyle¶
    

Represents the style of the button component.

New in version 2.0.

primary¶
    

Represents a blurple button for the primary action.

secondary¶
    

Represents a grey button for the secondary action.

success¶
    

Represents a green button for a successful action.

danger¶
    

Represents a red button for a dangerous action.

link¶
    

Represents a link button.

premium¶
    

Represents a button denoting that buying a SKU is required to perform this action.

New in version 2.4.

blurple¶
    

An alias for `primary`.

grey¶
    

An alias for `secondary`.

gray¶
    

An alias for `secondary`.

green¶
    

An alias for `success`.

red¶
    

An alias for `danger`.

url¶
    

An alias for `link`.

_class _discord.TextStyle¶
    

Represents the style of the text box component.

New in version 2.0.

short¶
    

Represents a short text box.

paragraph¶
    

Represents a long form text box.

long¶
    

An alias for `paragraph`.

_class _discord.AppCommandOptionType¶
    

The application command’s option type. This is usually the type of parameter an application command takes.

New in version 2.0.

subcommand¶
    

A subcommand.

subcommand_group¶
    

A subcommand group.

string¶
    

A string parameter.

integer¶
    

An integer parameter.

boolean¶
    

A boolean parameter.

user¶
    

A user parameter.

channel¶
    

A channel parameter.

role¶
    

A role parameter.

mentionable¶
    

A mentionable parameter.

number¶
    

A number parameter.

attachment¶
    

An attachment parameter.

_class _discord.AppCommandType¶
    

The type of application command.

New in version 2.0.

chat_input¶
    

A slash command.

user¶
    

A user context menu command.

message¶
    

A message context menu command.

_class _discord.AppCommandPermissionType¶
    

The application command’s permission type.

New in version 2.0.

role¶
    

The permission is for a role.

channel¶
    

The permission is for one or all channels.

user¶
    

The permission is for a user.

_class _discord.SeparatorSpacing¶
    

The separator’s size type.

New in version 2.6.

small¶
    

A small separator.

large¶
    

A large separator.

## Bot UI Kit¶

The library has helpers to aid in creating component-based UIs. These are all in the `discord.ui` package.

### View¶

Attributes

  * children
  * timeout
  * total_children_count



Methods

  * clsView.from_message
  * defadd_item
  * defclear_items
  * deffind_item
  * asyncinteraction_check
  * defis_dispatching
  * defis_finished
  * defis_persistent
  * asyncon_error
  * asyncon_timeout
  * defremove_item
  * defstop
  * asyncwait
  * defwalk_children



_class _discord.ui.View(_*_ , _timeout =180.0_)¶
    

Represents a UI view.

This object must be inherited to create a UI within Discord.

New in version 2.0.

Parameters
    

**timeout** (Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]) – Timeout in seconds from last interaction with the UI before no longer accepting input. If `None` then there is no timeout.

_classmethod _from_message(_message_ , _/_ , _*_ , _timeout =180.0_)¶
    

Converts a message’s components into a `View` or `LayoutView`.

The [`Message.components`](../api.html#discord.Message.components "discord.Message.components") of a message are read-only and separate types from those in the `discord.ui` namespace. In order to modify and edit message components they must be converted into a `View` or `LayoutView` first.

If the message has any v2 components, then you must use `LayoutView` in order for them to be converted into their respective items. `View` does not support v2 components.

Parameters
    

  * **message** ([`discord.Message`](../api.html#discord.Message "discord.Message")) – The message with components to convert into a view.

  * **timeout** (Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]) – The timeout of the converted view.



Returns
    

The converted view. This will always return one of `View` or `LayoutView`, and not one of its subclasses.

Return type
    

Union[`View`, `LayoutView`]

add_item(_item_)¶
    

Adds an item to the view.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (`Item`) – The item to add to the view.

Raises
    

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – An `Item` was not passed.

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – Maximum number of children has been exceeded, the row the item is trying to be added to is full or the item you tried to add is not allowed in this View.




remove_item(_item_)¶
    

Removes an item from the view.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (`Item`) – The item to remove from the view.

clear_items()¶
    

Removes all items from the view.

This function returns the class instance to allow for fluent-style chaining.

_property _children¶
    

The list of children attached to this view.

Type
    

List[`Item`]

find_item(_id_ , _/_)¶
    

Gets an item with `Item.id` set as `id`, or `None` if not found.

Warning

This is **not the same** as `custom_id`.

New in version 2.6.

Parameters
    

**id** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The ID of the component.

Returns
    

The item found, or `None`.

Return type
    

Optional[`Item`]

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within the view that checks whether the view should process item callbacks for the interaction.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `on_error()` is called.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the view children’s callbacks should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

is_dispatching()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Whether the view has been added for dispatching purposes.

is_finished()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Whether the view has finished interacting.

is_persistent()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Whether the view is set up as persistent.

A persistent view has all their components with a set `custom_id` and a `timeout` set to `None`.

_await _on_error(_interaction_ , _error_ , _item_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an item’s callback or `interaction_check()` fails with an error.

The default implementation logs to the library logger.

Parameters
    

  * **interaction** (`Interaction`) – The interaction that led to the failure.

  * **error** ([`Exception`](https://docs.python.org/3/library/exceptions.html#Exception "\(in Python v3.14\)")) – The exception that was raised.

  * **item** (`Item`) – The item that failed the dispatch.




_await _on_timeout()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when a view’s timeout elapses without being explicitly stopped.

stop()¶
    

Stops listening to interaction events from this view.

This operation cannot be undone.

_property _timeout¶
    

The timeout in seconds from last interaction with the UI before no longer accepting input. If `None` then there is no timeout.

Type
    

Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]

_property _total_children_count¶
    

The total number of children in this view, including those from nested items.

New in version 2.6.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_await _wait()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Waits until the view has finished interacting.

A view is considered finished when `stop()` is called or it times out.

Returns
    

If `True`, then the view timed out. If `False` then the view finished normally.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_for ... in _walk_children()¶
    

An iterator that recursively walks through all the children of this view and its children, if applicable.

New in version 2.6.

Yields
    

`Item` – An item in the view.

### LayoutView¶

Attributes

  * children
  * timeout
  * total_children_count



Methods

  * clsLayoutView.from_message
  * defadd_item
  * defclear_items
  * defcontent_length
  * deffind_item
  * asyncinteraction_check
  * defis_dispatching
  * defis_finished
  * defis_persistent
  * asyncon_error
  * asyncon_timeout
  * defremove_item
  * defstop
  * asyncwait
  * defwalk_children



_class _discord.ui.LayoutView(_*_ , _timeout =180.0_)¶
    

Represents a layout view for components.

This object must be inherited to create a UI within Discord.

This differs from a `View` in that it supports all component types and uses what Discord refers to as “v2 components”.

You can find usage examples in the [repository](https://github.com/Rapptz/discord.py/tree/master/examples)

New in version 2.6.

Parameters
    

**timeout** (Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]) – Timeout in seconds from last interaction with the UI before no longer accepting input. If `None` then there is no timeout.

_classmethod _from_message(_message_ , _/_ , _*_ , _timeout =180.0_)¶
    

Converts a message’s components into a `View` or `LayoutView`.

The [`Message.components`](../api.html#discord.Message.components "discord.Message.components") of a message are read-only and separate types from those in the `discord.ui` namespace. In order to modify and edit message components they must be converted into a `View` or `LayoutView` first.

If the message has any v2 components, then you must use `LayoutView` in order for them to be converted into their respective items. `View` does not support v2 components.

Parameters
    

  * **message** ([`discord.Message`](../api.html#discord.Message "discord.Message")) – The message with components to convert into a view.

  * **timeout** (Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]) – The timeout of the converted view.



Returns
    

The converted view. This will always return one of `View` or `LayoutView`, and not one of its subclasses.

Return type
    

Union[`View`, `LayoutView`]

add_item(_item_)¶
    

Adds an item to the view.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (`Item`) – The item to add to the view.

Raises
    

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – An `Item` was not passed.

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – Maximum number of children has been exceeded, the row the item is trying to be added to is full or the item you tried to add is not allowed in this View.




content_length()¶
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)"): Returns the total length of all text content in the view’s items.

A view is allowed to have a maximum of 4000 display characters across all its items.

_property _children¶
    

The list of children attached to this view.

Type
    

List[`Item`]

clear_items()¶
    

Removes all items from the view.

This function returns the class instance to allow for fluent-style chaining.

find_item(_id_ , _/_)¶
    

Gets an item with `Item.id` set as `id`, or `None` if not found.

Warning

This is **not the same** as `custom_id`.

New in version 2.6.

Parameters
    

**id** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The ID of the component.

Returns
    

The item found, or `None`.

Return type
    

Optional[`Item`]

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within the view that checks whether the view should process item callbacks for the interaction.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `on_error()` is called.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the view children’s callbacks should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

is_dispatching()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Whether the view has been added for dispatching purposes.

is_finished()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Whether the view has finished interacting.

is_persistent()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Whether the view is set up as persistent.

A persistent view has all their components with a set `custom_id` and a `timeout` set to `None`.

_await _on_error(_interaction_ , _error_ , _item_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an item’s callback or `interaction_check()` fails with an error.

The default implementation logs to the library logger.

Parameters
    

  * **interaction** (`Interaction`) – The interaction that led to the failure.

  * **error** ([`Exception`](https://docs.python.org/3/library/exceptions.html#Exception "\(in Python v3.14\)")) – The exception that was raised.

  * **item** (`Item`) – The item that failed the dispatch.




_await _on_timeout()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when a view’s timeout elapses without being explicitly stopped.

remove_item(_item_)¶
    

Removes an item from the view.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (`Item`) – The item to remove from the view.

stop()¶
    

Stops listening to interaction events from this view.

This operation cannot be undone.

_property _timeout¶
    

The timeout in seconds from last interaction with the UI before no longer accepting input. If `None` then there is no timeout.

Type
    

Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]

_property _total_children_count¶
    

The total number of children in this view, including those from nested items.

New in version 2.6.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_await _wait()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Waits until the view has finished interacting.

A view is considered finished when `stop()` is called or it times out.

Returns
    

If `True`, then the view timed out. If `False` then the view finished normally.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_for ... in _walk_children()¶
    

An iterator that recursively walks through all the children of this view and its children, if applicable.

New in version 2.6.

Yields
    

`Item` – An item in the view.

### Modal¶

Attributes

  * children
  * custom_id
  * timeout
  * title
  * total_children_count



Methods

  * defadd_item
  * defclear_items
  * deffind_item
  * asyncinteraction_check
  * defis_dispatching
  * defis_finished
  * defis_persistent
  * asyncon_error
  * asyncon_submit
  * asyncon_timeout
  * defremove_item
  * defstop
  * asyncwait
  * defwalk_children



_class _discord.ui.Modal(_*_ , _title =..._, _timeout =None_, _custom_id =..._)¶
    

Represents a UI modal.

This object must be inherited to create a modal popup window within discord.

New in version 2.0.

Examples
    
    
    import discord
    from discord import ui
    
    class Questionnaire(ui.Modal, title='Questionnaire Response'):
        name = ui.Label(text='Name', component=ui.TextInput())
        answer = ui.Label(text='Answer', component=ui.TextInput(style=discord.TextStyle.paragraph))
    
        async def on_submit(self, interaction: discord.Interaction):
            await interaction.response.send_message(f'Thanks for your response, {self.name.component.value}!', ephemeral=True)
    

Parameters
    

  * **title** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The title of the modal. Can only be up to 45 characters.

  * **timeout** (Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]) – Timeout in seconds from last interaction with the UI before no longer accepting input. If `None` then there is no timeout.

  * **custom_id** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The ID of the modal that gets received during an interaction. If not given then one is generated for you. Can only be up to 100 characters.




title¶
    

The title of the modal.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

custom_id¶
    

The ID of the modal that gets received during an interaction.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_await _on_submit(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Called when the modal is submitted.

Parameters
    

**interaction** (`Interaction`) – The interaction that submitted this modal.

_await _on_error(_interaction_ , _error_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when `on_submit()` fails with an error.

The default implementation logs to the library logger.

Parameters
    

  * **interaction** (`Interaction`) – The interaction that led to the failure.

  * **error** ([`Exception`](https://docs.python.org/3/library/exceptions.html#Exception "\(in Python v3.14\)")) – The exception that was raised.




add_item(_item_)¶
    

Adds an item to the view.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (`Item`) – The item to add to the view.

Raises
    

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – An `Item` was not passed.

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – Maximum number of children has been exceeded, the row the item is trying to be added to is full or the item you tried to add is not allowed in this View.




_property _children¶
    

The list of children attached to this view.

Type
    

List[`Item`]

clear_items()¶
    

Removes all items from the view.

This function returns the class instance to allow for fluent-style chaining.

find_item(_id_ , _/_)¶
    

Gets an item with `Item.id` set as `id`, or `None` if not found.

Warning

This is **not the same** as `custom_id`.

New in version 2.6.

Parameters
    

**id** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The ID of the component.

Returns
    

The item found, or `None`.

Return type
    

Optional[`Item`]

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within the view that checks whether the view should process item callbacks for the interaction.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `on_error()` is called.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the view children’s callbacks should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

is_dispatching()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Whether the view has been added for dispatching purposes.

is_finished()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Whether the view has finished interacting.

is_persistent()¶
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)"): Whether the view is set up as persistent.

A persistent view has all their components with a set `custom_id` and a `timeout` set to `None`.

_await _on_timeout()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when a view’s timeout elapses without being explicitly stopped.

remove_item(_item_)¶
    

Removes an item from the view.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (`Item`) – The item to remove from the view.

stop()¶
    

Stops listening to interaction events from this view.

This operation cannot be undone.

_property _timeout¶
    

The timeout in seconds from last interaction with the UI before no longer accepting input. If `None` then there is no timeout.

Type
    

Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]

_property _total_children_count¶
    

The total number of children in this view, including those from nested items.

New in version 2.6.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_await _wait()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Waits until the view has finished interacting.

A view is considered finished when `stop()` is called or it times out.

Returns
    

If `True`, then the view timed out. If `False` then the view finished normally.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_for ... in _walk_children()¶
    

An iterator that recursively walks through all the children of this view and its children, if applicable.

New in version 2.6.

Yields
    

`Item` – An item in the view.

### Item¶

Attributes

  * id
  * parent
  * view



Methods

  * asynccallback
  * asyncinteraction_check



_class _discord.ui.Item¶
    

Represents the base UI item that all UI components inherit from.

The current UI items supported are:

  * `discord.ui.Button`

  * `discord.ui.Select`

  * `discord.ui.TextInput`

  * `discord.ui.ActionRow`

  * `discord.ui.Container`

  * `discord.ui.File`

  * `discord.ui.MediaGallery`

  * `discord.ui.Section`

  * `discord.ui.Separator`

  * `discord.ui.TextDisplay`

  * `discord.ui.Thumbnail`

  * `discord.ui.Label`

  * `discord.ui.RadioGroup`

  * `discord.ui.CheckboxGroup`

  * `discord.ui.Checkbox`




New in version 2.0.

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

_property _id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_await _callback(_interaction_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

The callback associated with this UI item.

This can be overridden by subclasses.

Parameters
    

**interaction** (`Interaction`) – The interaction that triggered this UI item.

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within this item that checks whether the callback should be processed.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `View.on_error()` (or `LayoutView.on_error()`) is called.

For `DynamicItem` this does not call the `on_error` handler.

New in version 2.4.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the callback should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

### DynamicItem¶

Attributes

  * custom_id
  * id
  * item
  * parent
  * template
  * view



Methods

  * clsDynamicItem.from_custom_id
  * asynccallback
  * asyncinteraction_check



_class _discord.ui.DynamicItem(_item_ , _*_ , _row =None_)¶
    

Represents an item with a dynamic `custom_id` that can be used to store state within that `custom_id`.

The `custom_id` parsing is done using the `re` module by passing a `template` parameter to the class parameter list.

This item is generated every time the component is dispatched. This means that any variable that holds an instance of this class will eventually be out of date and should not be used long term. Their only purpose is to act as a “template” for the actual dispatched item.

When this item is generated, `view` is set to a regular `View` instance, but to a `LayoutView` if the component was sent with one, this is obtained from the original message given from the interaction. This means that custom view subclasses cannot be accessed from this item.

New in version 2.4.

Parameters
    

  * **item** (`Item`) – The item to wrap with dynamic custom ID parsing.

  * **template** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `re.Pattern`]) – The template to use for parsing the `custom_id`. This can be a string or a compiled regular expression. This must be passed as a keyword argument to the class creation.

  * **row** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The relative row this button belongs to. A Discord component can only have 5 rows. By default, items are arranged automatically into those 5 rows. If you’d like to control the relative positioning of the row then passing an index is advised. For example, row=1 will show up before row=2. Defaults to `None`, which is automatic ordering. The row number must be between 0 and 4 (i.e. zero indexed).




item¶
    

The item that is wrapped with dynamic custom ID parsing.

Type
    

`Item`

_property _template¶
    

The compiled regular expression that is used to parse the `custom_id`.

Type
    

`re.Pattern`

_property _custom_id¶
    

The ID of the dynamic item that gets received during an interaction.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

_classmethod await _from_custom_id(_interaction_ , _item_ , _match_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A classmethod that is called when the `custom_id` of a component matches the `template` of the class. This is called when the component is dispatched.

It must return a new instance of the `DynamicItem`.

Subclasses _must_ implement this method.

Exceptions raised in this method are logged and ignored.

Warning

This method is called before the callback is dispatched, therefore it means that it is subject to the same timing restrictions as the callback. Ergo, you must reply to an interaction within 3 seconds of it being dispatched.

Parameters
    

  * **interaction** (`Interaction`) – The interaction that the component belongs to.

  * **item** (`Item`) – The base item that is being dispatched.

  * **match** (`re.Match`) – The match object that was created from the `template` matching the `custom_id`.



Returns
    

The new instance of the `DynamicItem` with information from the `match` object.

Return type
    

`DynamicItem`

_await _callback(_interaction_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

The callback associated with this UI item.

This can be overridden by subclasses.

Parameters
    

**interaction** (`Interaction`) – The interaction that triggered this UI item.

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within this item that checks whether the callback should be processed.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `View.on_error()` (or `LayoutView.on_error()`) is called.

For `DynamicItem` this does not call the `on_error` handler.

New in version 2.4.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the callback should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

### Button¶

Attributes

  * custom_id
  * disabled
  * emoji
  * id
  * label
  * parent
  * sku_id
  * style
  * url
  * view



Methods

  * asynccallback
  * asyncinteraction_check



_class _discord.ui.Button(_*_ , _style= <ButtonStyle.secondary: 2>_, _label=None_ , _disabled=False_ , _custom_id=None_ , _url=None_ , _emoji=None_ , _row=None_ , _sku_id=None_ , _id=None_)¶
    

Represents a UI button.

New in version 2.0.

Parameters
    

  * **style** (`discord.ButtonStyle`) – The style of the button.

  * **custom_id** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The ID of the button that gets received during an interaction. If this button is for a URL, it does not have a custom ID. Can only be up to 100 characters.

  * **url** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The URL this button sends you to.

  * **disabled** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether the button is disabled or not.

  * **label** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The label of the button, if any. Can only be up to 80 characters.

  * **emoji** (Optional[Union[[`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji"), [`Emoji`](../api.html#discord.Emoji "discord.Emoji"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]]) – The emoji of the button, if available.

  * **row** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The relative row this button belongs to. A Discord component can only have 5 rows. By default, items are arranged automatically into those 5 rows. If you’d like to control the relative positioning of the row then passing an index is advised. For example, row=1 will show up before row=2. Defaults to `None`, which is automatic ordering. The row number must be between 0 and 4 (i.e. zero indexed).

Note

This parameter is ignored when used in a `ActionRow` or v2 component.

  * **sku_id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The SKU ID this button sends you to. Can’t be combined with `url`, `label`, `emoji` nor `custom_id`.

New in version 2.4.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The ID of this component. This must be unique across the view.

New in version 2.6.




_property _id¶
    

The ID of this button.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _style¶
    

The style of the button.

Type
    

`discord.ButtonStyle`

_property _custom_id¶
    

The ID of the button that gets received during an interaction.

If this button is for a URL, it does not have a custom ID.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

_property _url¶
    

The URL this button sends you to.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

_property _disabled¶
    

Whether the button is disabled or not.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _label¶
    

The label of the button, if available.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

_property _emoji¶
    

The emoji of the button, if available.

Type
    

Optional[[`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji")]

_property _sku_id¶
    

The SKU ID this button sends you to.

New in version 2.4.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_await _callback(_interaction_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

The callback associated with this UI item.

This can be overridden by subclasses.

Parameters
    

**interaction** (`Interaction`) – The interaction that triggered this UI item.

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within this item that checks whether the callback should be processed.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `View.on_error()` (or `LayoutView.on_error()`) is called.

For `DynamicItem` this does not call the `on_error` handler.

New in version 2.4.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the callback should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

@discord.ui.button(_*_ , _label=None_ , _custom_id=None_ , _disabled=False_ , _style= <ButtonStyle.secondary: 2>_, _emoji=None_ , _row=None_ , _id=None_)¶
    

A decorator that attaches a button to a component.

The function being decorated should have three parameters, `self` representing the `discord.ui.View`, the `discord.Interaction` you receive and the `discord.ui.Button` being pressed.

Note

Buttons with a URL or an SKU cannot be created with this function. Consider creating a `Button` manually instead. This is because these buttons cannot have a callback associated with them since Discord does not do any processing with them.

Parameters
    

  * **label** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The label of the button, if any. Can only be up to 80 characters.

  * **custom_id** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The ID of the button that gets received during an interaction. It is recommended not to set this parameter to prevent conflicts. Can only be up to 100 characters.

  * **style** (`ButtonStyle`) – The style of the button. Defaults to `ButtonStyle.grey`.

  * **disabled** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether the button is disabled or not. Defaults to `False`.

  * **emoji** (Optional[Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`Emoji`](../api.html#discord.Emoji "discord.Emoji"), [`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji")]]) – The emoji of the button. This can be in string form or a [`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji") or a full [`Emoji`](../api.html#discord.Emoji "discord.Emoji").

  * **row** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The relative row this button belongs to. A Discord component can only have 5 rows. By default, items are arranged automatically into those 5 rows. If you’d like to control the relative positioning of the row then passing an index is advised. For example, row=1 will show up before row=2. Defaults to `None`, which is automatic ordering. The row number must be between 0 and 4 (i.e. zero indexed).

Note

This parameter is ignored when used in a `ActionRow` or v2 component.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The ID of this component. This must be unique across the view.

New in version 2.6.




### Select Menus¶

The library provides classes to help create the different types of select menus.

#### Select¶

Attributes

  * custom_id
  * disabled
  * id
  * max_values
  * min_values
  * options
  * parent
  * placeholder
  * required
  * type
  * values
  * view



Methods

  * defadd_option
  * defappend_option
  * asynccallback
  * asyncinteraction_check



_class _discord.ui.Select(_*_ , _custom_id =..._, _placeholder =None_, _min_values =1_, _max_values =1_, _options =..._, _disabled =False_, _required =True_, _row =None_, _id =None_)¶
    

Represents a UI select menu with a list of custom options. This is represented to the user as a dropdown menu.

New in version 2.0.

Parameters
    

  * **custom_id** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The ID of the select menu that gets received during an interaction. If not given then one is generated for you. Can only be up to 100 characters.

  * **placeholder** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The placeholder text that is shown if nothing is selected, if any. Can only be up to 150 characters.

  * **min_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The minimum number of items that must be chosen for this select menu. Defaults to 1 and must be between 0 and 25.

  * **max_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The maximum number of items that must be chosen for this select menu. Defaults to 1 and must be between 1 and 25.

  * **options** (List[`discord.SelectOption`]) – A list of options that can be selected in this menu. Can only contain up to 25 items.

  * **disabled** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether the select is disabled or not.

  * **required** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether the select is required. Only applicable within modals.

New in version 2.6.

  * **row** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The relative row this select menu belongs to. A Discord component can only have 5 rows. By default, items are arranged automatically into those 5 rows. If you’d like to control the relative positioning of the row then passing an index is advised. For example, row=1 will show up before row=2. Defaults to `None`, which is automatic ordering. The row number must be between 0 and 4 (i.e. zero indexed).

Note

This parameter is ignored when used in a `ActionRow` or v2 component.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The ID of the component. This must be unique across the view.

New in version 2.6.




_property _values¶
    

A list of values that have been selected by the user.

Type
    

List[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

_property _type¶
    

The type of this component.

Type
    

`ComponentType`

_property _options¶
    

A list of options that can be selected in this menu.

Type
    

List[`discord.SelectOption`]

add_option(_*_ , _label_ , _value =..._, _description =None_, _emoji =None_, _default =False_)¶
    

Adds an option to the select menu.

To append a pre-existing `discord.SelectOption` use the `append_option()` method instead.

Parameters
    

  * **label** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The label of the option. This is displayed to users. Can only be up to 100 characters.

  * **value** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The value of the option. This is not displayed to users. If not given, defaults to the label. Can only be up to 100 characters.

  * **description** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – An additional description of the option, if any. Can only be up to 100 characters.

  * **emoji** (Optional[Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`Emoji`](../api.html#discord.Emoji "discord.Emoji"), [`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji")]]) – The emoji of the option, if available. This can either be a string representing the custom or unicode emoji or an instance of [`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji") or [`Emoji`](../api.html#discord.Emoji "discord.Emoji").

  * **default** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this option is selected by default.



Raises
    

[**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – The number of options exceeds 25.

append_option(_option_)¶
    

Appends an option to the select menu.

Parameters
    

**option** (`discord.SelectOption`) – The option to append to the select menu.

Raises
    

[**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – The number of options exceeds 25.

_await _callback(_interaction_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

The callback associated with this UI item.

This can be overridden by subclasses.

Parameters
    

**interaction** (`Interaction`) – The interaction that triggered this UI item.

_property _custom_id¶
    

The ID of the select menu that gets received during an interaction.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _disabled¶
    

Whether the select is disabled or not.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _id¶
    

The ID of this select.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within this item that checks whether the callback should be processed.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `View.on_error()` (or `LayoutView.on_error()`) is called.

For `DynamicItem` this does not call the `on_error` handler.

New in version 2.4.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the callback should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _max_values¶
    

The maximum number of items that can be chosen for this select menu.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _min_values¶
    

The minimum number of items that must be chosen for this select menu.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _placeholder¶
    

The placeholder text that is shown if nothing is selected, if any.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

_property _required¶
    

Whether the select is required or not. Only supported in modals.

New in version 2.6.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

#### ChannelSelect¶

Attributes

  * channel_types
  * custom_id
  * default_values
  * disabled
  * id
  * max_values
  * min_values
  * parent
  * placeholder
  * required
  * type
  * values
  * view



Methods

  * asynccallback
  * asyncinteraction_check



_class _discord.ui.ChannelSelect(_*_ , _custom_id =..._, _channel_types =..._, _placeholder =None_, _min_values =1_, _max_values =1_, _disabled =False_, _required =True_, _row =None_, _default_values =..._, _id =None_)¶
    

Represents a UI select menu with a list of predefined options with the current channels in the guild.

Please note that if you use this in a private message with a user, no channels will be displayed to the user.

New in version 2.1.

Parameters
    

  * **custom_id** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The ID of the select menu that gets received during an interaction. If not given then one is generated for you. Can only be up to 100 characters.

  * **channel_types** (List[[`ChannelType`](../api.html#discord.ChannelType "discord.ChannelType")]) – The types of channels to show in the select menu. Defaults to all channels.

  * **placeholder** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The placeholder text that is shown if nothing is selected, if any. Can only be up to 150 characters.

  * **min_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The minimum number of items that must be chosen for this select menu. Defaults to 1 and must be between 0 and 25.

  * **max_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The maximum number of items that must be chosen for this select menu. Defaults to 1 and must be between 1 and 25.

  * **disabled** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether the select is disabled or not.

  * **required** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether the select is required. Only applicable within modals.

New in version 2.6.

  * **default_values** (Sequence[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – 

A list of objects representing the channels that should be selected by default. Number of items must be in range of `min_values` and `max_values`.

New in version 2.4.

  * **row** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The relative row this select menu belongs to. A Discord component can only have 5 rows. By default, items are arranged automatically into those 5 rows. If you’d like to control the relative positioning of the row then passing an index is advised. For example, row=1 will show up before row=2. Defaults to `None`, which is automatic ordering. The row number must be between 0 and 4 (i.e. zero indexed).

Note

This parameter is ignored when used in a `ActionRow` or v2 component.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The ID of the component. This must be unique across the view.

New in version 2.6.




_await _callback(_interaction_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

The callback associated with this UI item.

This can be overridden by subclasses.

Parameters
    

**interaction** (`Interaction`) – The interaction that triggered this UI item.

_property _custom_id¶
    

The ID of the select menu that gets received during an interaction.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _disabled¶
    

Whether the select is disabled or not.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _id¶
    

The ID of this select.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within this item that checks whether the callback should be processed.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `View.on_error()` (or `LayoutView.on_error()`) is called.

For `DynamicItem` this does not call the `on_error` handler.

New in version 2.4.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the callback should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _max_values¶
    

The maximum number of items that can be chosen for this select menu.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _min_values¶
    

The minimum number of items that must be chosen for this select menu.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _placeholder¶
    

The placeholder text that is shown if nothing is selected, if any.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

_property _required¶
    

Whether the select is required or not. Only supported in modals.

New in version 2.6.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

_property _type¶
    

The type of this component.

Type
    

`ComponentType`

_property _channel_types¶
    

A list of channel types that can be selected.

Type
    

List[[`ChannelType`](../api.html#discord.ChannelType "discord.ChannelType")]

_property _values¶
    

A list of channels selected by the user.

Type
    

List[Union[`AppCommandChannel`, `AppCommandThread`]]

_property _default_values¶
    

A list of default values for the select menu.

New in version 2.4.

Type
    

List[`discord.SelectDefaultValue`]

#### RoleSelect¶

Attributes

  * custom_id
  * default_values
  * disabled
  * id
  * max_values
  * min_values
  * parent
  * placeholder
  * required
  * type
  * values
  * view



Methods

  * asynccallback
  * asyncinteraction_check



_class _discord.ui.RoleSelect(_*_ , _custom_id =..._, _placeholder =None_, _min_values =1_, _max_values =1_, _disabled =False_, _required =True_, _row =None_, _default_values =..._, _id =None_)¶
    

Represents a UI select menu with a list of predefined options with the current roles of the guild.

Please note that if you use this in a private message with a user, no roles will be displayed to the user.

New in version 2.1.

Parameters
    

  * **custom_id** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The ID of the select menu that gets received during an interaction. If not given then one is generated for you. Can only be up to 100 characters.

  * **placeholder** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The placeholder text that is shown if nothing is selected, if any. Can only be up to 150 characters.

  * **min_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The minimum number of items that must be chosen for this select menu. Defaults to 1 and must be between 0 and 25.

  * **max_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The maximum number of items that must be chosen for this select menu. Defaults to 1 and must be between 1 and 25.

  * **disabled** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether the select is disabled or not.

  * **required** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether the select is required. Only applicable within modals.

New in version 2.6.

  * **default_values** (Sequence[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – 

A list of objects representing the roles that should be selected by default. Number of items must be in range of `min_values` and `max_values`.

New in version 2.4.

  * **row** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The relative row this select menu belongs to. A Discord component can only have 5 rows. By default, items are arranged automatically into those 5 rows. If you’d like to control the relative positioning of the row then passing an index is advised. For example, row=1 will show up before row=2. Defaults to `None`, which is automatic ordering. The row number must be between 0 and 4 (i.e. zero indexed).

Note

This parameter is ignored when used in a `ActionRow` or v2 component.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The ID of the component. This must be unique across the view.

New in version 2.6.




_property _type¶
    

The type of this component.

Type
    

`ComponentType`

_property _values¶
    

A list of roles that have been selected by the user.

Type
    

List[[`discord.Role`](../api.html#discord.Role "discord.Role")]

_property _default_values¶
    

A list of default values for the select menu.

New in version 2.4.

Type
    

List[`discord.SelectDefaultValue`]

_await _callback(_interaction_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

The callback associated with this UI item.

This can be overridden by subclasses.

Parameters
    

**interaction** (`Interaction`) – The interaction that triggered this UI item.

_property _custom_id¶
    

The ID of the select menu that gets received during an interaction.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _disabled¶
    

Whether the select is disabled or not.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _id¶
    

The ID of this select.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within this item that checks whether the callback should be processed.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `View.on_error()` (or `LayoutView.on_error()`) is called.

For `DynamicItem` this does not call the `on_error` handler.

New in version 2.4.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the callback should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _max_values¶
    

The maximum number of items that can be chosen for this select menu.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _min_values¶
    

The minimum number of items that must be chosen for this select menu.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _placeholder¶
    

The placeholder text that is shown if nothing is selected, if any.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

_property _required¶
    

Whether the select is required or not. Only supported in modals.

New in version 2.6.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

#### MentionableSelect¶

Attributes

  * custom_id
  * default_values
  * disabled
  * id
  * max_values
  * min_values
  * parent
  * placeholder
  * required
  * type
  * values
  * view



Methods

  * asynccallback
  * asyncinteraction_check



_class _discord.ui.MentionableSelect(_*_ , _custom_id =..._, _placeholder =None_, _min_values =1_, _max_values =1_, _disabled =False_, _required =True_, _row =None_, _default_values =..._, _id =None_)¶
    

Represents a UI select menu with a list of predefined options with the current members and roles in the guild.

If this is sent in a private message, it will only allow the user to select the client or themselves. Every selected option in a private message will resolve to a [`discord.User`](../api.html#discord.User "discord.User"). It will not give the user any roles to select.

New in version 2.1.

Parameters
    

  * **custom_id** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The ID of the select menu that gets received during an interaction. If not given then one is generated for you. Can only be up to 100 characters.

  * **placeholder** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The placeholder text that is shown if nothing is selected, if any. Can only be up to 150 characters.

  * **min_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The minimum number of items that must be chosen for this select menu. Defaults to 1 and must be between 0 and 25.

  * **max_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The maximum number of items that must be chosen for this select menu. Defaults to 1 and must be between 1 and 25.

  * **disabled** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether the select is disabled or not.

  * **required** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether the select is required. Only applicable within modals.

New in version 2.6.

  * **default_values** (Sequence[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – 

A list of objects representing the users/roles that should be selected by default. if [`Object`](../api.html#discord.Object "discord.Object") is passed, then the type must be specified in the constructor. Number of items must be in range of `min_values` and `max_values`.

New in version 2.4.

  * **row** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The relative row this select menu belongs to. A Discord component can only have 5 rows. By default, items are arranged automatically into those 5 rows. If you’d like to control the relative positioning of the row then passing an index is advised. For example, row=1 will show up before row=2. Defaults to `None`, which is automatic ordering. The row number must be between 0 and 4 (i.e. zero indexed).

Note

This parameter is ignored when used in a `ActionRow` or v2 component.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The ID of the component. This must be unique across the view.

New in version 2.6.




_property _type¶
    

The type of this component.

Type
    

`ComponentType`

_await _callback(_interaction_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

The callback associated with this UI item.

This can be overridden by subclasses.

Parameters
    

**interaction** (`Interaction`) – The interaction that triggered this UI item.

_property _custom_id¶
    

The ID of the select menu that gets received during an interaction.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _disabled¶
    

Whether the select is disabled or not.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _id¶
    

The ID of this select.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within this item that checks whether the callback should be processed.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `View.on_error()` (or `LayoutView.on_error()`) is called.

For `DynamicItem` this does not call the `on_error` handler.

New in version 2.4.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the callback should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _max_values¶
    

The maximum number of items that can be chosen for this select menu.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _min_values¶
    

The minimum number of items that must be chosen for this select menu.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _placeholder¶
    

The placeholder text that is shown if nothing is selected, if any.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

_property _required¶
    

Whether the select is required or not. Only supported in modals.

New in version 2.6.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _values¶
    

A list of roles, members, and users that have been selected by the user.

If this is sent a private message, it will only allow the user to select the client or themselves. Every selected option in a private message will resolve to a [`discord.User`](../api.html#discord.User "discord.User").

If invoked in a guild, the values will always resolve to [`discord.Member`](../api.html#discord.Member "discord.Member").

Type
    

List[Union[[`discord.Role`](../api.html#discord.Role "discord.Role"), [`discord.Member`](../api.html#discord.Member "discord.Member"), [`discord.User`](../api.html#discord.User "discord.User")]]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

_property _default_values¶
    

A list of default values for the select menu.

New in version 2.4.

Type
    

List[`discord.SelectDefaultValue`]

#### UserSelect¶

Attributes

  * custom_id
  * default_values
  * disabled
  * id
  * max_values
  * min_values
  * parent
  * placeholder
  * required
  * type
  * values
  * view



Methods

  * asynccallback
  * asyncinteraction_check



_class _discord.ui.UserSelect(_*_ , _custom_id =..._, _placeholder =None_, _min_values =1_, _max_values =1_, _disabled =False_, _required =True_, _row =None_, _default_values =..._, _id =None_)¶
    

Represents a UI select menu with a list of predefined options with the current members of the guild.

If this is sent a private message, it will only allow the user to select the client or themselves. Every selected option in a private message will resolve to a [`discord.User`](../api.html#discord.User "discord.User").

New in version 2.1.

Parameters
    

  * **custom_id** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The ID of the select menu that gets received during an interaction. If not given then one is generated for you. Can only be up to 100 characters.

  * **placeholder** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The placeholder text that is shown if nothing is selected, if any. Can only be up to 150 characters.

  * **min_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The minimum number of items that must be chosen for this select menu. Defaults to 1 and must be between 0 and 25.

  * **max_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The maximum number of items that must be chosen for this select menu. Defaults to 1 and must be between 1 and 25.

  * **disabled** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether the select is disabled or not.

  * **required** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether the select is required. Only applicable within modals.

New in version 2.6.

  * **default_values** (Sequence[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – 

A list of objects representing the users that should be selected by default. Number of items must be in range of `min_values` and `max_values`.

New in version 2.4.

  * **row** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The relative row this select menu belongs to. A Discord component can only have 5 rows. By default, items are arranged automatically into those 5 rows. If you’d like to control the relative positioning of the row then passing an index is advised. For example, row=1 will show up before row=2. Defaults to `None`, which is automatic ordering. The row number must be between 0 and 4 (i.e. zero indexed).

Note

This parameter is ignored when used in a `ActionRow` or v2 component.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The ID of the component. This must be unique across the view.

New in version 2.6.




_property _type¶
    

The type of this component.

Type
    

`ComponentType`

_property _values¶
    

A list of members and users that have been selected by the user.

If this is sent a private message, it will only allow the user to select the client or themselves. Every selected option in a private message will resolve to a [`discord.User`](../api.html#discord.User "discord.User").

If invoked in a guild, the values will always resolve to [`discord.Member`](../api.html#discord.Member "discord.Member").

Type
    

List[Union[[`discord.Member`](../api.html#discord.Member "discord.Member"), [`discord.User`](../api.html#discord.User "discord.User")]]

_property _default_values¶
    

A list of default values for the select menu.

New in version 2.4.

Type
    

List[`discord.SelectDefaultValue`]

_await _callback(_interaction_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

The callback associated with this UI item.

This can be overridden by subclasses.

Parameters
    

**interaction** (`Interaction`) – The interaction that triggered this UI item.

_property _custom_id¶
    

The ID of the select menu that gets received during an interaction.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _disabled¶
    

Whether the select is disabled or not.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _id¶
    

The ID of this select.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within this item that checks whether the callback should be processed.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `View.on_error()` (or `LayoutView.on_error()`) is called.

For `DynamicItem` this does not call the `on_error` handler.

New in version 2.4.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the callback should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _max_values¶
    

The maximum number of items that can be chosen for this select menu.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _min_values¶
    

The minimum number of items that must be chosen for this select menu.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _placeholder¶
    

The placeholder text that is shown if nothing is selected, if any.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

_property _required¶
    

Whether the select is required or not. Only supported in modals.

New in version 2.6.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

#### select¶

@discord.ui.select(_*_ , _cls =discord.ui.select.Select[typing.Any]_, _options =..._, _channel_types =..._, _placeholder =None_, _custom_id =..._, _min_values =1_, _max_values =1_, _disabled =False_, _default_values =..._, _row =None_, _id =None_)¶
    

A decorator that attaches a select menu to a component.

The function being decorated should have three parameters, `self` representing the `discord.ui.View`, the `discord.Interaction` you receive and the chosen select class.

To obtain the selected values inside the callback, you can use the `values` attribute of the chosen class in the callback. The list of values will depend on the type of select menu used. View the table below for more information.

Select Type | Resolved Values  
---|---  
`discord.ui.Select` | List[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]  
`discord.ui.UserSelect` | List[Union[[`discord.Member`](../api.html#discord.Member "discord.Member"), [`discord.User`](../api.html#discord.User "discord.User")]]  
`discord.ui.RoleSelect` | List[[`discord.Role`](../api.html#discord.Role "discord.Role")]  
`discord.ui.MentionableSelect` | List[Union[[`discord.Role`](../api.html#discord.Role "discord.Role"), [`discord.Member`](../api.html#discord.Member "discord.Member"), [`discord.User`](../api.html#discord.User "discord.User")]]  
`discord.ui.ChannelSelect` | List[Union[`AppCommandChannel`, `AppCommandThread`]]  
  
Changed in version 2.1: Added the following keyword-arguments: `cls`, `channel_types`

Example
    
    
    class View(discord.ui.View):
    
        @discord.ui.select(cls=ChannelSelect, channel_types=[discord.ChannelType.text])
        async def select_channels(self, interaction: discord.Interaction, select: ChannelSelect):
            return await interaction.response.send_message(f'You selected {select.values[0].mention}')
    

Parameters
    

  * **cls** (Union[Type[`discord.ui.Select`], Type[`discord.ui.UserSelect`], Type[`discord.ui.RoleSelect`], Type[`discord.ui.MentionableSelect`], Type[`discord.ui.ChannelSelect`]]) – The class to use for the select menu. Defaults to `discord.ui.Select`. You can use other select types to display different select menus to the user. See the table above for the different values you can get from each select type. Subclasses work as well, however the callback in the subclass will get overridden.

  * **placeholder** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The placeholder text that is shown if nothing is selected, if any. Can only be up to 150 characters.

  * **custom_id** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The ID of the select menu that gets received during an interaction. It is recommended not to set this parameter to prevent conflicts. Can only be up to 100 characters.

  * **row** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The relative row this select menu belongs to. A Discord component can only have 5 rows. By default, items are arranged automatically into those 5 rows. If you’d like to control the relative positioning of the row then passing an index is advised. For example, row=1 will show up before row=2. Defaults to `None`, which is automatic ordering. The row number must be between 0 and 4 (i.e. zero indexed).

Note

This parameter is ignored when used in a `ActionRow` or v2 component.

  * **min_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The minimum number of items that must be chosen for this select menu. Defaults to 1 and must be between 0 and 25.

  * **max_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The maximum number of items that must be chosen for this select menu. Defaults to 1 and must be between 1 and 25.

  * **options** (List[`discord.SelectOption`]) – A list of options that can be selected in this menu. This can only be used with `Select` instances. Can only contain up to 25 items.

  * **channel_types** (List[[`ChannelType`](../api.html#discord.ChannelType "discord.ChannelType")]) – The types of channels to show in the select menu. Defaults to all channels. This can only be used with `ChannelSelect` instances.

  * **disabled** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether the select is disabled or not. Defaults to `False`.

  * **default_values** (Sequence[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – 

A list of objects representing the default values for the select menu. This cannot be used with regular `Select` instances. If `cls` is `MentionableSelect` and [`Object`](../api.html#discord.Object "discord.Object") is passed, then the type must be specified in the constructor. Number of items must be in range of `min_values` and `max_values`.

New in version 2.4.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The ID of the component. This must be unique across the view.

New in version 2.6.




### TextInput¶

Attributes

  * custom_id
  * default
  * id
  * label
  * max_length
  * min_length
  * parent
  * placeholder
  * required
  * style
  * value
  * view



_class _discord.ui.TextInput(_*_ , _label=None_ , _style= <TextStyle.short: 1>_, _custom_id=..._ , _placeholder=None_ , _default=None_ , _required=True_ , _min_length=None_ , _max_length=None_ , _row=None_ , _id=None_)¶
    

Represents a UI text input.

This a top-level layout component that can only be used in `Label`.

str(x)
    

Returns the value of the text input or an empty string if the value is `None`.

New in version 2.0.

Parameters
    

  * **label** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – 

The label to display above the text input. Can only be up to 45 characters.

Deprecated since version 2.6: This parameter is deprecated, use `discord.ui.Label` instead.

Changed in version 2.6: This parameter is now optional and defaults to `None`.

  * **custom_id** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The ID of the text input that gets received during an interaction. If not given then one is generated for you. Can only be up to 100 characters.

  * **style** (`discord.TextStyle`) – The style of the text input.

  * **placeholder** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The placeholder text to display when the text input is empty. Can only be up to 100 characters.

  * **default** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The default value of the text input. Can only be up to 4000 characters.

  * **required** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether the text input is required.

  * **min_length** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The minimum length of the text input. Must be between 0 and 4000.

  * **max_length** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The maximum length of the text input. Must be between 1 and 4000.

  * **row** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The relative row this text input belongs to. A Discord component can only have 5 rows. By default, items are arranged automatically into those 5 rows. If you’d like to control the relative positioning of the row then passing an index is advised. For example, row=1 will show up before row=2. Defaults to `None`, which is automatic ordering. The row number must be between 0 and 4 (i.e. zero indexed).

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The ID of the component. This must be unique across the view.

New in version 2.6.




_property _id¶
    

The ID of this text input.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _custom_id¶
    

The ID of the text input that gets received during an interaction.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _value¶
    

The value of the text input.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _label¶
    

The label of the text input.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _placeholder¶
    

The placeholder text to display when the text input is empty.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _required¶
    

Whether the text input is required.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _min_length¶
    

The minimum length of the text input.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _max_length¶
    

The maximum length of the text input.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _style¶
    

The style of the text input.

Type
    

`discord.TextStyle`

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

_property _default¶
    

The default value of the text input.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

### Container¶

Attributes

  * accent_color
  * accent_colour
  * children
  * id
  * parent
  * view



Methods

  * defadd_item
  * defclear_items
  * defcontent_length
  * deffind_item
  * asyncinteraction_check
  * defremove_item
  * defwalk_children



_class _discord.ui.Container(_* children_, _accent_colour =None_, _accent_color =None_, _spoiler =False_, _id =None_)¶
    

Represents a UI container.

This is a top-level layout component that can only be used on `LayoutView` and can contain `ActionRow`s, `TextDisplay`s, `Section`s, `MediaGallery`s, `File`s, and `Separator`s in it.

This can be inherited.

New in version 2.6.

Examples
    
    
    import discord
    from discord import ui
    
    # you can subclass it and add components as you would add them
    # in a LayoutView
    class MyContainer(ui.Container):
        action_row = ui.ActionRow()
    
        @action_row.button(label='A button in a container!')
        async def a_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('You clicked a button!')
    
    # or use it directly on LayoutView
    class MyView(ui.LayoutView):
        container = ui.Container(ui.TextDisplay('I am a text display on a container!'))
        # or you can use your subclass:
        # container = MyContainer()
    

Parameters
    

  * ***children** (`Item`) – The initial children of this container.

  * **accent_colour** (Optional[Union[[`Colour`](../api.html#discord.Colour "discord.Colour"), [`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]]) – The colour of the container. Defaults to `None`.

  * **accent_color** (Optional[Union[[`Colour`](../api.html#discord.Colour "discord.Colour"), [`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]]) – The color of the container. Defaults to `None`.

  * **spoiler** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether to flag this container as a spoiler. Defaults to `False`.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The ID of this component. This must be unique across the view.




_property _id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _children¶
    

The children of this container.

Type
    

List[`Item`]

_property _accent_colour¶
    

The colour of the container, or `None`.

Type
    

Optional[Union[[`discord.Colour`](../api.html#discord.Colour "discord.Colour"), [`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]]

_property _accent_color¶
    

The colour of the container, or `None`.

Type
    

Optional[Union[[`discord.Colour`](../api.html#discord.Colour "discord.Colour"), [`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]]

_for ... in _walk_children()¶
    

An iterator that recursively walks through all the children of this container and its children, if applicable.

Yields
    

`Item` – An item in the container.

content_length()¶
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)"): Returns the total length of all text content in this container.

add_item(_item_)¶
    

Adds an item to this container.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (`Item`) – The item to append.

Raises
    

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – An `Item` was not passed.

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – Maximum number of children has been exceeded (40) for the entire view.




remove_item(_item_)¶
    

Removes an item from this container.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (`Item`) – The item to remove from the container.

find_item(_id_ , _/_)¶
    

Gets an item with `Item.id` set as `id`, or `None` if not found.

Warning

This is **not the same** as `custom_id`.

Parameters
    

**id** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The ID of the component.

Returns
    

The item found, or `None`.

Return type
    

Optional[`Item`]

clear_items()¶
    

Removes all the items from the container.

This function returns the class instance to allow for fluent-style chaining.

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within this item that checks whether the callback should be processed.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `View.on_error()` (or `LayoutView.on_error()`) is called.

For `DynamicItem` this does not call the `on_error` handler.

New in version 2.4.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the callback should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

### File¶

Attributes

  * id
  * media
  * parent
  * spoiler
  * url
  * view



_class _discord.ui.File(_media_ , _*_ , _spoiler =..._, _id =None_)¶
    

Represents a UI file component.

This is a top-level layout component that can only be used on `LayoutView`.

New in version 2.6.

Example
    
    
    import discord
    from discord import ui
    
    class MyView(ui.LayoutView):
        file = ui.File('attachment://file.txt')
        # attachment://file.txt points to an attachment uploaded alongside this view
    

Parameters
    

  * **media** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `UnfurledMediaItem`, [`discord.File`](../api.html#discord.File "discord.File")]) – This file’s media. If this is a string it must point to a local file uploaded within the parent view of this item, and must meet the `attachment://<filename>` format.

  * **spoiler** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether to flag this file as a spoiler. Defaults to `False`.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The ID of this component. This must be unique across the view.




_property _id¶
    

The ID of this file component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _media¶
    

Returns this file media.

Type
    

`UnfurledMediaItem`

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _url¶
    

Returns this file’s url.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

_property _spoiler¶
    

Returns whether this file should be flagged as a spoiler.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

### Label¶

Attributes

  * component
  * description
  * id
  * parent
  * text
  * view



_class _discord.ui.Label(_*_ , _text_ , _component_ , _description =None_, _id =None_)¶
    

Represents a UI label within a modal.

This is a top-level layout component that can only be used on `Modal`.

New in version 2.6.

Parameters
    

  * **text** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The text to display above the input field. Can only be up to 45 characters.

  * **description** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The description text to display right below the label text. Can only be up to 100 characters.

  * **component** (`Item`) – The component to display below the label.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The ID of the component. This must be unique across the view.




text¶
    

The text to display above the input field. Can only be up to 45 characters.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

description¶
    

The description text to display right below the label text. Can only be up to 100 characters.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

component¶
    

The component to display below the label.

Type
    

`Item`

_property _id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

### MediaGallery¶

Attributes

  * id
  * items
  * parent
  * view



Methods

  * defadd_item
  * defappend_item
  * defclear_items
  * definsert_item_at
  * defremove_item



_class _discord.ui.MediaGallery(_* items_, _id =None_)¶
    

Represents a UI media gallery.

Can contain up to 10 `MediaGalleryItem`s.

This is a top-level layout component that can only be used on `LayoutView`.

New in version 2.6.

Parameters
    

  * ***items** (`MediaGalleryItem`) – The initial items of this gallery.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The ID of this component. This must be unique across the view.




_property _items¶
    

Returns a read-only list of this gallery’s items.

Type
    

List[`MediaGalleryItem`]

_property _id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

add_item(_*_ , _media_ , _description =..._, _spoiler =..._)¶
    

Adds an item to this gallery.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

  * **media** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`discord.File`](../api.html#discord.File "discord.File"), `UnfurledMediaItem`]) – The media item data. This can be a string representing a local file uploaded as an attachment in the message, which can be accessed using the `attachment://<filename>` format, or an arbitrary url.

  * **description** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The description to show within this item. Up to 256 characters. Defaults to `None`.

  * **spoiler** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this item should be flagged as a spoiler. Defaults to `False`.



Raises
    

[**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – Maximum number of items has been exceeded (10).

append_item(_item_)¶
    

Appends an item to this gallery.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (`MediaGalleryItem`) – The item to add to the gallery.

Raises
    

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – A `MediaGalleryItem` was not passed.

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – Maximum number of items has been exceeded (10).




insert_item_at(_index_ , _*_ , _media_ , _description =..._, _spoiler =..._)¶
    

Inserts an item before a specified index to the media gallery.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

  * **index** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The index of where to insert the field.

  * **media** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`discord.File`](../api.html#discord.File "discord.File"), `UnfurledMediaItem`]) – The media item data. This can be a string representing a local file uploaded as an attachment in the message, which can be accessed using the `attachment://<filename>` format, or an arbitrary url.

  * **description** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The description to show within this item. Up to 256 characters. Defaults to `None`.

  * **spoiler** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this item should be flagged as a spoiler. Defaults to `False`.



Raises
    

[**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – Maximum number of items has been exceeded (10).

remove_item(_item_)¶
    

Removes an item from the gallery.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (`MediaGalleryItem`) – The item to remove from the gallery.

clear_items()¶
    

Removes all items from the gallery.

This function returns the class instance to allow for fluent-style chaining.

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

### Section¶

Attributes

  * accessory
  * children
  * id
  * parent
  * view



Methods

  * defadd_item
  * defclear_items
  * defcontent_length
  * deffind_item
  * asyncinteraction_check
  * defremove_item
  * defwalk_children



_class _discord.ui.Section(_* children_, _accessory_ , _id =None_)¶
    

Represents a UI section.

This is a top-level layout component that can only be used on `LayoutView`.

New in version 2.6.

Parameters
    

  * ***children** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `TextDisplay`]) – The text displays of this section. Up to 3.

  * **accessory** (`Item`) – The section accessory. This is usually either a `Button` or `Thumbnail`.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The ID of this component. This must be unique across the view.




_property _id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _children¶
    

The list of children attached to this section.

Type
    

List[`Item`]

_property _accessory¶
    

The section’s accessory.

Type
    

`Item`

_for ... in _walk_children()¶
    

An iterator that recursively walks through all the children of this section and its children, if applicable. This includes the accessory.

Yields
    

`Item` – An item in this section.

content_length()¶
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)"): Returns the total length of all text content in this section.

add_item(_item_)¶
    

Adds an item to this section.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `Item`]) – The item to append, if it is a string it automatically wrapped around `TextDisplay`.

Raises
    

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – An `Item` or [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)") was not passed.

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – Maximum number of children has been exceeded (3) or (40) for the entire view.




remove_item(_item_)¶
    

Removes an item from this section.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (`Item`) – The item to remove from the section.

find_item(_id_ , _/_)¶
    

Gets an item with `Item.id` set as `id`, or `None` if not found.

Warning

This is **not the same** as `custom_id`.

Parameters
    

**id** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The ID of the component.

Returns
    

The item found, or `None`.

Return type
    

Optional[`Item`]

clear_items()¶
    

Removes all the items from the section.

This function returns the class instance to allow for fluent-style chaining.

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within this item that checks whether the callback should be processed.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `View.on_error()` (or `LayoutView.on_error()`) is called.

For `DynamicItem` this does not call the `on_error` handler.

New in version 2.4.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the callback should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

### Separator¶

Attributes

  * id
  * parent
  * spacing
  * view
  * visible



_class _discord.ui.Separator(_*_ , _visible=True_ , _spacing= <SeparatorSpacing.small: 1>_, _id=None_)¶
    

Represents a UI separator.

This is a top-level layout component that can only be used on `LayoutView`.

New in version 2.6.

Parameters
    

  * **visible** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this separator is visible. On the client side this is whether a divider line should be shown or not.

  * **spacing** (`SeparatorSpacing`) – The spacing of this separator.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The ID of this component. This must be unique across the view.




_property _id¶
    

The ID of this separator.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _visible¶
    

Whether this separator is visible.

On the client side this is whether a divider line should be shown or not.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _spacing¶
    

The spacing of this separator.

Type
    

`SeparatorSpacing`

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

### TextDisplay¶

Attributes

  * id
  * parent
  * view



_class _discord.ui.TextDisplay(_content_ , _*_ , _id =None_)¶
    

Represents a UI text display.

This is a top-level layout component that can only be used on `LayoutView`, `Section`, `Container`, or `Modal`.

New in version 2.6.

Parameters
    

  * **content** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The content of this text display. Up to 4000 characters.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The ID of this component. This must be unique across the view.




_property _id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

### Thumbnail¶

Attributes

  * id
  * media
  * parent
  * view



_class _discord.ui.Thumbnail(_media_ , _*_ , _description =..._, _spoiler =..._, _id =None_)¶
    

Represents a UI Thumbnail. This currently can only be used as a `Section`’s accessory.

New in version 2.6.

Parameters
    

  * **media** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`discord.File`](../api.html#discord.File "discord.File"), `discord.UnfurledMediaItem`]) – The media of the thumbnail. This can be a URL or a reference to an attachment that matches the `attachment://filename.extension` structure.

  * **description** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The description of this thumbnail. Up to 256 characters. Defaults to `None`.

  * **spoiler** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether to flag this thumbnail as a spoiler. Defaults to `False`.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The ID of this component. This must be unique across the view.




_property _id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _media¶
    

This thumbnail unfurled media data.

Type
    

`discord.UnfurledMediaItem`

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

### ActionRow¶

Attributes

  * children
  * id
  * parent
  * view



Methods

  * defadd_item
  * @button
  * defclear_items
  * defcontent_length
  * deffind_item
  * asyncinteraction_check
  * defremove_item
  * @select
  * defwalk_children



_class _discord.ui.ActionRow(_* children_, _id =None_)¶
    

Represents a UI action row.

This is a top-level layout component that can only be used on `LayoutView` and can contain `Button`s and `Select`s in it.

Action rows can only have 5 children. This can be inherited.

New in version 2.6.

Examples
    
    
    import discord
    from discord import ui
    
    # you can subclass it and add components with the decorators
    class MyActionRow(ui.ActionRow):
        @ui.button(label='Click Me!')
        async def click_me(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('You clicked me!')
    
    # or use it directly on LayoutView
    class MyView(ui.LayoutView):
        row = ui.ActionRow()
        # or you can use your subclass:
        # row = MyActionRow()
    
        # you can add items with row.button and row.select
        @row.button(label='A button!')
        async def row_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('You clicked a button!')
    

Parameters
    

  * ***children** (`Item`) – The initial children of this action row.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The ID of this component. This must be unique across the view.




_property _id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _children¶
    

The list of children attached to this action row.

Type
    

List[`Item`]

_for ... in _walk_children()¶
    

An iterator that recursively walks through all the children of this action row and its children, if applicable.

Yields
    

`Item` – An item in the action row.

content_length()¶
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)"): Returns the total length of all text content in this action row.

add_item(_item_)¶
    

Adds an item to this action row.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (`Item`) – The item to add to the action row.

Raises
    

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – An `Item` was not passed.

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – Maximum number of children has been exceeded (5) or (40) for the entire view.




remove_item(_item_)¶
    

Removes an item from the action row.

This function returns the class instance to allow for fluent-style chaining.

Parameters
    

**item** (`Item`) – The item to remove from the action row.

find_item(_id_ , _/_)¶
    

Gets an item with `Item.id` set as `id`, or `None` if not found.

Warning

This is **not the same** as `custom_id`.

Parameters
    

**id** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The ID of the component.

Returns
    

The item found, or `None`.

Return type
    

Optional[`Item`]

clear_items()¶
    

Removes all items from the action row.

This function returns the class instance to allow for fluent-style chaining.

button(_*_ , _label=None_ , _custom_id=None_ , _disabled=False_ , _style= <ButtonStyle.secondary: 2>_, _emoji=None_ , _id=None_)¶
    

A decorator that attaches a button to the action row.

The function being decorated should have three parameters, `self` representing the `discord.ui.ActionRow`, the `discord.Interaction` you receive and the `discord.ui.Button` being pressed.

Note

Buttons with a URL or a SKU cannot be created with this function. Consider creating a `Button` manually and adding it via `ActionRow.add_item()` instead. This is because these buttons cannot have a callback associated with them since Discord does not do any processing with them.

Parameters
    

  * **label** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The label of the button, if any. Can only be up to 80 characters.

  * **custom_id** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The ID of the button that gets received during an interaction. It is recommended to not set this parameter to prevent conflicts. Can only be up to 100 characters.

  * **style** (`ButtonStyle`) – The style of the button. Defaults to `ButtonStyle.grey`.

  * **disabled** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether the button is disabled or not. Defaults to `False`.

  * **emoji** (Optional[Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`Emoji`](../api.html#discord.Emoji "discord.Emoji"), [`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji")]]) – The emoji of the button. This can be in string form or a [`PartialEmoji`](../api.html#discord.PartialEmoji "discord.PartialEmoji") or a full [`Emoji`](../api.html#discord.Emoji "discord.Emoji").

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The ID of the component. This must be unique across the view.

New in version 2.6.




_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within this item that checks whether the callback should be processed.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and `View.on_error()` (or `LayoutView.on_error()`) is called.

For `DynamicItem` this does not call the `on_error` handler.

New in version 2.4.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the callback should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

select(_*_ , _cls =discord.ui.select.Select[typing.Any]_, _options =..._, _channel_types =..._, _placeholder =None_, _custom_id =..._, _min_values =1_, _max_values =1_, _disabled =False_, _default_values =..._, _id =None_)¶
    

A decorator that attaches a select menu to the action row.

The function being decorated should have three parameters, `self` representing the `discord.ui.ActionRow`, the `discord.Interaction` you receive and the chosen select class.

To obtain the selected values inside the callback, you can use the `values` attribute of the chosen class in the callback. The list of values will depend on the type of select menu used. View the table below for more information.

Select Type | Resolved Values  
---|---  
`discord.ui.Select` | List[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]  
`discord.ui.UserSelect` | List[Union[[`discord.Member`](../api.html#discord.Member "discord.Member"), [`discord.User`](../api.html#discord.User "discord.User")]]  
`discord.ui.RoleSelect` | List[[`discord.Role`](../api.html#discord.Role "discord.Role")]  
`discord.ui.MentionableSelect` | List[Union[[`discord.Role`](../api.html#discord.Role "discord.Role"), [`discord.Member`](../api.html#discord.Member "discord.Member"), [`discord.User`](../api.html#discord.User "discord.User")]]  
`discord.ui.ChannelSelect` | List[Union[`AppCommandChannel`, `AppCommandThread`]]  
  
Example
    
    
    class MyView(discord.ui.LayoutView):
        action_row = discord.ui.ActionRow()
    
        @action_row.select(cls=ChannelSelect, channel_types=[discord.ChannelType.text])
        async def select_channels(self, interaction: discord.Interaction, select: ChannelSelect):
            return await interaction.response.send_message(f'You selected {select.values[0].mention}')
    

Parameters
    

  * **cls** (Union[Type[`discord.ui.Select`], Type[`discord.ui.UserSelect`], Type[`discord.ui.RoleSelect`], Type[`discord.ui.MentionableSelect`], Type[`discord.ui.ChannelSelect`]]) – The class to use for the select menu. Defaults to `discord.ui.Select`. You can use other select types to display different select menus to the user. See the table above for the different values you can get from each select type. Subclasses work as well, however the callback in the subclass will get overridden.

  * **placeholder** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The placeholder text that is shown if nothing is selected, if any. Can only be up to 150 characters.

  * **custom_id** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The ID of the select menu that gets received during an interaction. It is recommended not to set this parameter to prevent conflicts. Can only be up to 100 characters.

  * **min_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The minimum number of items that must be chosen for this select menu. Defaults to 1 and must be between 0 and 25.

  * **max_values** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The maximum number of items that must be chosen for this select menu. Defaults to 1 and must be between 1 and 25.

  * **options** (List[`discord.SelectOption`]) – A list of options that can be selected in this menu. This can only be used with `Select` instances. Can only contain up to 25 items.

  * **channel_types** (List[[`ChannelType`](../api.html#discord.ChannelType "discord.ChannelType")]) – The types of channels to show in the select menu. Defaults to all channels. This can only be used with `ChannelSelect` instances.

  * **disabled** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether the select is disabled or not. Defaults to `False`.

  * **default_values** (Sequence[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – A list of objects representing the default values for the select menu. This cannot be used with regular `Select` instances. If `cls` is `MentionableSelect` and [`Object`](../api.html#discord.Object "discord.Object") is passed, then the type must be specified in the constructor. Number of items must be in range of `min_values` and `max_values`.

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – 

The ID of the component. This must be unique across the view.

New in version 2.6.




### FileUpload¶

Attributes

  * custom_id
  * id
  * max_values
  * min_values
  * parent
  * required
  * values
  * view



_class _discord.ui.FileUpload(_*_ , _custom_id =..._, _required =True_, _min_values =None_, _max_values =None_, _id =None_)¶
    

Represents a file upload component within a modal.

New in version 2.7.

Parameters
    

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The ID of the component. This must be unique across the view.

  * **custom_id** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The custom ID of the file upload component.

  * **max_values** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The maximum number of files that can be uploaded in this component. Must be between 1 and 10. Defaults to 1.

  * **min_values** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The minimum number of files that must be uploaded in this component. Must be between 0 and 10. Defaults to 0.

  * **required** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this component is required to be filled before submitting the modal. Defaults to `True`.




_property _id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _values¶
    

The list of attachments uploaded by the user.

You can call [`to_file()`](../api.html#discord.Attachment.to_file "discord.Attachment.to_file") on each attachment to get a [`File`](../api.html#discord.File "discord.File") for sending.

Type
    

List[[`discord.Attachment`](../api.html#discord.Attachment "discord.Attachment")]

_property _custom_id¶
    

The ID of the component that gets received during an interaction.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _min_values¶
    

The minimum number of files that must be user upload before submitting the modal.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _max_values¶
    

The maximum number of files that the user must upload before submitting the modal.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _required¶
    

Whether the component is required or not.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

### RadioGroup¶

Attributes

  * custom_id
  * id
  * options
  * parent
  * required
  * type
  * value
  * view



Methods

  * defadd_option
  * defappend_option



_class _discord.ui.RadioGroup(_*_ , _custom_id =..._, _required =True_, _options =..._, _id =None_)¶
    

Represents a radio group component within a modal that can only be used in `Label`.

New in version 2.7.

Parameters
    

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The ID of the component. This must be unique across the view.

  * **custom_id** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The custom ID of the component.

  * **options** (List[`discord.RadioGroupOption`]) – A list of options that can be selected in this radio group. Can contain between 2 and 10 items.

  * **required** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this component is required to be filled before submitting the modal. Defaults to `True`.




_property _id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _value¶
    

The value that has been selected by the user, if any.

Type
    

Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

_property _custom_id¶
    

The ID of the component that gets received during an interaction.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _type¶
    

The type of this component.

Type
    

`ComponentType`

_property _options¶
    

A list of options that can be selected in this radio group.

Type
    

List[`discord.RadioGroupOption`]

add_option(_*_ , _label_ , _value =..._, _description =None_, _default =False_)¶
    

Adds an option to the group.

To append a pre-existing `discord.RadioGroupOption` use the `append_option()` method instead.

Parameters
    

  * **label** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The label of the option. This is displayed to users. Can only be up to 100 characters.

  * **value** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The value of the option. This is not displayed to users. If not given, defaults to the label. Can only be up to 100 characters.

  * **description** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – An additional description of the option, if any. Can only be up to 100 characters.

  * **default** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this option is selected by default.



Raises
    

[**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – The number of options exceeds 10.

append_option(_option_)¶
    

Appends an option to the group.

Parameters
    

**option** (`discord.RadioGroupOption`) – The option to append to the group.

Raises
    

[**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – The number of options exceeds 10.

_property _required¶
    

Whether the component is required or not.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

### Checkbox¶

Attributes

  * custom_id
  * default
  * id
  * parent
  * type
  * value
  * view



_class _discord.ui.Checkbox(_*_ , _custom_id =..._, _default =False_, _id =None_)¶
    

Represents a checkbox component within a modal that can only be used in `Label`.

New in version 2.7.

Parameters
    

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The ID of the component. This must be unique across the view.

  * **custom_id** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The custom ID of the component.

  * **default** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this checkbox is selected by default.




_property _id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _value¶
    

`True` if this checkbox was selected, otherwise `False`.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

_property _custom_id¶
    

The ID of the component that gets received during an interaction.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _type¶
    

The type of this component.

Type
    

`ComponentType`

_property _default¶
    

Whether this checkbox is selected by default.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

### CheckboxGroup¶

Attributes

  * custom_id
  * id
  * max_values
  * min_values
  * options
  * parent
  * required
  * type
  * values
  * view



Methods

  * defadd_option
  * defappend_option



_class _discord.ui.CheckboxGroup(_*_ , _custom_id =..._, _required =True_, _min_values =None_, _max_values =None_, _options =..._, _id =None_)¶
    

Represents a checkbox group component within a modal that can only be used in `Label`.

New in version 2.7.

Parameters
    

  * **id** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The ID of the component. This must be unique across the view.

  * **custom_id** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The custom ID of the component.

  * **options** (List[`discord.CheckboxGroupOption`]) – A list of options that can be selected in this checkbox group. Can only contain up to 10 items.

  * **max_values** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The maximum number of options that can be selected in this component. Must be between 1 and 10. Defaults to 1.

  * **min_values** (Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]) – The minimum number of options that must be selected in this component. Must be between 0 and 10. Defaults to 0.

  * **required** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this component is required to be filled before submitting the modal. Defaults to `True`.




_property _id¶
    

The ID of this component.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _values¶
    

A list of values that have been selected by the user.

Type
    

List[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

_property _custom_id¶
    

The ID of the component that gets received during an interaction.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _type¶
    

The type of this component.

Type
    

`ComponentType`

_property _options¶
    

A list of options that can be selected in this menu.

Type
    

List[`discord.CheckboxGroupOption`]

_property _min_values¶
    

The minimum number of options that must be selected before submitting the modal.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_property _max_values¶
    

The maximum number of options that can be selected before submitting the modal.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

add_option(_*_ , _label_ , _value =..._, _description =None_, _default =False_)¶
    

Adds an option to the checkbox group.

To append a pre-existing `discord.CheckboxGroupOption` use the `append_option()` method instead.

Parameters
    

  * **label** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The label of the option. This is displayed to users. Can only be up to 100 characters.

  * **value** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The value of the option. This is not displayed to users. If not given, defaults to the label. Can only be up to 100 characters.

  * **description** (Optional[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – An additional description of the option, if any. Can only be up to 100 characters.

  * **default** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether this option is selected by default.



Raises
    

[**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – The number of options exceeds 10.

append_option(_option_)¶
    

Appends an option to the checkbox group.

Parameters
    

**option** (`discord.CheckboxGroupOption`) – The option to append to the checkbox group.

Raises
    

[**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – The number of options exceeds 10.

_property _required¶
    

Whether the component is required or not.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

_property _parent¶
    

This item’s parent, if applicable. Only available on items with children.

New in version 2.6.

Type
    

Optional[`Item`]

_property _view¶
    

The underlying view for this item.

Type
    

Optional[Union[`View`, `LayoutView`]]

## Application Commands¶

The library has helpers to aid in creation of application commands. These are all in the `discord.app_commands` package.

### CommandTree¶

Attributes

  * translator



Methods

  * defadd_command
  * defclear_commands
  * @command
  * @context_menu
  * defcopy_global_to
  * @error
  * asyncfetch_command
  * asyncfetch_commands
  * defget_command
  * defget_commands
  * asyncinteraction_check
  * asyncon_error
  * defremove_command
  * asyncset_translator
  * asyncsync
  * defwalk_commands



_class _discord.app_commands.CommandTree(_client_ , _*_ , _fallback_to_global =True_, _allowed_contexts =..._, _allowed_installs =..._)¶
    

Represents a container that holds application command information.

Parameters
    

  * **client** ([`Client`](../api.html#discord.Client "discord.Client")) – The client instance to get application command information from.

  * **fallback_to_global** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – If a guild-specific command is not found when invoked, then try falling back into a global command in the tree. For example, if the tree locally has a `/ping` command under the global namespace but the guild has a guild-specific `/ping`, instead of failing to find the guild-specific `/ping` command it will fall back to the global `/ping` command. This has the potential to raise more `CommandSignatureMismatch` errors than usual. Defaults to `True`.

  * **allowed_contexts** (`AppCommandContext`) – 

The default allowed contexts that applies to all commands in this tree. Note that you can override this on a per command basis.

New in version 2.4.

  * **allowed_installs** (`AppInstallationType`) – 

The default allowed install locations that apply to all commands in this tree. Note that you can override this on a per command basis.

New in version 2.4.




@command(_*_ , _name =..._, _description =..._, _nsfw =False_, _guild =..._, _guilds =..._, _auto_locale_strings =True_, _extras =..._)¶
    

A decorator that creates an application command from a regular function directly under this tree.

Parameters
    

  * **name** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The name of the application command. If not given, it defaults to a lower-case version of the callback name.

  * **description** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The description of the application command. This shows up in the UI to describe the application command. If not given, it defaults to the first line of the docstring of the callback shortened to 100 characters.

  * **nsfw** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether the command is NSFW and should only work in NSFW channels. Defaults to `False`.

Due to a Discord limitation, this does not work on subcommands.

  * **guild** (Optional[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – 

The guild to add the command to. If not given or `None` then it becomes a global command instead.

Note

Due to a Discord limitation, this keyword argument cannot be used in conjunction with contexts (e.g. `app_commands.allowed_contexts()`) or installation types (e.g. `app_commands.allowed_installs()`).

  * **guilds** (List[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – 

The list of guilds to add the command to. This cannot be mixed with the `guild` parameter. If no guilds are given at all then it becomes a global command instead.

Note

Due to a Discord limitation, this keyword argument cannot be used in conjunction with contexts (e.g. `app_commands.allowed_contexts()`) or installation types (e.g. `app_commands.allowed_installs()`).

  * **auto_locale_strings** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – If this is set to `True`, then all translatable strings will implicitly be wrapped into `locale_str` rather than [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"). This could avoid some repetition and be more ergonomic for certain defaults such as default command names, command descriptions, and parameter names. Defaults to `True`.

  * **extras** ([`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")) – A dictionary that can be used to store extraneous data. The library will not touch any values or keys within this dictionary.




@context_menu(_*_ , _name =..._, _nsfw =False_, _guild =..._, _guilds =..._, _auto_locale_strings =True_, _extras =..._)¶
    

A decorator that creates an application command context menu from a regular function directly under this tree.

This function must have a signature of `Interaction` as its first parameter and taking either a [`Member`](../api.html#discord.Member "discord.Member"), [`User`](../api.html#discord.User "discord.User"), or [`Message`](../api.html#discord.Message "discord.Message"), or a [`typing.Union`](https://docs.python.org/3/library/typing.html#typing.Union "\(in Python v3.14\)") of `Member` and `User` as its second parameter.

Examples
    
    
    @app_commands.context_menu()
    async def react(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message('Very cool message!', ephemeral=True)
    
    @app_commands.context_menu()
    async def ban(interaction: discord.Interaction, user: discord.Member):
        await interaction.response.send_message(f'Should I actually ban {user}...', ephemeral=True)
    

Parameters
    

  * **name** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The name of the context menu command. If not given, it defaults to a title-case version of the callback name. Note that unlike regular slash commands this can have spaces and upper case characters in the name.

  * **nsfw** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether the command is NSFW and should only work in NSFW channels. Defaults to `False`.

Due to a Discord limitation, this does not work on subcommands.

  * **guild** (Optional[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – 

The guild to add the command to. If not given or `None` then it becomes a global command instead.

Note

Due to a Discord limitation, this keyword argument cannot be used in conjunction with contexts (e.g. `app_commands.allowed_contexts()`) or installation types (e.g. `app_commands.allowed_installs()`).

  * **guilds** (List[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – 

The list of guilds to add the command to. This cannot be mixed with the `guild` parameter. If no guilds are given at all then it becomes a global command instead.

Note

Due to a Discord limitation, this keyword argument cannot be used in conjunction with contexts (e.g. `app_commands.allowed_contexts()`) or installation types (e.g. `app_commands.allowed_installs()`).

  * **auto_locale_strings** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – If this is set to `True`, then all translatable strings will implicitly be wrapped into `locale_str` rather than [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"). This could avoid some repetition and be more ergonomic for certain defaults such as default command names, command descriptions, and parameter names. Defaults to `True`.

  * **extras** ([`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")) – A dictionary that can be used to store extraneous data. The library will not touch any values or keys within this dictionary.




@error(_coro_)¶
    

A decorator that registers a coroutine as a local error handler.

This must match the signature of the `on_error()` callback.

The error passed will be derived from `AppCommandError`.

Parameters
    

**coro** ([coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "\(in Python v3.14\)")) – The coroutine to register as the local error handler.

Raises
    

[**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The coroutine passed is not actually a coroutine or does not match the signature.

_await _fetch_command(_command_id_ , _/_ , _*_ , _guild =None_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Fetches an application command from the application.

Parameters
    

  * **command_id** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The ID of the command to fetch.

  * **guild** (Optional[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – The guild to fetch the command from. If not passed then the global command is fetched instead.



Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Fetching the command failed.

  * [**MissingApplicationID**](../api.html#discord.MissingApplicationID "discord.MissingApplicationID") – The application ID could not be found.

  * [**NotFound**](../api.html#discord.NotFound "discord.NotFound") – The application command was not found. This could also be because the command is a guild command and the guild was not specified and vice versa.



Returns
    

The application command.

Return type
    

`AppCommand`

_await _fetch_commands(_*_ , _guild =None_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Fetches the application’s current commands.

If no guild is passed then global commands are fetched, otherwise the guild’s commands are fetched instead.

Note

This includes context menu commands.

Parameters
    

**guild** (Optional[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – The guild to fetch the commands from. If not passed then global commands are fetched instead.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Fetching the commands failed.

  * [**MissingApplicationID**](../api.html#discord.MissingApplicationID "discord.MissingApplicationID") – The application ID could not be found.



Returns
    

The application’s commands.

Return type
    

List[`AppCommand`]

copy_global_to(_*_ , _guild_)¶
    

Copies all global commands to the specified guild.

This method is mainly available for development purposes, as it allows you to copy your global commands over to a testing guild easily.

Note that this method will _override_ pre-existing guild commands that would conflict.

Parameters
    

**guild** ([`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")) – The guild to copy the commands to.

Raises
    

**CommandLimitReached** – The maximum number of commands was reached for that guild. This is currently 100 for slash commands and 15 for context menu commands.

add_command(_command_ , _/_ , _*_ , _guild =..._, _guilds =..._, _override =False_)¶
    

Adds an application command to the tree.

This only adds the command locally – in order to sync the commands and enable them in the client, `sync()` must be called.

The root parent of the command is added regardless of the type passed.

Parameters
    

  * **command** (Union[`Command`, `Group`]) – The application command or group to add.

  * **guild** (Optional[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – 

The guild to add the command to. If not given or `None` then it becomes a global command instead.

Note

Due to a Discord limitation, this keyword argument cannot be used in conjunction with contexts (e.g. `app_commands.allowed_contexts()`) or installation types (e.g. `app_commands.allowed_installs()`).

  * **guilds** (List[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – 

The list of guilds to add the command to. This cannot be mixed with the `guild` parameter. If no guilds are given at all then it becomes a global command instead.

Note

Due to a Discord limitation, this keyword argument cannot be used in conjunction with contexts (e.g. `app_commands.allowed_contexts()`) or installation types (e.g. `app_commands.allowed_installs()`).

  * **override** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether to override a command with the same name. If `False` an exception is raised. Default is `False`.



Raises
    

  * **CommandAlreadyRegistered** – The command was already registered and no override was specified.

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The application command passed is not a valid application command. Or, `guild` and `guilds` were both given.

  * **CommandLimitReached** – The maximum number of commands was reached globally or for that guild. This is currently 100 for slash commands and 15 for context menu commands.




remove_command(_command_ , _/_ , _*_ , _guild=None_ , _type= <AppCommandType.chat_input: 1>_)¶
    

Removes an application command from the tree.

This only removes the command locally – in order to sync the commands and remove them in the client, `sync()` must be called.

Parameters
    

  * **command** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The name of the root command to remove.

  * **guild** (Optional[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – The guild to remove the command from. If not given or `None` then it removes a global command instead.

  * **type** (`AppCommandType`) – The type of command to remove. Defaults to `chat_input`, i.e. slash commands.



Returns
    

The application command that got removed. If nothing was removed then `None` is returned instead.

Return type
    

Optional[Union[`Command`, `ContextMenu`, `Group`]]

clear_commands(_*_ , _guild_ , _type =None_)¶
    

Clears all application commands from the tree.

This only removes the commands locally – in order to sync the commands and remove them in the client, `sync()` must be called.

Parameters
    

  * **guild** (Optional[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – The guild to remove the commands from. If `None` then it removes all global commands instead.

  * **type** (`AppCommandType`) – The type of command to clear. If not given or `None` then it removes all commands regardless of the type.




get_command(_command_ , _/_ , _*_ , _guild=None_ , _type= <AppCommandType.chat_input: 1>_)¶
    

Gets an application command from the tree.

Parameters
    

  * **command** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The name of the root command to get.

  * **guild** (Optional[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – The guild to get the command from. If not given or `None` then it gets a global command instead.

  * **type** (`AppCommandType`) – The type of command to get. Defaults to `chat_input`, i.e. slash commands.



Returns
    

The application command that was found. If nothing was found then `None` is returned instead.

Return type
    

Optional[Union[`Command`, `ContextMenu`, `Group`]]

get_commands(_*_ , _guild =None_, _type =None_)¶
    

Gets all application commands from the tree.

Parameters
    

  * **guild** (Optional[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – The guild to get the commands from, not including global commands. If not given or `None` then only global commands are returned.

  * **type** (Optional[`AppCommandType`]) – The type of commands to get. When not given or `None`, then all command types are returned.



Returns
    

The application commands from the tree.

Return type
    

List[Union[`ContextMenu`, `Command`, `Group`]]

_for ... in _walk_commands(_*_ , _guild=None_ , _type= <AppCommandType.chat_input: 1>_)¶
    

An iterator that recursively walks through all application commands and child commands from the tree.

Parameters
    

  * **guild** (Optional[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – The guild to iterate the commands from, not including global commands. If not given or `None` then only global commands are iterated.

  * **type** (`AppCommandType`) – The type of commands to iterate over. Defaults to `chat_input`, i.e. slash commands.



Yields
    

Union[`ContextMenu`, `Command`, `Group`] – The application commands from the tree.

_await _on_error(_interaction_ , _error_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when any command raises an `AppCommandError`.

The default implementation logs the exception using the library logger if the command does not have any error handlers attached to it.

To get the command that failed, `discord.Interaction.command` should be used.

Parameters
    

  * **interaction** (`Interaction`) – The interaction that is being handled.

  * **error** (`AppCommandError`) – The exception that was raised.




_property _translator¶
    

The translator, if any, responsible for handling translation of commands.

To change the translator, use `set_translator()`.

Type
    

Optional[`Translator`]

_await _set_translator(_translator_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Sets the translator to use for translating commands.

If a translator was previously set, it will be unloaded using its `Translator.unload()` method.

When a translator is set, it will be loaded using its `Translator.load()` method.

Parameters
    

**translator** (Optional[`Translator`]) – The translator to use. If `None` then the translator is just removed and unloaded.

Raises
    

[**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The translator was not `None` or a `Translator` instance.

_await _sync(_*_ , _guild =None_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Syncs the application commands to Discord.

This also runs the translator to get the translated strings necessary for feeding back into Discord.

This must be called for the application commands to show up.

Parameters
    

**guild** (Optional[[`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – The guild to sync the commands to. If `None` then it syncs all global commands instead.

Raises
    

  * [**HTTPException**](../api.html#discord.HTTPException "discord.HTTPException") – Syncing the commands failed.

  * **CommandSyncFailure** – Syncing the commands failed due to a user related error, typically because the command has invalid data. This is equivalent to an HTTP status code of 400.

  * [**Forbidden**](../api.html#discord.Forbidden "discord.Forbidden") – The client does not have the `applications.commands` scope in the guild.

  * [**MissingApplicationID**](../api.html#discord.MissingApplicationID "discord.MissingApplicationID") – The client does not have an application ID.

  * **TranslationError** – An error occurred while translating the commands.



Returns
    

The application’s commands that got synced.

Return type
    

List[`AppCommand`]

_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A global check to determine if an `Interaction` should be processed by the tree.

The default implementation returns True (all interactions are processed), but can be overridden if custom behaviour is desired.

### Commands¶

#### Command¶

Attributes

  * allowed_contexts
  * allowed_installs
  * callback
  * checks
  * default_permissions
  * description
  * extras
  * guild_only
  * name
  * nsfw
  * parameters
  * parent
  * qualified_name
  * root_parent



Methods

  * defadd_check
  * @autocomplete
  * @error
  * defget_parameter
  * defremove_check



_class _discord.app_commands.Command(_*_ , _name_ , _description_ , _callback_ , _nsfw =False_, _parent =None_, _guild_ids =None_, _allowed_contexts =None_, _allowed_installs =None_, _auto_locale_strings =True_, _extras =..._)¶
    

A class that implements an application command.

These are usually not created manually, instead they are created using one of the following decorators:

  * `command()`

  * `Group.command`

  * `CommandTree.command`




New in version 2.0.

Parameters
    

  * **name** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The name of the application command.

  * **description** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The description of the application command. This shows up in the UI to describe the application command.

  * **callback** ([coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "\(in Python v3.14\)")) – The coroutine that is executed when the command is called.

  * **auto_locale_strings** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – If this is set to `True`, then all translatable strings will implicitly be wrapped into `locale_str` rather than [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"). This could avoid some repetition and be more ergonomic for certain defaults such as default command names, command descriptions, and parameter names. Defaults to `True`.

  * **nsfw** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether the command is NSFW and should only work in NSFW channels. Defaults to `False`.

Due to a Discord limitation, this does not work on subcommands.

  * **parent** (Optional[`Group`]) – The parent application command. `None` if there isn’t one.

  * **extras** ([`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")) – A dictionary that can be used to store extraneous data. The library will not touch any values or keys within this dictionary.




name¶
    

The name of the application command.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

description¶
    

The description of the application command. This shows up in the UI to describe the application command.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

checks¶
    

A list of predicates that take a `Interaction` parameter to indicate whether the command callback should be executed. If an exception is necessary to be thrown to signal failure, then one inherited from `AppCommandError` should be used. If all the checks fail without propagating an exception, `CheckFailure` is raised.

default_permissions¶
    

The default permissions that can execute this command on Discord. Note that server administrators can override this value in the client. Setting an empty permissions field will disallow anyone except server administrators from using the command in a guild.

Due to a Discord limitation, this does not work on subcommands.

Type
    

Optional[[`Permissions`](../api.html#discord.Permissions "discord.Permissions")]

guild_only¶
    

Whether the command should only be usable in guild contexts.

Due to a Discord limitation, this does not work on subcommands.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

allowed_contexts¶
    

The contexts that the command is allowed to be used in. Overrides `guild_only` if this is set.

New in version 2.4.

Type
    

Optional[`AppCommandContext`]

allowed_installs¶
    

The installation contexts that the command is allowed to be installed on.

New in version 2.4.

Type
    

Optional[`AppInstallationType`]

nsfw¶
    

Whether the command is NSFW and should only work in NSFW channels.

Due to a Discord limitation, this does not work on subcommands.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

parent¶
    

The parent application command. `None` if there isn’t one.

Type
    

Optional[`Group`]

extras¶
    

A dictionary that can be used to store extraneous data. The library will not touch any values or keys within this dictionary.

Type
    

[`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")

@autocomplete(_name_)¶
    

A decorator that registers a coroutine as an autocomplete prompt for a parameter.

The coroutine callback must have 2 parameters, the `Interaction`, and the current value by the user (the string currently being typed by the user).

To get the values from other parameters that may be filled in, accessing `Interaction.namespace` will give a `Namespace` object with those values.

Parent `checks` are ignored within an autocomplete. However, checks can be added to the autocomplete callback and the ones added will be called. If the checks fail for any reason then an empty list is sent as the interaction response.

The coroutine decorator **must** return a list of `Choice` objects. Only up to 25 objects are supported.

Warning

The choices returned from this coroutine are suggestions. The user may ignore them and input their own value.

Example:
    
    
    @app_commands.command()
    async def fruits(interaction: discord.Interaction, fruit: str):
        await interaction.response.send_message(f'Your favourite fruit seems to be {fruit}')
    
    @fruits.autocomplete('fruit')
    async def fruits_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        fruits = ['Banana', 'Pineapple', 'Apple', 'Watermelon', 'Melon', 'Cherry']
        return [
            app_commands.Choice(name=fruit, value=fruit)
            for fruit in fruits if current.lower() in fruit.lower()
        ]
    

Parameters
    

**name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The parameter name to register as autocomplete.

Raises
    

[**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The coroutine passed is not actually a coroutine or the parameter is not found or of an invalid type.

@error(_coro_)¶
    

A decorator that registers a coroutine as a local error handler.

The local error handler is called whenever an exception is raised in the body of the command or during handling of the command. The error handler must take 2 parameters, the interaction and the error.

The error passed will be derived from `AppCommandError`.

Parameters
    

**coro** ([coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "\(in Python v3.14\)")) – The coroutine to register as the local error handler.

Raises
    

[**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The coroutine passed is not actually a coroutine.

_property _callback¶
    

The coroutine that is executed when the command is called.

Type
    

[coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "\(in Python v3.14\)")

_property _parameters¶
    

Returns a list of parameters for this command.

This does not include the `self` or `interaction` parameters.

Returns
    

The parameters of this command.

Return type
    

List[`Parameter`]

get_parameter(_name_)¶
    

Retrieves a parameter by its name.

The name must be the Python identifier rather than the renamed one for display on Discord.

Parameters
    

**name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The parameter name in the callback function.

Returns
    

The parameter or `None` if not found.

Return type
    

Optional[`Parameter`]

_property _root_parent¶
    

The root parent of this command.

Type
    

Optional[`Group`]

_property _qualified_name¶
    

Returns the fully qualified command name.

The qualified name includes the parent name as well. For example, in a command like `/foo bar` the qualified name is `foo bar`.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

add_check(_func_ , _/_)¶
    

Adds a check to the command.

This is the non-decorator interface to `check()`.

Parameters
    

**func** – The function that will be used as a check.

remove_check(_func_ , _/_)¶
    

Removes a check from the command.

This function is idempotent and will not raise an exception if the function is not in the command’s checks.

Parameters
    

**func** – The function to remove from the checks.

#### Parameter¶

Attributes

  * autocomplete
  * channel_types
  * choices
  * command
  * default
  * description
  * display_name
  * locale_description
  * locale_name
  * max_value
  * min_value
  * name
  * required
  * type



_class _discord.app_commands.Parameter¶
    

A class that contains the parameter information of a `Command` callback.

New in version 2.0.

name¶
    

The name of the parameter. This is the Python identifier for the parameter.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

display_name¶
    

The displayed name of the parameter on Discord.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

description¶
    

The description of the parameter.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

autocomplete¶
    

Whether the parameter has an autocomplete handler.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

locale_name¶
    

The display name’s locale string, if available.

Type
    

Optional[`locale_str`]

locale_description¶
    

The description’s locale string, if available.

Type
    

Optional[`locale_str`]

required¶
    

Whether the parameter is required

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

choices¶
    

A list of choices this parameter takes, if any.

Type
    

List[`Choice`]

type¶
    

The underlying type of this parameter.

Type
    

`AppCommandOptionType`

channel_types¶
    

The channel types that are allowed for this parameter.

Type
    

List[[`ChannelType`](../api.html#discord.ChannelType "discord.ChannelType")]

min_value¶
    

The minimum supported value for this parameter.

Type
    

Optional[Union[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)"), [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]]

max_value¶
    

The maximum supported value for this parameter.

Type
    

Optional[Union[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)"), [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]]

default¶
    

The default value of the parameter, if given. If not given then this is [`MISSING`](../api.html#discord.utils.MISSING "discord.utils.MISSING").

Type
    

Any

command¶
    

The command this parameter is attached to.

Type
    

`Command`

#### ContextMenu¶

Attributes

  * allowed_contexts
  * allowed_installs
  * callback
  * checks
  * default_permissions
  * extras
  * guild_only
  * name
  * nsfw
  * qualified_name
  * type



Methods

  * defadd_check
  * @error
  * defremove_check



_class _discord.app_commands.ContextMenu(_*_ , _name_ , _callback_ , _type =..._, _nsfw =False_, _guild_ids =None_, _allowed_contexts =None_, _allowed_installs =None_, _auto_locale_strings =True_, _extras =..._)¶
    

A class that implements a context menu application command.

These are usually not created manually, instead they are created using one of the following decorators:

  * `context_menu()`

  * `CommandTree.context_menu`




New in version 2.0.

Parameters
    

  * **name** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The name of the context menu.

  * **callback** ([coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "\(in Python v3.14\)")) – The coroutine that is executed when the command is called.

  * **type** (`AppCommandType`) – The type of context menu application command. By default, this is inferred by the parameter of the callback.

  * **auto_locale_strings** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – If this is set to `True`, then all translatable strings will implicitly be wrapped into `locale_str` rather than [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"). This could avoid some repetition and be more ergonomic for certain defaults such as default command names, command descriptions, and parameter names. Defaults to `True`.

  * **nsfw** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether the command is NSFW and should only work in NSFW channels. Defaults to `False`.

  * **extras** ([`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")) – A dictionary that can be used to store extraneous data. The library will not touch any values or keys within this dictionary.




name¶
    

The name of the context menu.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

type¶
    

The type of context menu application command. By default, this is inferred by the parameter of the callback.

Type
    

`AppCommandType`

default_permissions¶
    

The default permissions that can execute this command on Discord. Note that server administrators can override this value in the client. Setting an empty permissions field will disallow anyone except server administrators from using the command in a guild.

Type
    

Optional[[`Permissions`](../api.html#discord.Permissions "discord.Permissions")]

guild_only¶
    

Whether the command should only be usable in guild contexts. Defaults to `False`.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

allowed_contexts¶
    

The contexts that this context menu is allowed to be used in. Overrides `guild_only` if set.

New in version 2.4.

Type
    

Optional[`AppCommandContext`]

allowed_installs¶
    

The installation contexts that the command is allowed to be installed on.

New in version 2.4.

Type
    

Optional[`AppInstallationType`]

nsfw¶
    

Whether the command is NSFW and should only work in NSFW channels. Defaults to `False`.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

checks¶
    

A list of predicates that take a `Interaction` parameter to indicate whether the command callback should be executed. If an exception is necessary to be thrown to signal failure, then one inherited from `AppCommandError` should be used. If all the checks fail without propagating an exception, `CheckFailure` is raised.

extras¶
    

A dictionary that can be used to store extraneous data. The library will not touch any values or keys within this dictionary.

Type
    

[`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")

@error(_coro_)¶
    

A decorator that registers a coroutine as a local error handler.

The local error handler is called whenever an exception is raised in the body of the command or during handling of the command. The error handler must take 2 parameters, the interaction and the error.

The error passed will be derived from `AppCommandError`.

Parameters
    

**coro** ([coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "\(in Python v3.14\)")) – The coroutine to register as the local error handler.

Raises
    

[**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The coroutine passed is not actually a coroutine.

_property _callback¶
    

The coroutine that is executed when the context menu is called.

Type
    

[coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "\(in Python v3.14\)")

_property _qualified_name¶
    

Returns the fully qualified command name.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

add_check(_func_ , _/_)¶
    

Adds a check to the command.

This is the non-decorator interface to `check()`.

Parameters
    

**func** – The function that will be used as a check.

remove_check(_func_ , _/_)¶
    

Removes a check from the command.

This function is idempotent and will not raise an exception if the function is not in the command’s checks.

Parameters
    

**func** – The function to remove from the checks.

#### Group¶

Attributes

  * allowed_contexts
  * allowed_installs
  * commands
  * default_permissions
  * description
  * extras
  * guild_only
  * name
  * nsfw
  * parent
  * qualified_name
  * root_parent



Methods

  * defadd_command
  * @command
  * @error
  * defget_command
  * asyncinteraction_check
  * asyncon_error
  * defremove_command
  * defwalk_commands



_class _discord.app_commands.Group(_*_ , _name =..._, _description =..._, _parent =None_, _guild_ids =None_, _guild_only =..._, _allowed_contexts =..._, _allowed_installs =..._, _nsfw =..._, _auto_locale_strings =True_, _default_permissions =..._, _extras =..._)¶
    

A class that implements an application command group.

These are usually inherited rather than created manually.

Decorators such as `guild_only()`, `guilds()`, and `default_permissions()` will apply to the group if used on top of a subclass. For example:
    
    
    from discord import app_commands
    
    @app_commands.guild_only()
    class MyGroup(app_commands.Group):
        pass
    

New in version 2.0.

Parameters
    

  * **name** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The name of the group. If not given, it defaults to a lower-case kebab-case version of the class name.

  * **description** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The description of the group. This shows up in the UI to describe the group. If not given, it defaults to the docstring of the class shortened to 100 characters.

  * **auto_locale_strings** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – If this is set to `True`, then all translatable strings will implicitly be wrapped into `locale_str` rather than [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"). This could avoid some repetition and be more ergonomic for certain defaults such as default command names, command descriptions, and parameter names. Defaults to `True`.

  * **default_permissions** (Optional[[`Permissions`](../api.html#discord.Permissions "discord.Permissions")]) – 

The default permissions that can execute this group on Discord. Note that server administrators can override this value in the client. Setting an empty permissions field will disallow anyone except server administrators from using the command in a guild.

Due to a Discord limitation, this does not work on subcommands.

  * **guild_only** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether the group should only be usable in guild contexts. Defaults to `False`.

Due to a Discord limitation, this does not work on subcommands.

  * **nsfw** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether the command is NSFW and should only work in NSFW channels. Defaults to `False`.

Due to a Discord limitation, this does not work on subcommands.

  * **parent** (Optional[`Group`]) – The parent application command. `None` if there isn’t one.

  * **extras** ([`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")) – A dictionary that can be used to store extraneous data. The library will not touch any values or keys within this dictionary.




name¶
    

The name of the group.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

description¶
    

The description of the group. This shows up in the UI to describe the group.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

default_permissions¶
    

The default permissions that can execute this group on Discord. Note that server administrators can override this value in the client. Setting an empty permissions field will disallow anyone except server administrators from using the command in a guild.

Due to a Discord limitation, this does not work on subcommands.

Type
    

Optional[[`Permissions`](../api.html#discord.Permissions "discord.Permissions")]

guild_only¶
    

Whether the group should only be usable in guild contexts.

Due to a Discord limitation, this does not work on subcommands.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

allowed_contexts¶
    

The contexts that this group is allowed to be used in. Overrides guild_only if set.

New in version 2.4.

Type
    

Optional[`AppCommandContext`]

allowed_installs¶
    

The installation contexts that the command is allowed to be installed on.

New in version 2.4.

Type
    

Optional[`AppInstallationType`]

nsfw¶
    

Whether the command is NSFW and should only work in NSFW channels.

Due to a Discord limitation, this does not work on subcommands.

Type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

parent¶
    

The parent group. `None` if there isn’t one.

Type
    

Optional[`Group`]

extras¶
    

A dictionary that can be used to store extraneous data. The library will not touch any values or keys within this dictionary.

Type
    

[`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")

@command(_*_ , _name =..._, _description =..._, _nsfw =False_, _auto_locale_strings =True_, _extras =..._)¶
    

A decorator that creates an application command from a regular function under this group.

Parameters
    

  * **name** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The name of the application command. If not given, it defaults to a lower-case version of the callback name.

  * **description** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The description of the application command. This shows up in the UI to describe the application command. If not given, it defaults to the first line of the docstring of the callback shortened to 100 characters.

  * **nsfw** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether the command is NSFW and should only work in NSFW channels. Defaults to `False`.

  * **auto_locale_strings** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – If this is set to `True`, then all translatable strings will implicitly be wrapped into `locale_str` rather than [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"). This could avoid some repetition and be more ergonomic for certain defaults such as default command names, command descriptions, and parameter names. Defaults to `True`.

  * **extras** ([`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")) – A dictionary that can be used to store extraneous data. The library will not touch any values or keys within this dictionary.




@error(_coro_)¶
    

A decorator that registers a coroutine as a local error handler.

The local error handler is called whenever an exception is raised in a child command. The error handler must take 2 parameters, the interaction and the error.

The error passed will be derived from `AppCommandError`.

Parameters
    

**coro** ([coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "\(in Python v3.14\)")) – The coroutine to register as the local error handler.

Raises
    

[**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The coroutine passed is not actually a coroutine, or is an invalid coroutine.

_property _root_parent¶
    

The parent of this group.

Type
    

Optional[`Group`]

_property _qualified_name¶
    

Returns the fully qualified group name.

The qualified name includes the parent name as well. For example, in a group like `/foo bar` the qualified name is `foo bar`.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

_property _commands¶
    

The commands that this group contains.

Type
    

List[Union[`Command`, `Group`]]

_for ... in _walk_commands()¶
    

An iterator that recursively walks through all commands that this group contains.

Yields
    

Union[`Command`, `Group`] – The commands in this group.

_await _on_error(_interaction_ , _error_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when a child’s command raises an `AppCommandError`.

To get the command that failed, `discord.Interaction.command` should be used.

The default implementation does nothing.

Parameters
    

  * **interaction** (`Interaction`) – The interaction that is being handled.

  * **error** (`AppCommandError`) – The exception that was raised.




_await _interaction_check(_interaction_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

A callback that is called when an interaction happens within the group that checks whether a command inside the group should be executed.

This is useful to override if, for example, you want to ensure that the interaction author is a given user.

The default implementation of this returns `True`.

Note

If an exception occurs within the body then the check is considered a failure and error handlers such as `on_error()` is called. See `AppCommandError` for more information.

Parameters
    

**interaction** (`Interaction`) – The interaction that occurred.

Returns
    

Whether the view children’s callbacks should be called.

Return type
    

[`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")

add_command(_command_ , _/_ , _*_ , _override =False_)¶
    

Adds a command or group to this group’s internal list of commands.

Parameters
    

  * **command** (Union[`Command`, `Group`]) – The command or group to add.

  * **override** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Whether to override a pre-existing command or group with the same name. If `False` then an exception is raised.



Raises
    

  * **CommandAlreadyRegistered** – The command or group is already registered. Note that the `CommandAlreadyRegistered.guild_id` attribute will always be `None` in this case.

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – There are too many commands already registered or the group is too deeply nested.

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The wrong command type was passed.




remove_command(_name_ , _/_)¶
    

Removes a command or group from the internal list of commands.

Parameters
    

**name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The name of the command or group to remove.

Returns
    

The command that was removed. If nothing was removed then `None` is returned instead.

Return type
    

Optional[Union[`Command`, `Group`]]

get_command(_name_ , _/_)¶
    

Retrieves a command or group from its name.

Parameters
    

**name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The name of the command or group to retrieve.

Returns
    

The command or group that was retrieved. If nothing was found then `None` is returned instead.

Return type
    

Optional[Union[`Command`, `Group`]]

### Decorators¶

@discord.app_commands.command(_*_ , _name =..._, _description =..._, _nsfw =False_, _auto_locale_strings =True_, _extras =..._)¶
    

Creates an application command from a regular function.

Parameters
    

  * **name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The name of the application command. If not given, it defaults to a lower-case version of the callback name.

  * **description** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")) – The description of the application command. This shows up in the UI to describe the application command. If not given, it defaults to the first line of the docstring of the callback shortened to 100 characters.

  * **nsfw** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether the command is NSFW and should only work in NSFW channels. Defaults to `False`.

Due to a Discord limitation, this does not work on subcommands.

  * **auto_locale_strings** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – If this is set to `True`, then all translatable strings will implicitly be wrapped into `locale_str` rather than [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"). This could avoid some repetition and be more ergonomic for certain defaults such as default command names, command descriptions, and parameter names. Defaults to `True`.

  * **extras** ([`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")) – A dictionary that can be used to store extraneous data. The library will not touch any values or keys within this dictionary.




@discord.app_commands.context_menu(_*_ , _name =..._, _nsfw =False_, _auto_locale_strings =True_, _extras =..._)¶
    

Creates an application command context menu from a regular function.

This function must have a signature of `Interaction` as its first parameter and taking either a [`Member`](../api.html#discord.Member "discord.Member"), [`User`](../api.html#discord.User "discord.User"), or [`Message`](../api.html#discord.Message "discord.Message"), or a [`typing.Union`](https://docs.python.org/3/library/typing.html#typing.Union "\(in Python v3.14\)") of `Member` and `User` as its second parameter.

Examples
    
    
    @app_commands.context_menu()
    async def react(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message('Very cool message!', ephemeral=True)
    
    @app_commands.context_menu()
    async def ban(interaction: discord.Interaction, user: discord.Member):
        await interaction.response.send_message(f'Should I actually ban {user}...', ephemeral=True)
    

Parameters
    

  * **name** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The name of the context menu command. If not given, it defaults to a title-case version of the callback name. Note that unlike regular slash commands this can have spaces and upper case characters in the name.

  * **nsfw** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – 

Whether the command is NSFW and should only work in NSFW channels. Defaults to `False`.

Due to a Discord limitation, this does not work on subcommands.

  * **auto_locale_strings** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – If this is set to `True`, then all translatable strings will implicitly be wrapped into `locale_str` rather than [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"). This could avoid some repetition and be more ergonomic for certain defaults such as default command names, command descriptions, and parameter names. Defaults to `True`.

  * **extras** ([`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")) – A dictionary that can be used to store extraneous data. The library will not touch any values or keys within this dictionary.




@discord.app_commands.describe(_** parameters_)¶
    

Describes the given parameters by their name using the key of the keyword argument as the name.

Example:
    
    
    @app_commands.command(description='Bans a member')
    @app_commands.describe(member='the member to ban')
    async def ban(interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f'Banned {member}')
    

Alternatively, you can describe parameters using Google, Sphinx, or Numpy style docstrings.

Example:
    
    
    @app_commands.command()
    async def ban(interaction: discord.Interaction, member: discord.Member):
        """Bans a member
    
        Parameters
        -----------
        member: discord.Member
            the member to ban
        """
        await interaction.response.send_message(f'Banned {member}')
    

Parameters
    

****parameters** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The description of the parameters.

Raises
    

[**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The parameter name is not found.

@discord.app_commands.rename(_** parameters_)¶
    

Renames the given parameters by their name using the key of the keyword argument as the name.

This renames the parameter within the Discord UI. When referring to the parameter in other decorators, the parameter name used in the function is used instead of the renamed one.

Example:
    
    
    @app_commands.command()
    @app_commands.rename(the_member_to_ban='member')
    async def ban(interaction: discord.Interaction, the_member_to_ban: discord.Member):
        await interaction.response.send_message(f'Banned {the_member_to_ban}')
    

Parameters
    

****parameters** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]) – The name of the parameters.

Raises
    

  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "\(in Python v3.14\)") – The parameter name is already used by another parameter.

  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The parameter name is not found.




@discord.app_commands.choices(_** parameters_)¶
    

Instructs the given parameters by their name to use the given choices for their choices.

Example:
    
    
    @app_commands.command()
    @app_commands.describe(fruits='fruits to choose from')
    @app_commands.choices(fruits=[
        Choice(name='apple', value=1),
        Choice(name='banana', value=2),
        Choice(name='cherry', value=3),
    ])
    async def fruit(interaction: discord.Interaction, fruits: Choice[int]):
        await interaction.response.send_message(f'Your favourite fruit is {fruits.name}.')
    

Note

This is not the only way to provide choices to a command. There are two more ergonomic ways of doing this. The first one is to use a [`typing.Literal`](https://docs.python.org/3/library/typing.html#typing.Literal "\(in Python v3.14\)") annotation:
    
    
    @app_commands.command()
    @app_commands.describe(fruits='fruits to choose from')
    async def fruit(interaction: discord.Interaction, fruits: Literal['apple', 'banana', 'cherry']):
        await interaction.response.send_message(f'Your favourite fruit is {fruits}.')
    

The second way is to use an [`enum.Enum`](https://docs.python.org/3/library/enum.html#enum.Enum "\(in Python v3.14\)"):
    
    
    class Fruits(enum.Enum):
        apple = 1
        banana = 2
        cherry = 3
    
    @app_commands.command()
    @app_commands.describe(fruits='fruits to choose from')
    async def fruit(interaction: discord.Interaction, fruits: Fruits):
        await interaction.response.send_message(f'Your favourite fruit is {fruits}.')
    

Parameters
    

****parameters** – The choices of the parameters.

Raises
    

[**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The parameter name is not found or the parameter type was incorrect.

@discord.app_commands.autocomplete(_** parameters_)¶
    

Associates the given parameters with the given autocomplete callback.

Autocomplete is only supported on types that have [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)"), or [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)") values.

`Checks` are supported, however they must be attached to the autocomplete callback in order to work. Checks attached to the command are ignored when invoking the autocomplete callback.

For more information, see the `Command.autocomplete()` documentation.

Warning

The choices returned from this coroutine are suggestions. The user may ignore them and input their own value.

Example:
    
    
    async def fruit_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        fruits = ['Banana', 'Pineapple', 'Apple', 'Watermelon', 'Melon', 'Cherry']
        return [
            app_commands.Choice(name=fruit, value=fruit)
            for fruit in fruits if current.lower() in fruit.lower()
        ]
    
    @app_commands.command()
    @app_commands.autocomplete(fruit=fruit_autocomplete)
    async def fruits(interaction: discord.Interaction, fruit: str):
        await interaction.response.send_message(f'Your favourite fruit seems to be {fruit}')
    

Parameters
    

****parameters** – The parameters to mark as autocomplete.

Raises
    

[**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "\(in Python v3.14\)") – The parameter name is not found or the parameter type was incorrect.

@discord.app_commands.guilds(_* guild_ids_)¶
    

Associates the given guilds with the command.

When the command instance is added to a `CommandTree`, the guilds that are specified by this decorator become the default guilds that it’s added to rather than being a global command.

If no arguments are given, then the command will not be synced anywhere. This may be modified later using the `CommandTree.add_command()` method.

Note

Due to an implementation quirk and Python limitation, if this is used in conjunction with the `CommandTree.command()` or `CommandTree.context_menu()` decorator then this must go below that decorator.

Note

Due to a Discord limitation, this decorator cannot be used in conjunction with contexts (e.g. `app_commands.allowed_contexts()`) or installation types (e.g. `app_commands.allowed_installs()`).

Example:
    
    
    MY_GUILD_ID = discord.Object(...)  # Guild ID here
    
    @app_commands.command()
    @app_commands.guilds(MY_GUILD_ID)
    async def bonk(interaction: discord.Interaction):
        await interaction.response.send_message('Bonk', ephemeral=True)
    

Parameters
    

***guild_ids** (Union[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)"), [`Snowflake`](../api.html#discord.abc.Snowflake "discord.abc.Snowflake")]) – The guilds to associate this command with. The command tree will use this as the default when added rather than adding it as a global command.

@discord.app_commands.guild_only(_func =None_)¶
    

A decorator that indicates this command can only be used in a guild context.

This is **not** implemented as a `check()`, and is instead verified by Discord server side. Therefore, there is no error handler called when a command is used within a private message.

This decorator can be called with or without parentheses.

Due to a Discord limitation, this decorator does nothing in subcommands and is ignored.

Examples
    
    
    @app_commands.command()
    @app_commands.guild_only()
    async def my_guild_only_command(interaction: discord.Interaction) -> None:
        await interaction.response.send_message('I am only available in guilds!')
    

@discord.app_commands.dm_only(_func =None_)¶
    

A decorator that indicates this command can only be used in the context of bot DMs.

This is **not** implemented as a `check()`, and is instead verified by Discord server side. Therefore, there is no error handler called when a command is used within a guild or group DM.

This decorator can be called with or without parentheses.

Due to a Discord limitation, this decorator does nothing in subcommands and is ignored.

Examples
    
    
    @app_commands.command()
    @app_commands.dm_only()
    async def my_dm_only_command(interaction: discord.Interaction) -> None:
        await interaction.response.send_message('I am only available in DMs!')
    

@discord.app_commands.private_channel_only(_func =None_)¶
    

A decorator that indicates this command can only be used in the context of DMs and group DMs.

This is **not** implemented as a `check()`, and is instead verified by Discord server side. Therefore, there is no error handler called when a command is used within a guild.

This decorator can be called with or without parentheses.

Due to a Discord limitation, this decorator does nothing in subcommands and is ignored.

New in version 2.4.

Examples
    
    
    @app_commands.command()
    @app_commands.private_channel_only()
    async def my_private_channel_only_command(interaction: discord.Interaction) -> None:
        await interaction.response.send_message('I am only available in DMs and GDMs!')
    

@discord.app_commands.allowed_contexts(_guilds =..._, _dms =..._, _private_channels =..._)¶
    

A decorator that indicates this command can only be used in certain contexts. Valid contexts are guilds, DMs and private channels.

This is **not** implemented as a `check()`, and is instead verified by Discord server side.

Due to a Discord limitation, this decorator does nothing in subcommands and is ignored.

New in version 2.4.

Examples
    
    
    @app_commands.command()
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    async def my_command(interaction: discord.Interaction) -> None:
        await interaction.response.send_message('I am only available in guilds and private channels!')
    

@discord.app_commands.user_install(_func =None_)¶
    

A decorator that indicates this command should be installed for users.

This is **not** implemented as a `check()`, and is instead verified by Discord server side.

Due to a Discord limitation, this decorator does nothing in subcommands and is ignored.

New in version 2.4.

Examples
    
    
    @app_commands.command()
    @app_commands.user_install()
    async def my_user_install_command(interaction: discord.Interaction) -> None:
        await interaction.response.send_message('I am installed in users by default!')
    

@discord.app_commands.guild_install(_func =None_)¶
    

A decorator that indicates this command should be installed in guilds.

This is **not** implemented as a `check()`, and is instead verified by Discord server side.

Due to a Discord limitation, this decorator does nothing in subcommands and is ignored.

New in version 2.4.

Examples
    
    
    @app_commands.command()
    @app_commands.guild_install()
    async def my_guild_install_command(interaction: discord.Interaction) -> None:
        await interaction.response.send_message('I am installed in guilds by default!')
    

@discord.app_commands.allowed_installs(_guilds =..._, _users =..._)¶
    

A decorator that indicates this command should be installed in certain contexts. Valid contexts are guilds and users.

This is **not** implemented as a `check()`, and is instead verified by Discord server side.

Due to a Discord limitation, this decorator does nothing in subcommands and is ignored.

New in version 2.4.

Examples
    
    
    @app_commands.command()
    @app_commands.allowed_installs(guilds=False, users=True)
    async def my_command(interaction: discord.Interaction) -> None:
        await interaction.response.send_message('I am installed in users by default!')
    

@discord.app_commands.default_permissions(_perms_obj =None_, _/_ , _** perms_)¶
    

A decorator that sets the default permissions needed to execute this command.

When this decorator is used, by default users must have these permissions to execute the command. However, an administrator can change the permissions needed to execute this command using the official client. Therefore, this only serves as a hint.

Setting an empty permissions field, including via calling this with no arguments, will disallow anyone except server administrators from using the command in a guild.

This is sent to Discord server side, and is not a `check()`. Therefore, error handlers are not called.

Due to a Discord limitation, this decorator does nothing in subcommands and is ignored.

Warning

This serves as a _hint_ and members are _not_ required to have the permissions given to actually execute this command. If you want to ensure that members have the permissions needed, consider using `has_permissions()` instead.

Parameters
    

  * ****perms** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Keyword arguments denoting the permissions to set as the default.

  * **perms_obj** ([`Permissions`](../api.html#discord.Permissions "discord.Permissions")) – 

A permissions object as positional argument. This can be used in combination with `**perms`.

New in version 2.5.




Examples
    
    
    @app_commands.command()
    @app_commands.default_permissions(manage_messages=True)
    async def test(interaction: discord.Interaction):
        await interaction.response.send_message('You may or may not have manage messages.')
    
    
    
    ADMIN_PERMS = discord.Permissions(administrator=True)
    
    @app_commands.command()
    @app_commands.default_permissions(ADMIN_PERMS, manage_messages=True)
    async def test(interaction: discord.Interaction):
        await interaction.response.send_message('You may or may not have manage messages.')
    

### Checks¶

@discord.app_commands.check(_predicate_)¶
    

A decorator that adds a check to an application command.

These checks should be predicates that take in a single parameter taking a `Interaction`. If the check returns a `False`-like value then during invocation a `CheckFailure` exception is raised and sent to the appropriate error handlers.

These checks can be either a coroutine or not.

Examples

Creating a basic check to see if the command invoker is you.
    
    
    def check_if_it_is_me(interaction: discord.Interaction) -> bool:
        return interaction.user.id == 85309593344815104
    
    @tree.command()
    @app_commands.check(check_if_it_is_me)
    async def only_for_me(interaction: discord.Interaction):
        await interaction.response.send_message('I know you!', ephemeral=True)
    

Transforming common checks into its own decorator:
    
    
    def is_me():
        def predicate(interaction: discord.Interaction) -> bool:
            return interaction.user.id == 85309593344815104
        return app_commands.check(predicate)
    
    @tree.command()
    @is_me()
    async def only_me(interaction: discord.Interaction):
        await interaction.response.send_message('Only you!')
    

Parameters
    

**predicate** (Callable[[`Interaction`], [`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")]) – The predicate to check if the command should be invoked.

@discord.app_commands.checks.has_role(_item_ , _/_)¶
    

A `check()` that is added that checks if the member invoking the command has the role specified via the name or ID specified.

If a string is specified, you must give the exact name of the role, including caps and spelling.

If an integer is specified, you must give the exact snowflake ID of the role.

This check raises one of two special exceptions, `MissingRole` if the user is missing a role, or `NoPrivateMessage` if it is used in a private message. Both inherit from `CheckFailure`.

New in version 2.0.

Note

This is different from the permission system that Discord provides for application commands. This is done entirely locally in the program rather than being handled by Discord.

Parameters
    

**item** (Union[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]) – The name or ID of the role to check.

@discord.app_commands.checks.has_any_role(_* items_)¶
    

A `check()` that is added that checks if the member invoking the command has **any** of the roles specified. This means that if they have one out of the three roles specified, then this check will return `True`.

Similar to `has_role()`, the names or IDs passed in must be exact.

This check raises one of two special exceptions, `MissingAnyRole` if the user is missing all roles, or `NoPrivateMessage` if it is used in a private message. Both inherit from `CheckFailure`.

New in version 2.0.

Note

This is different from the permission system that Discord provides for application commands. This is done entirely locally in the program rather than being handled by Discord.

Parameters
    

**items** (List[Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]]) – An argument list of names or IDs to check that the member has roles wise.

Example
    
    
    @tree.command()
    @app_commands.checks.has_any_role('Library Devs', 'Moderators', 492212595072434186)
    async def cool(interaction: discord.Interaction):
        await interaction.response.send_message('You are cool indeed')
    

@discord.app_commands.checks.has_permissions(_** perms_)¶
    

A `check()` that is added that checks if the member has all of the permissions necessary.

Note that this check operates on the permissions given by `discord.Interaction.permissions`.

The permissions passed in must be exactly like the properties shown under [`discord.Permissions`](../api.html#discord.Permissions "discord.Permissions").

This check raises a special exception, `MissingPermissions` that is inherited from `CheckFailure`.

New in version 2.0.

Note

This is different from the permission system that Discord provides for application commands. This is done entirely locally in the program rather than being handled by Discord.

Parameters
    

****perms** ([`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")) – Keyword arguments denoting the permissions to check for.

Example
    
    
    @tree.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    async def test(interaction: discord.Interaction):
        await interaction.response.send_message('You can manage messages.')
    

@discord.app_commands.checks.bot_has_permissions(_** perms_)¶
    

Similar to `has_permissions()` except checks if the bot itself has the permissions listed. This relies on `discord.Interaction.app_permissions`.

This check raises a special exception, `BotMissingPermissions` that is inherited from `CheckFailure`.

New in version 2.0.

@discord.app_commands.checks.cooldown(_rate_ , _per_ , _*_ , _key =..._)¶
    

A decorator that adds a cooldown to a command.

A cooldown allows a command to only be used a specific amount of times in a specific time frame. These cooldowns are based off of the `key` function provided. If a `key` is not provided then it defaults to a user-level cooldown. The `key` function must take a single parameter, the `discord.Interaction` and return a value that is used as a key to the internal cooldown mapping.

The `key` function can optionally be a coroutine.

If a cooldown is triggered, then `CommandOnCooldown` is raised to the error handlers.

Examples

Setting a one per 5 seconds per member cooldown on a command:
    
    
    @tree.command()
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def test(interaction: discord.Interaction):
        await interaction.response.send_message('Hello')
    
    @test.error
    async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(str(error), ephemeral=True)
    

Parameters
    

  * **rate** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The number of times a command can be used before triggering a cooldown.

  * **per** ([`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")) – The amount of seconds to wait for a cooldown when it’s been triggered.

  * **key** (Optional[Callable[[`discord.Interaction`], [`collections.abc.Hashable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Hashable "\(in Python v3.14\)")]]) – A function that returns a key to the mapping denoting the type of cooldown. Can optionally be a coroutine. If not given then defaults to a user-level cooldown. If `None` is passed then it is interpreted as a “global” cooldown.




@discord.app_commands.checks.dynamic_cooldown(_factory_ , _*_ , _key =..._)¶
    

A decorator that adds a dynamic cooldown to a command.

A cooldown allows a command to only be used a specific amount of times in a specific time frame. These cooldowns are based off of the `key` function provided. If a `key` is not provided then it defaults to a user-level cooldown. The `key` function must take a single parameter, the `discord.Interaction` and return a value that is used as a key to the internal cooldown mapping.

If a `factory` function is given, it must be a function that accepts a single parameter of type `discord.Interaction` and must return a `Cooldown` or `None`. If `None` is returned then that cooldown is effectively bypassed.

Both `key` and `factory` can optionally be coroutines.

If a cooldown is triggered, then `CommandOnCooldown` is raised to the error handlers.

Examples

Setting a cooldown for everyone but the owner.
    
    
    def cooldown_for_everyone_but_me(interaction: discord.Interaction) -> Optional[app_commands.Cooldown]:
        if interaction.user.id == 80088516616269824:
            return None
        return app_commands.Cooldown(1, 10.0)
    
    @tree.command()
    @app_commands.checks.dynamic_cooldown(cooldown_for_everyone_but_me)
    async def test(interaction: discord.Interaction):
        await interaction.response.send_message('Hello')
    
    @test.error
    async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(str(error), ephemeral=True)
    

Parameters
    

  * **factory** (Optional[Callable[[`discord.Interaction`], Optional[`Cooldown`]]]) – A function that takes an interaction and returns a cooldown that will apply to that interaction or `None` if the interaction should not have a cooldown.

  * **key** (Optional[Callable[[`discord.Interaction`], [`collections.abc.Hashable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Hashable "\(in Python v3.14\)")]]) – A function that returns a key to the mapping denoting the type of cooldown. Can optionally be a coroutine. If not given then defaults to a user-level cooldown. If `None` is passed then it is interpreted as a “global” cooldown.




### Cooldown¶

Attributes

  * per
  * rate



Methods

  * defcopy
  * defget_retry_after
  * defget_tokens
  * defreset
  * defupdate_rate_limit



_class _discord.app_commands.Cooldown(_rate_ , _per_)¶
    

Represents a cooldown for a command.

New in version 2.0.

rate¶
    

The total number of tokens available per `per` seconds.

Type
    

[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")

per¶
    

The length of the cooldown period in seconds.

Type
    

[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")

get_tokens(_current =None_)¶
    

Returns the number of available tokens before rate limiting is applied.

Parameters
    

**current** (Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]) – The time in seconds since Unix epoch to calculate tokens at. If not supplied then [`time.time()`](https://docs.python.org/3/library/time.html#time.time "\(in Python v3.14\)") is used.

Returns
    

The number of tokens available before the cooldown is to be applied.

Return type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

get_retry_after(_current =None_)¶
    

Returns the time in seconds until the cooldown will be reset.

Parameters
    

**current** (Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]) – The current time in seconds since Unix epoch. If not supplied, then [`time.time()`](https://docs.python.org/3/library/time.html#time.time "\(in Python v3.14\)") is used.

Returns
    

The number of seconds to wait before this cooldown will be reset.

Return type
    

[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")

update_rate_limit(_current =None_, _*_ , _tokens =1_)¶
    

Updates the cooldown rate limit.

Parameters
    

  * **current** (Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]) – The time in seconds since Unix epoch to update the rate limit at. If not supplied, then [`time.time()`](https://docs.python.org/3/library/time.html#time.time "\(in Python v3.14\)") is used.

  * **tokens** ([`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")) – The amount of tokens to deduct from the rate limit.



Returns
    

The retry-after time in seconds if rate limited.

Return type
    

Optional[[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]

reset()¶
    

Reset the cooldown to its initial state.

copy()¶
    

Creates a copy of this cooldown.

Returns
    

A new instance of this cooldown.

Return type
    

`Cooldown`

### Namespace¶

_class _discord.app_commands.Namespace¶
    

An object that holds the parameters being passed to a command in a mostly raw state.

This class is deliberately simple and just holds the option name and resolved value as a simple key-pair mapping. These attributes can be accessed using dot notation. For example, an option with the name of `example` can be accessed using `ns.example`. If an attribute is not found, then `None` is returned rather than an attribute error.

Warning

The key names come from the raw Discord data, which means that if a parameter was renamed then the renamed key is used instead of the function parameter name.

New in version 2.0.

x == y
    

Checks if two namespaces are equal by checking if all attributes are equal.

x != y
    

Checks if two namespaces are not equal.

x[key]
    

Returns an attribute if it is found, otherwise raises a [`KeyError`](https://docs.python.org/3/library/exceptions.html#KeyError "\(in Python v3.14\)").

key in x
    

Checks if the attribute is in the namespace.

iter(x)
    

Returns an iterator of `(name, value)` pairs. This allows it to be, for example, constructed as a dict or a list of pairs.

This namespace object converts resolved objects into their appropriate form depending on their type. Consult the table below for conversion information.

Option Type | Resolved Type  
---|---  
`AppCommandOptionType.string` | [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")  
`AppCommandOptionType.integer` | [`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")  
`AppCommandOptionType.boolean` | [`bool`](https://docs.python.org/3/library/functions.html#bool "\(in Python v3.14\)")  
`AppCommandOptionType.number` | [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")  
`AppCommandOptionType.user` | [`User`](../api.html#discord.User "discord.User") or [`Member`](../api.html#discord.Member "discord.Member")  
`AppCommandOptionType.channel` | `AppCommandChannel` or `AppCommandThread`  
`AppCommandOptionType.role` | [`Role`](../api.html#discord.Role "discord.Role")  
`AppCommandOptionType.mentionable` | [`User`](../api.html#discord.User "discord.User") or [`Member`](../api.html#discord.Member "discord.Member"), or [`Role`](../api.html#discord.Role "discord.Role")  
`AppCommandOptionType.attachment` | [`Attachment`](../api.html#discord.Attachment "discord.Attachment")  
  
Note

In autocomplete interactions, the namespace might not be validated or filled in. Discord does not send the resolved data as well, so this means that certain fields end up just as IDs rather than the resolved data. In these cases, a [`discord.Object`](../api.html#discord.Object "discord.Object") is returned instead.

This is a Discord limitation.

### Transformers¶

#### Transformer¶

Attributes

  * channel_types
  * choices
  * max_value
  * min_value
  * type



Methods

  * asyncautocomplete
  * asynctransform



_class _discord.app_commands.Transformer(_* args_, _** kwds_)¶
    

The base class that allows a type annotation in an application command parameter to map into a `AppCommandOptionType` and transform the raw value into one from this type.

This class is customisable through the overriding of methods and properties in the class and by using it as the second type parameter of the `Transform` class. For example, to convert a string into a custom pair type:
    
    
    class Point(typing.NamedTuple):
        x: int
        y: int
    
    class PointTransformer(app_commands.Transformer):
        async def transform(self, interaction: discord.Interaction, value: str) -> Point:
            (x, _, y) = value.partition(',')
            return Point(x=int(x.strip()), y=int(y.strip()))
    
    @app_commands.command()
    async def graph(
        interaction: discord.Interaction,
        point: app_commands.Transform[Point, PointTransformer],
    ):
        await interaction.response.send_message(str(point))
    

If a class is passed instead of an instance to the second type parameter, then it is constructed with no arguments passed to the `__init__` method.

New in version 2.0.

_property _type¶
    

The option type associated with this transformer.

This must be a [`property`](https://docs.python.org/3/library/functions.html#property "\(in Python v3.14\)").

Defaults to `string`.

Type
    

`AppCommandOptionType`

_property _channel_types¶
    

A list of channel types that are allowed to this parameter.

Only valid if the `type()` returns `channel`.

This must be a [`property`](https://docs.python.org/3/library/functions.html#property "\(in Python v3.14\)").

Defaults to an empty list.

Type
    

List[[`ChannelType`](../api.html#discord.ChannelType "discord.ChannelType")]

_property _min_value¶
    

The minimum supported value for this parameter.

Only valid if the `type()` returns `number` `integer`, or `string`.

This must be a [`property`](https://docs.python.org/3/library/functions.html#property "\(in Python v3.14\)").

Defaults to `None`.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _max_value¶
    

The maximum supported value for this parameter.

Only valid if the `type()` returns `number` `integer`, or `string`.

This must be a [`property`](https://docs.python.org/3/library/functions.html#property "\(in Python v3.14\)").

Defaults to `None`.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_property _choices¶
    

A list of up to 25 choices that are allowed to this parameter.

Only valid if the `type()` returns `number` `integer`, or `string`.

This must be a [`property`](https://docs.python.org/3/library/functions.html#property "\(in Python v3.14\)").

Defaults to `None`.

Type
    

Optional[List[`Choice`]]

_await _transform(_interaction_ , _value_ , _/_)¶
    

This function _could be a_ [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Transforms the converted option value into another value.

The value passed into this transform function is the same as the one in the `conversion table`.

Parameters
    

  * **interaction** (`Interaction`) – The interaction being handled.

  * **value** (_Any_) – The value of the given argument after being resolved. See the `conversion table` for how certain option types correspond to certain values.




_await _autocomplete(_interaction_ , _value_ , _/_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

An autocomplete prompt handler to be automatically used by options using this transformer.

Note

Autocomplete is only supported for options with a `type()` of `string`, `integer`, or `number`.

Parameters
    

  * **interaction** (`Interaction`) – The autocomplete interaction being handled.

  * **value** (Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)"), [`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")]) – The current value entered by the user.



Returns
    

A list of choices to be displayed to the user, a maximum of 25.

Return type
    

List[`Choice`]

#### Transform¶

_class _discord.app_commands.Transform¶
    

A type annotation that can be applied to a parameter to customise the behaviour of an option type by transforming with the given `Transformer`. This requires the usage of two generic parameters, the first one is the type you’re converting to and the second one is the type of the `Transformer` actually doing the transformation.

During type checking time this is equivalent to [`typing.Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated "\(in Python v3.14\)") so type checkers understand the intent of the code.

For example usage, check `Transformer`.

New in version 2.0.

#### Range¶

_class _discord.app_commands.Range¶
    

A type annotation that can be applied to a parameter to require a numeric or string type to fit within the range provided.

During type checking time this is equivalent to [`typing.Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated "\(in Python v3.14\)") so type checkers understand the intent of the code.

Some example ranges:

  * `Range[int, 10]` means the minimum is 10 with no maximum.

  * `Range[int, None, 10]` means the maximum is 10 with no minimum.

  * `Range[int, 1, 10]` means the minimum is 1 and the maximum is 10.

  * `Range[float, 1.0, 5.0]` means the minimum is 1.0 and the maximum is 5.0.

  * `Range[str, 1, 10]` means the minimum length is 1 and the maximum length is 10.




New in version 2.0.

Examples
    
    
    @app_commands.command()
    async def range(interaction: discord.Interaction, value: app_commands.Range[int, 10, 12]):
        await interaction.response.send_message(f'Your value is {value}', ephemeral=True)
    

#### Timestamp¶

Attributes

  * type



Methods

  * asynctransform



_class _discord.app_commands.Timestamp(_* args_, _** kwds_)¶
    

A type annotation that can be applied to a parameter for transforming a [Discord style timestamp](https://discord.com/developers/docs/reference#message-formatting) input to a [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "\(in Python v3.14\)").

New in version 2.7.

Warning

Due to a Discord limitation, no timezone is provided with the input. The UTC timezone has been supplanted instead.

Examples
    
    
    @app_commands.command()
    async def datetime(interaction: discord.Interaction, value: app_commands.Timestamp):
        await interaction.response.send_message(value.isoformat())
    

_property _type¶
    

The option type associated with this transformer.

This must be a [`property`](https://docs.python.org/3/library/functions.html#property "\(in Python v3.14\)").

Defaults to `string`.

Type
    

`AppCommandOptionType`

_await _transform(_interaction_ , _value_ , _/_)¶
    

This function _could be a_ [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Transforms the converted option value into another value.

The value passed into this transform function is the same as the one in the `conversion table`.

Parameters
    

  * **interaction** (`Interaction`) – The interaction being handled.

  * **value** (_Any_) – The value of the given argument after being resolved. See the `conversion table` for how certain option types correspond to certain values.




### Translations¶

#### Translator¶

Methods

  * asyncload
  * asynctranslate
  * asyncunload



_class _discord.app_commands.Translator¶
    

A class that handles translations for commands, parameters, and choices.

Translations are done lazily in order to allow for async enabled translations as well as supporting a wide array of translation systems such as [`gettext`](https://docs.python.org/3/library/gettext.html#module-gettext "\(in Python v3.14\)") and [Project Fluent](https://projectfluent.org).

In order for a translator to be used, it must be set using the `CommandTree.set_translator()` method. The translation flow for a string is as follows:

  1. Use `locale_str` instead of [`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)") in areas of a command you want to be translated.
    
     * Currently, these are command names, command descriptions, parameter names, parameter descriptions, and choice names.

     * This can also be used inside the `describe()` decorator.

  2. Call `CommandTree.set_translator()` to the translator instance that will handle the translations.

  3. Call `CommandTree.sync()`

  4. The library will call `Translator.translate()` on all the relevant strings being translated.




New in version 2.0.

_await _load()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

An asynchronous setup function for loading the translation system.

The default implementation does nothing.

This is invoked when `CommandTree.set_translator()` is called.

_await _unload()¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

An asynchronous teardown function for unloading the translation system.

The default implementation does nothing.

This is invoked when `CommandTree.set_translator()` is called if a tree already has a translator or when [`discord.Client.close()`](../api.html#discord.Client.close "discord.Client.close") is called.

_await _translate(_string_ , _locale_ , _context_)¶
    

This function is a [_coroutine_](https://docs.python.org/3/library/asyncio-task.html#coroutine).

Translates the given string to the specified locale.

If the string cannot be translated, `None` should be returned.

The default implementation returns `None`.

If an exception is raised in this method, it should inherit from `TranslationError`. If it doesn’t, then when this is called the exception will be chained with it instead.

Parameters
    

  * **string** (`locale_str`) – The string being translated.

  * **locale** ([`Locale`](../api.html#discord.Locale "discord.Locale")) – The locale being requested for translation.

  * **context** (`TranslationContext`) – The translation context where the string originated from. For better type checking ergonomics, the `TranslationContextTypes` type can be used instead to aid with type narrowing. It is functionally equivalent to `TranslationContext`.




#### locale_str¶

Attributes

  * extras
  * message



_class _discord.app_commands.locale_str(_message_ , _/_ , _** kwargs_)¶
    

Marks a string as ready for translation.

This is done lazily and is not actually translated until `CommandTree.sync()` is called.

The sync method then ultimately defers the responsibility of translating to the `Translator` instance used by the `CommandTree`. For more information on the translation flow, see the `Translator` documentation.

str(x)
    

Returns the message passed to the string.

x == y
    

Checks if the string is equal to another string.

x != y
    

Checks if the string is not equal to another string.

hash(x)
    

Returns the hash of the string.

New in version 2.0.

message¶
    

The message being translated. Once set, this cannot be changed.

Warning

This must be the default “message” that you send to Discord. Discord sends this message back to the library and the library uses it to access the data in order to dispatch commands.

For example, in a command name context, if the command name is `foo` then the message _must_ also be `foo`. For other translation systems that require a message ID such as Fluent, consider using a keyword argument to pass it in.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

extras¶
    

A dict of user provided extras to attach to the translated string. This can be used to add more context, information, or any metadata necessary to aid in actually translating the string.

Since these are passed via keyword arguments, the keys are strings.

Type
    

[`dict`](https://docs.python.org/3/library/stdtypes.html#dict "\(in Python v3.14\)")

#### TranslationContext¶

Attributes

  * data
  * location



_class _discord.app_commands.TranslationContext(_location_ , _data_)¶
    

A class that provides context for the `locale_str` being translated.

This is useful to determine where exactly the string is located and aid in looking up the actual translation.

location¶
    

The location where this string is located.

Type
    

`TranslationContextLocation`

data¶
    

The extraneous data that is being translated.

Type
    

Any

#### TranslationContextLocation¶

_class _discord.app_commands.TranslationContextLocation¶
    

An enum representing the location context that the translation occurs in when requested for translation.

New in version 2.0.

command_name¶
    

The translation involved a command name.

command_description¶
    

The translation involved a command description.

group_name¶
    

The translation involved a group name.

group_description¶
    

The translation involved a group description.

parameter_name¶
    

The translation involved a parameter name.

parameter_description¶
    

The translation involved a parameter description.

choice_name¶
    

The translation involved a choice name.

other¶
    

The translation involved something else entirely. This is useful for running `Translator.translate()` for custom usage.

### Exceptions¶

_exception _discord.app_commands.AppCommandError¶
    

The base exception type for all application command related errors.

This inherits from [`discord.DiscordException`](../api.html#discord.DiscordException "discord.DiscordException").

This exception and exceptions inherited from it are handled in a special way as they are caught and passed into various error handlers in this order:

  * `Command.error`

  * `Group.on_error`

  * `CommandTree.on_error`




New in version 2.0.

_exception _discord.app_commands.CommandInvokeError(_command_ , _e_)¶
    

An exception raised when the command being invoked raised an exception.

This inherits from `AppCommandError`.

New in version 2.0.

original¶
    

The original exception that was raised. You can also get this via the `__cause__` attribute.

Type
    

[`Exception`](https://docs.python.org/3/library/exceptions.html#Exception "\(in Python v3.14\)")

command¶
    

The command that failed.

Type
    

Union[`Command`, `ContextMenu`]

_exception _discord.app_commands.TransformerError(_value_ , _opt_type_ , _transformer_)¶
    

An exception raised when a `Transformer` or type annotation fails to convert to its target type.

This inherits from `AppCommandError`.

If an exception occurs while converting that does not subclass `AppCommandError` then the exception is wrapped into this exception. The original exception can be retrieved using the `__cause__` attribute. Otherwise if the exception derives from `AppCommandError` then it will be propagated as-is.

New in version 2.0.

value¶
    

The value that failed to convert.

Type
    

Any

type¶
    

The type of argument that failed to convert.

Type
    

`AppCommandOptionType`

transformer¶
    

The transformer that failed the conversion.

Type
    

`Transformer`

_exception _discord.app_commands.TranslationError(_* msg_, _string =None_, _locale =None_, _context_)¶
    

An exception raised when the library fails to translate a string.

This inherits from `AppCommandError`.

If an exception occurs while calling `Translator.translate()` that does not subclass this then the exception is wrapped into this exception. The original exception can be retrieved using the `__cause__` attribute. Otherwise it will be propagated as-is.

New in version 2.0.

string¶
    

The string that caused the error, if any.

Type
    

Optional[Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), `locale_str`]]

locale¶
    

The locale that caused the error, if any.

Type
    

Optional[[`Locale`](../api.html#discord.Locale "discord.Locale")]

context¶
    

The context of the translation that triggered the error.

Type
    

`TranslationContext`

_exception _discord.app_commands.CheckFailure¶
    

An exception raised when check predicates in a command have failed.

This inherits from `AppCommandError`.

New in version 2.0.

_exception _discord.app_commands.NoPrivateMessage(_message =None_)¶
    

An exception raised when a command does not work in a direct message.

This inherits from `CheckFailure`.

New in version 2.0.

_exception _discord.app_commands.MissingRole(_missing_role_)¶
    

An exception raised when the command invoker lacks a role to run a command.

This inherits from `CheckFailure`.

New in version 2.0.

missing_role¶
    

The required role that is missing. This is the parameter passed to `has_role()`.

Type
    

Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_exception _discord.app_commands.MissingAnyRole(_missing_roles_)¶
    

An exception raised when the command invoker lacks any of the roles specified to run a command.

This inherits from `CheckFailure`.

New in version 2.0.

missing_roles¶
    

The roles that the invoker is missing. These are the parameters passed to `has_any_role()`.

Type
    

List[Union[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)"), [`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]]

_exception _discord.app_commands.MissingPermissions(_missing_permissions_ , _* args_)¶
    

An exception raised when the command invoker lacks permissions to run a command.

This inherits from `CheckFailure`.

New in version 2.0.

missing_permissions¶
    

The required permissions that are missing.

Type
    

List[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

_exception _discord.app_commands.BotMissingPermissions(_missing_permissions_ , _* args_)¶
    

An exception raised when the bot’s member lacks permissions to run a command.

This inherits from `CheckFailure`.

New in version 2.0.

missing_permissions¶
    

The required permissions that are missing.

Type
    

List[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

_exception _discord.app_commands.CommandOnCooldown(_cooldown_ , _retry_after_)¶
    

An exception raised when the command being invoked is on cooldown.

This inherits from `CheckFailure`.

New in version 2.0.

cooldown¶
    

The cooldown that was triggered.

Type
    

`Cooldown`

retry_after¶
    

The amount of seconds to wait before you can retry again.

Type
    

[`float`](https://docs.python.org/3/library/functions.html#float "\(in Python v3.14\)")

_exception _discord.app_commands.CommandLimitReached(_guild_id_ , _limit_ , _type= <AppCommandType.chat_input: 1>_)¶
    

An exception raised when the maximum number of application commands was reached either globally or in a guild.

This inherits from `AppCommandError`.

New in version 2.0.

type¶
    

The type of command that reached the limit.

Type
    

`AppCommandType`

guild_id¶
    

The guild ID that reached the limit or `None` if it was global.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

limit¶
    

The limit that was hit.

Type
    

[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")

_exception _discord.app_commands.CommandAlreadyRegistered(_name_ , _guild_id_)¶
    

An exception raised when a command is already registered.

This inherits from `AppCommandError`.

New in version 2.0.

name¶
    

The name of the command already registered.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

guild_id¶
    

The guild ID this command was already registered at. If `None` then it was a global command.

Type
    

Optional[[`int`](https://docs.python.org/3/library/functions.html#int "\(in Python v3.14\)")]

_exception _discord.app_commands.CommandSignatureMismatch(_command_)¶
    

An exception raised when an application command from Discord has a different signature from the one provided in the code. This happens because your command definition differs from the command definition you provided Discord. Either your code is out of date or the data from Discord is out of sync.

This inherits from `AppCommandError`.

New in version 2.0.

command¶
    

The command that had the signature mismatch.

Type
    

Union[`Command`, `ContextMenu`, `Group`]

_exception _discord.app_commands.CommandNotFound(_name_ , _parents_ , _type= <AppCommandType.chat_input: 1>_)¶
    

An exception raised when an application command could not be found.

This inherits from `AppCommandError`.

New in version 2.0.

name¶
    

The name of the application command not found.

Type
    

[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")

parents¶
    

A list of parent command names that were previously found prior to the application command not being found.

Type
    

List[[`str`](https://docs.python.org/3/library/stdtypes.html#str "\(in Python v3.14\)")]

type¶
    

The type of command that was not found.

Type
    

`AppCommandType`

_exception _discord.app_commands.CommandSyncFailure(_child_ , _commands_)¶
    

An exception raised when `CommandTree.sync()` failed.

This provides syncing failures in a slightly more readable format.

This inherits from `AppCommandError` and [`HTTPException`](../api.html#discord.HTTPException "discord.HTTPException").

New in version 2.0.

#### Exception Hierarchy¶

  * [`DiscordException`](../api.html#discord.DiscordException "discord.DiscordException")
    
    * `AppCommandError`
    
      * `CommandInvokeError`

      * `TransformerError`

      * `TranslationError`

      * `CheckFailure`
    
        * `NoPrivateMessage`

        * `MissingRole`

        * `MissingAnyRole`

        * `MissingPermissions`

        * `BotMissingPermissions`

        * `CommandOnCooldown`

      * `CommandLimitReached`

      * `CommandAlreadyRegistered`

      * `CommandSignatureMismatch`

      * `CommandNotFound`

      * [`MissingApplicationID`](../api.html#discord.MissingApplicationID "discord.MissingApplicationID")

      * `CommandSyncFailure`

    * [`HTTPException`](../api.html#discord.HTTPException "discord.HTTPException")
    
      * `CommandSyncFailure`
