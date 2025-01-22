import unittest
from unittest.mock import patch, MagicMock
from wmk.packager import Packager

class TestPackager(unittest.TestCase):
    def setUp(self):
        self.test_dir = "/test/dir"
        self.packager = Packager(target=self.test_dir)

    @patch('wmk.packager.Path')
    @patch('wmk.packager.subprocess.run')
    @patch('wmk.packager.os.path.exists')
    def test_download_packages_success(self, mock_exists, mock_run, mock_path):
        # Setup mocks
        mock_exists.return_value = True
        mock_run.return_value = MagicMock(returncode=0)
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance

        # Execute test
        result = self.packager.download_packages()

        # Verify
        self.assertTrue(result)
        mock_path_instance.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_run.assert_called_once()

    @patch('wmk.packager.os.path.exists')
    def test_download_packages_no_requirements(self, mock_exists):
        mock_exists.return_value = False
        result = self.packager.download_packages()
        self.assertFalse(result)

    @patch('wmk.packager.subprocess.run')
    @patch('wmk.packager.os.path.exists')
    def test_download_packages_subprocess_error(self, mock_exists, mock_run):
        mock_exists.return_value = True
        mock_run.side_effect = Exception("Pip error")
        result = self.packager.download_packages()
        self.assertFalse(result)

    @patch('wmk.packager.ZipFile')
    @patch('wmk.packager.subprocess.check_output')
    @patch('wmk.packager.os.path.exists')
    def test_create_archive_tracked_files(self, mock_exists, mock_check_output, mock_zipfile):
        # Setup mocks
        mock_exists.return_value = True
        mock_check_output.return_value = "file1.py\nfile2.py"
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        # Execute test
        result = self.packager.create_archive("test.zip")

        # Verify
        self.assertTrue(result)
        self.assertEqual(mock_zip.write.call_count, 2)  # Two files should be written

    def test_generate_manifest(self):
        manifest = self.packager.generate_manifest()
        self.assertIsInstance(manifest, dict)
        self.assertEqual(manifest['runtime'], 'python')
        self.assertEqual(manifest['runtimeRequirements']['platform'], self.packager.platform)
        self.assertEqual(manifest['runtimeRequirements']['pythonVersion'], '')
        self.assertEqual(manifest['entities'], [])
        self.assertEqual(manifest['buildVersion'], '')
        self.assertTrue('timeStamp' in manifest)

    @patch('wmk.packager.os.walk')
    def test_get_nested_files(self, mock_walk):
        # Setup mock to simulate nested directory structure
        mock_walk.return_value = [
            ('/test/dir', ['subdir'], ['file1.txt']),
            ('/test/dir/subdir', [], ['file2.txt'])
        ]
        
        files = self.packager._get_nested_files('/test/dir', '/test/dir')
        
        expected_files = ['file1.txt', 'subdir/file2.txt']
        self.assertEqual(sorted(files), sorted(expected_files))

    @patch('wmk.packager.ZipFile')
    @patch('wmk.packager.os.path.exists')
    @patch('wmk.packager.os.path.isfile')
    @patch('wmk.packager.os.path.isdir')
    def test_create_archive_with_additional_files(self, mock_isdir, mock_isfile, mock_exists, mock_zipfile):
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_isdir.return_value = False
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        packager = Packager(target=self.test_dir, only_tracked=False, additional_files=['extra.txt'])
        result = packager.create_archive("test.zip")

        self.assertTrue(result)
        mock_zip.write.assert_called_with(f"{self.test_dir}/extra.txt", 'extra.txt')

    @patch('wmk.packager.ZipFile')
    @patch('wmk.packager.os.walk')
    @patch('wmk.packager.os.path.exists')
    def test_create_archive_untracked_files(self, mock_exists, mock_walk, mock_zipfile):
        mock_exists.return_value = True
        mock_walk.return_value = [
            (self.test_dir, [], ['file1.txt'])
        ]
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        packager = Packager(target=self.test_dir, only_tracked=False)
        result = packager.create_archive("test.zip")

        self.assertTrue(result)
        mock_zip.write.assert_called_with(f"{self.test_dir}/file1.txt", 'file1.txt')

    @patch('wmk.packager.ZipFile')
    def test_create_archive_error(self, mock_zipfile):
        mock_zipfile.side_effect = Exception("ZIP error")
        
        result = self.packager.create_archive("test.zip")
        
        self.assertFalse(result)

    @patch('wmk.packager.ZipFile')
    @patch('wmk.packager.os.path.exists')
    @patch('wmk.packager.os.walk')
    def test_create_archive_with_dependencies(self, mock_walk, mock_exists, mock_zipfile):
        mock_exists.return_value = True
        mock_walk.return_value = [
            (f"{self.test_dir}/dependencies", [], ['dep1.whl', 'dep2.whl'])
        ]
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        packager = Packager(target=self.test_dir, only_tracked=False)
        result = packager.create_archive("test.zip")

        self.assertTrue(result)
        self.assertEqual(mock_zip.write.call_count, 2)  # Two dependency files should be written
