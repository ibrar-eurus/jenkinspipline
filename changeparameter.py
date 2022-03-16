import sys


def change_params(StackNameStartsWith, ParameterKey, ParameterValue):
    StackNameStartsWith = StackNameStartsWith
    key = ParameterKey
    value = ParameterValue
    print("print valueas")
    print(StackNameStartsWith, key, value)


change_params(sys.argv[1], sys.argv[2], sys.argv[3])
