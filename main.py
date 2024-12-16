import argparse
from dependency_graph import DependencyGraph


def main():
    parser = argparse.ArgumentParser(description="Визуализатор графов зависимостей.")
    parser.add_argument("--path", required=True, help="Путь к программе для визуализации графов.")
    parser.add_argument("--package", required=True, help="Имя анализируемого пакета.")
    parser.add_argument("--output", required=True, help="Путь к файлу-результату в виде кода.")
    parser.add_argument("--max-depth", type=int, required=True, help="Максимальная глубина анализа зависимостей.")
    parser.add_argument("--repo-url", required=True, help="URL-адрес репозитория.")

    args = parser.parse_args()
    graph = DependencyGraph(repo_url=args.repo_url, max_depth=args.max_depth)
    graph.analyze_dependencies(args.package)

    plantuml_code = graph.to_plantuml()
    with open(args.output, "w") as output_file:
        output_file.write(plantuml_code)
    print(plantuml_code)


if __name__ == "__main__":
    main()
