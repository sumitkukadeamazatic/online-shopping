from storages.backends.s3boto import S3BotoStorage

# StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')


def MediaRootS3BotoStorage(): return S3BotoStorage(location='media')
