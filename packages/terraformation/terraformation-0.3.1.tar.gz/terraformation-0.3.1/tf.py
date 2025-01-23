#!/usr/bin/env python3
"""A simple Terraform wrapper to use variable definition files if they match
the workspace name."""

import glob
import os
import pathlib
import subprocess  # nosec
import sys

__version__ = "0.3.1"

TF_CLI = os.getenv("TF_CLI", "terraform")
TF_COMMANDS_TO_MODIFY = (
    [
        "console",
        "import",
        "plan",
        "refresh",
    ]
    if TF_CLI == "terraform"
    else [
        "apply",
        "console",
        "destroy",
        "destroy",
        "get",
        "import",
        "init",
        "output",
        "plan",
        "refresh",
        "taint",
        "untaint",
        "validate",
    ]
)


def get_workspace():
    """Return the Terraform workspace."""
    try:
        proc = subprocess.run(  # nosec
            [TF_CLI, "workspace", "show"],
            capture_output=True,
            check=True,
            text=True,
        )
    except FileNotFoundError:
        print(f"Can't find {TF_CLI}.", file=sys.stderr)
        sys.exit(1)
    return proc.stdout.strip()


def is_debug_set():
    """Check if the debug environment variable is set."""
    debug = os.getenv("TF_DEBUG", "").lower()
    return debug in ["1", "true"]


def wrapper():
    # In case tf was run with no arguments.
    if len(sys.argv) == 1:
        try:
            os.execlp(TF_CLI, TF_CLI)  # nosec
        except FileNotFoundError:
            print(f"Can't find {TF_CLI}.", file=sys.stderr)
            sys.exit(1)

    # Build a new argument list.
    args = sys.argv[:]
    args[0] = TF_CLI

    # Check if the Terraform command is one that we need to modify (include
    # tfvars files). If not, execute Terraform with the same arguments.
    for command in TF_COMMANDS_TO_MODIFY:
        if command in sys.argv:
            break
    else:
        try:
            os.execvp(TF_CLI, args)  # nosec
        except FileNotFoundError:
            print(f"Can't find {TF_CLI}.", file=sys.stderr)
            sys.exit(1)

    # We can't add -var-file to an apply command with a plan. So we check all
    # of the args after the apply arg and if all of them are switches we assume
    # that a plan isn't specified (technically the plan file can also start
    # with a "-" and look like a switch, but let's not go there).
    if command == "apply":
        apply_index = sys.argv.index("apply")
        if not all(
            map(lambda x: x.startswith("-"), sys.argv[apply_index + 1 :])
        ):
            # No all args are switches, so a plan is specified and we don't add
            # the -var-file switch.
            try:
                os.execvp(TF_CLI, args)  # nosec
            except FileNotFoundError:
                print(f"Can't find {TF_CLI}.", file=sys.stderr)
                sys.exit(1)

    # We need to add the var files after the Terraform command (if we add it
    # before Terraform doesn't accept them) but not at the end (not to modify
    # other argument that accept optional values). So we add them right after
    # the Terraform command.
    command_index = args.index(command)
    workspace = get_workspace()
    var_file = pathlib.Path(f"{workspace}.tfvars")
    var_dir = pathlib.Path(workspace)
    if var_file.exists() and var_file.is_file():
        args.insert(command_index + 1, f"-var-file={var_file}")
    elif var_dir.exists() and var_dir.is_dir():
        for var_file in glob.glob(f"{var_dir}/*.tfvars"):
            args.insert(command_index + 1, f"-var-file={var_file}")

    # Print the new argument list to stderr if debugging is enabled.
    if is_debug_set():
        print(args, file=sys.stderr)

    try:
        os.execvp(TF_CLI, args)  # nosec
    except FileNotFoundError:
        print(f"Can't find {TF_CLI}.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    wrapper()
