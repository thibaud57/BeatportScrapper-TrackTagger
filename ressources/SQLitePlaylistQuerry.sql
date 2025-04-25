SELECT DISTINCT m.fileName
FROM Playlist p
INNER JOIN PlaylistMediaRelation pm ON pm.playlist_id = p.id_playlist
INNER JOIN Media m ON m.id_media = pm.media_id
WHERE p.name = 'final'
ORDER BY CAST(m.fileName AS TEXT) COLLATE NOCASE;