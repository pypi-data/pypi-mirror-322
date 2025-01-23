import sys

# The function that displays quotes based on input
def quote(input_value=None):
    if input_value == "123":
        print("This is your last chance. After this, there is no turning back. "
              "You take the blue pill - the story ends, you wake up in your bed "
              "and believe whatever you want to believe. You take the red pill - "
              "you stay in Wonderland and I show you how deep the rabbit hole goes.")
    else:
        print("Neo. This is your last chance. After this, there is no turning back. "
              "You take the blue pill - the story ends, you wake up in your bed "
              "and believe whatever you want to believe. You take the red pill - "
              "you stay in Wonderland and I show you how deep the rabbit hole goes.")

# Make the module callable
class CallableModule:
    def __call__(self, input_value=None):
        return quote(input_value)

# Override the module object in sys.modules
sys.modules[__name__] = CallableModule()
