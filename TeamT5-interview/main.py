import os
from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade, migrate

from app import create_app
app = create_app('testing')
# app = create_app('development')


@app.cli.command()
def test():
    import unittest
    import sys
 
    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.errors or result.failures:
        sys.exit(1)

if __name__ == "__main__":
    app.run(debug=True)
