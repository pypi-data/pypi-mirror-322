from argumentative import argumentative, _get_field_docstring
import msgspec

@argumentative()
class User(msgspec.Struct):
    # name of the user
    name: str
    age: int | None = None # age of the user
    verbose: bool = False # whether to print verbose output

@argumentative()
class FakeCoverageClass(msgspec.Struct):
    fakeity_mc_fake_fake: str = "fake" # fakeity mc fake fake

def test_basic():
    # make sure we don't break existing functionality
    user = User(name="fizz", age=19)
    assert user.name == "fizz"
    assert user.age == 19

def test_arg_parsing():
    user = User.from_args(["fizz", "--age=19"])
    assert user.name == "fizz"
    assert user.age == 19
    user = User.from_args(["--age=19", "fizz"])
    assert user.name == "fizz"
    assert user.age == 19
    user = User.from_args(["fizz", "--age", "19"])
    assert user.name == "fizz"
    assert user.age == 19
    user = User.from_args(["--verbose", "fizz"])
    assert user.name == "fizz"
    assert user.age == None
    assert user.verbose == True
    try:
        User.from_args(["--verbose"])
        assert False
    except ValueError as e:
        assert "is a required argument" in str(e)
    try:
        User.from_args(["fizz", "--age"])
        assert False
    except ValueError as e:
        assert "No argument found for age" in str(e)

def test_docstring_util():
    field = msgspec.structs.FieldInfo(name="name", encode_name="name", type=str, default=msgspec.NODEFAULT, default_factory=msgspec.NODEFAULT)
    assert _get_field_docstring(User, field) == "name of the user"
    field = msgspec.structs.FieldInfo(name="age", encode_name="age", type=int | None, default=18, default_factory=msgspec.NODEFAULT) # we just manually construct a duplicate of the one in the class
    assert _get_field_docstring(User, field) == "age of the user"