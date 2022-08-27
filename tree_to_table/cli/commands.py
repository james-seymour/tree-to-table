import click


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    ctx.ensure_object(dict)


transform_choices = click.Choice("one-to-many", "many-to-one")


@cli.command()
@click.option("--transform", "-t", type=transform_choices)
def transform(transform):
    print(transform)


if __name__ == "__main__":
    cli()
