from logging import getLogger

from discord import Intents
from versecbot_interface import Plugin

from .jobs import ReactionGate
from .settings import ReactionLimiterSettings, ReactionGateSettings


logger = getLogger("discord").getChild("versecbot.plugins.reaction_limiter")


class ReactionLimiterPlugin(Plugin):
    name: str = "reaction_limiter"
    intents = [Intents.guild_messages, Intents.reactions]

    def __init__(self):
        super().__init__()

    def initialize(self, settings: ReactionLimiterSettings, client):
        logger.info(
            "Initializing Reaction Limiter plugin...",
        )

        # Register Reaction Gate jobs
        for handler_settings_raw in settings.handlers:
            handler_settings = ReactionGateSettings.model_validate(handler_settings_raw)
            try:
                gate = ReactionGate(client, handler_settings)
                gate.initialize(handler_settings, client)
            except Exception:
                logger.exception(
                    "Failed to initialize Reaction Limiter in channels %s",
                    ", ".join(channel.name for channel in gate.channels),
                )
            else:
                self.assign_job(gate)
                logger.info(
                    "Limiting reactions in channels %s",
                    ", ".join(channel.name for channel in gate.channels),
                )

        logger.info("Reaction Limiter initialized")
