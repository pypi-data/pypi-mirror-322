import click
from .config import Config


AliasConfig = Config()


class AliasedGroup(click.Group):
    """This subclass of a group supports looking up aliases in a config
    file and with a bit of magic makes your aliases for your CLI commands work.
    Adapted from Click's `aliases` example.
    See https://github.com/pallets/click/tree/main/examples/aliases.
    """

    def get_command(self, ctx, cmd_name):
        """Retrieves command associated with Click Group object. If
        command name is the full name, it executes the command as normal.
        If command name is the alias, it finds the actual command name and
        executes it as normal."""
        # Step one: builtin commands as normal
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        # Step two: look up an explicit command alias in the config
        aliases = AliasConfig.get_aliases()  # obtain aliases set by user
        if cmd_name in aliases:
            actual_cmd = aliases[cmd_name]
            return click.Group.get_command(self, ctx, actual_cmd)

    def resolve_command(self, ctx, args):
        """Retrieves command associated with Click Group object, if the
        supplied name doesn't match a command."""
        # always return the command's name, not the alias
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args
