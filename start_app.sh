#!/bin/bash
docker run -d -ti -p 5000:5000 -v ${PWD} file-system-display
