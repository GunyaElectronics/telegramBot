# Function def in function
def external():
    def internal():
        return 1
    print(internal())


external()
# internal() -> exception, name 'internal' is not defined

# private function example
p = lambda x, y: x + y

print(p(1, 2))
