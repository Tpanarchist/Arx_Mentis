# ADR 0007: Backend target

Status: Open question

## Context

Native code, bytecode, WebAssembly, another VM, transpilation, and continued direct
evaluation carry different semantic and operational constraints. There are not yet
programs, an IR, or deployment requirements that distinguish them responsibly.

## Question

Which backend target, if any, should complement the Python executable reference?

## Resolution evidence

Use checked programs, lowering experiments, portability requirements, diagnostics,
performance measurements, and distribution constraints. Avoid choosing a target
only because a library makes an early demo convenient.

## Safe deferral

The backend package defines only a future boundary. Reference evaluation remains
useful without selecting a production target, and no target-specific values or APIs
cross the semantic interface.

