CREATE TABLE "User" (
  "UserID" SERIAL PRIMARY KEY,
  "Username" VARCHAR NOT NULL UNIQUE,
  "Visibility" VARCHAR NOT NULL
);

CREATE TABLE "Song" (
  "SongID" SERIAL PRIMARY KEY,
  "ReleaseDate" DATE NOT NULL,
  "Name" VARCHAR NOT NULL
);

CREATE TABLE "Artist" (
  "ArtistID" SERIAL PRIMARY KEY,
  "Name" VARCHAR NOT NULL
);

CREATE TABLE "StreamingPlatform" (
  "StreamingPlatformID" SERIAL PRIMARY KEY,
  "Name" VARCHAR NOT NULL
);

CREATE TABLE "Album" (
  "AlbumID" SERIAL PRIMARY KEY,
  "Name" VARCHAR NOT NULL,
  "ArtistID" INT NOT NULL,
  FOREIGN KEY ("ArtistID") REFERENCES "Artist" ("ArtistID") ON DELETE CASCADE
);



-- Diary entries and diary related functionality

CREATE TABLE "DiaryEntry" (
  "EntryID" SERIAL PRIMARY KEY,
  "Date" DATE NOT NULL,
  "Description" TEXT,
  "Visibility" VARCHAR NOT NULL,
  "UserID" INT NOT NULL,
  FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE
);

CREATE TABLE "DiaryReport" (
  "ReportID" SERIAL PRIMARY KEY,
  "Date" DATE NOT NULL,
  "Visibility" VARCHAR NOT NULL,
  "Description" TEXT,
  "UserID" INT,
  FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE
);


-- In Between tables 

CREATE TABLE "Review" (
  "ReviewID" SERIAL PRIMARY KEY,
  "Contents" TEXT,
  "Visibility" VARCHAR NOT NULL,
  "SongID" INT NOT NULL,
  "UserID" INT NOT NULL,
  FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID") ON DELETE CASCADE,
  FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE
);


CREATE TABLE "ReportEntries" (
  "ReportID" int NOT NULL,
  "EntryID" int NOT NULL,
  PRIMARY KEY ("ReportID", "EntryID"),
  FOREIGN KEY ("ReportID") REFERENCES "DiaryReport" ("ReportID") ON DELETE CASCADE,
  FOREIGN KEY ("EntryID") REFERENCES "DiaryEntry" ("EntryID") ON DELETE CASCADE

);

CREATE TABLE "UserFriends" (
  "UserID" INT NOT NULL,
  "FriendUserID" INT,
  PRIMARY KEY ("UserID", "FriendUserID")
  FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE,
  FOREIGN KEY ("FriendUserID") REFERENCES "User" ("UserID") ON DELETE CASCADE

);

-- user activity

CREATE TABLE "UserDiaryEntries" (
  "UserID" INT NOT NULL,
  "EntryID" INT NOT NULL,
  PRIMARY KEY ("UserID", "EntryID")
  FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE,
  FOREIGN KEY ("EntryID") REFERENCES "DiaryEntry" ("EntryID") ON DELETE CASCADE
);

CREATE TABLE "UserDiaryReports" (
  "UserID" int NOT NULL,
  "ReportID" int NOT NULL,
  PRIMARY KEY ("UserID", "ReportID"),
  FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE,
  FOREIGN KEY ("ReportID") REFERENCES "DiaryReport" ("ReportID") ON DELETE CASCADE
);

CREATE TABLE "UserReviews" (
  "UserID" int NOT NULL,
  "ReviewID" int NOT NULL,
  PRIMARY KEY ("UserID", "ReviewID")
  FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE,
  FOREIGN KEY ("ReviewID") REFERENCES "Review" ("ReviewID") ON DELETE CASCADE
);

CREATE TABLE "DiaryEntrySongs" (
  "EntryID" INT NOT NULL,
  "SongID" INT NOT NULL,
  PRIMARY KEY ("EntryID", "SongID"),
  FOREIGN KEY ("EntryID") REFERENCES "DiaryEntry" ("EntryID") ON DELETE CASCADE,
  FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID") ON DELETE CASCADE
);

CREATE TABLE "StreamingPlatformSongs" (
  "StreamingPlatformID" INT NOT NULL,
  "SongID" INT NOT NULL,
  PRIMARY KEY ("StreamingPlatformID", "SongID")
  FOREIGN KEY ("StreamingPlatformID") REFERENCES "StreamingPlatform" ("StreamingPlatformID") ON DELETE CASCADE,
  FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID") ON DELETE CASCADE
);

CREATE TABLE "AlbumSongs" (
  "SongID" int NOT NULL,
  "AlbumID" int NOT NULL,
  PRIMARY KEY ("SongID", "AlbumID")
  FOREIGN KEY ("AlbumID") REFERENCES "Album" ("AlbumID") ON DELETE CASCADE,
  FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID") ON DELETE CASCADE
);

CREATE TABLE "ArtistAlbums" (
  "ArtistID" int NOT NULL,
  "AlbumID" int NOT NULL,
  PRIMARY KEY ("ArtistID", "AlbumID")
  FOREIGN KEY ("ArtistID") REFERENCES "Artist" ("ArtistID") ON DELETE CASCADE,
  FOREIGN KEY ("AlbumID") REFERENCES "Album" ("AlbumID") ON DELETE CASCADE
);

-- Add foreign key constraints with ON DELETE CASCADE

ALTER TABLE "DiaryEntry" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE;

ALTER TABLE "DiaryReport" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE SET NULL;

ALTER TABLE "Review" ADD FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID") ON DELETE CASCADE;

ALTER TABLE "ReportEntries" ADD FOREIGN KEY ("ReportID") REFERENCES "DiaryReport" ("ReportID") ON DELETE CASCADE;

ALTER TABLE "ReportEntries" ADD FOREIGN KEY ("EntryID") REFERENCES "DiaryEntry" ("EntryID") ON DELETE CASCADE;

ALTER TABLE "UserFriends" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID") ON DELETE CASCADE;

ALTER TABLE "UserFriends" ADD FOREIGN KEY ("FriendUserID") REFERENCES "User" ("UserID") ON DELETE CASCADE;

ALTER TABLE "UserDiaryEntries" ADD FOREIGN KEY ("EntryID") REFERENCES "DiaryEntry" ("EntryID") ON DELETE CASCADE;

ALTER TABLE "UserDiaryReports" ADD FOREIGN KEY ("ReportID") REFERENCES "DiaryReport" ("ReportID") ON DELETE CASCADE;

ALTER TABLE "UserReviews" ADD FOREIGN KEY ("ReviewID") REFERENCES "Review" ("ReviewID") ON DELETE CASCADE;

ALTER TABLE "DiaryEntrySongs" ADD FOREIGN KEY ("EntryID") REFERENCES "DiaryEntry" ("EntryID") ON DELETE CASCADE;

ALTER TABLE "DiaryEntrySongs" ADD FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID") ON DELETE CASCADE;

ALTER TABLE "StreamingPlatformSongs" ADD FOREIGN KEY ("StreamingPlatformID") REFERENCES "StreamingPlatform" ("StreamingPlatformID") ON DELETE CASCADE;

ALTER TABLE "StreamingPlatformSongs" ADD FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID") ON DELETE CASCADE;

ALTER TABLE "AlbumSongs" ADD FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID") ON DELETE CASCADE;

ALTER TABLE "AlbumSongs" ADD FOREIGN KEY ("AlbumID") REFERENCES "Album" ("AlbumID") ON DELETE CASCADE;

ALTER TABLE "ArtistAlbums" ADD FOREIGN KEY ("ArtistID") REFERENCES "Artist" ("ArtistID") ON DELETE CASCADE;

ALTER TABLE "ArtistAlbums" ADD FOREIGN KEY ("AlbumID") REFERENCES "Album" ("AlbumID") ON DELETE CASCADE;
