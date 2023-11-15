## If you make changes to your models, you will need to create a new migration script:
> alembic revision --autogenerate -m "new migration name"
## And then apply the migration
> alembic upgrade head
