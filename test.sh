#!/bin/bash
# Run the tests
PYTHONPATH=$PYTHONPATH:./lib/pymaker py.test --cov=d3m_keeper --cov-report=term --cov-append tests/ $@