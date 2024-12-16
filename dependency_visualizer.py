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

def main():
    parser = argparse.ArgumentParser(description="Dependency visualizer tool")
    parser.add_argument("--path", required=True, help="Path to the root package")
    parser.add_argument("--package", required=True, help="Name of the root package")
    parser.add_argument("--output", required=True, help="Path to the output file for PlantUML code")
    parser.add_argument("--depth", type=int, default=3, help="Maximum depth of dependency analysis")
    parser.add_argument("--repo", required=True, help="URL of the repository")

    args = parser.parse_args()

    visualizer = DependencyVisualizer(root_package=args.package, max_depth=args.depth, repository_url=args.repo)
    visualizer.analyze_package(args.path)

    plantuml_code = visualizer.generate_plantuml()

    with open(args.output, 'w', encoding='utf-8') as output_file:
        output_file.write(plantuml_code)

    print("PlantUML code generated successfully.")


if __name__ == "__main__":
    main()
