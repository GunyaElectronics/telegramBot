import ast


# Example of localisation file:
# {"Key 1": "Value", "Key n": "Value"}
# {
#  "Please, enter your new activity name": "Your language translation for this string key 1",
#  "Add your phone number": "Your language translation for this string key 2"
# }


class MyLocalisation:
    """a simple class for localizing program texts in your languages"""

    def __init__(self, file, encoding):
        self.file = file
        self.encoding = encoding
        with open(file, encoding=encoding) as f:
            data = f.read()
        # reconstructing the data as a dictionary
        d = ast.literal_eval(data)
        self.text = d
