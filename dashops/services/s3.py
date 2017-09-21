import boto3
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class S3Service:
    @classmethod
    def list_bucket(cls, region_name='us-west-1'):
        """
        Get the list of bucket names.
        :param region_name: region name to use.
        :return: a list of strings containing bucket names.
        """
        s3 = boto3.resource('s3', region_name=region_name)
        return [bucket.name for bucket in s3.buckets.all()]

    @classmethod
    def create_bucket(cls, bucket_name, region_name='us-west-1', enable_version=True):
        """
        Create a bucket at specified region.
        :param bucket_name: the name of the bucket.
        :param region_name: the region to create.
        :param enable_version: if to enable versioning.
        :return: the bucket object.
        """
        s3 = boto3.resource('s3', region_name=region_name)
        bucket = s3.Bucket(bucket_name)
        bucket.create(ACL='private', CreateBucketConfiguration={'LocationConstraint': region_name})
        if enable_version:
            bucket_versioning = bucket.Versioning()
            bucket_versioning.enable()
        return bucket

    @classmethod
    def download(cls, bucket_name, key, region_name='us-west-1', filename=None):
        """
        Download the given key from given bucket and return the content.
        If "filename" is specified, then download to the file and then return the content.
        :param bucket_name: name of the bucket to download from.
        :param key: object key on s3.
        :param region_name: region name to use.
        :param filename: if specified, download to the file.
        :return: content in the object.
        """
        s3 = boto3.resource('s3', region_name=region_name)
        bucket = s3.Bucket(bucket_name)
        bucket.load()
        if filename:
            bucket.download_file(key, filename)
            with open(filename) as f:
                return f.read()
        else:
            s = StringIO()
            bucket.download_fileobj(key, s)
            return s.read()
