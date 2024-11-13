#!/usr/bin/env bash

#
# add artists
#
curl -X POST http://localhost:5400/artist/ \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=The 1975"

curl -X POST http://localhost:5400/artist/ \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Alvvays"

curl -X POST http://localhost:5400/artist/ \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=The Japanese House"

curl -X POST http://localhost:5400/artist/ \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=The Strokes"

curl -X POST http://localhost:5400/artist/ \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Flipturn"

curl -X POST http://localhost:5400/artist/ \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Clairo"

#
# add albums
#
curl -X POST http://localhost:5400/album/The%201975 \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=The 1975"

curl -X POST http://localhost:5400/album/The%201975 \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=I Like It When You Sleep, for You Are So Beautiful Yet So Unaware of It"

curl -X POST http://localhost:5400/album/The%201975 \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Notes on a Conditional Form"

curl -X POST http://localhost:5400/album/The%201975 \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Being Funny in a Foreign Language"

curl -X POST http://localhost:5400/album/Alvvays \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Alvvays"

curl -X POST http://localhost:5400/album/Alvvays \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Antisocialites"

curl -X POST http://localhost:5400/album/Alvvays \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Blue Rev"

curl -X POST http://localhost:5400/album/The%20Japanese%20House \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Good at Falling"

curl -X POST http://localhost:5400/album/The%20Japanese%20House \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Chewing Cotton Wool"

curl -X POST http://localhost:5400/album/The%20Japanese%20House \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=In the End It Always Does"

curl -X POST http://localhost:5400/album/The%20Strokes \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Is This It"

curl -X POST http://localhost:5400/album/The%20Strokes \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Room on Fire"

curl -X POST http://localhost:5400/album/The%20Strokes \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=First Impressions of Earth"

curl -X POST http://localhost:5400/album/The%20Strokes \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=The New Abnormal"

curl -X POST http://localhost:5400/album/Flipturn \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Heavy Colors"

curl -X POST http://localhost:5400/album/Flipturn \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Citrona"

curl -X POST http://localhost:5400/album/Flipturn \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Shadowglow"


curl -X POST http://localhost:5400/album/Clairo \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Immunity"

curl -X POST http://localhost:5400/album/Clairo \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Sling"

curl -X POST http://localhost:5400/album/Clairo \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Charm"

#
# songs
#
curl -X POST http://localhost:5400/song/The%201975 \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=The 1975"

curl -X POST http://localhost:5400/song/The%201975 \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Settle Down"

curl -X POST http://localhost:5400/song/I%20Like%20It%20When%20You%20Sleep%2C%20for%20You%20Are%20So%20Beautiful%20Yet%20So%20Unaware%20of%20It \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=A Change of Heart"

curl -X POST http://localhost:5400/song/I%20Like%20It%20When%20You%20Sleep%2C%20for%20You%20Are%20So%20Beautiful%20Yet%20So%20Unaware%20of%20It \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Paris"

curl -X POST http://localhost:5400/song/Notes%20on%20a%20Conditional%20Form \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Roadkill"

curl -X POST http://localhost:5400/song/Notes%20on%20a%20Conditional%20Form \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Frail State of Mind"

curl -X POST http://localhost:5400/song/Being%20Funny%20in%20a%20Foreign%20Language \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Happiness"

curl -X POST http://localhost:5400/song/Being%20Funny%20in%20a%20Foreign%20Language \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Part of the Band"

curl -X POST http://localhost:5400/song/Alvvays \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Adult Diversion"

curl -X POST http://localhost:5400/song/Alvvays \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Archie, Marry Me"

curl -X POST http://localhost:5400/song/Antisocialites \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=In Undertow"

curl -X POST http://localhost:5400/song/Antisocialites \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Dreams Tonite"

curl -X POST http://localhost:5400/song/Blue%20Rev \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Pharmacist"

curl -X POST http://localhost:5400/song/Blue%20Rev \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Easy On Your Own?"

curl -X POST http://localhost:5400/song/Good%20at%20Falling \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Lilo"

curl -X POST http://localhost:5400/song/Good%20at%20Falling \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Maybe You’re the Reason"

curl -X POST http://localhost:5400/song/Chewing%20Cotton%20Wool \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Chewing Cotton Wool"

curl -X POST http://localhost:5400/song/In%20the%20End%20It%20Always%20Does \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Boyhood"

curl -X POST http://localhost:5400/song/Is%20This%20It \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Someday"

curl -X POST http://localhost:5400/song/Is%20This%20It \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Last Nite"

curl -X POST http://localhost:5400/song/Room%20on%20Fire \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Reptilia"

curl -X POST http://localhost:5400/song/Room%20on%20Fire \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Under Control"

curl -X POST http://localhost:5400/song/First%20Impressions%20of%20Earth \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Juicebox"

curl -X POST http://localhost:5400/song/First%20Impressions%20of%20Earth \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Heart in a Cage"

curl -X POST http://localhost:5400/song/The%20New%20Abnormal \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Bad Decisions"

curl -X POST http://localhost:5400/song/The%20New%20Abnormal \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=At the Door"

curl -X POST http://localhost:5400/song/Heavy%20Colors \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=August"

curl -X POST http://localhost:5400/song/Heavy%20Colors \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Eclipse"

curl -X POST http://localhost:5400/song/Citrona \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Vanilla"

curl -X POST http://localhost:5400/song/Citrona \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Six Below"

curl -X POST http://localhost:5400/song/Shadowglow \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Playground"

curl -X POST http://localhost:5400/song/Shadowglow \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Hollow"

curl -X POST http://localhost:5400/song/Immunity \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Bags"

curl -X POST http://localhost:5400/song/Immunity \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Sofia"

curl -X POST http://localhost:5400/song/Sling \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Amoeba"

curl -X POST http://localhost:5400/song/Sling \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Blouse"

curl -X POST http://localhost:5400/song/Charm \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Juna"

curl -X POST http://localhost:5400/song/Charm \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=Thank You"
