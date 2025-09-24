import aiohttp


class StakeDataProvider:
    @staticmethod
    async def get_stakers_count():
        url = "https://barter.company/api/stakes"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_json = await response.json()
                return int(response_json["total"])


    @staticmethod
    async def get_stake_data():
        url = "https://barter.company/api/tokenInfo"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_json = await response.json()
                return response_json["tokenInfo"]