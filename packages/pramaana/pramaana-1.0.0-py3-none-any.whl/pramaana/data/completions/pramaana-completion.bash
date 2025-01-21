_pramaana_complete() {
    local cur prev cmd
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    cmd="${COMP_WORDS[1]}"

    # List of all commands
    local commands="new edit find import export ls rm trash show open"

    # If we're completing the command name (first argument)
    if [ $COMP_CWORD -eq 1 ]; then
        COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
        return 0
    fi

    # Get pramaana data directory from config
    local data_dir=$(python3 -c '
import json
import os
with open(os.path.expanduser("~/.pramaana/config.json")) as f:
    print(os.path.expanduser(json.load(f)["pramaana_path"]))
')

    # Handle command-specific completions
    case "${cmd}" in
        ls|rm|trash|show|open|edit|grep|mv|cp|ln)
            # Complete with paths from pramaana data directory
            local paths=$(cd "$data_dir" && compgen -f -- "${cur}")
            COMPREPLY=( $(printf "%s\n" "${paths}") )
            ;;
        import)
            if [ "$prev" = "--via" ]; then
                COMPREPLY=( $(compgen -W "ln cp mv" -- ${cur}) )
            else
                # Complete both directories and .bib files
                local files=( $(compgen -f -X '!*.bib' -- "${cur}") )
                local dirs=( $(compgen -d -- "${cur}") )
                COMPREPLY=( "${files[@]}" "${dirs[@]}" )
            fi
            ;;
        export)
            # If no args yet, complete with export names from config
            if [ $COMP_CWORD -eq 2 ]; then
                local exports=$(python3 -c '
import json
import os
with open(os.path.expanduser("~/.pramaana/config.json")) as f:
    config = json.load(f)
    print(" ".join(config["exports"].keys()))
')
                COMPREPLY=( $(compgen -W "${exports}" -- ${cur}) )
            fi
            ;;
        *)
            ;;
    esac

    return 0
}

complete -F _pramaana_complete pramaana