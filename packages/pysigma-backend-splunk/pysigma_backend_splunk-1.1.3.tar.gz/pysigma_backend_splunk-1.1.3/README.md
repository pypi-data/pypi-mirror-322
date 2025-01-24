![Tests](https://github.com/SigmaHQ/pySigma-backend-splunk/actions/workflows/test.yml/badge.svg)
![Coverage Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/thomaspatzke/47c292239759399a6e3c73b0e9656b33/raw/SigmaHQ-pySigma-backend-splunk.json)
![Status](https://img.shields.io/badge/Status-pre--release-orange)

# pySigma Splunk Backend

This is the Splunk backend for pySigma. It provides the package `sigma.backends.splunk` with the `SplunkBackend` class.
Further, it contains the following processing pipelines in `sigma.pipelines.splunk`:

* splunk_windows_pipeline: Splunk Windows log support
* splunk_windows_sysmon_acceleration_keywords: Adds fiels name keyword search terms to generated query to accelerate search.

It supports the following output formats:

* default: plain Splunk queries
* savedsearches: Splunk savedsearches.conf format.

This backend is currently maintained by:

* [Thomas Patzke](https://github.com/thomaspatzke/)