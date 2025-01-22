<p align="center">
  <img src="https://raw.githubusercontent.com/balto-data/balto/main/etc/balto-banner.png" alt="balto logo" width="750"/>
</p>

# Welcome to Balto

Build durable data pipelines directly in Snowflake with no external orchestrators. Effortlessly scale your dbt projects from proof of concept to production grade data pipelines running millions of model executions per day. Orchestrate ML pipelines, data exports, and deletions directly in Snowflake with zero external dependencies. 

## Getting Started

Ready to get started? Check out the [installation instructions](https://baltodatatool.com). If you're already familiar with [dbt](https://github.com/dbt-labs/dbt-core), check out [our guide](https://baltodatatool.com) on what's new in Balto.

## Installation
Clone the repo and install from source, or install with pip:
```
pip install 'git+https://github.com/balto-data/balto.git@v0.0.10#egg=balto&subdirectory=core'
```

## Overview

![architecture](https://github.com/balto-data/balto/blob/main/etc/balto-diagram.svg)

Balto is comprised of two pieces. The Balto CLI, a drop-in replacement for the [dbt-core](https://github.com/dbt-labs/dbt-core) CLI, and the Balto orchestrator, which is implemented as a Snowflake Native App.  Balto orginated as a fork of dbt-core that has been rebuilt from the ground up to run as a Snowflake Native app. The following are the major design differences:

### Compilation

Balto simplifies the parsing process when building your project. Any database interactions are deferred during compilation, this allows us push all database interactions to the Balto Snowflake Native App installed in your account. This means if you use our [Github Integation](https://baltodatatool.com/cicd/), you can enable automated deployments without having to manage any external accounts or connections.

### Orchestration

Balto implements a batteries included orchestration engine inside the Snowflake App. When you deploy your
compiled projects via our Gitub integration (or via a call to our stored procedure), the Balto orchestrator handles deploying your compiled project from directly inside your Snowflake account.

Under the hood, Balto's orchestration engine uses Snowflake triggered tasks and streams to implement a completely event driven scheduler that allows it to scale to zero when no models are being executed.

### dbt macro executor

Balto includes a lightweight re-implementation of dbt's Jinja `macro` extension that allows it to execute your model inside a stored procedure that runs on the same warehouse the underlying queries get run on.

## Reporting bugs and contributing code

- Want to report a bug or request a feature? Let us know and open [an issue](https://github.com/balto-data/balto/issues/new/choose)
