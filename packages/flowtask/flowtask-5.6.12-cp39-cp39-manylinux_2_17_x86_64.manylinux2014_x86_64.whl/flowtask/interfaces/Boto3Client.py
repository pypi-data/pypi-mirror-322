from typing import Dict, List
import re
import boto3
from botocore.exceptions import ClientError
import aiofiles
from navconfig.logging import logging
from io import BytesIO
from ..conf import aws_region, aws_bucket, AWS_CREDENTIALS
from .client import ClientInterface
from ..exceptions import FileNotFound, FileError, ComponentError


logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("s3transfer").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)


class Boto3Client(ClientInterface):
    """
    Boto3 AWS Client.

        Overview

        Abstract class for interaction with Boto3 (AWS).

        .. table:: Properties
        :widths: auto

    +------------------------+----------+-----------+-------------------------------------------------------+
    | Name                   | Required | Summary                                                           |
    +------------------------+----------+-----------+-------------------------------------------------------+
    |_credentials            |   Yes    | The function is loaded and then we define the necessary code to   |
    |                        |          | call the script                                                   |
    +------------------------+----------+-----------+-------------------------------------------------------+
    |  _init_                |   Yes    | Component for Data Integrator                                     |
    +------------------------+----------+-----------+-------------------------------------------------------+
    |  _host                 |   Yes    | The IPv4 or domain name of the server                             |
    +------------------------+----------+-----------+-------------------------------------------------------+
    |  get_client            |   Yes    | Gets the client access credentials, by which the user logs in to  |
    |                        |          | perform an action                                                 |
    +------------------------+----------+-----------+-------------------------------------------------------+
    |  print                 |   Yes    | Print message to display                                          |
    +------------------------+----------+-----------+-------------------------------------------------------+
    | get_env_value          |   Yes    | Get env value  policies for setting virtual environment           |
    +------------------------+----------+-----------+-------------------------------------------------------+
    | processing_credentials |   Yes    | client credentials configured for used of the app                 |
    +------------------------+----------+-----------+-------------------------------------------------------+

            Return the list of arbitrary days


    """  # noqa

    _credentials: Dict = {
        "aws_key": str,
        "aws_secret": str,
        "client_id": str,
        "client_secret": str,
        "service": str,
        "region_name": str,
        "bucket": str,
    }

    def __init__(self, *args, **kwargs) -> None:
        self.region_name: str = kwargs.pop('region_name', None)
        self.service: str = kwargs.pop('service', 's3')
        self.bucket: str = kwargs.pop('bucket', None)
        self.ContentType: str = kwargs.pop('ContentType', 'application/octet-stream')
        super().__init__(*args, **kwargs)

    def define_host(self):
        return True

    async def open(self, credentials: dict, **kwargs):
        use_credentials = credentials.pop('use_credentials', True)
        self.processing_credentials(credentials)
        service = self.credentials.get('service', self.service)
        if use_credentials is False:
            print("Boto3: Enter anonymous")
            self._connection = boto3.client(
                service,
                region_name=self.credentials.get("region_name", self.region_name),
                config=boto3.session.Config(signature_version="unsigned"),
            )
        else:
            print("Boto3: Enter signed")
            cred = {
                "aws_access_key_id": self.credentials["aws_key"],
                "aws_secret_access_key": self.credentials["aws_secret"],
                "region_name": self.credentials["region_name"],
            }
            self._connection = boto3.client(
                service,
                **cred
            )
        return self

    def processing_credentials(self, credentials: dict = None):
        # getting credentials from self.credentials:
        if credentials:
            super().processing_credentials()
        else:
            # getting credentials from config
            self.credentials = AWS_CREDENTIALS.get(self.config, 'default')
        ## getting Tenant and Site from credentials:
        try:
            self.region_name = self.credentials["region_name"]
        except KeyError:
            self.region_name = aws_region
        try:
            self.bucket = self.credentials["bucket_name"]
        except KeyError:
            self.bucket = aws_bucket
        try:
            self.service = self.credentials["service"]
        except KeyError:
            self.service = "s3"

    async def get_s3_object(self, bucket: str, filename: str):
        """
        Retrieve an object from an S3 bucket.

        Parameters
        ----------
        bucket: str
            The name of the S3 bucket.
        filename: str
            The name of the file (key) in the S3 bucket.

        Returns
        -------
        dict
            A dictionary containing the object data and metadata.

        Raises
        ------
        FileNotFound
            If the object is not found in the bucket.
        ComponentError
            If there is an issue with retrieving the object.
        """
        # Ensure connection is established
        if not hasattr(self, "_connection"):
            raise ComponentError(
                "S3 client is not connected. Call `open` first."
            )

        # Get the object from S3
        obj = self._connection.get_object(Bucket=bucket, Key=filename)
        # Validate the response
        status_code = int(obj["ResponseMetadata"]["HTTPStatusCode"])
        if status_code != 200:
            raise FileNotFound(
                f"File '{filename}' not found in bucket '{bucket}'."
            )
        return obj

    async def download_file(self, filename, obj):
        result = None
        ob_info = obj["ResponseMetadata"]["HTTPHeaders"]
        rsp = obj["ResponseMetadata"]
        status_code = int(rsp["HTTPStatusCode"])
        if status_code == 200:
            print('Content  ', ob_info["content-type"])
            # file was found
            filepath = self.directory.joinpath(filename)
            if ob_info["content-type"] == self.ContentType:
                contenttype = ob_info["content-type"]
                data = None
                with obj["Body"] as stream:
                    data = stream.read()
                output = BytesIO()
                output.write(data)
                output.seek(0)
                result = {"type": contenttype, "data": output, "file": filepath}
                # then save it into directory
                await self.save_attachment(filepath, data)
            else:
                return FileError(
                    f'S3: Wrong File type: {ob_info["content-type"]!s}'
                )
        else:
            return FileNotFound(
                f"S3: File {filename} was not found: {rsp!s}"
            )
        return result

    async def save_attachment(self, filepath, content):
        try:
            self._logger.info(f"S3: Saving attachment file: {filepath}")
            if filepath.exists() is True:
                if (
                    "replace" in self.destination and self.destination["replace"] is True
                ):
                    # overwrite only if replace is True
                    async with aiofiles.open(filepath, mode="wb") as fp:
                        await fp.write(content)
                else:
                    self._logger.warning(
                        f"S3: File {filepath!s} was not saved, already exists."
                    )
            else:
                # saving file:
                async with aiofiles.open(filepath, mode="wb") as fp:
                    await fp.write(content)
        except Exception as err:
            raise FileError(f"File {filepath} was not saved: {err}") from err

    async def close(self, **kwargs):
        self._connection = None

    async def s3_list(self, suffix: str = "") -> List:
        kwargs = {
            "Bucket": self.bucket,
            "Delimiter": "/",
            "Prefix": self.source_dir,
        }
        prefix = self.source_dir
        files = []
        _patterns = []
        if not self._srcfiles:
            _patterns.append(re.compile(f"^{self.source_dir}.{suffix}+$"))
            # List objects in the S3 bucket with the specified prefix
            response = self._connection.list_objects_v2(**kwargs)
            if response["KeyCount"] == 0:
                raise FileNotFound(
                    f"S3 Bucket Error: Content not found on {self.bucket}"
                )
            for obj in response["Contents"]:
                key = obj["Key"]
                if obj["Size"] == 0:
                    # is a directory
                    continue
                if suffix is not None:
                    if key.startswith(prefix) and re.match(
                        prefix + suffix, key
                    ):
                        files.append(obj)
                else:
                    try:
                        for pat in _patterns:
                            mt = pat.match(key)
                            if mt:
                                files.append(obj)
                    except Exception as e:
                        self._logger.exception(e, stack_info=True)
        if self._srcfiles:
            for file in self._srcfiles:
                _patterns.append(re.compile(f"^{self.source_dir}.{file}+$"))
                while True:
                    try:
                        response = self._connection.list_objects_v2(**kwargs)
                        if response["KeyCount"] == 0:
                            raise FileNotFound(
                                f"S3 Bucket Error: Content not found on {self.bucket}"
                            )
                        for obj in response["Contents"]:
                            key = obj["Key"]
                            if obj["Size"] == 0:
                                # is a directory
                                continue
                            try:
                                if hasattr(self, "source") and "filename" in self.source:
                                    if self.source["filename"] == key:
                                        files.append(obj)
                            except (KeyError, AttributeError):
                                pass
                            if suffix is not None:
                                if key.startswith(prefix) and re.match(
                                    prefix + suffix, key
                                ):
                                    files.append(obj)
                            else:
                                try:
                                    for pat in _patterns:
                                        mt = pat.match(key)
                                        if mt:
                                            files.append(obj)
                                except Exception as e:
                                    self._logger.exception(e, stack_info=True)
                        try:
                            kwargs["ContinuationToken"] = response["NextContinuationToken"]
                        except KeyError:
                            break
                    except ClientError as err:
                        raise ComponentError(
                            f"S3 Bucket Error: {err}"
                        ) from err
        return files
