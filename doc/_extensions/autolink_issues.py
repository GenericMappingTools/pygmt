# _extensions/autolink_issues.py
from docutils import nodes
from sphinx.transforms import SphinxTransform
import re

ISSUE_PATTERN = re.compile(r'#(\d+)')

class AutolinkIssuesTransform(SphinxTransform):
    default_priority = 500

    def apply(self):
        for node in self.document.traverse(nodes.Text):
            if ISSUE_PATTERN.search(node):
                parent = node.parent
                new_nodes = []
                parts = ISSUE_PATTERN.split(node)

                for i, part in enumerate(parts):
                    if i % 2 == 1:  # Odd indices are issue numbers
                        issue_number = part
                        ref = f'https://github.com/{self.config.github_repo}/issues/{issue_number}'
                        new_node = nodes.reference(f'#{issue_number}', f'#{issue_number}', refuri=ref)
                        new_nodes.append(new_node)
                    else:
                        new_nodes.append(nodes.Text(part))

                parent.replace(node, new_nodes)

def setup(app):
    app.add_transform(AutolinkIssuesTransform)
    app.add_config_value('github_repo', '', 'env')

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
