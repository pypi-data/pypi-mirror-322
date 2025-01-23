class Config:
    """
    This is a simple class for storing, setting, and retrieving aliases.
    """

    def __init__(self):
        self.aliases = dict()

    def add_alias(self, value, cmd_name):
        self.aliases[cmd_name] = value

    def set_aliases(self, aliases):
        try:
            if not isinstance(aliases, dict):
                raise TypeError(
                    "Expected dict object, got {} instead.".format(
                        type(aliases).__name__
                    )
                )

            self.aliases = aliases
        except TypeError as e:
            pass

    def get_aliases(self):
        return self.aliases


AliasConfig = Config()
