proj := `basename "$(pwd)"`


# init local dev environment
sync:
    uv sync

# add news item of type
news type id *msg:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ "{{id}}" = "-" ]; then
      id=`git rev-parse --abbrev-ref HEAD | cut -d- -f1`
    else id="{{id}}"
    fi
    if [ "{{msg}}" = "" ]; then
      msg=`git rev-parse --abbrev-ref HEAD | sed 's/^[0-9][0-9]*-//' | uv run caseutil -csentence`
    fi
    uv run towncrier create -c "{{msg}}" "$id.{{type}}.md"

# run linters
lint:
    uv run mypy src
    uv run ruff check
    uv run ruff format --check
    shellcheck tests/*.sh

# build python package
build:
    uv lock
    make pkg

test *case:
    #!/usr/bin/env bash
    set -euo pipefail
    # build package wheel
    just build
    # build sample
    make samplepkg
    # re-create pip cache volume
    docker volume rm -f "{{proj}}_pipcache" >/dev/null
    docker compose run --rm --entrypoint /bin/true runtest
    # close all containers if interrupted
    trap 'docker compose kill' SIGINT
    # run tests
    if [ -n "{{case}}" ]; then
      docker compose run --rm -i runtest "{{case}}"
    else
      suites=`yq '.|keys[]' tests/cases.toml | xargs | tr ' ' ,`
      tags=`docker run --rm makukha/multipython:unsafe py ls --tag | xargs | tr ' ' ,`
      venvs=`yq 'to_entries[].value|to_entries[].value|keys[]' tests/cases.toml | sort -u | xargs | tr ' ' ,`
      cases="$(eval echo -n $(echo $suites-{$tags}-{$venvs}))"
      export COMPOSE_IGNORE_ORPHANS=True
      time parallel -j50% --color-failed --halt-on-error 1 'docker compose run --rm runtest {}' ::: $cases
    fi

debug *case:
    docker compose run --rm -i rundebug {{case}}

# update docs
docs:
  uv run docsub x generate
  uv run docsub apply -i README.md

# free disk space
clean:
  docker builder prune
  docker image prune
  docker network prune

# shell to testing container
shell:
    docker compose run --rm -i --entrypoint bash rundebug

#
#  Release
# ---------
#
# just lint
# just test
# just docs
#
# just version [patch|minor|major]
# just changelog
# (proofread changelog)
#
# just build
# just push-pypi
# (create github release)
#

# bump project version (major|minor|patch)
[group('release')]
version PART:
    uv run bump-my-version bump -- {{PART}}
    uv lock

# collect changelog entries
[group('release')]
changelog:
    #!/usr/bin/env bash
    set -euxo pipefail
    version=$(uv run bump-my-version show current_version 2>/dev/null)
    uv run towncrier build --yes --version "$version"
    sed -e's/^### \(.*\)$/***\1***/; s/\([a-z]\)\*\*\*$/\1:***/' -i '' CHANGELOG.md

# publish package on PyPI
[group('release')]
push-pypi:
    rm -rf dist
    make pkg
    uv publish
