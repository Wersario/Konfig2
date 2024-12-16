from typing import Dict, List, Set

class DependencyGraph:
    def __init__(self, repo_url: str, max_depth: int):
        self.repo_url = repo_url
        self.max_depth = max_depth
        self.dependencies: Dict[str, Set[str]] = {}

    def analyze_dependencies(self, package_name: str, current_depth: int = 0):
        if current_depth > self.max_depth:
            return

        new_dependencies = self._get_dependencies(package_name)
        if package_name not in self.dependencies:
            self.dependencies[package_name] = set()

        for dep in new_dependencies:
            if dep not in self.dependencies[package_name]:
                self.dependencies[package_name].add(dep)
                self.analyze_dependencies(dep, current_depth + 1)

    def _get_dependencies(self, package_name: str) -> List[str]:
        sample_dependencies = {
            "com.example.app": ["com.example.lib", "com.example.utils"],
            "com.example.lib": ["com.example.core"],
            "com.example.utils": [],
            "com.example.core": ["com.example.common"],
            "com.example.common": [],
        }
        return sample_dependencies.get(package_name, [])

    def to_plantuml(self) -> str:
        lines = ["@startuml"]
        for package, deps in self.dependencies.items():
            for dep in deps:
                lines.append(f"{package} --> {dep}")
        lines.append("@enduml")
        return "\n".join(lines)

