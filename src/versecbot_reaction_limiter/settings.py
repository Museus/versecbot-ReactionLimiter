from versecbot_interface import PluginSettings, WatcherSettings


class ReactionGateSettings(WatcherSettings):
    enabled: bool
    roles_required: list[int]


class ReactionLimiterSettings(PluginSettings):
    handlers: list[ReactionGateSettings]
