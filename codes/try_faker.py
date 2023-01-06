from faker import Faker
fake = Faker( )
a = fake.password()
print(a,type(a))