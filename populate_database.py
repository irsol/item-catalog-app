from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User
from database_setup import engine

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


user = User(name="Bob", email="bob@mail")
session.add(user)
session.commit()


country = Category(name="Spain",
                   description="Spain, a country on Europe’s Iberian Peninsula")
session.add(country)
session.commit()

city = Item(name="Barcelona", description="City Barcelona",
            category=country, user=user)
session.add(city)
session.commit()

city = Item(name="Bilbao", description="City Bilbao",
            category=country, user=user)
session.add(city)
session.commit()

city = Item(name="Malaga", description="City Malaga",
            category=country, user=user)
session.add(city)
session.commit()


country = Category(name="Italy", description="Country Italy")
session.add(country)
session.commit()

city = Item(name="Milan", description="City Milan", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Rome", description="City Rome", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Venice", description="City Venice", category=country,
            user=user)
session.add(city)
session.commit()


country = Category(name="Croatia", description="Country Croatia")
session.add(country)
session.commit()

city = Item(name="Zadar", description="City Zadar", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Dubrovnik", description="City Dubrovnik", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Omis", description="City Omis", category=country,
            user=user)
session.add(city)
session.commit()

country = Category(name="Portugal", description="Country Portugal")
session.add(country)
session.commit()

city = Item(name="Lisbon", description="City Lisbon", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Albufeira", description="City Albufeira", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Porto", description="City Porto", category=country,
            user=user)
session.add(city)
session.commit()

country = Category(name="France", description="Country France")
session.add(country)
session.commit()

city = Item(name="Paris", description="City Paris", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Bordeaux", description="City Bordeaux", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Marseille", description="City Marseille", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Biarritz", description="City Biarritz", category=country,
            user=user)
session.add(city)
session.commit()

country = Category(name="Netherlands", description="Country Netherlands")
session.add(country)
session.commit()

city = Item(name="Amsterdam", description="City Amsterdam", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Rotterdam", description="City Rotterdam", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="The Hague", description="City The Hague", category=country,
            user=user)
session.add(city)
session.commit()

country = Category(name="Poland", description="Country Poland")
session.add(country)
session.commit()

city = Item(name="Krakow", description="City Krakow", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Warsaw", description="City Warsaw", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Lublin", description="City Lublin", category=country,
            user=user)
session.add(city)
session.commit()

country = Category(name="Germany", description="Country Germany")
session.add(country)
session.commit()

city = Item(name="Berlin", description="City Berlin", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Frankfurt", description="City Frankfurt", category=country,
            user=user)
session.add(city)
session.commit()

city = Item(name="Hamburg", description="City Hamburg", category=country,
            user=user)
session.add(city)
session.commit()









