import unittest
from dependency_graph import DependencyGraph


class TestDependencyGraph(unittest.TestCase):
    def setUp(self):
        self.graph = DependencyGraph(repo_url="http://example.com", max_depth=3)

    def test_analyze_dependencies(self):
        self.graph.analyze_dependencies("com.example.app")
        expected_dependencies = {
            "com.example.app": {"com.example.lib", "com.example.utils"},
            "com.example.lib": {"com.example.core"},
            "com.example.core": {"com.example.common"},
            "com.example.common": set(),
            "com.example.utils": set(),
        }
        self.assertDictEqual(self.graph.dependencies, expected_dependencies)

    def test_to_plantuml(self):
        self.graph.dependencies = {
            "com.example.app": {"com.example.lib", "com.example.utils"},
            "com.example.lib": {"com.example.core"},
        }
        plantuml = self.graph.to_plantuml()
        expected_output = """@startuml
com.example.app --> com.example.lib
com.example.app --> com.example.utils
com.example.lib --> com.example.core
@enduml"""
        self.assertEqual(plantuml.strip(), expected_output.strip())


if __name__ == "__main__":
    unittest.main()
