import argparse
from lifemap.data.storage import DataStorage
from lifemap.visualization.renderer import GraphRenderer

def main():
    parser = argparse.ArgumentParser(description="Interactive Life Map CLI")
    parser.add_argument('--add', type=str, help='Add a new node to the Life Map')
    parser.add_argument('--remove', type=str, help='Remove a node from the Life Map')
    parser.add_argument('--visualize', action='store_true', help='Visualize the Life Map')
    
    args = parser.parse_args()
    
    storage = DataStorage()
    
    if args.add:
        storage.add_node(args.add)
        print(f"Node '{args.add}' added to the Life Map.")
    
    if args.remove:
        storage.remove_node(args.remove)
        print(f"Node '{args.remove}' removed from the Life Map.")
    
    if args.visualize:
        renderer = GraphRenderer(storage.get_all_nodes())
        renderer.render()

if __name__ == "__main__":
    main()