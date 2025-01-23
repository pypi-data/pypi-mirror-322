from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tach.errors import TachError
from tach.extension import check_external_dependencies, set_excluded_paths
from tach.utils.external import get_module_mappings, is_stdlib_module

if TYPE_CHECKING:
    from pathlib import Path

    from tach.extension import ProjectConfig


@dataclass
class ExternalCheckDiagnostics:
    undeclared_dependencies: dict[str, list[str]]
    unused_dependencies: dict[str, list[str]]


def extract_module_mappings(rename: list[str]) -> dict[str, list[str]]:
    try:
        return {
            module: [name] for module, name in [module.split(":") for module in rename]
        }
    except ValueError as e:
        raise TachError(
            "Invalid rename format: expected format is a list of 'module:name' pairs, e.g. ['PIL:pillow']"
        ) from e


def check_external(
    project_root: Path,
    project_config: ProjectConfig,
    exclude_paths: list[str],
) -> ExternalCheckDiagnostics:
    serialized_source_roots = [
        str(project_root / source_root) for source_root in project_config.source_roots
    ]
    set_excluded_paths(
        project_root=str(project_root),
        exclude_paths=exclude_paths,
        use_regex_matching=project_config.use_regex_matching,
    )

    metadata_module_mappings = get_module_mappings()
    if project_config.external.rename:
        metadata_module_mappings.update(
            extract_module_mappings(project_config.external.rename)
        )
    diagnostics = check_external_dependencies(
        project_root=str(project_root),
        source_roots=serialized_source_roots,
        module_mappings=metadata_module_mappings,
        ignore_type_checking_imports=project_config.ignore_type_checking_imports,
    )
    undeclared_dependencies_by_file = diagnostics[0]
    unused_dependencies_by_project = diagnostics[1]

    excluded_external_modules = set(project_config.external.exclude)
    filtered_undeclared_dependencies: dict[str, list[str]] = {}
    for filepath, undeclared_dependencies in undeclared_dependencies_by_file.items():
        dependencies = set(
            filter(
                lambda dependency: not is_stdlib_module(dependency)
                and dependency not in excluded_external_modules,
                undeclared_dependencies,
            )
        )
        if dependencies:
            filtered_undeclared_dependencies[filepath] = list(dependencies)
    filtered_unused_dependencies: dict[str, list[str]] = {}
    for filepath, unused_dependencies in unused_dependencies_by_project.items():
        dependencies = set(
            filter(
                lambda dependency: not is_stdlib_module(dependency)
                and dependency not in excluded_external_modules,
                unused_dependencies,
            )
        )
        if dependencies:
            filtered_unused_dependencies[filepath] = list(dependencies)

    return ExternalCheckDiagnostics(
        undeclared_dependencies=filtered_undeclared_dependencies,
        unused_dependencies=filtered_unused_dependencies,
    )


__all__ = ["check_external"]
