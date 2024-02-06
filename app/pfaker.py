from faker import Faker
from faker.providers import BaseProvider
import random
import string



class PurlProvider(BaseProvider):
    def random_string(self, length=8) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def random_number(self, length=8) -> str:
        return ''.join(random.choices(string.digits, k=length))
    
class PFaker:

    def __init__(self):
        self.fake = Faker()
        self.fake.add_provider(PurlProvider)

    def get_value(self, template):
        template = template.replace('fake.', 'self.fake.')
        out = eval(template)
        return out
    
pf = PFaker()