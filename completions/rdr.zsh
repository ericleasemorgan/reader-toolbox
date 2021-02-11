if [[ ! -o interactive ]]; then
    return
fi

compctl -K _rdr rdr

_rdr() {
  local word words completions
  read -cA words
  word="${words[2]}"

  if [ "${#words}" -eq 2 ]; then
    completions="$(rdr commands)"
  else
    completions="$(rdr completions "${word}")"
  fi

  reply=("${(ps:\n:)completions}")
}
