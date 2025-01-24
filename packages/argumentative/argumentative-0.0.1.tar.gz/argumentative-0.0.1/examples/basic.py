from argumentative import argumentative
import msgspec

@argumentative(exit_on_error=True)
class Args(msgspec.Struct):
    """
    basic.py - example of using argumentative
    """

    config: str # path to a config file
    verbose: bool = False # whether to print verbose output

args = Args.from_args()
print(args)
