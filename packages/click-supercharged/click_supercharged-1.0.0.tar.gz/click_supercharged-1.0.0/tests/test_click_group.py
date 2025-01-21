import unittest
import click.testing

from click_supercharged import SuperchargedClickGroup


@click.group(cls=SuperchargedClickGroup)
def cli():
    pass


@cli.command(default_command=True, aliases=["bar"])
def foo():
    click.echo("foo")

@cli.command(aliases=["bax", "bez", "buz"])
def baz():
    click.echo("baz")




class TestUnclutterDirectory(unittest.TestCase):
    def test_default_command(self):
        runner = click.testing.CliRunner()

        result = runner.invoke(cli)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("foo", result.output)

    def test_abbreviations_for_commands(self):
        runner = click.testing.CliRunner()

        result = runner.invoke(cli, ["f"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("foo", result.output)

    def test_duplicate_abbreviation(self):
        runner = click.testing.CliRunner()

        result = runner.invoke(cli, ["ba"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("Ambiguous command or alias: 'ba'. Possible matches: bar, baz, bax\n", result.output)

    def test_help_contains_all_abbreviations_and_default_mark(self):
        runner = click.testing.CliRunner()

        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("baz (bax, bez, buz)\n", result.output)
        self.assertIn("foo (*) (bar)\n", result.output)


if __name__ == "__main__":
    unittest.main()
