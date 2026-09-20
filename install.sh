#!/bin/bash
cd "$(git rev-parse --show-toplevel)/skills"
for d in */; do
  cp -r "$d" "$HOME/.config/opencode/skills/$d"
done
echo "✅ Installed $(ls -d */ | wc -l) skills"
