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
        try:
            with open(file, encoding=encoding) as f:
                data = f.read()
            # reconstructing the data as a dictionary
            d = ast.literal_eval(data)
        except FileNotFoundError:
            print(f'File {file} not found')
            d = {'localisation file not found': 'file not found error'}

        self.text = d

    def get_text(self, key):
        if self.text.get(key):
            return self.text.get(key)
        else:
            return key
