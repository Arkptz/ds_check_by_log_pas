"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from typing import List, Literal, Optional, TypedDict, Union
from typing_extensions import NotRequired, Required

from .activity import PartialPresenceUpdate
from .voice import GuildVoiceState
from .integration import BaseIntegration, IntegrationApplication
from .role import Role
from .channel import ChannelType, StageInstance
from .interactions import Interaction
from .invite import InviteTargetType
from .emoji import Emoji, PartialEmoji
from .member import MemberWithUser
from .snowflake import Snowflake
from .message import Message
from .sticker import GuildSticker
from .appinfo import PartialAppInfo
from .guild import Guild, UnavailableGuild, SupplementalGuild
from .user import Connection, User
from .threads import Thread, ThreadMember
from .scheduled_event import GuildScheduledEvent
from .channel import DMChannel, GroupDMChannel


PresenceUpdateEvent = PartialPresenceUpdate


class Gateway(TypedDict):
    url: str


class ShardInfo(TypedDict):
    shard_id: int
    shard_count: int


class ReadyEvent(TypedDict):
    analytics_token: str
    auth_token: NotRequired[str]
    connected_accounts: List[Connection]
    country_code: str
    friend_suggestion_count: int
    geo_ordered_rtc_regions: List[str]
    guilds: List[Guild]
    merged_members: List[List[MemberWithUser]]
    private_channels: List[Union[DMChannel, GroupDMChannel]]
    relationships: List[dict]
    required_action: NotRequired[str]
    sessions: List[dict]
    session_id: str
    session_type: str
    user: User
    user_guild_settings: dict
    user_settings: dict
    user_settings_proto: str
    users: List[User]
    v: int


class MergedPresences(TypedDict):
    friends: List[PresenceUpdateEvent]
    guilds: List[List[PresenceUpdateEvent]]


class ReadySupplementalEvent(TypedDict):
    guilds: List[SupplementalGuild]
    merged_members: List[List[MemberWithUser]]
    merged_presences: MergedPresences


ResumedEvent = Literal[None]

MessageCreateEvent = Message


class MessageDeleteEvent(TypedDict):
    id: Snowflake
    channel_id: Snowflake
    guild_id: NotRequired[Snowflake]


class MessageDeleteBulkEvent(TypedDict):
    ids: List[Snowflake]
    channel_id: Snowflake
    guild_id: NotRequired[Snowflake]


class MessageUpdateEvent(Message):
    channel_id: Snowflake


class MessageReactionAddEvent(TypedDict):
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    emoji: PartialEmoji
    member: NotRequired[MemberWithUser]
    guild_id: NotRequired[Snowflake]


class MessageReactionRemoveEvent(TypedDict):
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    emoji: PartialEmoji
    guild_id: NotRequired[Snowflake]


class MessageReactionRemoveAllEvent(TypedDict):
    message_id: Snowflake
    channel_id: Snowflake
    guild_id: NotRequired[Snowflake]


class MessageReactionRemoveEmojiEvent(TypedDict):
    emoji: PartialEmoji
    message_id: Snowflake
    channel_id: Snowflake
    guild_id: NotRequired[Snowflake]


InteractionCreateEvent = Interaction


UserUpdateEvent = User


class InviteCreateEvent(TypedDict):
    channel_id: Snowflake
    code: str
    created_at: str
    max_age: int
    max_uses: int
    temporary: bool
    uses: Literal[0]
    guild_id: NotRequired[Snowflake]
    inviter: NotRequired[User]
    target_type: NotRequired[InviteTargetType]
    target_user: NotRequired[User]
    target_application: NotRequired[PartialAppInfo]


class InviteDeleteEvent(TypedDict):
    channel_id: Snowflake
    code: str
    guild_id: NotRequired[Snowflake]


class _ChannelEvent(TypedDict):
    id: Snowflake
    type: ChannelType


ChannelCreateEvent = ChannelUpdateEvent = ChannelDeleteEvent = _ChannelEvent


class ChannelPinsUpdateEvent(TypedDict):
    channel_id: Snowflake
    guild_id: NotRequired[Snowflake]
    last_pin_timestamp: NotRequired[Optional[str]]


class ThreadCreateEvent(Thread, total=False):
    newly_created: bool
    members: List[ThreadMember]


ThreadUpdateEvent = Thread


class ThreadDeleteEvent(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    parent_id: Snowflake
    type: ChannelType


class ThreadListSyncEvent(TypedDict):
    guild_id: Snowflake
    threads: List[Thread]
    members: List[ThreadMember]
    channel_ids: NotRequired[List[Snowflake]]


class ThreadMemberUpdate(ThreadMember):
    guild_id: Snowflake


class ThreadMembersUpdate(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    member_count: int
    added_members: NotRequired[List[ThreadMember]]
    removed_member_ids: NotRequired[List[Snowflake]]


class GuildMemberAddEvent(MemberWithUser):
    guild_id: Snowflake


class GuildMemberRemoveEvent(TypedDict):
    guild_id: Snowflake
    user: User


class GuildMemberUpdateEvent(TypedDict):
    guild_id: Snowflake
    roles: List[Snowflake]
    user: User
    avatar: Optional[str]
    joined_at: Optional[str]
    nick: NotRequired[str]
    premium_since: NotRequired[Optional[str]]
    deaf: NotRequired[bool]
    mute: NotRequired[bool]
    pending: NotRequired[bool]
    communication_disabled_until: NotRequired[str]


class GuildEmojisUpdateEvent(TypedDict):
    guild_id: Snowflake
    emojis: List[Emoji]


class GuildStickersUpdateEvent(TypedDict):
    guild_id: Snowflake
    stickers: List[GuildSticker]


GuildCreateEvent = GuildUpdateEvent = Guild
GuildDeleteEvent = UnavailableGuild


class _GuildBanEvent(TypedDict):
    guild_id: Snowflake
    user: User


GuildBanAddEvent = GuildBanRemoveEvent = _GuildBanEvent


class _GuildRoleEvent(TypedDict):
    guild_id: Snowflake
    role: Role


class GuildRoleDeleteEvent(TypedDict):
    guild_id: Snowflake
    role_id: Snowflake


GuildRoleCreateEvent = GuildRoleUpdateEvent = _GuildRoleEvent


class GuildMembersChunkEvent(TypedDict):
    guild_id: Snowflake
    members: List[MemberWithUser]
    chunk_index: int
    chunk_count: int
    not_found: NotRequired[List[Snowflake]]
    presences: NotRequired[List[PresenceUpdateEvent]]
    nonce: NotRequired[str]


class GuildIntegrationsUpdateEvent(TypedDict):
    guild_id: Snowflake


class _IntegrationEvent(BaseIntegration, total=False):
    guild_id: Required[Snowflake]
    role_id: Optional[Snowflake]
    enable_emoticons: bool
    subscriber_count: int
    revoked: bool
    application: IntegrationApplication


IntegrationCreateEvent = IntegrationUpdateEvent = _IntegrationEvent


class IntegrationDeleteEvent(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    application_id: NotRequired[Snowflake]


class WebhooksUpdateEvent(TypedDict):
    guild_id: Snowflake
    channel_id: Snowflake


StageInstanceCreateEvent = StageInstanceUpdateEvent = StageInstanceDeleteEvent = StageInstance

GuildScheduledEventCreateEvent = GuildScheduledEventUpdateEvent = GuildScheduledEventDeleteEvent = GuildScheduledEvent


class _GuildScheduledEventUsersEvent(TypedDict):
    guild_scheduled_event_id: Snowflake
    user_id: Snowflake
    guild_id: Snowflake


GuildScheduledEventUserAdd = GuildScheduledEventUserRemove = _GuildScheduledEventUsersEvent

VoiceStateUpdateEvent = GuildVoiceState


class VoiceServerUpdateEvent(TypedDict):
    token: str
    guild_id: Snowflake
    channel_id: Snowflake
    endpoint: Optional[str]


class TypingStartEvent(TypedDict):
    channel_id: Snowflake
    user_id: Snowflake
    timestamp: int
    guild_id: NotRequired[Snowflake]
    member: NotRequired[MemberWithUser]
