# Planning assets

This directory is intentionally lightweight so that template users can decide how they want to track tasks. Populate the files here with any workflow notes that help your project stay organized, or delete the directory entirely if you do not need it.

Provided files:

- `TODO.md` – start new work items here.
- `DONE.md` – move completed items here if you keep a running log.
- `ToDo.archive.md` – optional long-lived notes or a backlog that you want to preserve.
- `tasks.manifest.json` – machine-readable view of the task list (empty by default).
- `state.json` – space to store automation metadata (empty by default).
- `pr.json` – optional scratch file for tracking an in-progress pull request.
- `add_manifest_tasks.sh` – helper for appending items to the manifest.
- `sync_state.sh` – stub script you can extend to keep your plan files in sync.

These files are blank templates to avoid leaking details from the project this repository originated from. Feel free to replace or remove them as needed.
