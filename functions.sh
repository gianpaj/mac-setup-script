# Convert video to gif file.
# Usage: video2gif filename (scale) (fps)
video2gif() {
  filename="${1%.*}"
  ffmpeg -i "${1}" -filter_complex "fps=${3:-10},scale=${2:-320}:-1:flags=lanczos,split [o1] [o2];[o1] palettegen [p]; [o2] fifo [o3];[o3] [p] paletteuse" "${filename}".gif
}