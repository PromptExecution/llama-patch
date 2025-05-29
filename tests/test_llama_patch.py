import pytest
import os
from click.testing import CliRunner
from llama_patch import apply_patch

@pytest.fixture
def setup_files():
    if not os.path.exists('src'):
        os.makedirs('src')
    with open('src/main.py', 'w') as f:
        f.write('''def target_function(x):
    # Original implementation
    return x + 1
class OldClass:
    def __init__(self):
        pass
''')

    yield

    # Cleanup after tests
    if os.path.exists('src/main.py'):
        os.remove('src/main.py')
    if os.path.exists('src'):
        os.rmdir('src')

@pytest.fixture
def patch_file():
    patch_content = '''--- src/main.py
?? def target_function
def target_function(x):
-    # Original implementation
+    # New implementation
-    return x + 1
+    return x * 2
--- src/main.py
?? class OldClass
- class OldClass:
-     def __init__(self):
-         pass
'''
    with open('patch.diff', 'w') as f:
        f.write(patch_content)
    yield 'patch.diff'
    os.remove('patch.diff')

def test_apply_patch_function(setup_files, patch_file):
    runner = CliRunner()
    result = runner.invoke(apply_patch, ['--llmpatch', patch_file, '--cwd', '.'])

    assert result.exit_code == 0

    with open('src/main.py', 'r') as f:
        content = f.read()
        assert 'def target_function(x):' in content
        assert '# New implementation' in content
        assert 'return x * 2' in content
        assert 'class OldClass' not in content

def test_apply_patch_stdin(setup_files):
    patch_content = '''--- src/main.py
?? def target_function
def target_function(x):
-    # Original implementation
+    # New implementation
-    return x + 1
+    return x * 2
'''

    runner = CliRunner()
    result = runner.invoke(apply_patch, ['--cwd', '.'], input=patch_content)

    assert result.exit_code == 0

    with open('src/main.py', 'r') as f:
        content = f.read()
        assert 'def target_function(x):' in content
        assert '# New implementation' in content
        assert 'return x * 2' in content

def test_prepend_append(setup_files):
    patch_content = '''--- src/main.py
?? <<
+import sys
--- src/main.py
?? >>
+print("End of file")
'''

    runner = CliRunner()
    result = runner.invoke(apply_patch, ['--llmpatch', '-', '--cwd', '.'], input=patch_content)

    assert result.exit_code == 0

    with open('src/main.py', 'r') as f:
        content = f.read()
        assert content.startswith('import sys\n')
        assert content.endswith('print("End of file")\n')

def test_verbose_flag(setup_files, patch_file):
    runner = CliRunner()
    result = runner.invoke(apply_patch, ['--llmpatch', patch_file, '--cwd', '.', '--verbose'])

    assert result.exit_code == 0
    assert 'DEBUG' in result.output

