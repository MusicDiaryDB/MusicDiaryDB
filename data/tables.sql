CREATE TABLE "User" (
  "UserID" SERIAL PRIMARY KEY,
  "Username" varchar NOT NULL UNIQUE,
  "Visibility" varchar NOT NULL
);

CREATE TABLE "DiaryEntry" (
  "EntryID" SERIAL PRIMARY KEY,
  "Date" date NOT NULL,
  "Description" text,
  "Visibility" varchar NOT NULL,
  "UserID" int NOT NULL
);

CREATE TABLE "DiaryReport" (
  "ReportID" SERIAL PRIMARY KEY,
  "Date" date NOT NULL,
  "Visibility" varchar NOT NULL,
  "Description" text,
  "UserID" int
);

CREATE TABLE "Review" (
  "ReviewID" SERIAL PRIMARY KEY,
  "Contents" text,
  "Visibility" varchar NOT NULL,
  "SongID" int NOT NULL
);

CREATE TABLE "Song" (
  "SongID" SERIAL PRIMARY KEY,
  "ReleaseDate" date NOT NULL,
  "Name" varchar NOT NULL
);

CREATE TABLE "StreamingPlatform" (
  "StreamingPlatformID" SERIAL PRIMARY KEY,
  "Name" varchar NOT NULL
);

CREATE TABLE "Album" (
  "AlbumID" SERIAL PRIMARY KEY,
  "Name" varchar NOT NULL
);

CREATE TABLE "Artist" (
  "ArtistID" SERIAL PRIMARY KEY,
  "Name" varchar NOT NULL
);

CREATE TABLE "ReportEntries" (
  "ReportID" int NOT NULL,
  "EntryID" int NOT NULL,
  PRIMARY KEY ("ReportID", "EntryID")
);

CREATE TABLE "UserFriends" (
  "UserID" int NOT NULL,
  "FriendUserID" int,
  PRIMARY KEY ("UserID", "FriendUserID")
);

CREATE TABLE "UserDiaryEntries" (
  "UserID" int NOT NULL,
  "EntryID" int NOT NULL,
  PRIMARY KEY ("UserID", "EntryID")
);

CREATE TABLE "UserDiaryReports" (
  "UserID" int NOT NULL,
  "ReportID" int NOT NULL,
  PRIMARY KEY ("UserID", "ReportID")
);

CREATE TABLE "UserReviews" (
  "UserID" int NOT NULL,
  "ReviewID" int NOT NULL,
  PRIMARY KEY ("UserID", "ReviewID")
);

CREATE TABLE "DiaryEntrySongs" (
  "EntryID" int NOT NULL,
  "SongID" int NOT NULL,
  PRIMARY KEY ("EntryID", "SongID")
);

CREATE TABLE "StreamingPlatformSongs" (
  "StreamingPlatformID" int NOT NULL,
  "SongID" int NOT NULL,
  PRIMARY KEY ("StreamingPlatformID", "SongID")
);

CREATE TABLE "AlbumSongs" (
  "SongID" int NOT NULL,
  "AlbumID" int NOT NULL,
  PRIMARY KEY ("SongID", "AlbumID")
);

CREATE TABLE "ArtistAlbums" (
  "ArtistID" int NOT NULL,
  "AlbumID" int NOT NULL,
  PRIMARY KEY ("ArtistID", "AlbumID")
);

-- Add foreign key constraints with ON DELETE CASCADE

ALTER TABLE "DiaryEntry" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE;

ALTER TABLE "DiaryReport" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE SET NULL; -- Optional: You may want to set this to NULL instead of CASCADE

ALTER TABLE "Review" ADD FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID") ON DELETE CASCADE;

ALTER TABLE "ReportEntries" ADD FOREIGN KEY ("ReportID") REFERENCES "DiaryReport" ("ReportID") ON DELETE CASCADE;

ALTER TABLE "ReportEntries" ADD FOREIGN KEY ("EntryID") REFERENCES "DiaryEntry" ("EntryID") ON DELETE CASCADE;

ALTER TABLE "UserFriends" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE;

ALTER TABLE "UserFriends" ADD FOREIGN KEY ("FriendUserID") REFERENCES "User" ("UserID") ON DELETE CASCADE;

ALTER TABLE "UserDiaryEntries" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE;

ALTER TABLE "UserDiaryEntries" ADD FOREIGN KEY ("EntryID") REFERENCES "DiaryEntry" ("EntryID") ON DELETE CASCADE;

ALTER TABLE "UserDiaryReports" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE;

ALTER TABLE "UserDiaryReports" ADD FOREIGN KEY ("ReportID") REFERENCES "DiaryReport" ("ReportID") ON DELETE CASCADE;

ALTER TABLE "UserReviews" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE;

ALTER TABLE "UserReviews" ADD FOREIGN KEY ("ReviewID") REFERENCES "Review" ("ReviewID") ON DELETE CASCADE;

ALTER TABLE "DiaryEntrySongs" ADD FOREIGN KEY ("EntryID") REFERENCES "DiaryEntry" ("EntryID") ON DELETE CASCADE;

ALTER TABLE "DiaryEntrySongs" ADD FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID") ON DELETE CASCADE;

ALTER TABLE "StreamingPlatformSongs" ADD FOREIGN KEY ("StreamingPlatformID") REFERENCES "StreamingPlatform" ("StreamingPlatformID") ON DELETE CASCADE;

ALTER TABLE "StreamingPlatformSongs" ADD FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID") ON DELETE CASCADE;

ALTER TABLE "AlbumSongs" ADD FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID") ON DELETE CASCADE;

ALTER TABLE "AlbumSongs" ADD FOREIGN KEY ("AlbumID") REFERENCES "Album" ("AlbumID") ON DELETE CASCADE;

ALTER TABLE "ArtistAlbums" ADD FOREIGN KEY ("ArtistID") REFERENCES "Artist" ("ArtistID") ON DELETE CASCADE;

ALTER TABLE "ArtistAlbums" ADD FOREIGN KEY ("AlbumID") REFERENCES "Album" ("AlbumID") ON DELETE CASCADE;
