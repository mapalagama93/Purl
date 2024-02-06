from faker import Faker

class PFaker:

    def __init__(self):
        self.fake = Faker()

    def get_value(self, template):
        template = template.replace('fake.', 'self.fake.')
        out = eval(template)
        return out

pf = PFaker()