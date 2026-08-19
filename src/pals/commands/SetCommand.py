from pydantic import model_serializer

from .FacilityCommand import CommandValue, FacilityCommand


class SetCommand(FacilityCommand):
    """The `set` command, which writes a parameter of the elements it matches.

    See the standard's Setting Parameters section. `parameter` is a pattern, so
    one command can write several elements. In the `value` expression,
    `PARAMETER` is the current value of the parameter being written and `SELF`
    is the element it belongs to.

    If both `absolute_error` and `relative_error` are given, the true error is
    `absolute_error + relative_error * |value|`. The standard documents both as
    defaulting to zero; they default to `None` here so that a value the file did
    not write stays out of the serialized output.

    Note that `set` is a reserved key of the `facility` list: an element cannot
    be named `set`.

    Example:
        >>> SetCommand(parameter="B1.*>BendP.e1", value="2*PARAMETER")
        SetCommand(parameter='B1.*>BendP.e1', value='2*PARAMETER', ...)
    """

    parameter: str
    value: CommandValue = None
    absolute_error: float | None = None
    relative_error: float | None = None

    @model_serializer(mode="plain")
    def _serialize_as_command(self) -> dict:
        """Serialize back into the one-key `set:` form the standard writes.

        A plain serializer (rather than a `model_dump` override, as the
        elements use) also covers the case where the enclosing model serializes
        the whole `facility` union at once.
        """
        return {"set": self.command_body()}

    def command_body(self) -> dict:
        """The command's properties, without the ones the file did not set.

        Unset properties are dropped, the same way `exclude_none` drops them
        for elements and for the root node.
        """
        body = {"parameter": self.parameter}
        for key in ("value", "absolute_error", "relative_error"):
            value = getattr(self, key)
            if value is not None:
                body[key] = value
        return body
