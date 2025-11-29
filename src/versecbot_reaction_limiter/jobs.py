from collections import defaultdict
from logging import getLogger

from discord import Client, Member
from versecbot_interface import ReactionWatcher
from versecbot_interface.reaction import VersecbotReaction

from .settings import ReactionGateSettings, ReactionLimiterSettings

logger = getLogger("discord").getChild(
    "versecbot.plugins.reaction_limiter.reaction_gate"
)


class ReactionGate(ReactionWatcher):
    client: Client
    name: str

    def __init__(self, client: Client, settings: ReactionGateSettings):
        super().__init__(settings)
        self.client = client
        self.channel_ids = settings.channel_ids
        self.channels = [
            self.client.get_channel(channel_id) for channel_id in settings.channel_ids
        ]
        self.roles_required = settings.roles_required
        self.data = defaultdict(dict)
        self.name = "watcher_reaction_gate"

    def initialize(self, settings: ReactionLimiterSettings, *args):
        """Nothing special to do here."""
        logger.debug("Initializing...")
        super().initialize(settings, *args)

    def user_has_any_roles(self, user: Member, role_ids: list[str]) -> bool:
        """Check if a user has any of the specified roles."""
        user_role_ids = [role.id for role in user.roles]
        return any(role_id in user_role_ids for role_id in role_ids)

    def should_act(self, reaction: VersecbotReaction) -> bool:
        if not super().should_act(reaction):
            return False

        if not self.roles_required:
            return False

        if self.user_has_any_roles(reaction.user, self.roles_required):
            return False

        return True

    async def act(self, reaction: VersecbotReaction):
        message = reaction.message
        user = reaction.user
        logger.info(
            "Removing reaction by %s <%s> from message %s in channel %s",
            user.name,
            user.id,
            message.id,
            message.channel.id,
        )

        await reaction.message.remove_reaction(reaction.emoji, user)
