import httpx
from app.core.config import settings

headers = {
    "X-NCP-APIGW-API-KEY-ID": settings.NAVER_CLIENT_ID,
    "X-NCP-APIGW-API-KEY": settings.NAVER_CLIENT_SECRET,
}


async def reverse_geocode(lat: float, lon: float) -> str:
    url = f"https://maps.apigw.ntruss.com/map-reversegeocode/v2/gc?coords={lon}%2C{lat}&output=json&orders=addr"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        result = response.json()

        if result["status"]["code"] != 0:
            raise ValueError(f"Reverse geocoding failed: {result['status']['message']}")

        addr_info = result["results"][0]["region"]
        if addr_info["area4"]["name"]:
            return f"{addr_info['area3']['name']} {addr_info['area4']['name']}"
        else:
            return f"{addr_info['area2']['name'].split(' ')[-1]} {addr_info['area3']['name']}"
