import unittest
from unittest import mock

from click.testing import CliRunner

from dashops.services import S3Service


class Bucket:
    def __init__(self, name):
        self.name = name
        self.called = False

    def create(self, **kwargs):
        self.called = True

    def load(self):
        pass

    def download_file(self, key, filename):
        with open(filename, 'w') as f:
            f.write(key)

    def download_fileobj(self, key, fileobj):
        fileobj.write(key.encode('utf-8'))

    class Versioning:
        called = False

        def enable(self):
            Bucket.Versioning.called = True


class MockS3:
    def __init__(self):
        self.buckets = BucketManager()
        self.Bucket = Bucket


class BucketManager:
    def __init__(self):
        self._objects = [Bucket('bucket1'), Bucket('bucket2')]

    def all(self):
        return self._objects


class TestS3Service(unittest.TestCase):
    @mock.patch('dashops.services.s3.boto3', autospec=True)
    def test_list(self, mock_boto3):
        mock_boto3.resource.return_value = MockS3()

        bucket_names = S3Service.list_bucket()
        expected_names = ['bucket1', 'bucket2']
        mock_boto3.resource.assert_called_once_with('s3', region_name='us-west-1')
        self.assertEqual(bucket_names, expected_names)

    @mock.patch('dashops.services.s3.boto3', autospec=True)
    def test_create_bucket(self, mock_boto3):
        mock_boto3.resource.return_value = MockS3()
        # test create without versioning
        bucket = S3Service.create_bucket('bucket3', enable_version=False)
        mock_boto3.resource.assert_called_once_with('s3', region_name='us-west-1')
        self.assertEqual(bucket.name, 'bucket3')
        self.assertTrue(bucket.called)
        self.assertFalse(Bucket.Versioning.called)

        # test create with versioning
        bucket = S3Service.create_bucket('bucket4', region_name='test')
        mock_boto3.resource.assert_called_with('s3', region_name='test')
        self.assertEqual(bucket.name, 'bucket4')
        self.assertTrue(bucket.called)
        self.assertTrue(Bucket.Versioning.called)

    @mock.patch('dashops.services.s3.boto3', autospec=True)
    def test_download(self, mock_boto3):
        mock_boto3.resource.return_value = MockS3()
        key = '/key/to/file'
        # test download to file
        runner = CliRunner()
        with runner.isolated_filesystem():
            filename = 'test.txt'
            ret = S3Service.download('test_bucket', key, region_name='test_region', filename=filename)
            self.assertEqual(ret, key)
            with open(filename) as f:
                self.assertEqual(f.read(), key)
        mock_boto3.resource.assert_called_once_with('s3', region_name='test_region')

        # test download to fileobj
        ret = S3Service.download('test_bucket', key, region_name='test_region2')
        self.assertEqual(ret, key)
        mock_boto3.resource.assert_called_with('s3', region_name='test_region2')
