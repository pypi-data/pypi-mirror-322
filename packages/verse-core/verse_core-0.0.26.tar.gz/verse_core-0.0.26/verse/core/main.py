import argparse
from typing import Any

from ._arg_parser import ArgParser
from ._loader import Loader


def run(
    path: str,
    manifest: str,
    handle: str | None,
    tag: str | None,
    statement: str | None,
) -> Any:
    """
    Verse Run
    """
    loader = Loader(path=path, manifest=manifest)
    root_component = loader.load_component(handle=handle, tag=tag)
    operation = None
    if statement is not None:
        operation = ArgParser.convert_execute_operation(statement, None)
    return root_component.__run__(
        operation=operation,
        path=path,
        manifest=manifest,
        handle=handle,
        tag=tag,
    )


def requirements(
    path: str,
    manifest: str,
    handle: str | None,
    tag: str | None,
    out: str | None,
):
    """
    Verse Requirements
    """
    loader = Loader(path=path, manifest=manifest)
    requirements = loader.generate_requirements(
        handle=handle, tag=tag, out=out
    )
    return requirements


def main():
    parser = argparse.ArgumentParser(prog="verse", description="Verse CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="Run the Verse application")
    requirements_parser = subparsers.add_parser(
        "requirements", help="Generate the pip requirements"
    )
    run_parser.add_argument(
        "pos_handle",
        type=str,
        nargs="?",
        default=None,
        help="Root handle (optional positional argument)",
    )
    run_parser.add_argument(
        "pos_tag",
        type=str,
        nargs="?",
        default=None,
        help="Provide tag (optional positional argument)",
    )
    run_parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Project directory",
    )
    run_parser.add_argument(
        "--manifest",
        type=str,
        default=Loader.MANIFEST_FILE,
        help="Manifest filename",
    )
    run_parser.add_argument(
        "--handle",
        type=str,
        default=None,
        help="Root handle",
    )
    run_parser.add_argument(
        "--tag",
        type=str,
        default=None,
        help="Provider tag",
    )
    run_parser.add_argument(
        "--execute",
        type=str,
        default=None,
        help="Operation to execute",
    )

    requirements_parser.add_argument(
        "pos_handle",
        type=str,
        nargs="?",
        default=None,
        help="Root handle (optional positional argument)",
    )
    requirements_parser.add_argument(
        "pos_tag",
        type=str,
        nargs="?",
        default=None,
        help="Provide tag (optional positional argument)",
    )
    requirements_parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Project directory",
    )
    requirements_parser.add_argument(
        "--manifest",
        type=str,
        default=Loader.MANIFEST_FILE,
        help="Manifest filename",
    )
    requirements_parser.add_argument(
        "--handle",
        type=str,
        default=None,
        help="Root handle",
    )
    requirements_parser.add_argument(
        "--tag",
        type=str,
        default=None,
        help="Provider tag",
    )
    requirements_parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output path",
    )

    args = parser.parse_args()
    if args.command == "run":
        response = run(
            path=args.path,
            manifest=args.manifest,
            handle=args.pos_handle or args.handle,
            tag=args.pos_tag or args.tag,
            statement=args.execute,
        )
        print(response)
    elif args.command == "requirements":
        requirements(
            path=args.path,
            manifest=args.manifest,
            handle=args.pos_handle or args.handle,
            tag=args.pos_tag or args.tag,
            out=args.out,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
