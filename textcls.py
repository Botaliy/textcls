import asyncio
from editor import Editor


async def main():
    editor = Editor()
    await editor.run()


if __name__ == "__main__":
    asyncio.run(main())
