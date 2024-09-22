# To be executed in the music-list-play root directory.
pyinstaller main.py --clean --noconfirm --onedir --name music-list-player --add-data='C:\Program Files\VideoLAN\VLC\plugins':plugins --add-data='C:\Program Files\VideoLAN\VLC':VLC

Remove-Item -Path 'dist\music-list-player\_internal/plugins/plugins.dat'
Copy-Item -Path "configuration.toml" -Destination "dist\music-list-player\configuration.toml"
Copy-Item -Path "playlist.txt" -Destination "dist\music-list-player\playlist.txt"
New-Item -ItemType Directory -Force -Path "dist\music-list-player\.cache"

$compress = @{
  Path = "dist\music-list-player"
  CompressionLevel = "Fastest"
  DestinationPath = "music-list-player.zip"
}
Compress-Archive @compress