from dataclasses import replace
from typing import Optional

from simfile.types import Simfile
from .behaviors import *


__all__ = [
    "tidy",
    "Preset",
    "Whitespace",
    "LineEndings",
    "RemoveComments",
    "CreateComments",
    "CreateMissingProperties",
    "DestructivelyRemoveProperties",
    "SortProperties",
]


def tidy(
    sim: Simfile,
    preset: Optional[Preset] = None,
    *,
    whitespace: Optional[Whitespace] = None,
    line_endings: Optional[LineEndings] = None,
    remove_comments: Optional[RemoveComments] = None,
    create_comments: Optional[CreateComments] = None,
    create_missing_properties: Optional[CreateMissingProperties] = None,
    destructively_remove_properties: Optional[DestructivelyRemoveProperties] = None,
    sort_properties: Optional[SortProperties] = None,
):
    """
    Tidy up a simfile for future serialization, mutating it in-memory.

    This function has many optional parameters that toggle various
    tidying **behaviors**. The simplest way to call it is to pass a preset
    as the second argument::

        import tidy, Preset from simfile.tidy
        tidy(sim, Preset.RECOMMENDED)  # or Preset.SM5

    Without a preset, all behaviors default to off. If you don't specify
    a preset, you must set at least one behavior to a non-empty value, or
    specify the :data:`~Preset.NO_OP` preset to allow no behaviors.

    Each optional behavior has an associated enum. Some behaviors' enums
    are flags that can be combined using bitwise operators, for example::

        import tidy, RemoveComments from simfile.tidy
        tidy(
            sim,
            remove_comments=RemoveComments.PREAMBLE | RemoveComments.CHART_PREAMBLE,
        )

    All flag enums include an ``ALL`` alias, a union of all the other fields.

    Returns `True` only if changes were made to the simfile.
    Raises `ValueError` if no preset or behaviors are specified.
    """
    if not any(
        (
            preset,
            whitespace,
            line_endings,
            remove_comments,
            create_comments,
            create_missing_properties,
            destructively_remove_properties,
            sort_properties,
        )
    ):
        raise ValueError(
            "Must specify a preset or at least one behavior"
            " (pass `Preset.NO_OP` as the second argument to silence this error)"
        )

    changed = False

    if whitespace:
        changed |= whitespace.run(sim)
    if line_endings:
        changed |= line_endings.run(sim)
    if remove_comments:
        changed |= remove_comments.run(sim)
    if create_comments:
        changed |= create_comments.run(sim)
    if create_missing_properties:
        changed |= create_missing_properties.run(sim)
    if destructively_remove_properties:
        changed |= destructively_remove_properties.run(sim)
    if sort_properties:
        changed |= sort_properties.run(sim)

    return changed


def set_preamble_comment(sim: Simfile, text: str):
    first_property = next(iter(sim._properties.values()))
    first_property.msd_parameter = replace(
        first_property.msd_parameter,
        preamble="".join(
            f"// {line}\n" if not line.startswith("//") else line
            for line in text.splitlines()
        ),
    )
