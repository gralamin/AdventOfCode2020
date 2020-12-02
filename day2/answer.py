class Policy:

    def __init__(self, str):
        split_str = str.split(" ")
        min_max = split_str[0].split("-")
        self.letter = split_str[1]
        self.min_occurance = int(min_max[0])
        self.max_occurance = int(min_max[1])

    def is_valid(self, password):
        num = len([x for x in password if x == self.letter])
        return num >= self.min_occurance and num <= self.max_occurance

class PasswordInput:

    def __init__(self, str):
        split_str = str.split(":")
        policy = split_str[0]
        password = split_str[1].strip()
        self.password = password
        if self.password[-1] == "\n":
            self.password = self.password[:-1]
        self.policy = Policy(policy)

    def is_valid(self):
        return self.policy.is_valid(self.password)


inputs = []

with open("input", "r") as f:
    for r in f:
        inputs.append(PasswordInput(r))

print(len([x for x in inputs if x.is_valid()]))
