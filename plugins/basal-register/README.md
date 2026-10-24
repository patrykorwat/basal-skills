# basal-register — Hermes desktop plugin

A bottom pane for the Hermes desktop app that keeps the basal community's
decision register at hand:

- propose an item (BASAL-NNN, timestamped)
- decide it (sets status + a review date +30d)
- review outcomes (worked / partial / failed)
- copy the whole register as markdown (plain decision-register format)

## Install

1. Copy `plugin.js` to `<hermes-home>/desktop-plugins/basal-register/plugin.js`
   (folder name must equal the plugin id).
2. In the desktop app: command palette (⌘K) → **Reload desktop plugins**.
3. The "basal register" pane docks under the conversation.

Data persists in the plugin's own storage. Entries live in the pane until you
paste the markdown export into the register file.
