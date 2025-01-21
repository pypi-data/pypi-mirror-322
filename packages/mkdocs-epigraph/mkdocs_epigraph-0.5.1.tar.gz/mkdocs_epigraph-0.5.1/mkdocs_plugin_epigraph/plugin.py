from mkdocs.plugins import BasePlugin
from logging import getLogger
from pathlib import Path
from mkdocs import utils

log = getLogger('mkdocs.epigraph')

class EpigraphPlugin(BasePlugin):

    def on_config(self, config):
        """Add the epigraph.css file to the extra_css list."""
        css = Path("css/epigraph.css")
        self.css_output_path = Path(config["site_dir"]) / css
        self.css_base_path = Path(__file__).parent / css

        config["extra_css"].append(str(css))
        return config

    def on_page_content(self, html, page, config, files):
        """Process the page content and add the epigraph if it exists."""
        if "epigraph" not in page.meta:
            return html
        text = page.meta["epigraph"]["text"]
        source = page.meta["epigraph"]["source"]
        lines = html.split("\n")

        # Find first header tag
        for i, line in enumerate(lines):
            if "<h" in line:
                lines.insert(
                    i + 1,
                    (
                        f'<blockquote class="epigraph">{text}'
                        f"<footer>{source}</footer></blockquote>"
                    ),
                )
                break
        else:
            log.warning("No header found in %s", page.file.src_path)

        return "\n".join(lines)

    def on_post_build(self, config):
        """Copy the epigraph.css file to the site directory."""
        utils.copy_file(self.css_base_path, self.css_output_path)
