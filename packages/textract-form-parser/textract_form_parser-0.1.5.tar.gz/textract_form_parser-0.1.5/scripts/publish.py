import argparse
import os
import subprocess

import requests
import semver
from dotenv import load_dotenv
from packaging import version


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Publish package to PyPI")
    parser.add_argument("--test", action="store_true", help="Publish to Test PyPI")
    return parser.parse_args()


def clean_previous_builds():
    """Remove previous build artifacts"""
    print("Cleaning previous builds...")
    subprocess.run(["rm", "-rf", "dist/", "build/", "*.egg-info/"])


def build_package():
    """Build the package"""
    print("Building package...")
    subprocess.run(["python", "-m", "build"])


def upload_to_pypi(test=False):
    """Upload to PyPI or Test PyPI"""
    load_dotenv()

    username = os.getenv("PYPI_USERNAME")
    password = os.getenv("PYPI_PASSWORD")

    if not username or not password:
        raise ValueError("PyPI credentials not found in environment variables")

    repository = (
        "https://test.pypi.org/legacy/" if test else "https://upload.pypi.org/legacy/"
    )
    print(f"Uploading to {'Test ' if test else ''}PyPI...")

    pypirc_content = f"""[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = {username}
password = {password}

[testpypi]
repository = https://test.pypi.org/legacy/
username = {username}
password = {password}
"""

    with open(os.path.expanduser("~/.pypirc"), "w") as f:
        f.write(pypirc_content)

    try:
        if test:
            subprocess.run(["twine", "upload", "--repository", "testpypi", "dist/*"])
        else:
            subprocess.run(["twine", "upload", "dist/*"])
    finally:
        os.remove(os.path.expanduser("~/.pypirc"))


def get_pypi_versions(package_name):
    """Get existing versions from PyPI"""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        if response.status_code == 200:
            return list(response.json()["releases"].keys())
        return []
    except:
        return []


def validate_version(new_version, package_name="textract-form-parser"):
    """Validate that the new version doesn't exist"""
    existing_versions = get_pypi_versions(package_name)
    if new_version in existing_versions:
        raise ValueError(
            f"Version {new_version} already exists on PyPI. Please increment version."
        )

    try:
        version.parse(new_version)
    except version.InvalidVersion:
        raise ValueError(f"Invalid version format: {new_version}")


def get_latest_version(package_name="textract-form-parser"):
    """Get the latest version from PyPI"""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        if response.status_code == 200:
            versions = list(response.json()["releases"].keys())
            return sorted(versions, key=lambda v: [int(x) for x in v.split(".")])[-1]
        return "0.1.5"  # Default if package doesn't exist
    except:
        return "0.1.5"


def increment_version(current_version):
    """Increment the patch version"""
    v = semver.VersionInfo.parse(current_version)
    return str(v.bump_patch())


def update_version():
    """Update package version in setup.py"""
    current_version = os.getenv("PACKAGE_VERSION")
    if not current_version:
        current_version = get_latest_version()
        new_version = increment_version(current_version)
    else:
        new_version = current_version

    print(f"Updating version to {new_version}...")

    with open("setup.py", "r") as f:
        content = f.read()

    import re

    new_content = re.sub(r'version="[^"]*"', f'version="{new_version}"', content)

    with open("setup.py", "w") as f:
        f.write(new_content)

    return new_version


def main():
    """Main publishing workflow"""
    try:
        args = parse_args()
        load_dotenv()

        update_version()
        clean_previous_builds()
        build_package()

        if args.test:
            print("\nPublishing to Test PyPI...")
            upload_to_pypi(test=True)
        else:
            print("\nPublishing to PyPI...")
            upload_to_pypi(test=False)

        print("\nPackage published successfully!")

    except Exception as e:
        print(f"\nError during publishing: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
