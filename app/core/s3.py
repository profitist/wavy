from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from fastapi import HTTPException
from starlette import status
from app.config import S3_ID, S3_SECRET


class S3Client:
    """
    Асинхронный клиент для работы с Yandex Object Storage (или любым S3).
    Работает полностью в памяти — без временных файлов.
    """

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_bytes(self, data: bytes, filename: str):
        """
        Загружает файл в S3 напрямую из памяти.
        filename — имя файла (например: cover.jpg)
        data — байты файла
        """
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=filename,
                    Body=data,
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File can't be uploaded: {str(e)}",
            )

    async def download_bytes(self, filename: str) -> bytes:
        """
        Скачивает объект в виде байтов.
        """
        try:
            filename += ".png"
            async with self.get_client() as client:
                response = await client.get_object(
                    Bucket=self.bucket_name,
                    Key=filename,
                )
                async with response["Body"] as stream:
                    return await stream.read()

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found",
            )
