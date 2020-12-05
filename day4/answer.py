import re

BIRTH_YEAR = "byr"
ISSUE_YEAR = "iyr"
EXPIRATION_YEAR = "eyr"
HEIGHT = "hgt"
HAIR_COLOR = "hcl"
EYE_COLOR = "ecl"
PASSPORT_ID = "pid"
COUNTRY_ID = "cid"


def validate_height(height):
    regex_match = re.match("^([0-9]+)(cm|in)$", height)
    if regex_match:
        num = int(regex_match.groups()[0])
        cm_in = regex_match.groups()[1]
        if cm_in == "cm":
            return num >= 150 and num <= 193
        return num >= 59 and num <= 76


class Passport:
    def __init__(self):
        self.birth_year = None
        self.issue_year = None
        self.expiration_year = None
        self.height = None
        self.hair_color = None
        self.eye_color = None
        self.passport_id = None
        self.country_id = None
        self.inputs = []

    def add_str(self, str):
        attr_map = {
            COUNTRY_ID: "country_id",
            PASSPORT_ID: "passport_id",
            EYE_COLOR: "eye_color",
            HAIR_COLOR: "hair_color",
            HEIGHT: "height",
            EXPIRATION_YEAR: "expiration_year",
            ISSUE_YEAR: "issue_year",
            BIRTH_YEAR: "birth_year",
        }
        self.inputs.append(str)

        split_str = str.split(" ")
        for x in split_str:
            key_value = x.split(":")
            key = key_value[0]
            value = key_value[1]
            value = value.strip()
            setattr(self, attr_map[key], value)

    def is_valid(self):
        check_attrs = [
            self.passport_id
            and len(self.passport_id) == 9
            and int(self.passport_id) >= 0,
            self.eye_color in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
            self.hair_color and re.match("^#[0-9a-f]{6}$", self.hair_color),
            self.height and validate_height(self.height),
            self.expiration_year and re.match("^20(2[0-9]|30)$", self.expiration_year),
            self.issue_year and re.match("^20(1[0-9]|20)$", self.issue_year),
            self.birth_year
            and int(self.birth_year) >= 1920
            and int(self.birth_year) <= 2002,
        ]

        return all(check_attrs)

    def __str__(self):
        sb = [
            f"{BIRTH_YEAR}: {self.birth_year}",
            f"{ISSUE_YEAR}: {self.issue_year}",
            f"{EXPIRATION_YEAR}: {self.expiration_year}",
            f"{HEIGHT}: {self.height}",
            f"{HAIR_COLOR}: {self.hair_color}",
            f"{EYE_COLOR}: {self.eye_color}",
            f"{PASSPORT_ID}: {self.passport_id}",
            f"{COUNTRY_ID}: {self.country_id}",
            f"input: '{self.inputs}'",
        ]
        return "\n".join(sb)


def get_input_passports():
    cur_passport = Passport()
    with open("input", "r") as f:
        for x in f:
            if x == "\n":
                yield cur_passport
                cur_passport = Passport()
                continue
            cur_passport.add_str(x)
    yield cur_passport


valid_passports = [x for x in get_input_passports() if x.is_valid()]
print(f"Answer 2: {len(valid_passports)}")
