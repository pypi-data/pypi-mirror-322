#!/usr/bin/env python

import click
import sys

try:
    from .inspector import Inspector
except (ValueError, ImportError):
    from inspector import Inspector


@click.command(
    help="Shows command line necessary to run copy of existing Docker container.")
@click.argument("container", required=False)
@click.option(
    "--no-name",
    is_flag=True,
    help="Do not include container name in output")
@click.option(
    "--use-volume-id",
    is_flag=True,
    help="Keep the automatically assigned volume id")
@click.option("-p", "--pretty", is_flag=True)
@click.option("-s", "--stdin", is_flag=True)
@click.option("-l", "--no-labels", is_flag=True, help="Do not include labels in output")

def cli(container, no_name, use_volume_id, pretty, stdin, no_labels):

    # TODO: -i, -t, -d as added options that override the inspection
    if container or stdin:
        ins = Inspector(container, no_name, use_volume_id, pretty, no_labels)
        if container:
            ins.inspect()
        elif stdin:
            raw_json = click.get_text_stream('stdin').read()
            ins.set_container_facts(raw_json)

        print(ins.format_cli())
    else:
        raise click.UsageError("usage error")

def main():
    cli()

if __name__ == "__main__":
    main()
