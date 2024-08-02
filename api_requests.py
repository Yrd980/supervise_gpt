from backoff import on_exception, expo
from httpx import AsyncClient


class APIRequest:

    @staticmethod
    @on_exception(expo, Exception, max_tries=5)
    async def post(url: str, data=None, files=None):
        async with AsyncClient(timeout=None) as client:
            response = await client.post(url, json=data, files=files)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 500:
                print(f"Server error for URL: {url}, retrying...")
                raise Exception("Server error")
            else:
                return {"error": "Request failed", "status_code": response.status_code}
