# main.py
import asyncio
from society_module import Society
from logging_config import configure_logger

async def main():
    configure_logger()  # Set up logging configuration
    society = Society()  # Instantiate Society
    await society.simulate()  # Run the simulation asynchronously

if __name__ == "__main__":
    asyncio.run(main())  # Run main if this file is executed directly