#!/bin/bash

set -e

sudo cp .github/hooks/pre-commit .git/hooks/
sudo chmod +x .git/hooks/pre-commit