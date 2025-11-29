# VerSecBot - Reaction Limiter

This plugin instructs VerSecBot to only allow specific roles to add message reactions in a given channel. If a user without a matching role tries to react, VerSecBot will remove the reaction.

This was created to allow public polls with a subset of voters.

To use it, install the package and add the following block to your configuration, replacing values in <> with your desired values:

```
    [versecbot.plugins.reaction_limiter]
        enabled = true

    [[versecbot.plugins.reaction_limiter.handlers]]
        enabled = true
        channel_ids = [list of channels that should be restricted]
        roles_required = [list of roles that can react in specified channels]

    [[versecbot.plugins.reaction_limiter.handlers]]
        enabled = true
        channel_ids = [list of channels that should be restricted]
        roles_required = [list of roles that can react in specified channels]

```
