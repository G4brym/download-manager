from main import provider, DatabaseService


@provider.inject
def migrate(database: DatabaseService):
    database.initial_migration()
    print("Migration applied!")


migrate()
