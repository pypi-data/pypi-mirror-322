#!/bin/bash

# This script will combine the various sources of information to generate the README_pypi.md file.
#
# The intention behind this method is to make it clear where the information is maintained and allow for easier
# maintaining of documentation.

# shellcheck disable=SC2028
echo "# EIT Pathogena Client

The command line interface for the EIT Pathogena platform.

The client enables privacy-preserving sequence data submission and retrieval of analytical output files. Prior to
upload, sample identifiers are anonymised and human host sequences are removed. A computer with Linux or MacOS is
required to use the client. When running human read removal prior to upload a computer with a modern multi-core
processor and at least 16GB of RAM is recommended.
" > README_pypi.md

docs=("install" "auth" "balance" "upload" "decontaminate" "download" "validate" "query-raw" "query-status" "autocomplete")

for i in "${docs[@]}"; do
  cat docs/"$i".md >> README_pypi.md;
done;

echo "
## Support
" >> README_pypi.md
echo "For technical support, please open an issue or contact pathogena.support@eit.org" >> README_pypi.md
