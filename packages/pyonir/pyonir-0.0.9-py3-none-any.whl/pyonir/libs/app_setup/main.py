import os
import pyonir
from backend.controllers import endpoints
# Instantiate pyonir application
demo_app = pyonir.init(os.path.dirname(__file__))

# Install plugins
# demo_app.register_plugins([YOUR_PLUGIN_MODULE_HERE])

# Generate static website
# demo_app.generate_static_website()

# Run server
demo_app.run(endpoints=endpoints)
