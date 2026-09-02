---
name: codex-file-reading
description: Read local non-Markdown files through deterministic, offline text extraction. Use when a PDF, DOCX, PPTX, XLSX, HTML, CSV, JSON, XML, ZIP, EPUB, image, or audio file must be inspected as part of a Codex task.
---

# Codex File Reading

Use the installed local converter for files that are not plain text:

```bash
markitdown <file> -o /tmp/_md_output.md
```

Then read `/tmp/_md_output.md`. The base conversion is local-only and does not call an API. Treat image description and audio transcription as opt-in enhanced operations; do not enable them silently, and never send private project, client, vault, credential, or session content to an external service.

Preserve the original file. Do not write the converted output into the repository unless the task explicitly requests an artifact there. If conversion fails or the output is incomplete, report the limitation and use an appropriate installed format-specific skill rather than guessing from the filename.
