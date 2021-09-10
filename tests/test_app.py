from click.testing import CliRunner
from wishlist import wish

def test_wish_cli():
    runner = CliRunner()
    result = runner.invoke(wish, ["ls"])
    assert result.exit_code == 0
    assert result.output == "test1\n"

if __name__ == '__main__':
    test_wish_cli()
