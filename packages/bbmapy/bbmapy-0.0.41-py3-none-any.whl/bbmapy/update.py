import os
import re
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path

def get_bbmap_version(vendor_dir):
    """Get BBMap version by running bbmap.sh version"""
    try:
        # Run bbmap.sh version and capture output
        bbmap_path = os.path.join(vendor_dir, 'bbmap', 'bbmap.sh')
        # print(bbmap_path)
        result = subprocess.run([bbmap_path, 'version'], capture_output=True)
        
        # Get second line and extract version
        # print(result.stderr)
        version_line = result.stderr.decode('utf-8').split('\n')[1]
        # print(version_line)
        version_match = re.search(r'BBTools version (\d+\.\d+)', version_line)
        if version_match:
            return version_match.group(1)
        raise ValueError("Could not parse BBMap version from output")
    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to run bbmap.sh version")

def download_bbtools():
    """Download latest BBTools from SourceForge"""
    bbtools_url = "https://sourceforge.net/projects/bbmap/files/latest/download"
    
    print("Downloading BBTools...")
    with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as tmp_file:
        urllib.request.urlretrieve(bbtools_url, tmp_file.name)
        return tmp_file.name

def extract_bbtools(archive_path, vendor_dir):
    """Extract BBTools archive to vendor directory"""
    print("Extracting BBTools...")
    
    # Clear vendor directory
    if os.path.exists(vendor_dir):
        shutil.rmtree(vendor_dir)
    os.makedirs(vendor_dir)
    
    # Extract archive
    shutil.unpack_archive(archive_path, vendor_dir)

def update_version(new_version):
    """Update version in pyproject.toml and README.md"""
    # Update pyproject.toml
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        # Update version in pyproject.toml
        version_match = re.search(r'version = "0.0.(\d+)"', content)
        new_version = int(version_match.group(1))+1
        new_version = f"0.0.{new_version}"
        content = re.sub(
            r'version = "[^"]+"',
            f'version = "{new_version}"',
            content
        )
        pyproject_path.write_text(content)
        print(f"Updated pyproject.toml version to {new_version}")
    
    # Update README.md
    readme_path = Path("README.md")
    if readme_path.exists():
        content = readme_path.read_text()
        # Update version badge or version section in README
        content = re.sub(
            r'Current BBMap version: 0.0.\d+',
            f'Current BBMap version: {new_version}',
            content
        )
        readme_path.write_text(content)
        print(f"Updated README.md version to {new_version}")

def regenerate_commands():
    """Regenerate Python commands from BBTools scripts"""
    print("Regenerating commands...")
    subprocess.run(['python', '-m', 'bbmapy.scanner'], check=True)

def main():
    # Get package root directory
    package_root = Path(__file__).parent.parent
    print(package_root)
    vendor_dir = package_root / "bbmapy/vendor"
    # bbmap_dir = vendor_dir / "bbmap"
    os.makedirs(vendor_dir, exist_ok=True)
    
    try:
        # Download and extract BBTools
        archive_path = download_bbtools()
        extract_bbtools(archive_path, vendor_dir)
        os.unlink(archive_path)
        
        # Get and update version
        bbmap_version = get_bbmap_version(vendor_dir)
        update_version(bbmap_version)
        
        # Regenerate commands
        regenerate_commands()
        
        print("Update completed successfully!")
        
    except Exception as e:
        print(f"Error during update: {e}")
        raise

if __name__ == "__main__":
    main() 