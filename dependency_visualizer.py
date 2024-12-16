import os
import argparse
from collections import defaultdict
import re

class DependencyVisualizer:
    def __init__(self, root_package, max_depth, repository_url):
        self.root_package = root_package
        self.max_depth = max_depth
        self.repository_url = repository_url
        self.dependencies = defaultdict(set)

    def analyze_package(self, package_path, current_depth=0):
        if current_depth > self.max_depth:
            return

        for root, _, files in os.walk(package_path):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    self._extract_dependencies(file_path)

        for dependency in self.dependencies[self.root_package]:
            if dependency not in self.dependencies:
                dependency_path = self._resolve_dependency_path(dependency)
                if dependency_path:
                    self.analyze_package(dependency_path, current_depth + 1)

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            matches = re.findall(r'import\s+([a-zA-Z0-9_.]+);', content)
            for match in matches:
                if match.startswith(self.root_package):
                    self.dependencies[self.root_package].add(match)

    def _resolve_dependency_path(self, dependency):
        return os.path.join(self.repository_url, dependency.replace('.', '/'))

    def generate_plantuml(self):
        lines = ["@startuml", "skinparam defaultFontName Courier"]
        for package, deps in self.dependencies.items():
            for dep in deps:
                lines.append(f"{package} --> {dep}")
        lines.append("@enduml")
        return "\n".join(lines)
