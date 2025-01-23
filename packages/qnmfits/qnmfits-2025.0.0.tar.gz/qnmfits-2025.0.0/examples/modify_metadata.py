import os
import json
from pathlib import Path

cce_dir = Path('../qnmfits/data')

for ID in range(1,14):

    metadata_dir = cce_dir / f'SXS:BBH_ExtCCE:{ID:04d}' / 'Lev4'
    
    # List files in the metadata directory
    metadata_files = os.listdir(metadata_dir)
    
    for filename in metadata_files:
        if filename.endswith('superrest.json'):

            # Open metadata
            with open(metadata_dir / filename, 'r') as f:
                metadata = json.load(f)

            # Modify keys
            new_metadata = {
                'remnant_mass': metadata['Mf'],
                'remnant_dimensionless_spin': metadata['chif']
            }

            # Write new metadata
            with open(metadata_dir / filename, 'w') as f:
                json.dump(new_metadata, f)
