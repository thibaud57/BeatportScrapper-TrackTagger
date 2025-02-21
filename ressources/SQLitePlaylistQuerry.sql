SELECT DISTINCT m.fileName, a.name, m.title
FROM Playlist p
INNER JOIN PlaylistMediaRelation pm ON pm.playlist_id = p.id_playlist
INNER JOIN Media m ON m.id_media = pm.media_id
INNER JOIN Artist a ON a.id_artist = m.artist_id
WHERE p.name = 'final'
ORDER BY CAST(m.fileName AS TEXT) COLLATE NOCASE
