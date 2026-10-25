# basal-register — Hermes desktop plugin

A small bottom pane for the Hermes desktop app: a personal decision
tracker. Entries live in the pane's own storage; nothing outside the pane
is read or written.

- propose an item (BASAL-NNN, timestamped)
- decide it (sets status + a review date +30d)
- review outcomes (worked / partial / failed)
- copy the whole list as markdown (plain BASAL-NNN format)

## Install

1. Copy `plugin.js` to `<hermes-home>/desktop-plugins/basal-register/plugin.js`
   (folder name must equal the plugin id).
2. In the desktop app: command palette (⌘K) → **Reload desktop plugins**.
3. The "basal register" pane docks under the conversation.

Data persists in the plugin's own storage until you paste the markdown
export wherever you keep your notes.
