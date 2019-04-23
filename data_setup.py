#!/usr/bin/env/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, User, Category, CategoryItem

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Tiny Tim", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/\
             2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

print "Added User Tiny Tim"

# Populate categories
Category1 = Category(name="Soccer")
session.add(Category1)
session.commit()

Category2 = Category(name="Basketball")
session.add(Category2)
session.commit()

Category3 = Category(name="Baseball")
session.add(Category3)
session.commit()

Category4 = Category(name="Frisbee")
session.add(Category4)
session.commit()

Category5 = Category(name="Snowboarding")
session.add(Category5)
session.commit()

Category6 = Category(name="Rock Climbing")
session.add(Category6)
session.commit()

Category7 = Category(name="Foosball")
session.add(Category7)
session.commit()

Category8 = Category(name="Skating")
session.add(Category8)
session.commit()

Category9 = Category(name="Hockey")
session.add(Category9)
session.commit()

print "Added 9 Categories"

# Add Category Item
categoryItem1 = CategoryItem(name="Freeride Snowboard",
                             description="This snowboard is appropriate for \
                             children ages 5 to 15. Weight limit is up to \
                             95 lbs", category_id=5, user_id=1)
session.add(categoryItem1)
session.commit()

print "Added Freeride Snowboard catalog item"
