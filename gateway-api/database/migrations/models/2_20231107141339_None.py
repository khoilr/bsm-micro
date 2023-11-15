from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "dummymodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL,
    "description" VARCHAR(155) NOT NULL
);
COMMENT ON TABLE "dummymodel" IS 'Model for demo purpose.';
CREATE TABLE IF NOT EXISTS "Person" (
    "person_id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255),
    "gender" INT,
    "dob" TIMESTAMPTZ,
    "phone" VARCHAR(15),
    "avatar_url" VARCHAR(255),
    "position" VARCHAR(255),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "Person" IS 'Tortoise-based log model.';
CREATE TABLE IF NOT EXISTS "Face" (
    "face_id" SERIAL NOT NULL PRIMARY KEY,
    "FrameFilePath" TEXT,
    "X" DOUBLE PRECISION,
    "Y" DOUBLE PRECISION,
    "Width" INT,
    "Height" INT,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "person_id" INT REFERENCES "Person" ("person_id") ON DELETE CASCADE
);
COMMENT ON TABLE "Face" IS 'Tortoise-based log model.';
CREATE TABLE IF NOT EXISTS "User" (
    "user_id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(200) NOT NULL,
    "username" VARCHAR(200) NOT NULL UNIQUE,
    "password" VARCHAR(200) NOT NULL,
    "manager" BOOL NOT NULL,
    "person_id" INT NOT NULL UNIQUE REFERENCES "Person" ("person_id") ON DELETE CASCADE
);
COMMENT ON TABLE "User" IS 'Data model for user.';
CREATE TABLE IF NOT EXISTS "Zone" (
    "zone_id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255),
    "description" VARCHAR(255),
    "placeholder_url" VARCHAR(255),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "Zone" IS 'Tortoise-based zone model.';
CREATE TABLE IF NOT EXISTS "AttendanceTracking" (
    "tracking_id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "camera_id" INT REFERENCES "Zone" ("zone_id") ON DELETE CASCADE,
    "face_id" INT REFERENCES "Face" ("face_id") ON DELETE CASCADE
);
COMMENT ON TABLE "AttendanceTracking" IS 'Tortoise-based log model.';
CREATE TABLE IF NOT EXISTS "Camera" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255),
    "description" VARCHAR(256),
    "connect_uri" VARCHAR(256),
    "placeholder_url" VARCHAR(255),
    "type" INT,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "zone_id" INT REFERENCES "Zone" ("zone_id") ON DELETE CASCADE
);
COMMENT ON TABLE "Camera" IS 'Tortoise-based camera model.';
CREATE TABLE IF NOT EXISTS "Log" (
    "log_id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "camera_id" INT NOT NULL REFERENCES "Zone" ("zone_id") ON DELETE CASCADE,
    "face_id" INT NOT NULL REFERENCES "Face" ("face_id") ON DELETE CASCADE
);
COMMENT ON TABLE "Log" IS 'Tortoise-based log model.';
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
COMMENT ON TABLE "EventLog" IS 'Tortoise-based log model.';
CREATE TABLE IF NOT EXISTS "ZoneSetting" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "description" VARCHAR(255),
    "config" VARCHAR(255) NOT NULL,
    "zone_id" INT REFERENCES "Zone" ("zone_id") ON DELETE CASCADE
);
COMMENT ON TABLE "ZoneSetting" IS 'Model for demo purpose.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
