#Django Tutorial
#Install Django via pip install Django
# Created a subdirectory called src then nagivated to it
# ran django-admin startproject trydjango . // Not sure what the period is for
# Test that things are running correctly with python manage.py runserver
# Run python manage.py migrate to create a database and start db. Go to setting to change the name of the db.
# Create a superuser with python manage.py createsuperuser.
# You can then log on to the admin via the ip add that comes up when you start the project.
# Logging in takes you to the django admin page.
# To create a new component python manage.py startapp componentName
# Went to Products (The new component name) Went to models. Created new model, added it do settings Installed Apps
# Then to add this new model to database python manage.py makemigrations
# Then python manage.py migrate
# If you make a change to models in the user created component. Run python manage.py makemigrations and python migrate.py migrate again
# Register the model in the admin file of the component
# Then go to admin page to add products to the database

# Working with python manage.py shell
# from products.model import Product
# Product.objects.all()
# Product.objects.create(title="New Product", description="another one",price="3", summary="ok")
# The above code prints objects that exist in db, and also adds a product. Just a way to do it in the interpreter instead
# of on the online admin form.\

# Field Types.
# To reset db, delete migration files and the database.