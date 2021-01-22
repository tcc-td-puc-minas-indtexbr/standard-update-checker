# Standard Update Checker Lambda Function
Micro serviço em Lambda Function responsável por verificar atualizações de normas do sistema SIGO que faz parte do meu TCC do curso Especialização em Arquitetura de Software Distribuído da PUC Minas


[comment]: <> (https://github.com/mbertolacci/lorem-rss)

[comment]: <> (https://blog.feedspot.com/iso_rss_feeds/)

[comment]: <> (https://www.iso.org/contents/shared/rss/latest-standards.rss)

[comment]: <> (https://www.iso.org/publication/PUB100208.html)


[comment]: <> (Important:)

[comment]: <> (https://github.com/sanic-org/sanic/issues/1323)

[comment]: <> (http://localhost:8002/update_checker)

[comment]: <> (http://localhost:8003/)


[comment]: <> (## Running Locally)

[comment]: <> (```)

[comment]: <> ( ./bin/chalice/run-local.sh )

[comment]: <> (```)

[comment]: <> (## Running via Docker)

[comment]: <> (```)

[comment]: <> ( ./bin/docker/build.sh)

[comment]: <> ( ./bin/docker/run.sh )

[comment]: <> (```)


[comment]: <> (## Samples)

[comment]: <> (See the project samples in this folder [here]&#40;/samples&#41;.)

[comment]: <> (## Running tests)

[comment]: <> (To run the unit tests of the project you can execute the follow command:)

[comment]: <> (All tests:)

[comment]: <> ( ```)

[comment]: <> ( ./bin/venv-exec.sh ./bin/tests/tests.sh )

[comment]: <> ( ``` )

[comment]: <> (Unit tests:)

[comment]: <> ( ```)

[comment]: <> (./bin/venv-exec.sh ./bin/tests/unit-tests.sh)

[comment]: <> ( ``` )

[comment]: <> (Integration tests:)

[comment]: <> ( ```)

[comment]: <> (./bin/venv-exec.sh ./bin/tests/integration-tests.sh)

[comment]: <> ( ``` )

[comment]: <> (## Generating coverage reports)

[comment]: <> (To execute coverage tests you can execute the follow commands:)

[comment]: <> (Unit test coverage:)

[comment]: <> (``` )

[comment]: <> (./bin/venv-exec.sh ./bin/tests/unit-coverage.sh)

[comment]: <> (``` )

[comment]: <> (Integration test coverage:)

[comment]: <> (``` )

[comment]: <> (./bin/venv-exec.sh ./bin/tests/integration-coverage.sh)

[comment]: <> (``` )

[comment]: <> (> Observation:)

[comment]: <> (The result can be found in the folder `target/integration` and `target/unit`.)