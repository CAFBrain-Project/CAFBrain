from agent.state import State
from agent.format_specifications import FORMAT_SPECIFICATIONS, DEFAULT_FORMAT_SPECIFICATIONS

def determine_format_specifications(state: State):
    target_format = state["target_format"]
    format_specifications = FORMAT_SPECIFICATIONS.get(target_format, DEFAULT_FORMAT_SPECIFICATIONS)

    print(f"Format determination complete for {target_format}")
    # print(format_specifications)

    # TODO: Do we need history?
    # state["format_specifications"] = state.get("format_specifications", []) + [format_specifications]
    state["format_specifications"] = format_specifications

    return state 