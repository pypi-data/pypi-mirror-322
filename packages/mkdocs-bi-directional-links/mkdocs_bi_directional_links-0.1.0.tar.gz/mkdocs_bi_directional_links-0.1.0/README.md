# MkDocs Bi-Directional Links Plugin

[![PyPI Version](https://img.shields.io/pypi/v/mkdocs-bi-directional-links)](https://pypi.org/project/mkdocs-bi-directional-links/)
[![License](https://img.shields.io/pypi/l/mkdocs-bi-directional-links)](https://github.com/yourusername/mkdocs-bi-directional-links/blob/main/LICENSE)

A MkDocs plugin to support bi-directional links in Markdown files, allowing you to easily link between pages, images, videos, and audio files.

## Features

- **Bi-Directional Links**: Use `[[page]]` or `[[page|text]]` syntax to create links between Markdown files.
- **File Type Support**: Supports linking to Markdown files, images (`.png`, `.jpg`, etc.), videos (`.mp4`, `.webm`), and audio files (`.mp3`, `.wav`).
- **Dynamic Path Resolution**: Automatically resolves file paths based on the current file's location.
- **Site URL Integration**: If `site_url` is configured in MkDocs, the plugin will dynamically adjust links to include the correct base path.

## Installation

Install the plugin via pip:

```bash
pip install mkdocs-bi-directional-links
```

## Usage

1. Add the plugin to your `mkdocs.yml` configuration file:

    ```yaml
    plugins:
      - bi_directional_links
    ```

2. Use the `[[page]]` or `[[page|text]]` syntax in your Markdown files to create bi-directional links.

    ```markdown
    [[page1]]  # Links to page1.md
    [[page2|Custom Text]]  # Links to page2.md with custom text
    [[image.png]]  # Embeds an image
    [[video.mp4]]  # Embeds a video
    [[audio.mp3]]  # Embeds an audio file
    ```

3. Build your MkDocs site as usual:

    ```bash
    mkdocs build
    ```

## Configuration

The plugin supports the following optional configuration in `mkdocs.yml`:

```yaml
plugins:
  - bi_directional_links:
      debug: false  # Enable debug logging
```

## Examples

### Linking to a Markdown File

```markdown
[[page1]]  # Links to page1.md
[[page2|Custom Text]]  # Links to page2.md with custom text
```

### Embedding an Image

```markdown
[[image.png]]  # Embeds an image
```

### Embedding a Video

```markdown
[[video.mp4]]  # Embeds a video
```

### Embedding an Audio File

```markdown
[[audio.mp3]]  # Embeds an audio file
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/yourusername/mkdocs-bi-directional-links).

## Support

If you encounter any issues or have questions, please open an issue on [GitHub](https://github.com/yourusername/mkdocs-bi-directional-links).
