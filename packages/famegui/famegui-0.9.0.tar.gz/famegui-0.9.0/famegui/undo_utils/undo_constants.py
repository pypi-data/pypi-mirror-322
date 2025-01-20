from enum import Enum


class UndoActions(Enum):
    # agent
    UNDO_AGENT_MOVED = 1
    UNDO_AGENT_ATTRIBUTES_CHANGED = 2
    UNDO_AGENTS_REARRANGED = 3
    UNDO_AGENT_DELETED = 4
    UNDO_AGENT_CREATED = 4

    # contract
    UNDO_CONTRACT_FIELDS_CHANGED = 6
    UNDO_CONTRACT_DELETION = 7
    UNDO_CONTRACT_CREATION = 8

    # properties
    UNDO_SCENARIO_PROPERTIES = 9
