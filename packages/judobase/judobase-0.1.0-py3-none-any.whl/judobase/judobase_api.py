import asyncio
from datetime import datetime

from .base import _Base
from .schemas import Competition, Contest


class JudoBase(_Base):

    async def get_all_comps(self) -> list[Competition]:
        """Returns data for all competitions."""

        return await self._get_competition_list()

    async def get_all_contests(self) -> list[Contest]:
        """Returns data for all contests using concurrent calls to _find_contests."""

        comps = await self.get_all_comps()
        tasks = [self._find_contests(c.id_competition) for c in comps]

        results = await asyncio.gather(*tasks)

        contests = [contest for sublist in results for contest in sublist]
        return contests

    async def get_comps_in_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> list[Competition]:
        """Returns data for competitions in specified date range."""

        all_comps = await self.get_all_comps()
        return [c for c in all_comps if start_date <= c.date_from <= end_date]
