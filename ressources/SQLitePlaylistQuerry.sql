SELECT DISTINCT m.filename, a.name, m.title
FROM Playlist p
Inner Join playlistmediarelation pm ON pm.playlist_id=p.id_playlist
Inner Join Media m ON m.id_media=pm.media_id
Inner Join MediaArtistRelation ma ON ma.artist_id=m.artist_id
Inner Join artist a on a.id_artist=m.artist_id
WHERE p.name = 'final'
ORDER BY m.filename