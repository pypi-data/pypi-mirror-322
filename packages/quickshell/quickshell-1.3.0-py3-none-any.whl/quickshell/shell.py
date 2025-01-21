import asyncio
from typing import Tuple


async def run_shell(cmd, print_output: bool = False) -> Tuple[str, str]:
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = [], []

    async def stream_output(stream, array, print_output):
        while True:
            text = await stream.read(1)
            if text:
                text = text.decode(errors='ignore')
                array.append(text)
                if print_output:
                    print(text, end="")
            else:
                break

    try:
        await asyncio.gather(
            stream_output(process.stdout, stdout, print_output),
            stream_output(process.stderr, stderr, print_output)
        )
        await process.wait()
    except asyncio.CancelledError:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=5)
        except asyncio.TimeoutError:
            process.kill()
        finally:
            await process.wait()

    return "".join(stdout), "".join(stderr)