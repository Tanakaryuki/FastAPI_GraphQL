alembic-revision:
    @read -p "Enter migration message: " message; \
    docker compose exec oauth_graphql alembic revision --autogenerate -m "$$message"

alembic-upgrade-head:
	docker compose exec oauth_graphql alembic upgrade head

alembic-upgrade-version:
	@read -p "Enter version: " version; \
	docker compose exec oauth_graphql alembic upgrade $$version

alembic-downgrade-head:
	docker compose exec oauth_graphql alembic downgrade head

alembic-downgrade-version:
	@read -p "Enter version: " version; \
	docker compose exec oauth_graphql alembic downgrade $$version

alembic-history:
	docker compose exec oauth_graphql alembic history

install-package:
	@read -p "Enter package name: " package; \
	docker compose exec oauth_graphql poetry add $$package

remove-package:
	@read -p "Enter package name: " package; \
	docker compose exec oauth_graphql poetry remove $$package

reset-db:
	docker compose exec oauth_graphql python -m api.reset_db