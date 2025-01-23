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

# Directly expose the `quote` function in the module's namespace
globals()['quote'] = quote
