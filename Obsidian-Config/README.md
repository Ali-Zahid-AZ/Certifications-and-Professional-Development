# Portable Obsidian configuration

This bundle was reconstructed from the `.obsidian` configuration in the private `obsidian-personal` vault for use on a separate work vault.

## Intentionally excluded

- **Obsidian Git** plugin and all of its configuration, per request.
- Personal recent-file history.
- Personal bookmarks.
- Hotkeys that pointed directly to personal vault files.
- `obsidian-icon-folder/data.json`, because it maps icons to personal vault paths/folders.
- Plugin executables (`main.js`), downloaded theme code, and icon packs/assets. Install the listed plugins and the **AnuPpuccin** theme normally through Obsidian, then copy this `.obsidian` configuration over the new vault.

## Notes

- The source `appearance.json` referenced CSS snippets named `code-block-width` and `nord-headers`, but those files are not present in the source Git repository. They were therefore removed from the portable enabled-snippet list.
- All custom CSS snippets that are actually present in the source repository are included under `.obsidian/snippets/`.
- Templater and Various Complements retain the original vault-relative template/dictionary paths. Adjust those paths if the work vault uses a different folder structure.

## Community plugins to install

Mononote, Table Editor, Dataview, Various Complements, Callout Manager, URL into Selection, Recent Files, Trash Explorer, Icon Folder, Auto Link Title, Automatic Table of Contents, Templater, Hotkeys for Specific Files, Regex Replace, Tag Wrangler, Status Bar Organizer, Settings Search, and Style Settings.

After installing the plugins and AnuPpuccin, close Obsidian, copy the `.obsidian` folder from this directory into the target vault, and reopen Obsidian.
