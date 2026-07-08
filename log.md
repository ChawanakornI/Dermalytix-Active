# Log

## 2026-07-08 12:27:45 +07

- Started Dermalytix Active rename implementation.
- Updated runtime app labels and package/bundle identifiers across Flutter, Android, iOS, web, macOS, Linux, and Windows.
- Updated project-facing documentation and backend docstrings for the new name.
- Cleaned local VS Code and ignore-path references that still used the old project folder name.
- Fixed the Flutter asset declaration to use the existing `assets/models/` directory instead of missing `assets/model/`.
- Left `assets/images/AllcareTextVector.svg` unchanged per request; current wordmark asset references still point to that file until a replacement wordmark is available.

## 2026-07-08 13:20:00 +07

- Flattened the repository layout by moving tracked Flutter/backend project files from `AllCare/` into the repository root.
- Replaced the old root README and `.gitignore` with the app-level versions.
- Removed tracked `.DS_Store` files during the layout cleanup.
