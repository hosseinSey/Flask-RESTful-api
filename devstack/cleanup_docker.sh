#!/bin/bash
docker ps -aq --filter name=udemiapi | xargs -I {} sh -c "[ -n \"{}\" ] && docker stop {} && docker rm -f {}"
