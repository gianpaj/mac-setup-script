# Local archive before wiping a Mac

`archive-local.py` copies local code, configuration, data, and Git history to an external drive. It preserves the folder hierarchy, verifies new file copies with SHA-256, and saves commits and stashes absent from previously verified remotes in Git bundles. It never fetches, pulls, pushes, or deletes source repositories.

Requires Python 3 and Git. The default destination is `/Volumes/WD_BLACK/mbp-archive` and must already exist. Each new run creates a dated subfolder; it does not overwrite earlier archives.

## State files

New repository archives use machine-specific audit files from `~/backup-repo-audit`:

- `inventory.json`: repository paths.
- `fetch-results.json`: completed remote fetches and their reference namespaces.
- `results.json`: repository audit results.
- `outside-repositories.json`: loose files and directories outside repositories.

These files are not included in this repository. The previously fetched `refs/backup-audit/20261003-confirm/` references must still exist in the source repositories. Set `MBP_ARCHIVE_STATE_DIR` to use another state directory. This script does not perform a fresh remote audit.

The included folder selections reflect the October 2026 laptop archive: Git projects under `github`, `freelance`, and `projects-old`; full source/history copies for `twinfoundation/ui`, `Thinkful-Ed`, and `tts-api-bench`; and all eleven selected Downloads folders. Clark/Azure and Onova/Bitbucket projects are excluded. Review these selections before using the script for another backup.

## Usage

Run from this folder:

```sh
# Show the selected files and estimated size without copying.
python3 archive-local.py --plan-only

# Create the repository and Downloads archive.
python3 archive-local.py

# Resume the existing archive, using its saved plan.
python3 archive-local.py --resume "/Volumes/WD_BLACK/mbp-archive/local-only-2026-10-03-102556" --fast-resume

# Copy only the selected Downloads folders into a separate dated archive.
python3 archive-local.py --downloads-only
```

`--fast-resume` checks file existence and size and reuses previous checksum verification for completed items. Omit it to rehash completed files. New copies always receive checksum verification. Files changing during a copy get up to five attempts; persistently changing files stop the run so their application can be closed before resuming.

Repository scans exclude `node_modules`, `.next`, `.venv`, and other named dependency/cache folders. Downloads folders are copied in full. Other generated directories such as `build` are preserved conservatively. Symlinks are recorded in manifests, and filenames incompatible with exFAT are encoded with their original names retained for restoration. Extended macOS metadata is not fully preserved.

Git bundles preserve branch history, stashes, reflog-only commits, and full local history where remote recovery cannot be verified. A temporary bare repository supplies names for reflog-only commits without changing the source repository's refs. Repositories without commits preserve their working files and staged/unstaged patches.

Each archive contains `RESTORE.txt`, per-item manifests, and `archive-manifest.json`. Treat a run as complete only when the script reports `Archive complete` and the manifest has `complete: true`. Use the restoration instructions and test important files before wiping the laptop.

## Recovery checks

These checks use temporary repositories and local files; they do not access the external drive or GitHub:

```sh
python3 check-archive.py
python3 check-resume.py
python3 check-unborn.py
```

They exercise full/incremental bundle recovery, stashes, reflog-only commits, partially staged changes, interrupted copies, changing files, fast resume, and repositories without commits or reflogs.
