import subprocess
import os
import logging
import json
import platform
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

class Packager:
    def __init__(self, target=None, platform="manylinux2014_x86_64", only_tracked=True, additional_files=None):
        self.target_dir = target or os.getcwd()
        self.platform = platform
        self.only_tracked = only_tracked
        self.additional_files = additional_files
        self.dependencies_dir = os.path.join(self.target_dir, 'dependencies')
        self.logger = logging.getLogger(__name__)

    def download_packages(self):
        """Download packages specified in requirements.txt with specific platform constraints"""
        try:
            # Ensure dependencies directory exists
            Path(self.dependencies_dir).mkdir(parents=True, exist_ok=True)
            
            # Check for different dependency specification files
            # and construct the appropriate pip download command
            requirements_path = os.path.join(self.target_dir, 'requirements.txt')
            if os.path.exists(requirements_path):
                self.logger.info("Downloading packages from requirements.txt")
                cmd = [
                    'pip', 'download',
                    '-r', requirements_path,
                    '-d', self.dependencies_dir,
                    '--platform', self.platform,
                    '--only-binary=:all:'
                ]
            elif os.path.exists(os.path.join(self.target_dir, 'pyproject.toml')) or os.path.exists(os.path.join(self.target_dir, 'setup.py')):
                self.logger.info("Downloading packages from pyproject.toml or setup.py")
                cmd = [
                    'pip', 'download',
                    '.', 
                    '-d', self.dependencies_dir,
                    '--platform', self.platform,
                    '--only-binary=:all:'
                ]
            else:
                raise FileNotFoundError(f"No dependency specification file found (requirements.txt, pyproject.toml, or setup.py)")
            
            # Execute pip download command
            # TODO: Print out the command output in real-time
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.logger.info("Package download completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error downloading packages: {e}")
            self.logger.error(f"Error output: {e.stderr}")
            return False
        
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return False
    
    def generate_manifest(self):
        """Generate a manifest file containing package metadata"""
        manifest = {
            "timeStamp": datetime.now().isoformat(),
            "platformVersion": self.platform,
            "entities": [],
            "runtime": "python",
            "runtimeVersion": platform.python_version(),
            "buildVersion": "",
            "buildType": "release"
        }
        
        self.logger.info("Manifest generated successfully")
        return manifest

    def create_archive(self, archive_name):
        """Create a ZIP archive of the downloaded packages"""
        try:
            dir_to_archive = Path(self.target_dir)
            archive_path = os.path.join(self.target_dir, archive_name)
            
            # Generate manifest as JSON string
            manifest = self.generate_manifest()
            manifest_str = json.dumps(manifest, indent=2)

            if self.only_tracked:
                # Get tracked files using git
                files = subprocess.check_output(
                    ['git', 'ls-files', '--exclude-standard'],
                    cwd=dir_to_archive,
                    text=True
                ).splitlines()
            else:
                # Get all files in the directory
                files = self._get_nested_files(dir_to_archive, dir_to_archive)
            
            # Add dependencies directory
            if os.path.exists(self.dependencies_dir):
                dependencies_files = self._get_nested_files(self.dependencies_dir, dir_to_archive)
                files.extend(file for file in dependencies_files if file not in files)
            
            # Add additional files
            if self.additional_files:
                for path in self.additional_files:
                    full_path = os.path.join(dir_to_archive, path)
                    if os.path.isfile(full_path):
                        files.append(path)
                    elif os.path.isdir(full_path):
                        additional_files = self._get_nested_files(full_path, dir_to_archive)
                        files.extend(additional_files)
            
            self.logger.info(f"Files to be included in the archive: {files}")

            with ZipFile(archive_path, 'w') as zip_file:
                # Add manifest directly as string
                zip_file.writestr('manifest.json', manifest_str)
                
                # Add files
                for file in files:
                    file_path = os.path.join(dir_to_archive, file)
                    zip_file.write(file_path, file)

            self.logger.info(f"Archive created successfully: {archive_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating archive: {e}")
            return False

    def _get_nested_files(self, target_dir, base_dir):
        files = []
        for root, _, filenames in os.walk(target_dir):
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), base_dir)
                files.append(rel_path)
        return files

    def download_and_archive(self, archive_name):
        """Main method to download packages and create archive"""
        if self.download_packages():
            self.create_archive(archive_name)
        else:
            self.logger.error("Skipping archive creation due to download errors")