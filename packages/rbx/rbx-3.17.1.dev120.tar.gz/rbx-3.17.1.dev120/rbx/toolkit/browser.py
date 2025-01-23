import datetime
import logging
from typing import NamedTuple, Optional

from playwright.async_api import async_playwright, TimeoutError

logger = logging.getLogger(__name__)


class Recording(NamedTuple):
    location: str
    delay: Optional[int] = 0
    source: Optional[str] = None


async def record(
    dirname: str, duration: int, height: int, url: str, width: int
) -> Recording:
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            args=["--autoplay-policy=no-user-gesture-required"]
        )
        context = await browser.new_context(
            record_video_dir=dirname,
            record_video_size={"width": width, "height": height},
            viewport={"width": width, "height": height},
        )
        page = await context.new_page()
        await page.set_viewport_size({"width": width, "height": height})
        await page.goto(url, wait_until="domcontentloaded")
        start = datetime.datetime.now(datetime.UTC)

        try:
            # Wait for the "action=p0" console log, i.e. the play event.
            # The play event is always expected to occur within 2 seconds, so we never wait any
            # longer than that. When the play event is not seen, we assume no video on the target.
            waiting = True
            while waiting:
                async with page.expect_console_message(timeout=2000) as msg_info:
                    message = await msg_info.value
                    if message.type == "log":
                        for arg in message.args:
                            if "action=p0" in await arg.json_value():
                                ready = datetime.datetime.now(datetime.UTC)
                                waiting = False

                if (datetime.datetime.now(datetime.UTC) - start).total_seconds() >= 2:
                    raise TimeoutError("Could not find video")

        except TimeoutError as e:
            checkpoint = datetime.datetime.now(datetime.UTC)
            logger.debug(
                f"Recording without video @ {to_ms(checkpoint - start)}ms\n{e}"
            )
            ready = start
            src = None

            elapsed = int(1000 * (checkpoint - start).total_seconds())
            remaining = duration - elapsed
            if remaining > 0:
                logger.debug(f"{remaining}ms left to record")
                expression = (
                    "window.recording = 1; setTimeout(() => { window.recording = 0 }, "
                    + str(remaining)
                    + ");"
                )
                await page.evaluate(expression)
                await page.wait_for_function("() => window.recording == 0")
            else:
                logger.debug("Nothing left to record")

            finished = datetime.datetime.now(datetime.UTC)

        else:
            logger.debug(f"Ready with video @ {to_ms(ready - start)}ms")
            video = page.locator("video")
            await video.wait_for(timeout=2000)
            for source in await video.locator("source").all():
                if await source.get_attribute("type") == "video/mp4":
                    value = await source.get_attribute("src")
                    src, _, _ = value.partition("?")

            # Record until the end of the video, at which point the `video` element will be set
            # as hidden.
            await page.locator("video").first.wait_for(state="hidden", timeout=60000)
            checkpoint = datetime.datetime.now(datetime.UTC)
            finished = datetime.datetime.now(datetime.UTC)

            # Continue recording until the required duration.
            checkpoint = datetime.datetime.now(datetime.UTC)
            elapsed = int(1000 * (checkpoint - ready).total_seconds())
            remaining = duration - elapsed
            if remaining > 0:
                logger.debug(f"{remaining}ms left to record")
                expression = (
                    "window.recording = 1; setTimeout(() => { window.recording = 0 }, "
                    + str(remaining)
                    + ");"
                )
                await page.evaluate(expression)
                await page.wait_for_function("() => window.recording == 0")
            else:
                logger.debug("Nothing left to record")

            finished = datetime.datetime.now(datetime.UTC)

        logger.debug(f"Finished @ {to_ms(finished - ready)}ms")
        await context.close()
        location = await page.video.path()
        await browser.close()

    # The delay is the lag between the start of the recording session and the time the video
    # started playing.
    delay = to_ms(ready - start)
    logger.debug(f"Recorded with delay of {delay}ms")

    return Recording(delay=delay, location=location, source=src)


async def screenshot(filename: str, height: int, url: str, width: int) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({"width": width, "height": height})
        await page.goto(url, wait_until="networkidle")
        await page.screenshot(path=filename)
        await browser.close()


def to_ms(timedelta: datetime.timedelta) -> int:
    return round(1000 * timedelta.total_seconds())
