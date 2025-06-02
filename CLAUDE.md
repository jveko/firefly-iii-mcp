# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Firefly III MCP (Model Context Protocol) server implementation. The project appears to be in early development stages.

## Development Setup

Since this is a Python project with minimal dependencies currently defined:

1. Ensure Python >= 3.11 is installed (as specified in pyproject.toml)
2. Install project in development mode: `pip install -e .`

## Project Structure

- `main.py` - Entry point for the application
- `pyproject.toml` - Project configuration and dependencies
- `docs/fastmcp.txt` - FastMCP documentation reference

## MCP Implementation Context

This project will likely implement an MCP server to interface with Firefly III, a personal finance manager. When implementing MCP functionality:

1. Follow the FastMCP patterns documented in `docs/fastmcp.txt`
2. MCP servers typically implement tools, resources, and prompts
3. Consider implementing handlers for logging, progress monitoring, and other advanced features as outlined in the FastMCP documentation