#!/usr/bin/env python

import logging
from app.db.init_db import init_db

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Starting database initialization from root...")
    init_db()
    logging.info("Database initialization complete.")
