import json
import click

import uffutils.file
from uffutils.view import AggregationMode, CustomJSONEncoder, UFFDataView


@click.group()
def cli(): ...


@cli.command()
@click.argument("inputfile", type=click.Path(exists=True))
@click.option("--fields", type=str, default="")
@click.option("--summary", "aggregation", flag_value=AggregationMode.SUMMARY, default=True)
@click.option("--full", "aggregation", flag_value=AggregationMode.FULL)
def view(inputfile: str, fields: str, aggregation: AggregationMode):
    data = uffutils.file.read(inputfile)
    view = UFFDataView(data)
    res = view.as_dict()
    if fields: 
        _split_fields = fields.split(",")
        res = {key: res[key] for key in _split_fields if key in view.fields}
    else: 
        click.echo(json.dumps(res, indent=2, cls=CustomJSONEncoder))


@cli.command()
@click.argument("inputfile", type=click.Path(exists=True))
@click.argument("outputfile", type=click.Path())
@click.option("--node-selection", type=str, default="")
@click.option("--node-step", type=int, default=0)
@click.option("--node-count", type=int, default=0)
def modify(
    inputfile: str,
    outputfile: str,
    node_selection: str,
    node_step: int,
    node_count: int,
):
    data = uffutils.read(inputfile)
    if node_selection or node_step or node_count:
        if node_selection:
            target_nodes = list(map(int, node_selection.split(",")))
        else:
            target_nodes = None
        data.subset(target_nodes=target_nodes, step=node_step, n_max=node_count)
    uffutils.write(outputfile, data)
