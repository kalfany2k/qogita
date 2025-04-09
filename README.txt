-- DESIGN CHOICES --
Upon a brief inspection, I noticed that there are some null entries in the Variant Barcode section of the CSV file, so the first natural thing to do was to check whether such a product can exist. So, upon finding out that if you are the only seller of a product or if it is a store brand it may not need a GTIN, I treated it as such.

Additionally, I noticed that they differ in lengths, so I decided it was best to check whether all of them were valid. From what I gathered so far, it would seem the only options for GTINs are 8, 12, 13 and 14 digit wide.

In my CSV parser, an empty GTIN field was treated as an empty string that was passed around to the pydantic validator, and thus I decided to refine the value to None to add products with no GTIN to the DB.

-- SETUP --

To test the environment yourself, there are a few key steps you need to take;

1. Initialize a virtual environment using python3 -m venv venv to separate project-related packages from globally-used ones

2. Activate the virtual environment and install all packages from requirements.txt using pip install -r requirements.txt

3. Log into psql's CLI using your desired administrator user

4. Create a database for our testing environment and an user who will be accessing it

5. Grant all privileges both on the public schema and on the database itself for the newly created user

6. Create a .env file containing the fields present in config.py, with values chosen upon setting everything up

7. Migrate the changes present in the alembic folder using alembic upgrade head to locally have the same PostgreSQL table structure as in models.py

~7. If the previous step is unsuccessful, you can also choose to delete the versions folder from alembic and the alembic_version table from the newly created database, and create the tables from scratch using alembic revision --autogenerate -m "..."

8. Run uvicorn app.main:app --reload on your desired port