# Codegen CLI

A command-line interface for the Codegen API that helps you transform your code with AI.

[![Documentation](https://img.shields.io/badge/docs-view%20docs-blue)](https://docs.codegen.com/)

## Installation

To install the latest release:

```
uv tool install codegen
```

## Development

- Clone a repo onto your filesystem, e.g. `codegen-staging`
- Set up a uv environment:

```
uv venv --python 3.13.0
source .venv/bin/activate
```

- pip install the `codegen-cli` package locally

```
uv pip install -e path/to/codegen-cli
```

- changes to the `codegen-cli` directory are now immediately reflected.

## Installation in Devin

```bash
uv tool install --upgrade codegen
```

## Quick Start

1. Log in to authenticate with Codegen:

```
codegen login
```

This will open your browser to get an authentication token. You can also pass a token directly with `--token`.

2. Initialize `codegen` from within your Git repository:

```
codegen init
```

This creates the necessary folder structure and downloads documentation and examples. An error will be thrown if you are not in a git repository.

3. Create a codemod:

```
codegen create my-codemod-name --description "delete all my unused functions"
```

This will create a new codemod in the folder `codegen-sh/codemod/my-codemod-name/run.py`

When passed the `--description` argument, a Codegen expert AI will generate this first draft. Therefore, it's helpful to provide as much info as possible.

4. Run your codemod:

Execute this codemod and view output with `codegen run`:

```
codegen run my-codemod-name --apply-local
```

`--apply-local` will apply the changes to your current local filesystem.

Note: use `ENV=prod` if you want to point the CLI to prod instead of staging

## Working with AI

When editing your codemod using Cursor, you can now `@codegen-sh` in any chat or composer window to pull in relevant documentation and context about your codemods and the Codegen API.

This provides:

- Documentation about available APIs and utilities
- Context about your active codemod
- Examples of similar codemods
- Relevant code snippets

The AI will use this context to provide more accurate and helpful responses about working with Codegen.

## Available Commands

- `login` - Authenticate with Codegen
- `logout` - Clear stored authentication
- `init` - Initialize Codegen in your repository
- `create` - Create a new codemod
- `run` - Execute the active codemod
  - `--web` - Open results in web browser
  - `--apply-local` - Apply changes locally
- `expert` - Ask the Codegen AI expert questions
- `profile` - View current user and codemod info
- `set-active` - Select which codemod to run
- `docs-search` - Search documentation and examples

## Project Structure

After initialization, Codegen creates the following structure:

```
codegen-sh/
├── codemods/     # Your codemods live here
├── docs/         # API documentation
└── examples/     # Example codemods
```

