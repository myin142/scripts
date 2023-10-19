DIR="$(pwd)"
KRITA="$HOME/.local/share/krita/pykrita"

ln -sf $DIR/exporter $KRITA/
ln -sf $DIR/exporter.desktop $KRITA/

ln -sf $DIR/toggle_docker $KRITA/
ln -sf $DIR/toggle_docker.desktop $KRITA/
