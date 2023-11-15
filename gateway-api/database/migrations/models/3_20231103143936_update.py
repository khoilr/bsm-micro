from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "Event" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "description" VARCHAR(255),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "Event" IS 'Tortoise-based log model.';
        CREATE TABLE IF NOT EXISTS "EventLog" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "video_url" VARCHAR(255),
    "image_id" VARCHAR(255),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "event_id" INT REFERENCES "Event" ("id") ON DELETE CASCADE,
    "face_id" INT REFERENCES "Face" ("face_id") ON DELETE CASCADE
);
COMMENT ON TABLE "EventLog" IS 'Tortoise-based log model.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "Event";
        DROP TABLE IF EXISTS "EventLog";"""
