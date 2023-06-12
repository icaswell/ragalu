
function get_if_empty () {
  filename="$1"
  url="$2"
  if [ -s $filename ]; then
    echo "The file is not empty.";
  else
    wget -O "$filename" "$url"
  fi
}

for i in `seq 1001 36095` ; do
    get_if_empty "everything_post_${i}" "https://www.rasikas.org/forums/viewtopic.php?t=$i"
done
